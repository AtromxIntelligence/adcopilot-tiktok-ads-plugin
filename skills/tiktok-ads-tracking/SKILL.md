---
name: tiktok-ads-tracking
description: Check the TikTok Pixel on the customer's website through Google Tag Manager, meaning whether a TikTok Pixel tag exists, what fires it, whether it is a draft or sits in a saved version, and which TikTok events are tagged, and stage a TikTok base-code tag and a thank-you-page trigger when asked. Also guides TikTok conversion setup. Use when the user asks about the TikTok Pixel, TikTok tracking, TikTok conversion tracking, TikTok events, whether a TikTok pixel is working, a TikTok tag in Google Tag Manager, or why TikTok Ads shows no conversions.
---

# TikTok Pixel check, through Tag Manager

The customer wants to know whether TikTok can see what happens on their site. TikTok's Pixel is a snippet that has to be on the pages, and most sites load it through Google Tag Manager. Answer through the AdCopilot connector at `https://mcp.adcopilot.cloud/mcp`.

Open your first answer in this conversation with the sentence below, once, and do not repeat it later:

> Today AdCopilot can check your TikTok Pixel and stage tags in Google Tag Manager, report your TikTok traffic and key events in Google Analytics (GA4), find UTM mistakes, guide your conversion setup, plan campaigns, draft video scripts and ad text, and do the budget pacing math. It cannot yet read your TikTok ad account: that arrives when TikTok approves AdCopilot's API access, and no date is promised.

AdCopilot reads no TikTok data for this. It can read Tag Manager. It cannot see inside TikTok.

**Every change is proposed first.** Say what it changes and how to undo it, and make it only after the customer's explicit yes in this conversation. Changes in Tag Manager are staged in the "AdCopilot" workspace and never published: publishing is the customer's click in Tag Manager. Nothing is ever deleted. Every number is a tool's number or a figure the customer gave you, never an invented one.

## Start

Call `get_org_context` with `source: "claude-plugin/adcopilot-tiktok-ads/0.1.0"` first, before any other tool. Send `source` exactly as written. In a scheduled run, started by a Claude scheduled task or a Claude Code routine with nobody there to answer, send `source: "claude-scheduled"` instead and change nothing.

Its `next_step` and `playbook` describe the whole workspace, not this request. Do THIS request, keep any limit `next_step` adds, and offer what else it suggests afterwards. If it names an AdCopilot skill that is not installed here, carry on with this one.

If Google Tag Manager is not connected, say what connecting it unlocks, in the server's own words (its `unlocks`), give the connect link the server returns, and stop. Never use a link from memory, and invent nothing about a container you cannot read.

## Read: is the Pixel there?

Work in this order. Name accounts and containers by the display names the server returns, never by an ID from memory.

1. `gtm_list_accounts`, then `gtm_list_containers`. If there is more than one container, ask which one is on the website the TikTok ads send people to.
2. `gtm_list_workspaces`, then `gtm_list_tags` on the workspace the customer works in (usually "Default Workspace") and on the "AdCopilot" workspace if it exists.
3. `gtm_list_triggers` for the same workspaces, to turn the firing trigger ids on each tag into names. Built-in triggers are not in that list: `2147479553` is Tag Manager's built-in All Pages trigger.
4. `gtm_list_version_headers`: the container's saved versions, their names and what each holds.

Recognise the Pixel by what a tag holds, never by its name alone:

- A Custom HTML tag (type `html`) whose HTML contains `ttq.load(` with the pixel ID, or loads a script from `analytics.tiktok.com`. This is TikTok's base code.
- A tag from TikTok's own Tag Manager template. Its type starts `cvt_` and it carries parameters named `event` and `pixel_code`.
- A tag whose HTML calls `ttq.track(` with an event name. This is an event tag.

Tell the customer what you found in plain sentences, not as a copy of the rows:

- Whether there is a base-code tag, how many (two base-code tags send every page view twice, so say so), and its pixel ID. The ID is read from the tag and is not a secret: it is in the page's source. Ask the customer to confirm it is the one shown in TikTok's Events Manager.
- Whether the tag is paused (a paused tag never fires), and what fires it. Base code belongs on every page, which is All Pages. On a narrower trigger, TikTok never sees the other pages.
- Which events are tagged, by the names the tags use, and on what.
- Which workspace each tag is in, and what the saved versions show.

## What these reads cannot say

Say these plainly, because each one is the first thing a customer assumes:

