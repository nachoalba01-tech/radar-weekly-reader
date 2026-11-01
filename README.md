# radar-weekly-reader

Small personal, non-commercial, **read-only** script that reads public Reddit
discussions once a week to produce a private summary of market narratives
(macro, rates, bonds, volatility, sectors) emailed only to its author.

- Subreddits: r/options, r/investing, r/stocks, r/wallstreetbets, r/Economics
- Per run: top posts of the week, ~15 relevant threads, top 10-20 comments each
- Volume: ~20-40 API calls per week, once a week
- No write actions: no posting, commenting, voting, messaging or moderation
- No user profiles or private data; raw data is not retained after the run
- Data is never sold, shared, redistributed or used to train AI/ML models

## Usage

```
pip install -r requirements.txt
export REDDIT_CLIENT_ID=... REDDIT_CLIENT_SECRET=... REDDIT_USERNAME=... REDDIT_PASSWORD=...
python reddit_weekly_reader.py > week.json
```

Credentials are provided through environment variables and are never committed.
