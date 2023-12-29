from marvin import ai_fn

print(client)


@ai_fn(client=client)
def sentiment(text: str) -> float:
    """Given `text`, returns a number between 1 (positive) and -1 (negative) indicating its sentiment score."""


print(sentiment("I love working with Marvin!"))  # 0.8
print(sentiment("These examples could use some work..."))  # -0.2
