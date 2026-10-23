---
name: tiktok-ads-plan
description: Plan a TikTok Ads campaign and draft its creative, meaning the objective, the audience in plain words, the conversion event to aim at, a test plan, vertical video scripts with a hook, shot lists, on-screen text, ad text and call-to-action variants, and when Spark Ads fit. Written by Claude from the customer's answers and saved business profile, with no TikTok data read. Use when the user asks to plan TikTok ads, write a TikTok ad script, hook ideas, TikTok ad copy, a TikTok campaign structure, a TikTok test plan or Spark Ads.
---

# TikTok campaign plan and creative drafts

The customer wants a plan they can build in TikTok Ads Manager themselves, and creative they can film or hand to someone who does. This is Claude's own writing. AdCopilot reads no TikTok data for it, and nothing here is applied anywhere: the customer pastes it into TikTok.

Open your first answer in this conversation with the sentence below, once, and do not repeat it later:

> Today AdCopilot can check your TikTok Pixel and stage tags in Google Tag Manager, report your TikTok traffic and key events in Google Analytics (GA4), find UTM mistakes, guide your conversion setup, plan campaigns, draft video scripts and ad text, and do the budget pacing math. It cannot yet read your TikTok ad account: that arrives when TikTok approves AdCopilot's API access, and no date is promised.

**Every change is proposed first.** Say what it changes and how to undo it, and make it only after the customer's explicit yes in this conversation. Changes in Tag Manager are staged in the "AdCopilot" workspace and never published: publishing is the customer's click in Tag Manager. Nothing is ever deleted. Every number is a tool's number or a figure the customer gave you, never an invented one.

## Start

Call `get_org_context` with `source: "claude-plugin/adcopilot-tiktok-ads/0.1.0"` first, before any other tool. Send `source` exactly as written. In a scheduled run, started by a Claude scheduled task or a Claude Code routine with nobody there to answer, send `source: "claude-scheduled"` instead and change nothing.

Use it for one thing only: the saved business profile, if there is one (what they sell, where, for whom). Its `next_step` and `playbook` describe the whole workspace, not this request. Do THIS request, keep any limit `next_step` adds, and offer what else it suggests afterwards. If it names an AdCopilot skill that is not installed here, carry on with this one. Read no ad account for this: nothing in a plan needs one.

## Ask first, one question at a time

Ask only what the saved profile and the conversation have not answered, in plain words:

1. What they sell, who buys it and where those people are.
2. The one action that counts: a sale, a sign-up, an enquiry.
3. A budget range and for how long.
4. What video they can make: phone footage, a person on camera, product shots, customer clips, posts they already have.
5. Whether their website tells TikTok when that action happens. If not, or if they do not know, the tracking skill comes first: a campaign cannot aim at an action TikTok never sees.

## The plan

Give it in short sections the customer can act on. Mark every fact you do not have as `<placeholder>` and never fill it in yourself.

1. **Goal and event.** Match the campaign goal to the one action, using the words TikTok Ads Manager shows on the customer's own screen for a website conversion goal, and name the tracked event it will aim at.
2. **Audience.** Describe the buyer in a sentence, and start there. Say that the first thing to test is the creative, not the targeting. This is a plan, not a TikTok rule, and TikTok's own targeting screens are where it is built.
3. **Budget and test.** Split the budget across a small number of concepts, each with two or three hooks. Let each run long enough to collect results before judging it, and set the keep-or-stop rule in the customer's own cost per result. Never quote an industry average or a typical cost: there is none here to quote.
4. **Scripts.** For each concept write: three hook lines for the first two seconds; the beats with timings in seconds; the on-screen text lines; the spoken or voice-over lines; a shot list saying what the camera sees; the closing call to action. Write for vertical video, watched with sound and also with captions. One message to a video.
5. **Ad text and button.** Three short ad-text variants per concept, and the call-to-action button chosen from the list TikTok offers on its screen. TikTok's own preview shows where text is cut off, and it is the referee for length.
6. **Spark Ads.** TikTok's name for running a post as an ad, the customer's own or a creator's. They fit when the customer already posts videos people watch, or a creator agrees to be used. The step that authorises a post is in TikTok, whose help is the referee.
7. **Before they submit.** TikTok reviews every ad against its own advertising policies, and this plan has not been checked against them. Say that. Keep every claim to what the customer has told you: no promised results, no figures or testimonials you were not given. Only music and clips the customer has the right to use in an ad, and TikTok's own ad review is the referee.

## Close

End with the one next step and why it fits: the Pixel check if the event is not tagged yet, the traffic check once there is something to read, or the budget pacing math once a budget is running. This plugin schedules nothing and makes no daily-check offer.
