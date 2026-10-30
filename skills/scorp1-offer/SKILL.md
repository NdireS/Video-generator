---
name: scorp1-offer
description: Scorp1 style "offer": a fast, loud, deadline-driven promo for a discount, bundle, seasonal deal or limited run, built to stop the scroll and drive one action now. Used by /scorp1 --style offer; not a standalone workflow.
---

# Scorp1 style: offer

The deal is the headline. The viewer must understand what they get, what it costs, until when, and how to claim it, in under 15 seconds and with the sound off. Big type, bold colour, a beat that pushes.

If invoked directly (`/scorp1-offer <url>`), run `/scorp1 <url> --style offer` instead: Scorp1 runs the work, and this file is the creative brief it follows.

## When to pick it
- The brief or the latest posts mention a price cut, a percentage, a bundle, "buy one get one", a season (Christmas, Valentine's, Easter, Black Friday, back to school) or a date.
- Never invent an offer. If there is none in the sources, ask the person for the exact terms before planning.

## Defaults
| Setting | Value |
|---|---|
| Format | vertical; square for Facebook feed |
| Duration | 15s (range 6–20; 6s for a bumper) |
| Captions | on, and the key numbers on screen regardless |
| Voice | elevenlabs (or none: this style works silent) |

## Structure
| Beat | Share of length | What happens |
|---|---|---|
| Stop | 0–15% | The number: "30% OFF", "2 for 1", "KSh 999", huge, slamming in on the first beat. |
| What | 15–45% | The product or bundle that the deal applies to, with the old and new price if public. |
| When | 45–70% | The deadline or the season ("This weekend only", "Until 14 Feb"), with a ticking or countdown motif. |
| Claim | last 30% | How to claim it: code, keyword, link, location; logo; one verb. |

## Voice
- Narrator: energetic, upbeat, a smile in the voice, slightly faster. Voice Library search: "energetic promo announcer <country>" or "radio ad <gender>".
- Model and settings: `eleven_v3` with tags `excited` or `energetic` (generate two takes), or `eleven_multilingual_v2` at stability 0.35, similarity 0.8, style 0.4, speed 1.08; `wps` 2.9.
- Writing: lead with the number, then the thing, then the deadline, then the action. Repeat the deal once at the end. Plain words: "half price", "free delivery", "this weekend only".
- Line pattern example: "Thirty percent off every birthday cake!" / "This weekend only." / "Order on WhatsApp before Sunday."

## Look
- Type: heavy (900) condensed or rounded display at the largest size that fits; the number at 40–60% of the frame width; strike-through on the old price.
- Colour: brand primary plus one hot accent (yellow, red, lime) for the number; high contrast throughout so it reads silent.
- Layout: number centred; product beneath or behind; deadline as a band or sticker; CTA in a button shape.
- Imagery: product cut-outs on flat colour; stickers, badges and starbursts are welcome here.

## Motion and effects
- Pace: a change every 1–2s; the whole video moves to the beat.
- Effects: scale slam with a small screen shake on the number, a strike-through drawn across the old price, a countdown or ticking clock, sticker pops, a looping marquee band with the deadline. Registry searches: "shake", "slam", "marquee", "countdown", "sticker", "burst".
- Eases: `back.out(2)` and `elastic.out(1, 0.5)` for slams and stickers; `steps()` for ticking; `expo.out` for type.

## Transitions
- Hard cuts on strong beats; a quick zoom blur or flash frame (one frame of accent colour) at most twice. Overlaps of 0–0.15s.

## Music
- Bundled pick: `assets/music/happy-beats-business-moves-vol-10-by-ende-dot-app.mp3` (punchy) or `…-vol-1-…`; volume 0.4, `duck_to` 0.45 (the bed stays loud).
- Or ElevenLabs Music: "high energy Afrobeats / amapiano groove, log drums, 115 BPM, festive, no vocals", or a seasonal variant ("festive Christmas pop, sleigh bells, 120 BPM").

## Sound effects
- Count: 5–8 for 15s.
- Families: `impactSoft_heavy_*` or `impactPunch_medium_*` on the number, `casino/chips-stack-*` on prices, `interface/switch_*` or `ui/click*` on the CTA, `casino/chips-collide-*` on the claim.
- Custom ideas: a cash register "ka-ching", a whoosh, a stopwatch tick.

## Captions
- Always on, big and centred, 1–3 words per caption, numbers in the accent colour.

## Call to action
- The claim path in full (code, keyword, link or place) and the deadline again; hold 2s.

## Avoid
- Small print you can't read; more than one offer; fake urgency (no real deadline, no countdown); invented "was" prices.
