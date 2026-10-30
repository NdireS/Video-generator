---
name: scorp1-product
description: Scorp1 style "product": a spotlight advert for one product or service, built around close-ups, details, price and the reason to want it now. Used by /scorp1 --style product (pair with --product "<name>"); not a standalone workflow.
---

# Scorp1 style: product

One thing, shown like it matters. The product is the hero of every frame; the voice gives it a reason to want it, and the price (if public) and how to get it close the sale. Sensory and close-up, with a confident rhythm.

If invoked directly (`/scorp1-product <url>`), run `/scorp1 <url> --style product` instead: Scorp1 runs the work, and this file is the creative brief it follows.

## When to pick it
- `--product` was given, or one item dominates the site's hero, the best-performing posts or the comments.
- The business has good close-up photos or video of that item.

## Defaults
| Setting | Value |
|---|---|
| Format | vertical (Reels, TikTok, Status) |
| Duration | 20s (range 10–30) |
| Captions | on |
| Voice | elevenlabs |

## Structure
| Beat | Share of length | What happens |
|---|---|---|
| Hook | 0–12% | The product, full-frame and close, with a 3–5 word line that names a desire ("Soft. Moist. Gone by Sunday."). |
| Details | 12–55% | Two or three detail shots or features, each tied to a benefit in the voice (texture, size, ingredients, what it does). |
| Proof or use | 55–80% | It in use or in someone's hands, or one real review line or rating. |
| Offer and CTA | last 20% | Name, price (only if public), how to order, one verb. |

## Voice
- Narrator: close and intimate, almost talking to one person; slightly lower energy than launch. Voice Library search: "<country> <gender> smooth intimate narration" or "ASMR-light conversational".
- Model and settings: `eleven_multilingual_v2`, stability 0.5, similarity 0.8, style 0.3, speed 0.95; `wps` 2.4. For a playful brand, `eleven_v3` with tags such as `softly` or `playful`.
- Writing: sensory words from the product's real description; short fragments allowed; one benefit per line; say the price the way people say it ("just fifteen hundred bob" if that is how the brand talks).
- Line pattern example: "Three layers. Real butter." / "Baked the morning you collect it." / "Red velvet, fifteen hundred shillings. Order on WhatsApp."

## Look
- Type: large, few words, set over or beside the product; product name in the brand font at 800; price in a contrasting pill or tag.
- Colour: background sampled from the product photo or brand colour; keep it calm so the product pops.
- Layout: product centred and large (60–80% of the frame); text above or below, never covering it.
- Imagery: the best real photos, cut out (`npx hyperframes remove-background` via `/media-use`) when the background is busy; a soft shadow under cut-outs; never stretch a low-resolution photo full-frame.

## Motion and effects
- Pace: 2–4s per shot; a move on every shot.
- Effects: slow push-in and parallax on stills (product and background at different speeds), a gentle 2–4° rotation on cut-outs, light sweep or sheen across glossy products, detail zooms with a circular mask, a price tag that drops and settles. Registry searches: "parallax", "light sweep", "price tag", "zoom".
- Eases: `power3.out` for pushes, `back.out(1.6)` for the price tag, `expo.out` for text.

## Transitions
- Zoom-through from hook to details (the camera pushes into a detail, 0.3s overlap).
- Whip pans or quick slides between details (0.25s), all in the same direction.
- Hard cut on a strong beat into the offer.

## Music
- Bundled pick: `assets/music/happy-beats-business-moves-vol-10-by-ende-dot-app.mp3` for snappy, `…-vol-12-…` for premium; volume 0.32, `duck_to` 0.35.
- Or ElevenLabs Music: "smooth modern R&B instrumental, warm bass, soft keys, 95 BPM, premium, no vocals" (food, beauty, fashion) or "punchy electronic pop, 120 BPM" (tech, gadgets).

## Sound effects
- Count: 3–5 for 20s.
- Families: `impactSoft_medium_*` on the hero reveal, `casino/card-place-*` or `interface/drop_*` as details land, `casino/chip-lay-*` on the price, `ui/click*` on the order tap.
- Custom ideas: the product's own sound (a fizz, a crunch, a zip, a sizzle, a box opening).

## Captions
- On: bold, 2–4 words per caption, centred in the lower third, the spoken word in the brand accent; never over the product.

## Call to action
- Product name, price if public, and the channel ("DM 'CAKE' to order", "Tap the link in bio"). Hold 2s after the voice ends.

## Avoid
- More than one product; lists of features without benefits; prices that aren't public; text over the product; slow fades.
