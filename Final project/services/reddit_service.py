import praw


reddit = praw.Reddit(
    client_id="cSeIELrQowYBYTRmKR5TEg",
    client_secret="NZfYvz-ra668oVdRy7aZVPLSENToug",  
    user_agent="SocialSentiment by /u/KENPCHI3115"
)

def fetch_posts(subreddit_name, limit=20):
    """
    Fetches 'limit' posts from a subreddit.
    Returns a list of post titles + selftext.
    """
    subreddit_name = subreddit_name.strip().replace("/r/", "")
    if not subreddit_name:
        raise ValueError("Subreddit name cannot be empty.")

    subreddit = reddit.subreddit(subreddit_name)

    posts = []
    try:
        for submission in subreddit.hot(limit=limit):
            content = submission.title
            if submission.selftext:
                content += " " + submission.selftext
            posts.append(content)
    except Exception as e:
        raise RuntimeError(f"Error fetching posts from Reddit: {e}")

    if not posts:
        raise RuntimeError("No posts found. Check the subreddit name.")

    return posts
