---
name: scorp1-story
description: Scorp1 style "story": a warm, cinematic brand-story advert about who is behind the business, why they started and the craft, ending on an invitation. Used by /scorp1 --style story; not a standalone workflow.
---

# Scorp1 style: story

People buy from people. This advert makes the viewer feel they know the owner and trust the craft. It is slower, warmer and more cinematic than the other styles, with room for silence and one emotional turn.

If invoked directly (`/scorp1-story <url>`), run `/scorp1 <url> --style story` instead: Scorp1 runs the work, and this file is the creative brief it follows.

## When to pick it
- The profile has an About page, founder posts, behind-the-scenes content, or the owner's face on the account.
- The posts that get the most comments are personal (the first cake, the hard year, the team).
- The business sells craft, care or community more than price.

## Defaults
| Setting | Value |
|---|---|
| Format | landscape (YouTube, website, Facebook); vertical cut-down for Reels |
| Duration | 45s (range 30–60) |
| Captions | on (people watch stories silent) |
| Voice | elevenlabs; first person ("I") if the owner tells it, third person if a narrator does |

## Structure
| Beat | Share of length | What happens |
|---|---|---|
| Moment | 0–12% | A quiet, specific image and line: hands at work, the shop at dawn. "Every cake starts at five a.m." |
| Origin | 12–40% | Why they started; one real fact from the About page or posts (the year, the first customer, the kitchen). |
| Craft | 40–70% | How it is made or done, in close detail; what they refuse to compromise on. |
| Today | 70–85% | The business now: customers, the team, the shop, the website; a real number if public (years, orders, followers). |
| Invitation | last 15% | Logo, where to find them, a warm verb ("Come say hello", "Order your first one"). |

## Voice
- Narrator: the owner's age, gender and accent where known; calm, sincere, unhurried. Voice Library search: "<country> <gender> storytelling warm calm" or "documentary narrator gentle".
- Model and settings: `eleven_multilingual_v2`, stability 0.6, similarity 0.85, style 0.2, speed 0.92; `wps` 2.3. `eleven_v3` with `warmly` or `softly` for one or two lines at most.
- Writing: concrete memories over adjectives; short sentences with a pause after; one line of their own words from the site or a post, quoted. No hype words.
- Line pattern example: "My mum baked on a jiko. I still use her recipe." / "Twelve years later, Juja knows our cakes." / "Come and taste where it started."

## Look
- Type: an elegant serif (for example the brand's, or a bundled serif) for spoken-word quotes; a light sans for labels; small and generous margins; letterboxed 2.39:1 bars optional in landscape.
- Colour: warm, slightly desaturated grade on photos (through `npx hyperframes media-treatment` via `/media-use`, never CSS filters); brand colour used sparingly, mostly at the end.
- Layout: full-bleed photos; text small in a lower corner or centred over darkened space.
- Imagery: the business's own photos of people, hands, place and process. Ken Burns movement on every still. If there are no people photos, use process and place, never stock faces.

## Motion and effects
- Pace: 4–7s per shot; long holds are allowed.
- Effects: slow Ken Burns (3–6% over the shot), soft film grain and a gentle vignette through media-treatment, light leaks on one or two transitions, quote text revealed line by line with a soft blur-in. Registry searches: "film grain", "light leak", "ken burns", "quote".
- Eases: `sine.inOut` and `power1.inOut`, 1–2s; nothing bounces.

## Transitions
- Slow cross-dissolves (0.8–1.2s overlap); one dip to black before the "Today" beat; a match on shape or colour where possible.

## Music
- Bundled pick: `assets/music/happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` at volume 0.18 only if nothing else is available; it is upbeat for this style.
- Preferred: ElevenLabs Music with `source: "elevenlabs"` and vol-12 as `fallback`: "gentle acoustic piano and soft strings, warm and hopeful, slow build, 75 BPM, cinematic, no vocals". Volume 0.28, `duck_to` 0.4.

## Sound effects
- Count: 1–3 for 45s. Mostly let music and voice carry it.
- Families: `impactBell_heavy_003` softly on the logo; `impactWood_light_*` on one tactile moment.
- Custom ideas: real ambience of the trade under the first scene (a kitchen at dawn, a sewing machine, rain on a shop roof), 2–4s, low.

## Captions
- On, sentence-style (not word-pop), lower third, light weight, one line where possible, a soft shadow; no highlighting.

## Call to action
- Gentle and specific: "Visit us on Kamiti Road" or "Order at faithpastries.co.ke"; logo on brand colour; hold 3s with music resolving.

## Avoid
- Invented biography details; stock footage of people; fast cuts; slams and loud effects; reading the About page verbatim.
