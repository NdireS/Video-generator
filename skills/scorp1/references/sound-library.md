# Sound library

Everything here ships in `<skill-dir>/assets/`. Paths in `plan.json` are relative to `<skill-dir>` (for example `assets/sfx/interface/drop_001.ogg`). Catalogue adapted from the brag plugin (MIT).

## Music

All are "Happy Beats / Business Moves" by Sascha Ende (ende.app), **CC BY 4.0**. The credit `Music: Sascha Ende, ende.app (CC BY 4.0)` must go in `credits.txt` and the post caption. Each has a cue preset in `assets/music/cues/` (beats and strong cues for the first 25 seconds; past that, snap to the beat grid by eye or run `npx hyperframes beats`).

| File (`assets/music/…`) | Length | Character | Good for |
|---|---|---|---|
| `happy-beats-business-moves-vol-1-by-ende-dot-app.mp3` | 2:44 | Most energetic, bright | launch, offer |
| `happy-beats-business-moves-vol-9-by-ende-dot-app.mp3` | 1:54 | Mid energy, laid back | howto, proof |
| `happy-beats-business-moves-vol-10-by-ende-dot-app.mp3` | 1:00 | Compact, punchy | offer, product (short cuts) |
| `happy-beats-business-moves-vol-11-by-ende-dot-app.mp3` | 1:28 | Warm, business-like | proof, howto |
| `happy-beats-business-moves-vol-12-by-ende-dot-app.mp3` | 1:58 | Steady, clean, polished | launch, product, story (low) |

All five are upbeat. For a mood they can't do (emotional, cinematic, Afrobeats or amapiano, luxury, lo-fi), use ElevenLabs Music with a prompt and keep a bundled `fallback` (see `plan.md`).

Levels under a voice: bed at 0.25–0.35 `volume`, `duck_to` 0.3–0.4. Without voice: 0.5–0.7.

## Sound effects

Kenney (CC0) and unicae_games keyboard set (CC0). Read `assets/sfx/sfx-analysis.md` for brightness and harshness per file. Prefer low or medium high-frequency risk for anything repeated or under a voice.

### `assets/sfx/interface/`
| Files | Character | Use for |
|---|---|---|
| `click_001–005.ogg` | Sharp, precise | Button tap, CTA tap |
| `select_008.ogg` | Selection click | Item focus, a choice made |
| `drop_001–003.ogg` | Soft drop | Text or card landing, gentle reveal |
| `switch_001–002.ogg`, `switch_004–007.ogg` | Toggle | Option switched on |
| `bong_001.ogg` | Deep bell | One announcement, sparingly |
| `glitch_002.ogg`, `glitch_004.ogg` | Digital distortion | Tech moment, deliberate glitch |
| `error_005–006.ogg` | Negative buzz | "Before" pain point, comic fail |

### `assets/sfx/impact/`
| Files | Character | Use for |
|---|---|---|
| `impactSoft_medium_000–004.ogg` | Medium soft thud | Reveal, hard cut (safest) |
| `impactSoft_heavy_000–004.ogg` | Heavy soft thud | Weight, a price slam |
| `impactBell_heavy_000.ogg`, `_003`, `_004` | Deep bell | Logo, hero reveal, big claim |
| `impactWood_light_000–004.ogg` / `_medium_` | Warm wood knock | Organic, food, craft, handmade |
| `impactGlass_light_001–003.ogg` | Glass clink | Sparkle, drinks, delicate success |
| `impactPlate_light_000–004.ogg` | Light metal plate | Notification, crisp accent |
| `impactPunch_medium_000–004.ogg` / `_heavy_` | Punch | Aggressive beat, sale slam |
| `impactGeneric_light_000–004.ogg` | Light hit | Small accent anywhere |
| `footstep_wood_000–002.ogg`, `_004` | Soft step | Scroll, step-through |

### `assets/sfx/casino/`
| Files | Character | Use for |
|---|---|---|
| `card-slide-1–8.ogg` | Slide | Swipe, a panel sliding in |
| `card-place-1–4.ogg` | Placement | Item or photo landing |
| `card-fan-1–2.ogg` | Fan | Several items appearing |
| `cards-pack-open-1–2.ogg` | Pack opening | Unboxing, product reveal |
| `chip-lay-1–3.ogg` | Chip placed | Price or number confirmed |
| `chips-stack-1–6.ogg` | Stacking | Counter climbing, savings adding up |
| `chips-collide-1–4.ogg` | Clink | Success with weight, a deal |

### `assets/sfx/ui/`
| Files | Character | Use for |
|---|---|---|
| `click1–5.ogg`, `mouseclick1.ogg` | Clean clicks | Simulated taps and clicks |
| `rollover1–2.ogg`, `rollover4–5.ogg` | Very soft | Hover, subtle highlight |
| `switch1–38.ogg` | Switch variants | Toggles, mode changes |

### `assets/sfx/keyboard/`
`keypress-001.wav` … `keypress-032.wav`: one keypress each. For typing on screen, use a different file per character, and thin them out under a voice.

## Timing

- A sound starts with the action: 0–0.1s before the element's first visible frame.
- Under a voice, place effects in the gaps between words, or on the word that names the action.
- In a sequence, sound the first, the last, or the strongest item, not every one.
- One palette per advert. A bakery gets wood and glass, a fintech app gets clicks and plates, a club night gets punches.
