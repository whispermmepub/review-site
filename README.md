# Book Review Terminal 📚

Retro terminal style နဲ့ ပြန်ဆောက်ထားတဲ့ **Whisper Of Words** ရဲ့ မြန်မာစာအုပ်စာအညွှန်း site ပါ။
Static HTML/CSS/JS သက်သက်မို့ framework မလို၊ Cloudflare Pages မှာ free deploy လို့ရတယ်။

## Site Links

- **Live (Cloudflare Pages):** https://whisperofwords-review.pages.dev
- **Original GitHub Pages:** https://whispermmepub.github.io/Review/
- **Review repo:** https://github.com/whispermmepub/Review

## Features

- 🖥️ Retro terminal boot animation
- 📚 Review post 109 ခု — ရှာဖွေနိုင်၊ နှစ်အလိုက် filter လုပ်နိုင်
- 📖 ပို့စ်တိုင်းရဲ့ အပြည့်အစုံ content — site ထဲမှာ တိုက်ရိုက် ဖတ်လို့ရ
- 🔖 Save for Later (localStorage bookmark)
- 📤 Telegram / Facebook / Viber share buttons
- ⏰ Live clock, date, signal, battery status bar

## ဖိုင်ဖွဲ့စည်းပုံ

```
review-site/
├── index.html        # page structure
├── styles.css        # design
├── script.js         # app logic + post list data (embedded)
└── data/
    └── posts.json    # ပို့စ်အပြည့်အစုံ content (body ပါ)
```

## ပို့စ်အသစ်ထည့်နည်း

`data/posts.json` ထဲကို post object အသစ် ထည့်ရုံပါပဲ။
`script.js` ထဲက embedded summary ကိုလည်း အသစ်ရဲ့ `id, title, date, author, image, excerpt, tags, blog` နဲ့ update လုပ်ပေးပါ။

## Deploy

```bash
npx wrangler pages deploy review-site --project-name=whisperofwords-review
```
