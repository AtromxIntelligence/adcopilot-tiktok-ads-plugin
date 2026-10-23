# AdCopilot for TikTok Ads

TikTok Ads help in your AI client, through AdCopilot. Today it checks your TikTok Pixel in Google Tag Manager, reports your TikTok traffic and conversions in Google Analytics (GA4), finds UTM mistakes, guides conversion setup, plans campaigns, drafts video ad scripts and ad text, and does the budget pacing math. Direct access to your TikTok ad account comes when TikTok approves AdCopilot's API access; there is no date yet. Every change is proposed first and made only on your yes.

Made by Atromx Intelligence (https://adcopilot.cloud). Not affiliated with or endorsed by TikTok. TikTok and TikTok Ads are trademarks of their owner. This plugin is not related to other products named AdCopilot.

The plugin is free (MIT). The AdCopilot connector is a hosted service: Free plan available; paid plans on https://adcopilot.cloud/pricing.

## What it does today

- **Checks your TikTok Pixel in Google Tag Manager.** It reads your containers, workspaces, tags, triggers and saved versions (`gtm_list_accounts`, `gtm_list_containers`, `gtm_list_workspaces`, `gtm_list_tags`, `gtm_list_triggers`, `gtm_list_version_headers`) and says whether a TikTok Pixel tag exists, what fires it, whether it is a draft, and which events are tagged.
- **Stages tags for you, and never publishes them.** If you paste your base code, it proposes a Custom HTML tag and a thank-you-page trigger (`gtm_create_tag`, `gtm_create_trigger`, and, if the page-path variable is off, `gtm_list_built_in_variables` and `gtm_enable_built_in_variable`). They land in a Tag Manager workspace named "AdCopilot", and publishing is your click.
- **Reports TikTok traffic and conversions in Google Analytics (GA4).** Sessions, engaged sessions, key events and revenue by source, medium and campaign, with Paid Social against Organic Social (`ga4_list_account_summaries`, `ga4_get_metadata`, `ga4_run_report`, `ga4_list_conversion_events`). It calls out UTM mistakes and writes a UTM link set for each campaign.
- **Guides conversion setup**, from naming the one action that counts to testing it with TikTok's own tools.
- **Plans, drafts and does the arithmetic itself.** Campaign plans, vertical video scripts with a hook, shot lists, on-screen text, ad text and call-to-action variants, and budget pacing math. Claude writes these. AdCopilot reads no TikTok data for them, and the budget skill uses no tool at all.

**Later:** reading your TikTok ad account, when TikTok approves AdCopilot's API access. There is no date. Nothing here reads or changes a TikTok ad account today; when that arrives, it will come as an update to this plugin.

## Install

Add the plugin, then sign in to the connector it brings with it. The second step is the one people miss.

### claude.ai, Cowork and the desktop app

1. Open **Customize**, then **Plugins**, search for AdCopilot for TikTok Ads, and click **Add**.
2. Open the plugin's **Connectors** tab, click **Connect** beside `adcopilot`, and sign in.

There is nothing to add by hand: the plugin registers the connector for you.

### Claude Code

```
/plugin marketplace add AtromxIntelligence/adcopilot-tiktok-ads-plugin
/plugin install adcopilot-tiktok-ads@adcopilot-tiktok-ads-plugin
/mcp
```

The last step opens the connector list. Choose `adcopilot` and sign in. The plugin registers the connector at `https://mcp.adcopilot.cloud/mcp` for you, so there is no `claude mcp add` step.

### Then, on every surface

Signing in links your AdCopilot workspace, so you need an AdCopilot account. Your Google products are connected once, inside AdCopilot at https://app.adcopilot.cloud, not in your AI client. A fresh sign-in can report nothing connected: that is the server answering correctly. Run `/adcopilot-tiktok-ads:setup` first to see what is connected.

## Already use another AdCopilot plugin?

There is one connector and one AdCopilot account, whichever AdCopilot plugins you add. Every AdCopilot plugin points at the same address, so your AI client treats them as one connector. In Claude Code, `/mcp` shows the connector once, under whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry. If Claude asks you to sign in again after you add or remove an AdCopilot plugin, run `/mcp` and sign in once.

## What you get

Three commands, which you type:

- `/adcopilot-tiktok-ads:setup` checks the connector is connected and signed in, says what works today, and says what each connected Google product unlocks.
- `/adcopilot-tiktok-ads:check` looks at the Pixel in Tag Manager and the TikTok traffic in Analytics together, then says what to fix first.
- `/adcopilot-tiktok-ads:plan` plans a campaign and drafts the creative.

Four skills, which Claude draws on when the conversation calls for them:

- **tiktok-ads-tracking** reads Tag Manager (`get_org_context`, `gtm_list_accounts`, `gtm_list_containers`, `gtm_list_workspaces`, `gtm_list_tags`, `gtm_list_triggers`, `gtm_list_version_headers`) and, on your yes, stages tags (`gtm_create_trigger`, `gtm_create_tag`, `gtm_list_built_in_variables`, `gtm_enable_built_in_variable`).
- **tiktok-ads-traffic** reads Analytics (`get_org_context`, `ga4_list_account_summaries`, `ga4_get_metadata`, `ga4_run_report`, `ga4_list_conversion_events`).
- **tiktok-ads-plan** writes the plan and the creative. It reads only your saved business profile (`get_org_context`).
- **tiktok-ads-budget** does the pacing arithmetic from your figures. It uses no tool.

## What it will not do

- Publish Tag Manager. Changes are staged in the "AdCopilot" workspace, and you publish.
- Delete anything. None of these skills has a delete tool to use.
- Change anything without your yes. Every change is proposed first, with what it changes and how to undo it.
- Read or change your TikTok ad account. That is the "Later" above.
- Ask for your TikTok password or access token.
- Quote benchmarks or promise results. Every number is a tool's number, one you gave it, or arithmetic on yours with the working shown.

## Platform facts, checked 23 October 2026

The Pixel steps follow TikTok's published Tag Manager template and Google's Analytics help pages as they stood on that day. TikTok's pages change, so its Events Manager, Test Events tab and Pixel Helper are the referee for what your Pixel is doing.

## Data

The plugin is instructions only: it runs no code and sends nothing anywhere itself. The AdCopilot connector at mcp.adcopilot.cloud reads and, on your yes, writes your Google products through Google's APIs with your Google sign-in. Neither the plugin nor the connector contacts TikTok. Privacy policy: https://adcopilot.cloud/privacy. Terms: https://adcopilot.cloud/terms.

## Support

- Something wrong with the plugin (a command, a skill, this README): [open an issue here](https://github.com/AtromxIntelligence/adcopilot-tiktok-ads-plugin/issues).
- Something wrong with the connector (sign-in, a tool call, your account): support@adcopilot.cloud.

## Version

**0.1.0 (2026-10-23, written against AdCopilot v2.44.0, live since 2026-10-22)** First release: four skills (`tiktok-ads-tracking`, `tiktok-ads-traffic`, `tiktok-ads-plan`, `tiktok-ads-budget`), three commands (`setup`, `check`, `plan`) and the connector registration for `https://mcp.adcopilot.cloud/mcp`. Every tool the skills name is in the connector's tool list for that version. The structural tests and `claude plugin validate --strict` pass. The skills have not yet been run against a live Tag Manager container that carries a TikTok Pixel, so read the first answers as reviewed text, not as field-tested. Reading a TikTok ad account is not in this version.

## Licence

MIT. Copyright Atromx Intelligence Private Limited. See [LICENSE](LICENSE).

## What CI runs

Two workflows run on every push to `main` and every pull request, and neither reads a secret. `checks.yml` installs Claude Code from npm at a pinned version, runs `claude plugin validate --strict` on the plugin and its manifest, checks that the manifests parse and every skill and command has a name and a description, runs the structural tests in `tests/`, and checks that no download-and-execute pattern is in the repository and that the manifest version is not behind the latest tag. `leak-check.yml` runs gitleaks over every commit, from its published container image pinned by digest.
