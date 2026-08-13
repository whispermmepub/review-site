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
├── index.html                    # page structure
├── styles.css                    # design
├── script.js                     # app logic + post list data (embedded)
├── data/
│   └── posts.json                # ပို့စ်အပြည့်အစုံ content (body ပါ)
├── scripts/
│   └── build_data.py             # Review repo ကနေ data ပြန်ထုတ်တဲ့ script
└── .github/workflows/
    └── sync-and-deploy.yml       # နာရီတိုင်း auto sync + deploy
```

## Auto Update 🤖

ဒီ repo မှာ GitHub Action (`sync-and-deploy.yml`) ပါပြီးသားမို့
မူရင်း Review repo (`whispermmepub/Review` — Blogspot auto-sync) က post အသစ်တွေ ပေါ်တာနဲ့
**နာရီတိုင်း** အလိုအလျောက် extract လုပ်ပြီး Cloudflare Pages ကို deploy လုပ်ပေးပါတယ်။

လိုအပ်တဲ့ repo secrets:
- `CLOUDFLARE_API_TOKEN` — Cloudflare API token
- `CLOUDFLARE_ACCOUNT_ID` — Cloudflare account ID

Actions tab ကနေ **Sync Review Posts & Deploy** ကို `Run workflow` နှိပ်ပြီး အချိန်မရွေး manually run လို့လည်းရတယ်။

## ပို့စ်အသစ် manually ထည့်နည်း

`data/posts.json` ထဲကို post object အသစ် ထည့်ပြီး
`python3 scripts/build_data.py /path/to/Review .` နဲ့ `script.js` ထဲက embedded summary ကို ပြန်ထုတ်ပါ။

## Deploy

```bash
npx wrangler pages deploy . --project-name=whisperofwords-review
```
