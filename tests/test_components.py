"""The skills, the commands and the README, checked without a model.

What is held here:

- every skill and command has front matter that parses, a `name` equal to its
  folder or file stem, and a `description` that is one text value;
- every tool a skill names is in `tests/connector_tools.txt` (the connector's
  tool list at AdCopilot v2.44.1), and each skill names exactly the tools it
  is meant to;
- no skill or command spells a tool by its namespaced full name, whose prefix
  belongs to whichever AdCopilot plugin loaded first;
- the first call carries this plugin's marker, `claude-plugin/<name>/<version>`,
  and no other form of it;
- every skill holds the approval paragraph, and every skill and `/setup` says
  what works today and what comes later;
- the README holds the trademark line and enough words.

Stdlib only; no environment variable is read.
"""

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
NAME = PLUGIN["name"]
VERSION = PLUGIN["version"]
MARKER = "claude-plugin/%s/%s" % (NAME, VERSION)

TODAY_LATER = "Today AdCopilot can check your TikTok Pixel and stage tags in Google Tag Manager, report your TikTok traffic and key events in Google Analytics (GA4), find UTM mistakes, guide your conversion setup, plan campaigns, draft video scripts and ad text, and do the budget pacing math. It cannot yet read your TikTok ad account: that arrives when TikTok approves AdCopilot's API access, and no date is promised."
APPROVAL = '**Every change is proposed first.** Say what it changes and how to undo it, and make it only after the customer\'s explicit yes in this conversation. Changes in Tag Manager are staged in the "AdCopilot" workspace and never published: publishing is the customer\'s click in Tag Manager. Nothing is ever deleted. Every number is a tool\'s number or a figure the customer gave you, never an invented one.'

# The tools each skill names, exactly: a skill that names fewer has dropped a
# step, and one that names more has gone past what this plugin promises.
SKILL_TOOLS = {'tiktok-ads-budget': [],
 'tiktok-ads-plan': ['get_org_context'],
 'tiktok-ads-tracking': ['get_org_context',
                         'gtm_list_accounts',
                         'gtm_list_containers',
                         'gtm_list_workspaces',
                         'gtm_list_tags',
                         'gtm_list_triggers',
                         'gtm_list_version_headers',
                         'gtm_list_built_in_variables',
                         'gtm_enable_built_in_variable',
                         'gtm_create_trigger',
                         'gtm_create_tag'],
 'tiktok-ads-traffic': ['get_org_context',
                        'ga4_list_account_summaries',
                        'ga4_get_metadata',
                        'ga4_run_report',
                        'ga4_list_conversion_events']}
COMMANDS = ["setup", "check", "plan"]

CONNECTOR_TOOLS = {
    line.strip() for line in (ROOT / "tests" / "connector_tools.txt").read_text(encoding="utf-8").splitlines()
    if line.strip() and not line.startswith("#")
}
# Tools the connector has but does not serve to every workspace: never named.
SWITCHED_OFF = {"shopping_product_issues", "lsa_leads", "lsa_rate_lead"}
PREFIXES = ("gsc_", "ga4_", "gtm_")
BACKTICKED = re.compile(r"`([a-z][a-z0-9]*(?:_[a-z0-9]+)+)`")
# A plain-scalar front matter value: no ": " or " #" inside it and none of the
# characters that open a YAML list, map, block scalar, alias, tag or quote.
YAML_STARTERS = set("[]{}|>&*!%@`'\",#-?:")


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), "%s has no front matter" % path
    end = text.index("\n---\n", 4)
    fields = {}
    for line in text[4:end].split("\n"):
        key, sep, value = line.partition(":")
        assert sep and key.strip() and key == key.strip(), "%s: bad front matter line %r" % (path, line)
        assert key not in fields, "%s: %s twice" % (path, key)
        fields[key] = value.strip()
    return fields, text[end + len("\n---\n"):]


def components():
    out = []
    for skill in sorted((ROOT / "skills").iterdir()):
        out.append(("skill", skill.name, skill / "SKILL.md"))
    for cmd in sorted((ROOT / "commands").glob("*.md")):
        out.append(("command", cmd.stem, cmd))
    return out


