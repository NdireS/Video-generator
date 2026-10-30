# Styles

A style is a skill named `scorp1-<style>`. It sets the advert's structure, pacing, voice, look, effects, transitions, music, sound effects, captions and call to action. Scorp1 runs the work; the style decides how it looks and sounds.

## Bundled styles

| Style | Skill | Use when | Default format, length |
|---|---|---|---|
| `launch` | `scorp1-launch` | Something is new: a website, app, shop, branch, menu or service | landscape, 30s |
| `product` | `scorp1-product` | One product or service should be the hero | vertical, 20s |
| `offer` | `scorp1-offer` | A discount, bundle, seasonal deal or deadline | vertical, 15s |
| `story` | `scorp1-story` | Who is behind it, why they started, the craft | landscape, 45s |
| `proof` | `scorp1-proof` | Real public reviews, ratings or customer posts do the selling | vertical, 25s |
| `howto` | `scorp1-howto` | Buying or booking has steps people don't know | vertical, 30s |

## Recommending one

Read the profile's angle and platform usage:
- There's news (just opened, new site, new branch) → `launch`.
- One item dominates the sales, posts or comments → `product`.
- There's a price, a date or "limited" in the brief → `offer`.
- The founder, the craft or the place is the draw (often seen in posts that get the most comments) → `story`.
- There are strong public reviews and the business is still unknown → `proof`.
- People ask "how do I order?" in the comments, or ordering is unusual (WhatsApp builder, booking deposits) → `howto`.

Say which one and why in a line, and offer the runner-up.

## Finding a style skill

Look for `scorp1-<style>/SKILL.md` in these places, first match wins:
1. `./.scorp1/styles/` in the current folder (a project's own styles),
2. `~/.claude/skills/` and `~/.agents/skills/` (the person's own styles),
3. the Scorp1 plugin's `skills/` folder, which is the parent of `<skill-dir>` (the bundled styles).

In Claude Code you can also load it with the Skill tool (`scorp1:scorp1-<style>` for bundled ones); in Codex, `$scorp1-<style>`. Reading the `SKILL.md` file directly works everywhere.

`/scorp1 styles` lists every style found in those places with its description line.

## Making a new style

Copy `<skill-dir>/templates/style-template.md` to `~/.claude/skills/scorp1-<name>/SKILL.md` (and/or `~/.agents/skills/` for Codex), fill in every section, and it is available as `--style <name>`. The template is the style contract: a style that leaves a section out falls back to the `launch` style for that section.
