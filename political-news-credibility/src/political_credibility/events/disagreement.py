import numpy as np


#takes list of sentiment scores and tells how spread out they are.
#Higher variance = more disagreement between sources
#mainly used to determine if an event is controversial or not ie.e. measure the disagreement between sources
#Variance is in squared sentiment units; standard deviation is reported alongside for interpretability.
def sentiment_variance(scores: list[float]) -> float:
    if len(scores) < 2:
        return 0.0
    return float(np.var(scores, ddof=0)) #calculate variance with population formula (ddof=0)



def is_high_disagreement(scores: list[float], threshold: float = 0.15) -> bool: #var is 0.15 or higher - controversial if not no
    return sentiment_variance(scores) >= threshold


def sentiment_std(scores: list[float]) -> float:
    """Return standard deviation of sentiment scores in original [-1, +1] units."""
    return float(np.sqrt(sentiment_variance(scores)))

