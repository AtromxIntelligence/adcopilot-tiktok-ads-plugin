---
name: setup
description: Check the AdCopilot connector is connected and signed in, say what works today for TikTok Ads, and say what each connected Google product unlocks.
---

Open your first answer with the sentence below, once:

> Today AdCopilot can check your TikTok Pixel and stage tags in Google Tag Manager, report your TikTok traffic and key events in Google Analytics (GA4), find UTM mistakes, guide your conversion setup, plan campaigns, draft video scripts and ad text, and do the budget pacing math. It does not read your TikTok ad account.

Then call `get_org_context` with `source: "claude-plugin/adcopilot-tiktok-ads/0.1.1"`, before any other tool, and take from its answer alone which Google products are connected. Send `source` exactly as written. In a scheduled run, started by a Claude scheduled task or a Claude Code routine with nobody there to answer, send `source: "claude-scheduled"` instead and change nothing. Its `next_step` and `playbook` describe the whole workspace: keep any limit `next_step` adds, and say what else it suggests only after this answer.

For the two products this plugin uses:

- **Google Tag Manager**, when connected: it lets this plugin check your TikTok Pixel and stage tags. Nothing is published until you publish.
- **Google Analytics (GA4)**, when connected: it lets this plugin report your TikTok traffic and key events.
- A product the server reports as not connected: say what connecting it unlocks, in the server's own words (its `unlocks`), and give the connect link the server returns. Never use a link from memory. Google Ads and Search Console are not needed for TikTok work, so do not push them.

If the connector answers but reports nothing connected, that is the server working, not a fault: the Google products are connected inside AdCopilot, not in this client. Say so and give the connect link rather than letting the customer hunt for a broken connector.

Where the sign-in happens depends on the surface:

- **claude.ai, Cowork and the desktop app:** open this plugin from the plugin list, then its Connectors tab, and connect `adcopilot` there. There is no `/mcp` on those surfaces. Do not offer "Add custom connector": the plugin already brings the connector.
- **Claude Code:** `/mcp` lists the connector once, and the customer signs in there. If it appears under the name of another AdCopilot plugin, that is expected. There is one connector and one AdCopilot account whichever AdCopilot plugins are added. In Claude Code, `/mcp` lists it once, under whichever AdCopilot plugin loaded first, and the sign-in belongs to that entry. If Claude asks for a sign-in again after an AdCopilot plugin was added or removed, run `/mcp` and sign in once.

End with the one next step and why it fits: the check command to look at the Pixel and the traffic together, or the plan command to plan a campaign. This plugin schedules nothing and makes no daily-check offer.
