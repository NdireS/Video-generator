---
name: scorp1-howto
description: Scorp1 style "howto": a clear step-by-step advert showing exactly how to order, book or use the business (WhatsApp ordering, booking, delivery, an app flow), so the barrier disappears. Used by /scorp1 --style howto; not a standalone workflow.
---

# Scorp1 style: howto

Show the path, step by step, with the real screens or the real counter. The viewer should finish thinking "that's easy, I can do that now", then do it. Friendly, clear and numbered.

If invoked directly (`/scorp1-howto <url>`), run `/scorp1 <url> --style howto` instead: Scorp1 runs the work, and this file is the creative brief it follows.

## When to pick it
- Comments ask "how do I order?", "do you deliver?", "how much?".
- Ordering is unusual or has steps: a WhatsApp builder, a deposit, a booking form, an app sign-up, M-Pesa payment.
- The website has a clear flow to show.

## Defaults
| Setting | Value |
|---|---|
| Format | vertical (phone flows look native); landscape if the flow is a desktop site |
| Duration | 30s (range 20–45) |
| Captions | on |
| Voice | elevenlabs |

## Structure
| Beat | Share of length | What happens |
|---|---|---|
| Promise | 0–12% | The outcome and how easy it is: "Your custom cake in three taps." |
| Steps | 12–80% | Three to five numbered steps, each a scene: the real screen or place, a finger or cursor doing the one action, the step number and a 2–4 word label. |
| Result | 80–90% | What arrives: the confirmation message, the delivery, the product in hand. |
| CTA | last 10–15% | Where to start (URL, number, handle, QR code), logo. |

## Voice
- Narrator: a helpful friend explaining, patient and upbeat. Voice Library search: "<country> <gender> friendly explainer clear".
- Model and settings: `eleven_multilingual_v2`, stability 0.55, similarity 0.8, style 0.15, speed 1.0; `wps` 2.5.
- Writing: imperative verbs, one per step ("Pick", "Type", "Tap", "Pay", "Collect"); say the step number only if it helps; name the real button labels exactly as they appear.
- Line pattern example: "Ordering is easy." / "Pick your cake and size." / "Type the message for the top." / "Tap Order on WhatsApp. Done."

## Look
- Type: big step numbers (1, 2, 3) in the brand accent; labels at 600 weight; the real UI text left as it is.
- Colour: neutral backgrounds so the brand's UI stands out; brand colour for numbers, highlights and the progress bar.
- Layout: a phone or browser frame centred and large; the step number and label above; a progress indicator (dots or a bar) for the steps.
- Imagery: real screens from the capture, re-created as HTML where a screenshot would be blurry (copy the exact labels, colours and layout from the site's code or capture); real photos for the result.

## Motion and effects
- Pace: one step per 4–6s; the action inside each step happens on the word that names it.
- Effects: a finger or cursor tap with a ripple, typing with a caret, a highlight ring around the button about to be tapped, zoom into the part of the screen that matters, a progress bar advancing per step, a chat bubble arriving for WhatsApp flows. Registry searches: "tap ripple", "cursor", "typing", "progress", "chat bubble", "phone mockup".
- Eases: `power3.inOut` for camera zooms, `power2.out` for taps (0.1s), `expo.out` for labels.

## Transitions
- Slide left per step (0.3s overlap) so it reads as moving forward; a zoom out to the full result; a brand flood into the CTA.

## Music
- Bundled pick: `assets/music/happy-beats-business-moves-vol-9-by-ende-dot-app.mp3` or `…-vol-11-…`; volume 0.28, `duck_to` 0.3 (clarity matters).
- Or ElevenLabs Music: "light upbeat lo-fi pop, soft beat, 95 BPM, friendly, no vocals".

## Sound effects
- Count: one per step plus the result, 5–8 for 30s.
- Families: `ui/mouseclick1` or `interface/click_*` on taps, `keyboard/keypress-*` thinned for typing, `casino/card-slide-*` on step changes, `interface/drop_*` when a message lands, `impactBell_heavy_000` or `casino/chips-collide-*` on the result.
- Custom ideas: a WhatsApp-style message "pop" (generic, not the real WhatsApp tone), a delivery doorbell.

## Captions
- On; the step label stays on screen, so captions carry only the narrator's extra words; lower third, above the phone frame's bottom.

## Call to action
- The exact starting point (URL, number, handle, QR) big enough to copy, logo, and "Start now" or "Order today"; hold 3s.

## Avoid
- Skipping a real step; UI that doesn't match the live site; tiny screens; more than five steps (split into two adverts instead).
