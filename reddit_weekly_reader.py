"""Weekly read-only reader of public Reddit discussions for a personal report.

Read-only: no posting, commenting, voting, messaging or moderation.
Runs once a week. ~20-40 API calls per run.
Credentials come from environment variables, never from this repo.
"""
import os
import praw

SUBREDDITS = ["options", "investing", "stocks", "wallstreetbets", "Economics"]
TOPICS = ["fed", "rate", "yield", "treasury", "bond", "inflation", "cpi", "jobs",
          "recession", "dollar", "oil", "gold", "vix", "volatility", "hedge",
          "puts", "tariff", "earnings", "market", "sector"]
THREADS_PER_SUB = 3
TOP_COMMENTS = 20


def client() -> praw.Reddit:
    reddit = praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=os.environ["REDDIT_USERNAME"],
        password=os.environ["REDDIT_PASSWORD"],
        user_agent=f"script:radar-weekly-reader:v1.0 (by u/{os.environ['REDDIT_USERNAME']})",
    )
    reddit.read_only = True
    return reddit


def relevant(title: str) -> bool:
    t = title.lower()
    return any(k in t for k in TOPICS)


def collect(reddit: praw.Reddit) -> list[dict]:
    out = []
    for name in SUBREDDITS:
        posts = [p for p in reddit.subreddit(name).top(time_filter="week", limit=25)
                 if relevant(p.title)]
        posts.sort(key=lambda p: p.num_comments, reverse=True)
        for p in posts[:THREADS_PER_SUB]:
            p.comment_sort = "top"
            p.comments.replace_more(limit=0)
            comments = [{"score": c.score, "body": c.body[:600]}
                        for c in list(p.comments)[:TOP_COMMENTS]]
            out.append({"subreddit": name, "title": p.title,
                        "url": f"https://www.reddit.com{p.permalink}",
                        "score": p.score, "num_comments": p.num_comments,
                        "selftext": p.selftext[:1500], "comments": comments})
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(collect(client()), ensure_ascii=False, indent=2))