def tool_like(text):
    names = set()
    for token in BACKTICKED.findall(text):
        if token.startswith(PREFIXES) or token in CONNECTOR_TOOLS or token in SWITCHED_OFF:
            names.add(token)
    if "get_org_context" in text:
        names.add("get_org_context")
    return names


class FrontMatter(unittest.TestCase):

    def test_the_plugin_has_exactly_the_planned_skills_and_commands(self):
        self.assertEqual(sorted(p.name for p in (ROOT / "skills").iterdir()), sorted(SKILL_TOOLS))
        self.assertEqual(sorted(p.stem for p in (ROOT / "commands").glob("*.md")), sorted(COMMANDS))

    def test_every_skill_and_command_parses_and_is_named_for_its_folder_or_file(self):
        for kind, name, path in components():
            fields, body = front_matter(path)
            self.assertEqual(sorted(fields), ["description", "name"], path)
            self.assertEqual(fields["name"], name, path)
            desc = fields["description"]
            self.assertTrue(desc, path)
            self.assertNotIn(": ", desc, path)
            self.assertNotIn(" #", desc, path)
            self.assertNotIn(desc[0], YAML_STARTERS, path)
            self.assertTrue(body.strip(), "%s has no body" % path)
            if kind == "skill":
                self.assertIn("Use when", desc, path)

    def test_skill_names_cannot_collide_with_another_adcopilot_plugin(self):
        for name in SKILL_TOOLS:
            self.assertTrue(name.startswith("tiktok-ads-"), name)
        for name in SKILL_TOOLS:
            self.assertNotIn(name, ("adcopilot-seo", "adcopilot-meta"))


