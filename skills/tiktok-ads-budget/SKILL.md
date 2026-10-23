---
name: tiktok-ads-budget
description: Do TikTok Ads budget pacing math from the customer's own figures, meaning projected spend, the daily amount that lands the budget exactly, and whether spending is over or under pace. Claude's own arithmetic, with no tool and no TikTok data read. Use when the user asks whether their TikTok spend is on pace, how much to spend per day, what a TikTok budget will cost by the end of the month, or to split a TikTok budget across campaigns or days.
---

# TikTok budget pacing

The customer wants to know whether TikTok spend is on track. This skill calls no AdCopilot tool and reads no TikTok data. The figures are the customer's, copied from their own TikTok Ads Manager report, and the arithmetic is Claude's, shown in full so they can check it.

Open your first answer in this conversation with the sentence below, once, and do not repeat it later:

> Today AdCopilot can check your TikTok Pixel and stage tags in Google Tag Manager, report your TikTok traffic and key events in Google Analytics (GA4), find UTM mistakes, guide your conversion setup, plan campaigns, draft video scripts and ad text, and do the budget pacing math. It cannot yet read your TikTok ad account: that arrives when TikTok approves AdCopilot's API access, and no date is promised.

**Every change is proposed first.** Say what it changes and how to undo it, and make it only after the customer's explicit yes in this conversation. Changes in Tag Manager are staged in the "AdCopilot" workspace and never published: publishing is the customer's click in Tag Manager. Nothing is ever deleted. Every number is a tool's number or a figure the customer gave you, never an invented one.

## What to ask for

Ask for what is missing, one question at a time, and use the customer's currency and calendar as they give them:

1. The budget, and whether it is a total for the period or a daily amount.
2. The period's first and last day.
3. The spend so far, and the date it is as of.
4. Whether those figures include tax. Compare like with like: do not set a figure with tax beside one without.

## The arithmetic

Let B be the budget for the period, T the days in it, D the days gone as of the date given, and S the spend so far.

- Average per day so far: S / D.
- Projected spend at that pace: (S / D) x T.
- Pace against budget: S / (B x D / T), as a percentage. Over 100% is over pace, under 100% is under.
- Daily amount that lands exactly on budget from the next day: (B - S) / (T - D).

Worked example, in the customer's own currency: a budget of 1,500 over 30 days, with 600 spent after 10 days. The average is 60 a day. The projection is 60 x 30 = 1,800, which is 300 over budget. The pace is 600 / (1,500 x 10 / 30) = 600 / 500 = 120%. To land on budget, spend (1,500 - 600) / (30 - 10) = 45 a day from tomorrow.

Then say it in one plain sentence: "At this pace you will spend X by the end of the period, which is Y over (or under) your budget. To land on it, spend Z a day from tomorrow."

If the customer gives a daily budget and not a total, treat the total as the daily amount times the days in the period, and say you did.

To split a budget across campaigns or days, use the weights the customer gives and show each share. If they give none, ask for them. Do not choose weights for them.

## What this cannot know

- What TikTok will actually spend. TikTok decides how spend is delivered, and it can vary from day to day. TikTok's own report is the referee for what has been spent, and its own screens for what a campaign can spend per day.
- Anything about results. This is arithmetic on spend. It says nothing about whether the spend is working.
- Never quote a benchmark, an average cost or a recommended budget. Every number is one the customer gave you or one computed from theirs, with the working shown.

## Close

If the pace is off, say what the customer would change in TikTok Ads Manager's own budget settings (they make the change, not you), and offer the traffic check to see what the spend brought to the site. This plugin schedules nothing and makes no daily-check offer.
