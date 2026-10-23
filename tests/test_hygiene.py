"""What the plugin directory's scanner looks for, held here so none of it
arrives unnoticed.

The patterns are built by concatenation, so this file never matches the
patterns it checks for. Stdlib only. Nothing here reads an environment
variable, and nothing here asks for a credential: that is the point of the
first test.
"""

import os
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__"}
TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".txt", ""}


def repo_files():
    for dirpath, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if not f.endswith(".pyc"):
                yield Path(dirpath) / f


def text_files():
    for path in repo_files():
        if path.suffix.lower() in TEXT_SUFFIXES and path.name != "icon.png":
            yield path


def customer_text():
    """The files a customer or the model reads."""
    for rel in ("README.md", ".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
        yield ROOT / rel
    for path in sorted((ROOT / "skills").rglob("*.md")):
        yield path
    for path in sorted((ROOT / "commands").glob("*.md")):
        yield path


def read(path):
    return path.read_text(encoding="utf-8")


class NoCredentialRead(unittest.TestCase):

    PATTERNS = {
        "an environment read (Python)": re.compile("os" + r"\." + "environ"),
        "an environment read (getenv)": re.compile("get" + r"env\("),
        "an environment read (Node)": re.compile("process" + r"\." + "env"),
        "a credential variable": re.compile(r"\$\{[^}]*(?:TOK" + "EN|SEC" + "RET|K" + "EY|PASS" + r"WORD)[^}]*\}"),
        "an authorization header": re.compile("Authoriz" + "ation:"),
        "a bearer token": re.compile("Bear" + "er "),
    }

    def test_no_file_reads_or_sends_a_credential(self):
        for path in text_files():
            text = read(path)
            for what, pattern in self.PATTERNS.items():
                self.assertIsNone(pattern.search(text), "%s holds %s" % (path.relative_to(ROOT), what))


class NoLauncherOrDownloadAndExecute(unittest.TestCase):

    LAUNCHERS = re.compile(
        r"\b(?:" + "|".join([
            "np" + "x", "bun" + "x", "pnpm" + r"\s+dlx", "yarn" + r"\s+dlx", "uv" + "x",
            "pipx" + r"\s+run", "uv" + r"\s+run",
        ]) + r")\b")
    DOWNLOAD_AND_EXECUTE = re.compile(
        r"(?:cu" + "rl|wg" + r"et)[^|;\n]*\|\s*(?:sudo\s+)?(?:ba)?" + "sh")

    def test_no_package_launcher_anywhere(self):
        for path in text_files():
            self.assertIsNone(self.LAUNCHERS.search(read(path)), path.relative_to(ROOT))

    def test_no_download_and_execute_pattern_anywhere(self):
        for path in text_files():
            self.assertIsNone(self.DOWNLOAD_AND_EXECUTE.search(read(path)), path.relative_to(ROOT))


class NoStrayFiles(unittest.TestCase):

    BANNED_NAMES = {
        ".DS_Store", "Thumbs.db", "desktop.ini", ".gitmodules", ".gitattributes", "CLAUDE.md",
        "package.json", "package-lock.json", "npm-shrinkwrap.json", "bun.lock", "bun.lockb",
        ".npmrc", "bunfig.toml", "uv.toml",
    }
    BANNED_SUFFIXES = (".mcpb", ".dxt")
    BANNED_DIRS = {"__MACOSX", "bin", "hooks", "agents", "evals"}

    def test_none_of_the_files_the_directory_holds_or_blocks(self):
        for path in repo_files():
            rel = path.relative_to(ROOT)
            self.assertNotIn(path.name, self.BANNED_NAMES, rel)
            self.assertFalse(path.name.endswith(self.BANNED_SUFFIXES), rel)
            self.assertFalse(set(rel.parts[:-1]) & self.BANNED_DIRS, rel)
            self.assertFalse(path.is_symlink(), rel)

    def test_no_directory_is_a_symlink(self):
        for dirpath, dirs, _files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for d in dirs:
                self.assertFalse((Path(dirpath) / d).is_symlink(), d)

    def test_no_svg_icon(self):
        self.assertFalse(list(ROOT.rglob("*.svg")))

    def test_no_image_path_in_text_the_model_or_the_customer_reads(self):
        # The manifest's icon field is the one place an image path belongs.
        for path in customer_text():
            if path.parent.name == ".claude-plugin":
                continue
            self.assertIsNone(re.search(r"\.(?:png|jpe?g|gif|webp|svg|woff2?|ttf|otf)\b", read(path), re.I),
                              path.relative_to(ROOT))


class NoPriceAndNoClaimToBeTheirs(unittest.TestCase):

    def test_no_price_figure_outside_the_plans_line(self):
        pattern = re.compile(r"\$\s?\d|/mo\b|/month|/year|per month|per year")
        for path in customer_text():
            self.assertIsNone(pattern.search(read(path)), path.relative_to(ROOT))

    def test_no_claim_to_be_the_platforms_own(self):
        claim = re.compile("off" + "icial", re.I)
        # "by <Platform>" is allowed only as "not by" and as "endorsed by".
        by_platform = re.compile(
            r"(?<!not )(?<!endorsed )\b" + "by" + r" (?:Goo" + "gle|Me" + "ta|Linked" + "In|X|Tik" + "Tok|Micro" + r"soft)\b")
        for path in text_files():
            text = read(path)
            self.assertIsNone(claim.search(text), path.relative_to(ROOT))
            self.assertIsNone(by_platform.search(text), path.relative_to(ROOT))

    def test_no_other_platforms_name_is_used_as_the_product(self):
        for other in ("Meta Ads", "LinkedIn Ads", "X Ads", "Microsoft Ads"):
            for path in customer_text():
                self.assertNotIn(other, read(path), path.relative_to(ROOT))


if __name__ == "__main__":
    unittest.main()
