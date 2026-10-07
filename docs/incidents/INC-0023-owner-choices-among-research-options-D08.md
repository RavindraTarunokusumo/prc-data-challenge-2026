---
schema: incident-v1
incident_id: INC-0023
type: owner_intervention
created_utc: 2026-10-07T22:10:59Z
status: open
---

# Day 8: owner choices among researcher-written research options (D08-S03, 2026-10-07)

**Raised by:** the researcher, under X-D08-S03-0004 Q3. Every owner intervention is logged (brief §1). G3 makes an owner choice among research items an incident of INC-0015's type.

**Times.** The chat's UTC times were not measured. Each is bounded by the commit times on either side (`git show -s --format=%cI`, converted to UTC).

## Exchange 1: the weather hosts unreachable

**Time:** after commit `e93eb64` (18:50:08Z), before `3209793` (19:21:12Z).

**Options the researcher offered (verbatim):**
> 1. **Run the download yourself** from your own terminal in the repo. It saves monthly files and a manifest, and I take it from there
> 2. **Let this session reach the two weather sites.** You'd change that in your Claude Code permission settings. I can't change it myself.
> 3. **Drop weather** for this phase. I'd move on to the next items on the list that need no outside data: recording conventions at airports other than Rome, the routed Rome subgroup, and how many training rounds CatBoost uses.

**Owner (verbatim):**
> Your script doesn't work. I'll adjust the permissions. What do I need to do.

**Reading:** the owner chose to keep weather (not option 3). The researcher's diagnosis behind option 2 was wrong (D8-C14).

## Exchange 2: the nine-airport fetch

**Time:** after `3790c82` (19:25:54Z).

**The researcher's request (verbatim):**
> **What I need from you:** the same download for the other nine airports.

The researcher stated the alternative as:
> If you'd rather skip the extra download, the other option is to drop weather and move on to the remaining items that need no outside data.

The request rested on a mechanism the researcher overstated (D8-C15).

**Owner (verbatim):** "It's running"

## Exchange 3: after the weather pilot

**Time:** after `2d53d34` (21:34:39Z), before `a37f95e` (21:41:44Z).

**Options the researcher offered (verbatim, abridged to the option lines):**
> 1. **Accept dropping weather.** That leaves three items, and none looks strong: [recording quirks at airports other than Rome; the routed Rome subgroup; CatBoost's number of training rounds]. My recommendation is a short look at the first one, using only the months no fold scores on. If nothing turns up, close Day 8 with the current champion kept and no new upload.
> 2. **Override my rule** and have me propose the weather-for-ordinary-flights version anyway, with the selection stated openly.

**Option 2 offered the owner a route around a pre-registered rule.** It invited a restricted weather candidate after `WX_pilot_params.yaml`'s rule had failed. The researcher should not have offered it (X-D08-S03-0004 Q3).

**Owner (verbatim):**
> Option 1, go ahead with the recording quirks look

## Exchange 4: after the item 1 look

**Time:** after `e65515f` (21:42:19Z), before 21:44:22Z (DAY_SUMMARY's measured time).

**Options the researcher offered (verbatim, abridged to the option lines):**
> 1. **Close Day 8 now (my recommendation).** The advisor reviews the phase close, and we keep the current champion with no new upload, which is the default rule anyway. We would then decide whether Days 9–12 continue or the project refreezes.
> 2. **Try one of the last two items first:** the routed Rome subgroup [...]; CatBoost's number of training rounds [...]. I think both are weak.

**Owner (verbatim):**
> Option 1, close Day 8

## Effect

- **The owner chose among researcher-written options,** as in INC-0015. The owner selected no feature, parameter, threshold or population.
- **Every option the owner took** was the researcher's recommendation, or an option keeping existing rules:
  - keep weather;
  - the nine-airport fetch;
  - drop weather and look at item 1;
  - close Day 8.
- **No option the owner took changed a pre-registered rule.**
- **The choices were research-direction choices.**
  - DAY_SUMMARY's "No G2 or G3 breach is recorded in Day 8" is amended to cite this incident.
  - The final report discloses it.
- **From X-D08-S03-0004 on,** the only question put to the owner is "continue or refreeze", with the review's bounds stated (Q3).

## Resolution

Open. Closes at the last Day 8–12 phase close, with its disclosure in the final report.
