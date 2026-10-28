# Rich 2 Ruin — media

Public-domain archive images and published reels for the Rich 2 Ruin account.

- `images.json`: images to fetch from Wikimedia Commons
- `scripts/fetch_images.py`: downloads them, keeps only public domain / CC0, writes `credits.json`
- `.github/workflows/fetch-images.yml`: runs the script on GitHub Actions
