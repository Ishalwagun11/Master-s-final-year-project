from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Calculates sentiment scores for text using VADER 
#it returns a compound score between -1 and 1, where -1 is most negative, 0 is neutral, and 1 is most positive
class VaderScorer:
    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def compound(self, text: str) -> float:
        return float(self._analyzer.polarity_scores(text or "")["compound"])

