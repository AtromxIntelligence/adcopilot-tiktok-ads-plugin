"""What the plugin directory's scanner looks for, held here so none of it
arrives unnoticed. It also holds one promise of ours: no wording that claims a
relationship with TikTok.

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


# Words that read as a claim of a relationship with TikTok: that it approved,
# partnered with or granted something to AdCopilot, that AdCopilot is built into
# its systems, or that something is on its way. The plugin makes no such claim and
# promises nothing about later. The patterns are generic, and the phrases they must
# catch are built from pieces, so this file never matches itself.
OWNER = "TikTok"
CERT = "certifi" + "ed"
RELATIONSHIP_PATTERNS = [
    r"(?i)\bapproved\s+by\s+" + OWNER + r"\b",
    r"(?i)\b(?:" + CERT + r"|sponsored)\s+(?:by|from)\s+" + OWNER + r"\b",
    r"(?i)\b" + OWNER + r"[\s-]+certifi(?:ed|cation)\b",
    r"(?i)\b" + OWNER + r"\s+partners?\b",
    r"(?i)\bpartnership\b",
    r"(?i)\bAds\s+API\b",
    r"(?i)\bAPI\s+access\b",
    r"(?i)\b" + OWNER + r"(?:['\u2019]s)?(?:\s+Ads)?\s+API\b",
    r"(?i)\b" + OWNER + r"(?:\s+Ads)?\s+integration\b",
    r"(?i)\bintegration\s+with\s+" + OWNER + r"\b",
    r"(?i)\b" + OWNER + r"\s+(?:has\s+)?(?:approved|granted)\b",
    r"(?i)\b" + OWNER + r"\s+approves\b",
    r"(?i)\bapproval\s+(?:from|by)\s+" + OWNER + r"\b",
    r"(?i)\b" + OWNER + r"['\u2019]s\s+approval\b",
    r"(?i)\bcom(?:es|ing)\s+(?:when|soon|later)\b",
]


class NoTikTokRelationshipWords(unittest.TestCase):

    def test_no_file_says_tiktok_approved_partnered_or_integrated(self):
        # Every text file, the tests and the CI files included.
        for path in text_files():
            text = " ".join(read(path).split())
            for pattern in RELATIONSHIP_PATTERNS:
                hit = re.search(pattern, text)
                with self.subTest(file=str(path.relative_to(ROOT)), pattern=pattern):
                    self.assertIsNone(hit, hit and hit.group(0))

    def test_the_ban_catches_the_ways_it_is_said_and_leaves_the_plain_sentences(self):
        # The phrases are built at run time, so this file carries none of them.
        caught = [
            "approved by {o}", CERT + " by {o}", "sponsored by {o}", "{o}-" + CERT,
            "{o} certifi" + "cation", "{o} partner", "{o} partners", "{o} part" + "nership",
            "part" + "nership with {o}", "Ads " + "API", "API " + "access",
            "API " + "access from {o}", "{o} API", "{o}'s API", "{o}\u2019s API",
            "{o} Ads " + "API", "{o} integration", "the {o} Ads integration",
            "integration with {o}", "{o} approved our API " + "access",
            "{o} has approved AdCopilot", "{o} granted API " + "access",
            "{o} approves", "when {o} approves", "approval from {o}",
            "approval by {o}", "{o}'s approval", "{o}\u2019s approval",
            "com" + "es when {o} replies", "com" + "ing soon", "what com" + "es later",
        ]
        passed = [
            "It does not read your {o} ad account.",
            "Not affiliated with or endorsed by {o}",
            "Made by Atromx Intelligence, not by {o}.",
            "the {o} Pixel and the Events API",
            "{o}'s Events API is its way of sending events from a server.",
            "the {o} Ads Manager Test Events tab",
            "your Google products through Google's APIs",
            "the tracking skill comes first",
        ]

        def matched(phrase):
            return [p for p in RELATIONSHIP_PATTERNS if re.search(p, phrase.format(o=OWNER))]

        for phrase in caught:
            self.assertNotEqual(matched(phrase), [], phrase)
        for phrase in passed:
            self.assertEqual(matched(phrase), [], phrase)


if __name__ == "__main__":
    unittest.main()