class Tools(unittest.TestCase):

    def test_the_tool_list_is_the_connectors_and_is_not_empty(self):
        self.assertGreater(len(CONNECTOR_TOOLS), 100)
        for tool in ("get_org_context", "gtm_create_tag", "ga4_run_report", "gsc_list_sites"):
            self.assertIn(tool, CONNECTOR_TOOLS)
        for tool in SWITCHED_OFF:
            self.assertNotIn(tool, CONNECTOR_TOOLS)

    def test_every_tool_a_skill_or_command_names_is_real_and_is_the_planned_one(self):
        for kind, name, path in components():
            text = path.read_text(encoding="utf-8")
            named = tool_like(text)
            for tool in sorted(named):
                self.assertIn(tool, CONNECTOR_TOOLS, "%s names %s, which the connector does not have" % (path, tool))
            if kind == "skill":
                self.assertEqual(sorted(named), sorted(SKILL_TOOLS[name]), path)

    def test_the_readme_names_only_real_tools(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for tool in sorted(tool_like(text)):
            self.assertIn(tool, CONNECTOR_TOOLS, tool)

    def test_a_tool_is_named_by_its_bare_name_never_by_a_namespaced_one(self):
        needle = "mcp__" + "plugin_"
        for path in ROOT.rglob("*"):
            if path.is_file() and ".git" not in path.parts and path.suffix in (".md", ".json", ".yml", ".py", ".txt"):
                self.assertNotIn(needle, path.read_text(encoding="utf-8"), path)


class FirstCall(unittest.TestCase):

    def test_get_org_context_carries_this_plugins_marker_and_no_other_form(self):
        for kind, name, path in components():
            text = path.read_text(encoding="utf-8")
            if "get_org_context" in text:
                self.assertIn("source: \"%s\"" % MARKER, text, path)
            for found in re.findall(r"claude-plugin[^\s\"'`)>,.]*(?:\.\d+)*", text):
                self.assertEqual(found, MARKER, "%s: %r is not this plugin's marker" % (path, found))
            if "get_org_context" in text:
                # A scheduled run is told to change nothing, and says so.
                self.assertIn("claude-scheduled", text, path)

    def test_the_marker_has_the_plugin_name_and_a_version_the_server_reads(self):
        self.assertEqual(MARKER, "claude-plugin/%s/%s" % (NAME, VERSION))
        self.assertRegex(VERSION, r"^\d+\.\d+\.\d+$")
        # The server reads what follows the slash as a version only when it is
        # X.Y.Z at or above 0.2.7; anything else is "no version", so the turn
        # is never handed to skills this plugin does not carry.
        self.assertNotRegex(MARKER, r"^claude-plugin/\d")

    def test_no_skill_or_command_schedules_anything(self):
        for kind, name, path in components():
            text = path.read_text(encoding="utf-8").lower()
            self.assertNotIn("/schedule", text, path)
            self.assertNotIn("scheduled task for you", text, path)


class Honesty(unittest.TestCase):

    def test_every_skill_holds_the_approval_paragraph(self):
        for name in SKILL_TOOLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(APPROVAL, text, name)

    def test_every_skill_and_setup_says_what_works_today_and_what_comes_later(self):
        for name in SKILL_TOOLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(text.count(TODAY_LATER), 1, name)
        setup = (ROOT / "commands" / "setup.md").read_text(encoding="utf-8")
        self.assertEqual(setup.count(TODAY_LATER), 1)

    def test_the_sentence_is_plain_about_the_gap(self):
        self.assertIn("cannot yet read your TikTok ad account", TODAY_LATER)
        self.assertIn("approves AdCopilot's API access", TODAY_LATER)
        self.assertIn("no date is promised", TODAY_LATER)

    def test_planning_and_budget_say_that_adcopilot_reads_no_tiktok_data(self):
        for name in ("tiktok-ads-plan", "tiktok-ads-budget", "tiktok-ads-tracking", "tiktok-ads-traffic"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("reads no TikTok data", text, name)

    def test_the_budget_skill_calls_no_tool(self):
        text = (ROOT / "skills" / "tiktok-ads-budget" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("calls no AdCopilot tool", text)

    def test_platform_facts_are_dated_and_name_their_referee(self):
        text = (ROOT / "skills" / "tiktok-ads-tracking" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("checked 23 October 2026", text)
        self.assertIn("referee", text)
        self.assertIn("at the time of writing", text)

    def test_gtm_writes_are_staged_never_published(self):
        text = (ROOT / "skills" / "tiktok-ads-tracking" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("staged", text)
        self.assertIn("never published", text)
        self.assertIn("publishing is theirs", text)


class Readme(unittest.TestCase):

    def setUp(self):
        self.text = (ROOT / "README.md").read_text(encoding="utf-8")

    def words_outside_code(self):
        outside = re.sub(r"```.*?```", " ", self.text, flags=re.S)
        return len(outside.split())

    def test_the_readme_is_long_enough_for_the_directory(self):
        count = self.words_outside_code()
        self.assertGreaterEqual(count, 600, count)
        self.assertLessEqual(count, 1200, count)

    def test_the_readme_starts_with_the_display_name(self):
        self.assertTrue(self.text.startswith("# %s\n" % PLUGIN["displayName"]))

    def test_the_readme_holds_the_trademark_line_and_the_made_by_line(self):
        self.assertIn("Made by Atromx Intelligence (https://adcopilot.cloud).", self.text)
        self.assertIn("Not affiliated with or endorsed by TikTok", self.text)
        self.assertIn("are trademarks of", self.text)
        self.assertIn("not related to other products named AdCopilot", self.text)

    def test_the_readme_says_the_plans_line_and_nothing_more_about_price(self):
        self.assertIn("The plugin is free (MIT). The AdCopilot connector is a hosted service: "
                      "Free plan available; paid plans on https://adcopilot.cloud/pricing.", self.text)

    def test_the_readme_holds_the_install_dedupe_data_and_support_sections(self):
        for needle in (
            "## Install", "### claude.ai, Cowork and the desktop app", "### Claude Code",
            "/plugin marketplace add AtromxIntelligence/", "/plugin install %s@" % NAME, "/mcp",
            "https://app.adcopilot.cloud", "## Already use another AdCopilot plugin?",
            "One connector, one sign-in, whichever AdCopilot plugins you add.",
            "sign in once", "## What it will not do", "## Data",
            "The plugin is instructions only: it runs no code and sends nothing anywhere itself.",
            "https://adcopilot.cloud/privacy", "## Support", "support@adcopilot.cloud",
            "/issues", "## Licence", "## What CI runs",
        ):
            self.assertIn(needle, self.text, needle)

    def test_the_readme_states_what_works_today_and_what_does_not(self):
        self.assertIn("**Later:**", self.text)
        self.assertIn("approves AdCopilot's API access", self.text)
        self.assertIn("There is no date", self.text)


if __name__ == "__main__":
    unittest.main()
