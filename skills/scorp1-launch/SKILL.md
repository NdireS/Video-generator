---
name: scorp1-launch
description: Scorp1 style "launch": a confident "we're live" advert for something new (a website, app, shop, branch, menu or service), showing the real thing and how to start using it. Used by /scorp1 --style launch; not a standalone workflow.
---

# Scorp1 style: launch

News, told with pride. The viewer should finish knowing what just opened, why it is better than before, and the exact first step. Bright, clean and fast in the picture, unhurried in the voice.

If invoked directly (`/scorp1-launch <url>`), run `/scorp1 <url> --style launch` instead: Scorp1 runs the work, and this file is the creative brief it follows.

## When to pick it
- The profile mentions something new: "now online", "grand opening", "new branch", "new menu", a new app or site, a rebrand.
- Recent posts announce or tease it.

## Defaults
| Setting | Value |
|---|---|
| Format | landscape for website and YouTube; vertical if the profile says Reels or TikTok first |
| Duration | 30s (range 20–45) |
| Captions | off in landscape, on in vertical |
| Voice | elevenlabs |

## Structure
| Beat | Share of length | What happens |
|---|---|---|
| Hook | 0–12% | The news in one line over the hero image or product: "Juja's favourite cake plug just went online." Brand colour fills the frame by the first second. |
| Reveal | 12–30% | The new thing itself: the site on a device, the shop front, the menu. One push-in. |
| Highlights | 30–80% | Two or three concrete things it lets you do, each a scene: real screens or real products, one action each (a tap, a pick, a send). |
| CTA | last 15–20% | Logo, the exact address or handle, one verb ("Order today", "Visit us at…"). Logo lands on a strong music cue. |

## Voice
- Narrator: the business's own register, warm and proud; often a local voice of the owner's age group. Voice Library search: "<country> <gender> warm narration" or "friendly announcer".
- Model and settings: `eleven_multilingual_v2`, stability 0.45, similarity 0.8, style 0.25, speed 1.0; `wps` 2.6.
- Writing: short sentences, "you" and "your", present tense, one fact per line. The hook names the place or the audience. No "introducing" as the first word.
- Line pattern example: "Nairobi, your weekend brunch spot is now on your phone." / "Book a table in two taps." / "Mama Oliech's. Open now."

## Look
- Type: the brand font if known; otherwise Inter or Nunito at 800 for headlines, 500 for labels. Headlines 2–6 words, sentence case, tight tracking (−0.03em).
- Colour: brand primary as large flat fields; one accent for buttons and highlights; cream or near-white for screens to sit on.
- Layout: big type on the left third, media on the right two thirds (landscape); type top, media middle, CTA bottom (vertical). 90% action-safe.
- Imagery: real photos cut into simple shapes (arches, circles, rounded cards) with a soft shadow; site screens in a clean device frame or a floating card, never a blurry screenshot.

## Motion and effects
- Pace: a new scene every 4–7s; something moves inside each scene every 1–1.5s.
- Effects: mask reveals (wipe or shape), per-word headline rise, a slow 3–5% push-in on photos, a cursor or finger tap on real UI, a counter or price tick where real numbers exist. Registry searches: "mask reveal", "kinetic type", "device mockup", "cursor".
- Eases: entrances `expo.out` 0.5–0.7s; UI taps `power2.out` 0.08–0.15s; settle with `back.out(1.4)` on stickers and badges only.

## Transitions
- Brand-colour wipe from the hook to the reveal (0.4s overlap).
- Match cuts or slides between highlights (0.3s overlap); keep the direction consistent.
- Colour flood into the CTA (0.4s overlap).

## Music
- Bundled pick: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` (polished), or `…-vol-1-…` for louder, younger brands; volume 0.3, `duck_to` 0.35, fade out 1.5s.
- Or ElevenLabs Music: "upbeat modern pop instrumental, bright plucks and claps, 110 BPM, optimistic, clean, no vocals".

## Sound effects
- Count: 4–6 for 30s.
- Families: `interface/drop_*` for headlines landing, `ui/mouseclick1` or `interface/click_*` for taps on screens, `casino/card-place-*` for photos landing, one `impactBell_heavy_000` or `interface/bong_001` for the logo.
- Custom ideas: a sound from the trade (an oven ding, a till drawer, a door chime, a coffee machine hiss) on the reveal.

## Captions
- Vertical only: bottom third above the platform UI, 2 lines at most, white on a 70% brand-dark pill, the spoken word highlighted in the accent colour.

## Call to action
- Show the logo, the exact URL or handle, and the one action ("Order on WhatsApp"); say the action and the name. Hold at least 2.5s after the voice ends.

## Avoid
- A logo-only first second; stock footage; claims the site doesn't make ("fastest", "#1"); more than three highlights; reading the URL letter by letter.
