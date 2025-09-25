from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(posts):
    positive, neutral, negative = 0, 0, 0
    words = []

    # Parallel sentiment scoring
    def score_post(post):
        return post, analyzer.polarity_scores(post)['compound']

    with ThreadPoolExecutor() as executor:
        scored_posts = list(executor.map(score_post, posts))

    # Count positive, neutral, negative and collect words
    for post, score in scored_posts:
        if score >= 0.05:
            positive += 1
        elif score <= -0.05:
            negative += 1
        else:
            neutral += 1

        # collect words for word cloud
        clean_words = re.findall(r'\w+', post.lower())
        words.extend(clean_words)

    # Top positive and negative posts
    top_positive = sorted(scored_posts, key=lambda x: x[1], reverse=True)[:3]
    top_negative = sorted(scored_posts, key=lambda x: x[1])[:3]

    word_count = Counter(words).most_common(20)

    return {
        'positive': positive,
        'neutral': neutral,
        'negative': negative,
        'words': word_count,
        'top_positive': top_positive,
        'top_negative': top_negative
    }
