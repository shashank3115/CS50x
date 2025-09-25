from flask import Flask, render_template, request, jsonify
from services.reddit_service import fetch_posts
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    subreddit = request.form.get("subreddit", "").strip()
    keyword = request.form.get("keyword", "").strip()

    try:
        limit = int(request.form.get("limit", 20))
    except ValueError:
        limit = 20

    # Input validation
    if not subreddit:
        return jsonify({"error": "Please enter a valid subreddit name."})

    if limit < 1:
        limit = 10
    elif limit > 50:
        limit = 50

    # Clean subreddit
    subreddit = subreddit.replace("/r/", "").strip()

    # Fetch posts
    try:
        posts = fetch_posts(subreddit, limit)
    except Exception as e:
        return jsonify({"error": f"Error fetching posts: {str(e)}"})

    # Sentiment analysis
    positive = 0
    neutral = 0
    negative = 0
    top_positive = []
    top_negative = []
    all_words = []

    for post in posts:
        score = analyzer.polarity_scores(post)['compound']

        if score >= 0.05:
            positive += 1
            top_positive.append((post, round(score, 4)))
        elif score <= -0.05:
            negative += 1
            top_negative.append((post, round(score, 4)))
        else:
            neutral += 1

        # Collect words for word cloud
        all_words.extend(post.lower().split())

    # Top words (excluding common stopwords)
    stopwords = set([
        'the', 'i', 'to', 'and', 'a', 'it', 'of', 'for', 'in', 'is',
        'on', 'this', 'my', 'that', 'with', 'was', 'but', 'are', 'as',
        'at', 'be', 'so', 'just', 'or', 'if', 'from', 'they', 'we'
    ])
    filtered_words = [w for w in all_words if w not in stopwords]
    word_counts = Counter(filtered_words).most_common(20)

    # Sort top posts by score
    top_positive = sorted(top_positive, key=lambda x: x[1], reverse=True)[:5]
    top_negative = sorted(top_negative, key=lambda x: x[1])[:5]

    return jsonify({
        "positive": positive,
        "neutral": neutral,
        "negative": negative,
        "top_positive": top_positive,
        "top_negative": top_negative,
        "words": word_counts
    })

if __name__ == "__main__":
    app.run(debug=True)