- **Whether a tag is published.** `gtm_list_tags` shows a workspace's draft. `gtm_list_version_headers` shows saved versions without saying which one is live and without their contents. Tag Manager's own Versions screen marks the live version, and its Preview mode shows whether a tag fires on a page (both at the time of writing).
- **Whether it fires on the live site, and whether TikTok received the event.** TikTok's Events Manager (its Test Events tab) and the TikTok Pixel Helper browser extension show that, at the time of writing, and they are the referee. Ask the customer to do the action once with one of them open and tell you what it shows.
- **Anything inside TikTok Ads Manager:** campaigns, spend, which event a campaign is set to optimise for, ad approval.
- **Consent.** Whether a visitor's cookie choice lets the Pixel fire is the customer's own setup in Tag Manager and their banner. This skill does not change consent settings.

## When the Pixel is missing or wrong

Propose the fix and wait for the yes. Never ask for a TikTok password or an access token, and never offer to take one: the base code is not a credential.

1. Ask the customer to copy their own base code from TikTok's Events Manager and paste it here. It has their pixel ID in it. List the tags first: a container that already carries a base-code tag needs no second one, because two send every page view twice.
2. On a yes, stage the base code with `gtm_create_tag` on the container: a Custom HTML tag (type `html`) named "TikTok Pixel - base code", with the pasted code as its `html` parameter and `supportDocumentWrite` set to `false`, firing on All Pages (`2147479553`).
3. For one action that matters, stage an event tag on the page only a finished action reaches (a thank-you page, say). Create the trigger with `gtm_create_trigger`: type `domReady` (DOM Ready), filtered on the Page Path containing the thank-you page's path. Then create the event tag with `gtm_create_tag`: a Custom HTML tag whose HTML is a script calling `ttq.track` with the event name, firing on that trigger. DOM Ready comes after the Page View the base code fires on, so the base code has already run when the event is sent.
4. The filter reads Tag Manager's Page Path variable. If that built-in variable is off in the container, the trigger matches nothing and never says so: check with `gtm_list_built_in_variables`, and if it is missing propose `gtm_enable_built_in_variable` like any other change.
5. Read it back: `gtm_list_tags` and `gtm_list_triggers` on the "AdCopilot" workspace (its path is in `gtm_list_workspaces`). Give the customer the workspace's address as the server returns it, and say that publishing is theirs: in Tag Manager, Submit, then Publish (at the time of writing). Nothing fires until they do. To undo before then, they leave it unpublished or remove the tag and trigger in Tag Manager themselves.

Choose the event name with the customer: `CompleteRegistration` for a sign-up. For other actions, TikTok has been renaming some standard events, so read the exact name off the customer's own Events Manager rather than assuming. **Say what it counts:** a thank-you page view counts page views, including reloads, not proven new sign-ups.

If the customer set TikTok up through Events Manager's guided Tag Manager setup, or uses TikTok's Event Builder, their tags may look different from the shapes above. Read them by the parameters above and do not stage a second base code beside them.

## Conversion setup, in the order that works

Say each step in a sentence and what breaks if it is skipped:

1. Name the one action that counts: a sign-up, an enquiry or a sale.
2. Base code on every page.
3. The event for that action, on the page only a finished action reaches.
4. Test with one real action, in Test Events or the Pixel Helper.
5. Only then, in TikTok Ads Manager, choose that event as the campaign's goal. These are TikTok's own screens: AdCopilot cannot see or set them, and TikTok's help is the referee for the labels.
6. TikTok's Events API is its way of sending events from a server instead of the browser. AdCopilot cannot set it up: it is a developer's job or TikTok's own setup flow. If it is added beside the Pixel, TikTok's help describes how the two are matched so one action is not counted twice.

## Facts checked 23 October 2026

- TikTok's published Tag Manager template page (its README, changed 8 September 2026): base code goes in a Custom HTML tag on All Pages; the template needs the base code installed first; the template reads Google Analytics 4 events from the data layer and converts them into TikTok events; Events Manager's guided setup and Event Builder are TikTok's recommended routes.
- The base code loads its script from `analytics.tiktok.com` (the file is `/i18n/pixel/events.js` at the time of writing) and calls `ttq.load` with the pixel ID.
- The standard event names TikTok's template knows: ViewContent, ClickButton, Search, AddToWishlist, AddToCart, InitiateCheckout, AddPaymentInfo, CompletePayment, PlaceAnOrder, Contact, Download, SubmitForm, CompleteRegistration, Subscribe, CustomizeProduct, FindLocation, Schedule, ApplicationApproval, StartTrial, SubmitApplication and Purchase.

For anything not on that list, TikTok's own Events Manager and help are the referee: say so rather than answering from memory.

## Then

Offer, one at a time, the traffic check (what Analytics counts from TikTok) or the campaign plan. This plugin schedules nothing and makes no daily-check offer.
