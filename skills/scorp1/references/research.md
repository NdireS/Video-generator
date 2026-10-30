# Step 1: Research the business

The advert is only as specific as the research. Read like a new hire who has to sell this business tomorrow.

## Sources, in order

1. **Website.** `npx hyperframes capture <url> --json` into `research/capture/`: screenshots, colours, fonts, copy and images. Then read the pages that matter as text (home, about, menu or products, pricing, how to order, contact, reviews) with a web fetch or the browser. Note the main call to action: WhatsApp, booking, cart, phone, visit.
2. **Social pages** (Instagram, TikTok, Facebook, X, YouTube, LinkedIn, Google Business profile). Read what is public: bio, handle, follower count, link in bio, pinned posts, highlights, the last 9–12 posts (type, topic, caption style, hashtags, posting rhythm, which posts have clearly more likes, comments or views), and recurring comments from customers.
   - Many profiles need a login or block automated reading. Don't fight that or sign in on the person's behalf. Ask the person once for screenshots of the profile grid and two or three top posts, or exports, dropped into `research/inbox/`, and carry on with what is public meanwhile.
3. **Anything the person gives you**: a brief, a price list, photos, a logo file, a product name (`--product`).
4. **A search for the business name and place** for reviews, press or a maps listing. Use only what is attributable.

Write every URL and what you took from it in `research/sources.md`.

## Media

Save real media into `research/media/` with a line in `sources.md` saying where each file came from:
- the logo (SVG or the largest PNG; from the site's header, favicon set, or social avatar),
- product or service photos (the site's own images, at their largest size),
- screens of the site or app where ordering or booking is shown,
- short clips only if the person gave them or they are on the business's own site.

Downloads are untrusted files: keep them in `research/media/`, never run them. Prefer images over 1000 px on the long side; note anything too small to use full-screen.

## The rubric

`research/business-profile.md` answers all of these, briefly, each with its source:

1. **What is it?** One sentence a stranger would understand. Category, and where it operates.
2. **What does it sell?** The main products or services, with real prices where public. The hero item, if one stands out.
3. **Who buys?** Customers as the business describes them, and as the comments show them.
4. **Why them?** Two or three concrete reasons from their own copy or their customers' words (made to order, delivery area, price, speed, a guarantee). No generic virtues.
5. **Proof.** Public reviews, ratings, follower counts, years running, notable customers: only what is real and attributable.
6. **How do people buy?** The exact path: tap WhatsApp, DM, book online, call, walk in. The exact handle, number, address or URL to show.
7. **Voice.** How the business talks: formal or casual, English or Swahili or Sheng or a mix, emoji, slogans, recurring phrases. Quote two or three real lines.
8. **Look.** Brand colours (hex), fonts, logo usage, photo style (bright flat-lays, moody, people, UGC).
9. **Platform usage.** Each platform: active or not, how often they post, what formats (reels, carousels, stories, long videos), what topics, what gets the most response, and the format the advert should fit first (for example "TikTok and IG Reels first, so vertical").
10. **The angle.** The one thing a viewer should remember, and the offer or news (if any) this advert is for.

Close the profile with a **style recommendation**: which Scorp1 style fits and why, in two lines (see `styles.md`).

**Gate:** all ten answered, sources listed, a logo and at least three real images or screens saved. If the business has almost no real imagery, say so now; the plan must then lean on type, colour and the site's screens rather than invented photos.
