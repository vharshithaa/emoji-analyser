from sentiment import add_emoji_to_text

if __name__ == "__main__":
    msg = input("Enter your message: ")
    print("With emoji:", add_emoji_to_text(msg))