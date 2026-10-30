"""The manifest, the connector file and the marketplace entry.

Everything here is held to the values the founder decided for this listing on
2026-10-23, and to the directory's pre-submission checklist. Stdlib only; the
tests read no environment variable. Run with
`python3 -m unittest discover -s tests -v` from the repository root.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NAME = 'adcopilot-tiktok-ads'
REPO = 'adcopilot-tiktok-ads-plugin'
DISPLAY_NAME = 'AdCopilot for TikTok Ads'
DESCRIPTION = "TikTok Ads help in your AI client, through AdCopilot. Today it checks your TikTok Pixel in Google Tag Manager, reports TikTok traffic and conversions in Google Analytics (GA4) by source, medium and campaign, finds UTM mistakes, guides conversion setup, plans campaigns, drafts video ad scripts and ad text, and does the budget pacing math. It does not read your TikTok ad account. Every change is proposed first and made only on your yes. Made by Atromx Intelligence, not by TikTok."
KEYWORDS = ['tiktok-ads',
 'tiktok-advertising',
 'tiktok-pixel',
 'video-ads',
 'ad-scripts',
 'paid-social',
 'conversions',
 'utm',
 'google-analytics',
 'ga4',
 'google-tag-manager',
 'ad-copy',
 'campaign-planning',
 'budget-pacing',
 'adcopilot']

# The same file in every AdCopilot plugin, byte for byte as parsed: one key,
# one URL spelling, so every copy points at one connector and one sign-in.
CANONICAL_MCP = {"mcpServers": {"adcopilot": {"type": "http", "url": "https://mcp.adcopilot.cloud/mcp"}}}

PLUGIN_KEYS = [
    "name", "version", "description", "author", "homepage", "privacyPolicyUrl",
    "documentationUrl", "termsOfServiceUrl", "supportUrl", "repository", "license",
    "keywords", "displayName", "icon",
]
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$")
SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def urls_in(value):
    if isinstance(value, str):
        if "://" in value:
            yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from urls_in(v)
    elif isinstance(value, list):
        for v in value:
            yield from urls_in(v)


class PluginJson(unittest.TestCase):

    def setUp(self):
        self.plugin = load(".claude-plugin/plugin.json")

    def test_the_field_set_and_its_order(self):
        self.assertEqual(list(self.plugin), PLUGIN_KEYS)

    def test_name_is_the_permanent_lowercase_name(self):
        self.assertEqual(self.plugin["name"], NAME)
        self.assertRegex(self.plugin["name"], NAME_RE)

    def test_display_name_is_exactly_the_decided_listing_name(self):
        self.assertEqual(self.plugin["displayName"], DISPLAY_NAME)

    def test_version_is_semver(self):
        self.assertRegex(self.plugin["version"], SEMVER_RE)
        self.assertEqual(self.plugin["version"], "0.1.1")

    def test_description(self):
        d = self.plugin["description"]
        self.assertEqual(d, DESCRIPTION)
        self.assertLessEqual(len(d), 620)
        self.assertTrue(d.endswith("Made by Atromx Intelligence, not by TikTok."), d)
        # The plain statement the platform plugins owe: what works today, and
        # that the ad account is not read. It promises nothing about later.
        self.assertIn("Today it checks", d)
        self.assertIn("It does not read your TikTok ad account.", d)
        self.assertNotIn("approves", d)
        self.assertNotIn("no date", d)
        self.assertIn("proposed first and made only on your yes", d)

    def test_author_and_links(self):
        p = self.plugin
        self.assertEqual(p["author"], {"name": "Atromx Intelligence", "url": "https://adcopilot.cloud"})
        self.assertEqual(p["homepage"], "https://adcopilot.cloud")
        self.assertEqual(p["documentationUrl"], "https://adcopilot.cloud/docs/")
        self.assertEqual(p["privacyPolicyUrl"], "https://adcopilot.cloud/privacy")
        self.assertEqual(p["termsOfServiceUrl"], "https://adcopilot.cloud/terms")
        self.assertEqual(p["supportUrl"], "https://github.com/AtromxIntelligence/%s/issues" % REPO)
        self.assertEqual(p["repository"], "https://github.com/AtromxIntelligence/%s" % REPO)
        self.assertEqual(p["license"], "MIT")

    def test_keywords(self):
        k = self.plugin["keywords"]
        self.assertEqual(k, KEYWORDS)
        self.assertLessEqual(len(k), 15)
        self.assertEqual(len(set(k)), len(k))
        for word in k:
            self.assertRegex(word, KEBAB_RE)
            self.assertEqual(word, word.lower())

    def test_icon_exists_and_is_a_png(self):
        rel = self.plugin["icon"]
        self.assertEqual(rel, "./.claude-plugin/icon.png")
        path = ROOT / rel
        self.assertTrue(path.is_file(), rel)
        self.assertEqual(path.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_every_url_is_https(self):
        for name in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".mcp.json"):
            for url in urls_in(load(name)):
                self.assertTrue(url.startswith("https://"), "%s: %s" % (name, url))

    def test_the_license_file_is_the_mit_text_with_the_company_name(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertTrue(text.startswith("MIT License"))
        self.assertIn("Copyright (c) 2026 Atromx Intelligence Private Limited", text)


class ConnectorFile(unittest.TestCase):

    def test_mcp_json_is_the_canonical_file(self):
        self.assertEqual(load(".mcp.json"), CANONICAL_MCP)

    def test_mcp_json_holds_no_header_or_command(self):
        server = load(".mcp.json")["mcpServers"]["adcopilot"]
        self.assertEqual(sorted(server), ["type", "url"])


class Marketplace(unittest.TestCase):

    def test_marketplace_names_the_plugin_and_carries_no_listing_fields(self):
        m = load(".claude-plugin/marketplace.json")
        self.assertEqual(sorted(m), ["description", "name", "owner", "plugins"])
        self.assertEqual(m["name"], REPO)
        self.assertEqual(m["owner"], {"name": "Atromx Intelligence", "url": "https://adcopilot.cloud"})
        self.assertEqual(len(m["plugins"]), 1)
        entry = m["plugins"][0]
        self.assertEqual(entry["name"], NAME)
        self.assertEqual(entry["source"], "./")
        self.assertEqual(entry["category"], "Marketing")
        # The directory-listing fields belong in plugin.json, and validate
        # reports them in a marketplace entry as unknown.
        self.assertEqual(sorted(entry), ["category", "description", "name", "source"])
        # The ad account is said not to be read in the same words as in the manifest.
        self.assertTrue(entry["description"].endswith("It does not read your TikTok ad account."),
                        entry["description"])


class ReadmeAndVersion(unittest.TestCase):

    def test_readme_version_paragraph_matches_the_manifest(self):
        version = load(".claude-plugin/plugin.json")["version"]
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        paragraphs = [p for p in text.split("\n\n") if p.startswith("**%s (" % version)]
        self.assertEqual(len(paragraphs), 1, "the README needs one paragraph that starts with **%s (" % version)
        self.assertIn("written against AdCopilot v2.44.0, live since 2026-10-22)**", paragraphs[0])
        self.assertNotIn("\n\n", paragraphs[0])


if __name__ == "__main__":
    unittest.main()
