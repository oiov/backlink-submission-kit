# Gotchas

Everything here was hit for real across ~130 sites. Read this before debugging a stuck form — the answer is usually already below.

## 1. Form and framework traps

| Symptom | Cause | Fix |
| --- | --- | --- |
| Values fill in, then vanish on the next step | Nuxt / Vue / Livewire controlled component rerendered | Write every field in one pass, then submit; or use real keystrokes |
| Filled, but the submitted value is empty | DOM changed without the framework's `onChange` | Same: real typing (`click → select-all → type`) |
| `Illegal invocation` error | Classic PHP form rejects native setter calls | Use plain `fill()` per field |
| Dropdown will not open, or selection does not stick | react-select-style widget, underlying input has width 0 | Click the visible container by real coordinates, then click the option element; Enter usually just closes it |
| Option list seems too short | Lazy-loaded options | Scroll to the bottom of the list first |
| Submit button does nothing | Cookie banner or modal overlaying it | Accept/close the banner, then click |
| Upload succeeds but the field looks empty | Hidden `input[type=file]`; `files` is cleared after upload | Upload via the hidden input; trust the on-page counter ("Screenshots 1/6"), not `files.length` |
| Image silently rejected | Minimum size (e.g. ≥50 KB) or exact dimensions | Upscale / convert to PNG, then retry |
| Submit clears the form: no redirect, no error | That *is* the success state on some legacy sites | Look for a confirmation email or the new entry in the account list |
| Arithmetic or image captcha at the last step | Human gate | Fill everything else first, then hand the page to the human |

## 2. Platform families worth recognising

- **Typeform** (Startup Stash, many "apply to be listed" forms): one question per screen. Input `type` is `short_text`, not `text` — `input[type=text]` selects nothing. Controlled inputs need real keystrokes; paste inserts at the caret instead of replacing. Question text must be read from a screenshot, not `innerText` (which keeps previous questions). Choice lists load lazily — scroll to see later options.
- **Nuxt / Vue submit pages** (e.g. PitchWall): fields often have `id` only, no `name`; every rerender wipes previous values. Write all fields in a single evaluate pass, then submit.
- **Discourse forums** (e.g. Chinese indie forums): editor is ProseMirror — `fill()` does nothing. Either click and type, or use the API: `GET /session/csrf`, then `POST /posts.json` with `{title, raw, category}`. A new account's first posts always land in moderation → you get `pending_post.id`, not a public topic URL.
- **Google Forms embedded in a directory**: locate by aria-label; the snapshot's `textbox "Tool Name *"` is not a CSS selector. Success = the literal string "Your response has been recorded."
- **Legacy PHP/ASP directories** (9sites, SoMuch, Launching Next): buttons are `input[type=button][value="Continue"]` or `button#cmdSubmit` — `button:has-text()` fails. Enumerate `form input, form button` first. Arithmetic captcha (2+3) is readable from `form.innerText`; image captchas are not — hand off.
- **Static-hosting "directories"** (Surge, Netlify, Vercel, Cloudflare Pages, Neocities): these are not submission forms, they are deploy targets. The value is a dofollow homepage on a separate domain. CLI/token flows break easily in a non-TTY environment (`npx vercel login` just spins) — use dashboard tokens or skip.
- **Cloudflare interstitials**: "Checking your browser" often clears itself in 8–10 s. Wait 8–10 s, then decide. Never script around it.

## 3. Site behaviour that costs queue slots

