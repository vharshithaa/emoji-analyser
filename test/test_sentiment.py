from app.sentiment import analyze_sentiment, add_emoji_to_text

def test_positive():
    assert analyze_sentiment("I love pizza!") == "Positive 😊"

def test_negative():
    assert analyze_sentiment("This is the worst day ever.") == "Negative 😢"

def test_neutral():
    assert analyze_sentiment("Today is Monday.") == "Neutral 😐"

def test_add_emoji():
    result = add_emoji_to_text("This is amazing")
    assert result.endswith("😊") or result.endswith("😐") or result.endswith("😢")