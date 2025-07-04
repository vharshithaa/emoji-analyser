from textblob import TextBlob

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.3:
        return "Positive 😊"
    elif polarity < -0.3:
        return "Negative 😢"
    else:
        return "Neutral 😐"

def add_emoji_to_text(text):
    sentiment = analyze_sentiment(text)
    emoji = sentiment.split(" ")[-1]
    return text + " " + emoji