- **`$0` plans that require a permanent badge** (SaaSFame, NewTool, ToolFame, twelve.tools, Fazier, Better Launch). Free listing, but dofollow only with their badge on your site, forever, periodically checked. Not free.
- **Top-3-only dofollow** (Startup Fast): a free launch gives a dofollow link only if you reach the Top 3 *and* display their badge.
- **"Free" = save a draft for review** (Tiny Startups, several others): instant publication is the paid option; the free path is a human queue. Not a defect, just record it correctly.
- **Auto-scrape is unreliable** (Tiny Startups, Uneed, 10015.io): the tagline lands in the Name field, tags get invented ("Screen Recording" for a video *downloader*), descriptions get exaggerated. Re-type everything.
- **Approval ≠ live** (Awesome Indie, PeerPush, Uneed): approval can place you in a launch window weeks or months out, or keep the entry invisible while queued. Record the window.
- **Vote thresholds** (Uneed): the free entry stays only if it gets ≥10 upvotes on the day; ≥20 keeps the dofollow link. A submission with no audience behind it can evaporate.
- **Email-gated completion** (SoMuch deletes after 3 days without verification; Toolradar needs a domain email or DNS; 9sites has no receipt at all). These belong in "next action", not "done".
- **Duplicate detection** (LibHunt): submitting a repo that is already listed returns "already submitted, suggest changes" — that is success, not failure.
- **Category emptiness** (productivity.directory has 39 productivity categories and no media/download one): if the category does not exist, the site is not eligible, however free it is.
- **Entry pages die quietly**: `/submit` 302s to `/premium#pricing`, or returns 404 under construction. Treat a redirect to pricing as "paid only".
- **Phone / SMS gates** (SourceForge `Phone Verification Required`, some Chinese platforms): account exists, project cannot be created. Hand off.

## 4. Browser and environment

- **Native permission bubbles** (notifications, camera) are browser UI, not DOM. Automation loses the tab. Hand the space back to the human; afterwards `about:blank` frees it.
- **Google OAuth account picking** is the flakiest step. Click the account by real coordinates; if the click times out, `.click()` the button element. After sign-in, confirm the callback actually returned to the form — being logged into Google is not being logged into the directory.
- **OAuth consent scope**: expect name, avatar, email. Anything more → abort.
- **Screenshots are expensive**: use a DOM snapshot to find controls, screenshot only for visual confirmation (captcha, crop dialog, overlay).
- **One task space, one tab, reused.** Extra tabs multiply the chance of losing state.

## 5. Site-specific notes (the short list)

Full detail per site is in `data/directories.csv` → `notes`. Highlights that generalise poorly and are therefore worth repeating:

- **Indie Hackers**: creating the product page is only step one; the entry appears in the directory after completing `/edit` and ticking published.
- **SaaSHub**: at least 3 categories; competitor selection is a separate step — skip it and the submission is incomplete.
- **Uneed**: logo required or the status stays "Incomplete"; the rich description and tags are always wrong; the schedule modal pushes $39.99/$14.99/$249 — choose the free waiting line.
- **osalt**: a trailing slash on the homepage triggers `Error in input`; submit without it.
- **PitchWall**: screenshots under 50 KB are rejected silently; upscale to a few hundred KB.
- **10015.io**: the free listing is nofollow with a 3–4 month queue; pricing classification is a **required** field — if pricing is unverified, stop instead of guessing.
- **Peerlist Launchpad**: launching requires profile verification first; logging in is not enough.
- **appsgit**: needs a self-hostable app with deployment docs and activity in the last 12 months; submitting only the repo URL is enough.
- **OpenAlternative**: repo needs ≥50 stars (or ≥250 for repos under 6 months); browser extensions are excluded.
- **Softpedia**: the form opens with "No AI-written code" — a factual declaration. If the commit history says otherwise, skip.
- **Fazier / twelve.tools**: free tier requires their link on your homepage or footer. Business decision, never auto-accepted.
- **Hacker Noon / Medium / dev.to / Substack / Hashnode**: content platforms. Links are `nofollow`/`ugc`; value is referral traffic and brand search, not link equity. Also: an empty editor is not a submission — these need an actual article.
- **Chinese communities** (出海栈 bbs.ss, 小众软件 meta.appinn.net): bbs.ss requires ≥500 characters and a cover image (the publish button is disabled with no message otherwise); appinn forbids URLs in titles, one product per thread, and new accounts' first posts are moderated.

## 6. Before you conclude a site is broken

1. Re-read that row's `notes`.
2. Re-inspect the page (state changed after a step?).
3. Try the flow as a normal user: click, type, wait.
4. Check whether the "failure" is actually the success state (form cleared, entry already exists, pending review).
5. Only then record `blocked` / `dead` — with the exact observation and date, so the next person does not repeat the investigation.
