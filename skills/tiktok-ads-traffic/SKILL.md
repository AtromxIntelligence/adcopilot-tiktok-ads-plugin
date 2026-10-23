---
name: tiktok-ads-traffic
description: Report the customer's TikTok traffic and conversions as Google Analytics (GA4) counts them, by source, medium and campaign, with Paid Social against Organic Social, key events and revenue, find UTM mistakes, and write a UTM link set for each TikTok campaign. Use when the user asks how TikTok traffic is doing in Analytics, TikTok sessions, TikTok conversions in GA4, UTM parameters or UTM links for TikTok, why TikTok traffic shows as direct or referral, or why TikTok Ads and Analytics disagree.
---

# TikTok traffic, as Analytics counts it

The customer wants to know what their TikTok ads and posts bring to the site. Answer from Google Analytics (GA4) through the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`.

Open your first answer in this conversation with the sentence below, once, and do not repeat it later:

> Today AdCopilot can check your TikTok Pixel and stage tags in Google Tag Manager, report your TikTok traffic and key events in Google Analytics (GA4), find UTM mistakes, guide your conversion setup, plan campaigns, draft video scripts and ad text, and do the budget pacing math. It cannot yet read your TikTok ad account: that arrives when TikTok approves AdCopilot's API access, and no date is promised.

AdCopilot reads no TikTok data for this. Everything below is what Analytics recorded on the customer's site. Anything from TikTok itself (spend, clicks, impressions) is a figure the customer pastes, and what you do with it is arithmetic you show.

**Every change is proposed first.** Say what it changes and how to undo it, and make it only after the customer's explicit yes in this conversation. Changes in Tag Manager are staged in the "AdCopilot" workspace and never published: publishing is the customer's click in Tag Manager. Nothing is ever deleted. Every number is a tool's number or a figure the customer gave you, never an invented one.

This skill only reads. It changes nothing in Analytics. Marking a key event is the customer's click (in Analytics, at the time of writing: Admin, then Data display, then Events, then the Key events tab).

## Start

Call `get_org_context` with `source: "claude-plugin/adcopilot-tiktok-ads/0.1.0"` first, before any other tool. Send `source` exactly as written. In a scheduled run, started by a Claude scheduled task or a Claude Code routine with nobody there to answer, send `source: "claude-scheduled"` instead and change nothing.

Its `next_step` and `playbook` describe the whole workspace, not this request. Do THIS request, keep any limit `next_step` adds, and offer what else it suggests afterwards. If it names an AdCopilot skill that is not installed here, carry on with this one.

If Google Analytics is not connected, say what connecting it unlocks, in the server's own words (its `unlocks`), give the connect link the server returns, and stop. Never use a link from memory, and invent nothing about a property you cannot read.

## Read

1. **Which property.** `ga4_list_account_summaries`, then use the exact `properties/<id>` it returns. If there is more than one, ask which is the website the TikTok traffic lands on, by display name.
2. **Which names it has.** `ga4_get_metadata` for that property. Use the names it returns. The usual ones are the dimensions `sessionSourceMedium`, `sessionCampaignName` and `sessionDefaultChannelGroup`, and the metrics `sessions`, `engagedSessions`, `keyEvents` and `totalRevenue`. An older property may list `conversions` where `keyEvents` is. If a name is not in the metadata, say so and do not guess one.
3. **The window.** Analytics says its data can take 24 to 48 hours to settle (checked 23 October 2026), so end the window two days before today, use 28 days unless the customer names a period, and say which dates you read. Pass `start_date` and `end_date` as `YYYY-MM-DD`.
4. **By source.** `ga4_run_report` with the dimensions `sessionSourceMedium` and `sessionDefaultChannelGroup` and the metrics above, with `limit` set high (1000). The tool has no filter, so read every row and keep the ones whose source contains `tiktok` in any spelling or case. If the rows returned equal the limit, say the list is cut and the TikTok rows may be incomplete.
5. **By campaign.** The same call with `sessionSourceMedium` and `sessionCampaignName`.
6. **Which events count.** `ga4_list_conversion_events`. If its answer flags visit events marked as key events (`visit_key_events`), say what that does: Analytics counts every ordinary visit as a result, so the key-event numbers mean little until that is changed.

## Say, in sentences

- TikTok sessions, how many were engaged, key events, and revenue if there is any. No revenue means no purchase event with a value reaches Analytics, not that nothing sold.
- Where the TikTok traffic sits: Paid Social, Organic Social, Referral, Direct or Unassigned.
- The top campaigns, and how much sits under a campaign of `(not set)`.
- One plain line on why the two reports disagree. Analytics counts the sessions it recorded, by that session's source. TikTok Ads Manager counts clicks and conversions by its own attribution settings. The two will not match, and neither is wrong. Never "reconcile" them by adjusting a figure.
- If the customer pastes TikTok spend or clicks, show the arithmetic against the Analytics sessions or key events (cost per session, cost per key event), and say that clicks are not sessions.

## UTM hygiene

Google's rules, checked 23 October 2026 against Google's own help pages:

- Analytics is case sensitive: `utm_source=google` and `utm_source=Google` are different sources. The same holds for `tiktok` and `TikTok`.
- `utm_source` names where the traffic comes from, `utm_medium` the kind of marketing, `utm_campaign` the individual campaign, `utm_content` tells apart ads or links within a campaign, and `utm_term` is for paid search keywords.
- A session lands in the Paid Social channel when its source is in Google's list of social sites and its medium matches `^(.*cp.*|ppc|retargeting|paid.*)$`. It lands in Organic Social when the source is in that list, or when the medium is one of social, social-network, social-media, sm, social network or social media. When no rule matches, Analytics uses Unassigned. Google keeps its list of social sites in a downloadable spreadsheet, so whether `tiktok` is on it is something the customer's own channel column shows: traffic tagged `paid_social` that lands in Paid Social is recognised, and tagged traffic that lands in Unassigned or Referral is not.

What to look for in the customer's own rows, and say only what the rows show:

- The same source in several spellings, or the same traffic under several mediums (`paid`, `cpc`, `paid_social`, `social`). It splits one campaign across rows.
- TikTok traffic with a medium of `referral`, `(none)` or `organic`, and no campaign. It arrived without UTM tags: a link in a post or a profile, or an ad whose link was never tagged. The report cannot say which.
- Direct traffic that climbs on the days a campaign runs. It may be untagged ad traffic. It cannot be proven from here, so say it is a lead to check.
- A campaign of `(not set)`: usually the link had no `utm_campaign`.

When the customer names their campaigns, write the link set for each, in lower case with no spaces, one spelling for ever:

`?utm_source=tiktok&utm_medium=paid_social&utm_campaign=<campaign-slug>&utm_content=<creative-slug>`

If the page address already has a `?`, join with `&` instead. Leave `utm_term` out unless it means something. The medium `paid_social` matches the Paid Social rule above, and the customer's own channel column is the referee. TikTok has a way to fill campaign details into a link automatically, its dynamic URL parameters (at the time of writing). The placeholders are TikTok's: ask the customer to open TikTok's help page on dynamic URL parameters and paste what it lists, and use only those. AdCopilot does not know them.

## Then

Offer, one at a time, the Pixel check in Tag Manager (the tracking skill) or the campaign plan. This plugin schedules nothing and makes no daily-check offer.
