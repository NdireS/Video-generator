---
name: scorp1-proof
description: Scorp1 style "proof": a social-proof advert where real public reviews, ratings, customer posts and numbers do the selling, framed by the product and a clear CTA. Used by /scorp1 --style proof; not a standalone workflow.
---

# Scorp1 style: proof

Let customers sell it. Real, attributable quotes and numbers arrive one after another as the product appears between them, until the viewer thinks "everyone loves this" and gets told how to try it.

If invoked directly (`/scorp1-proof <url>`), run `/scorp1 <url> --style proof` instead: Scorp1 runs the work, and this file is the creative brief it follows.

## When to pick it
- There are public Google, Facebook, Jumia or site reviews, a strong star rating, glowing comments on posts, or tags from customers.
- The business is good but not yet well known, so trust is the barrier.

## Integrity rules (non-negotiable)
- Only use reviews and comments that are public and visible in the sources, quoted word for word (trimmed with "…" is fine; never reworded).
- Attribute each one as the platform shows it (first name and initial, or the handle). If the person prefers anonymity, use "Google review" and the date.
- Ratings and counts must match the source on the day. Note each source in `research/sources.md`.
- If there are fewer than three usable reviews, tell the person and suggest `launch` or `product` instead.

## Defaults
| Setting | Value |
|---|---|
| Format | vertical; square for Facebook |
| Duration | 25s (range 15–35) |
| Captions | on |
| Voice | elevenlabs (narrator reads the frame lines; the reviews are read on screen, optionally voiced by a second voice) |

## Structure
| Beat | Share of length | What happens |
|---|---|---|
| Hook | 0–12% | The strongest number or quote: "4.9 stars from 230 reviews", or a short wild quote. |
| Quotes | 12–70% | Three or four review cards, each with a product shot between or behind it; the narrator links them in a few words. |
| Number | 70–85% | One real aggregate (rating, orders, years, followers) counting up. |
| CTA | last 15% | "Join them": the product, logo and the action. |

## Voice
- Narrator: friendly and trustworthy, mid energy. Voice Library search: "<country> <gender> friendly conversational". Optional second voice for reading one review aloud (a different age or gender; label it `VO0n` like any line).
- Model and settings: `eleven_multilingual_v2`, stability 0.5, similarity 0.8, style 0.2, speed 1.0; `wps` 2.6.
- Writing: the narrator never praises; customers do. Narrator lines are bridges: "They said it first." / "And again." / "Two hundred and thirty of them agree."
- Line pattern example: "Don't take our word for it." / "Four point nine stars, from two hundred and thirty reviews." / "Try your first one this week."

## Look
- Type: quotes in large quotation marks, 500 weight, sentence case, at most 18 words per card; the reviewer's name small beneath with the platform icon and stars.
- Colour: cards in white or brand-light with a soft shadow over brand-colour or product backgrounds; stars in gold (#F5B301) or the brand accent.
- Layout: one card at a time, centred, 80% wide; product photography fills the background, blurred or darkened enough for contrast.
- Imagery: real product photos and, where public, the actual post or review screenshot cropped neatly.

## Motion and effects
- Pace: each review holds at least 0.3s per word plus 1s; cards replace each other every 3–5s.
- Effects: card stack (new card slides over the old), stars filling one by one, a counter rolling up for the aggregate, a highlight pen stroke under the key phrase in a quote. Registry searches: "card stack", "star rating", "counter", "highlighter".
- Eases: `expo.out` card entrances 0.5s, `power2.inOut` stack moves, `steps` or `power1.out` for counters.

## Transitions
- Card-over-card slides inside the quotes beat (0.3s overlap); a push to the number; a brand-colour wipe into the CTA.

## Music
- Bundled pick: `assets/music/happy-beats-business-moves-vol-11-by-ende-dot-app.mp3` (warm) or `…-vol-9-…`; volume 0.3, `duck_to` 0.35.
- Or ElevenLabs Music: "feel-good acoustic pop, hand claps, bright guitar, 100 BPM, no vocals".

## Sound effects
- Count: 4–6 for 25s.
- Families: `casino/card-slide-*` per card (first and last at least), `impactGlass_light_*` or `interface/select_008` as stars fill, `casino/chips-stack-*` under the counter, `impactBell_heavy_000` on the CTA.

## Captions
- On for the narrator only (review text is already on screen); small, lower third.

## Call to action
- "Join <n> happy customers" only if n is real; product, logo, action and handle; hold 2s.

## Avoid
- Invented or edited reviews; stock "customer" photos; showing personal details beyond the public name; overcrowded cards.
