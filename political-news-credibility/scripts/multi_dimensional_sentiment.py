
import sys
from pathlib import Path


# This block must run BEFORE any "from src..." or project-level imports below,
# otherwise Python won't know where to find them and will raise ModuleNotFoundError.
ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DISSERTATION_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import historical_events as he
from political_credibility.events.disagreement import sentiment_variance
from political_credibility.nlp.sentiment import VaderScorer
import pandas as pd
import numpy as np

try:
    from transformers import pipeline
    ROBERTA_AVAILABLE = True
except ImportError:
    ROBERTA_AVAILABLE = False
    print("Warning: transformers not available, using VADER only")


def get_roberta_sentiment(text, sentiment_pipeline): #Get sentiment score using RoBERTa model
    
    if not ROBERTA_AVAILABLE:
        return 0.0
    
    result = sentiment_pipeline(text)
    
    # return value is a  list of lists of dictionaries
    # Example: [[{'label': 'LABEL_0', 'score': 0.42}, {'label': 'LABEL_1', 'score': 0.55}, {'label': 'LABEL_2', 'score': 0.03}]]
    # Labels are: LABEL_0 (negative), LABEL_1 (neutral), LABEL_2 (positive)
    
    # Extract the first element (which contains the list of dicts)
    if isinstance(result, list) and len(result) > 0:
        if isinstance(result[0], list):
            result = result[0]
        # If result[0] is already a dict, the list contains a single dict
        elif isinstance(result[0], dict):
            result = [result[0]]
    
    # Calculate compound score
    scores = {}
    for item in result:
        if isinstance(item, dict) and 'label' in item and 'score' in item:
            scores[item['label']] = item['score']
    
    # Map labels to sentiment
    positive = scores.get('LABEL_2', 0)
    negative = scores.get('LABEL_0', 0)
    
    # Calculate compound score
    compound = positive - negative
    return compound


def main():
    print("Comparing VADER and RoBERTa sentiment analysis")
    print()
    
    # Load data
    rows = he.flatten_events(he.EVENTS) # Flatten the events data into a list of rows
    scorer = VaderScorer()
    
    # Get VADER scores
    print("Calculating VADER sentiment scores...")
    for r in rows:
        r["vader_tone"] = scorer.compound(r["article_headline"])
    
    # Get RoBERTa scores (if available)
    if ROBERTA_AVAILABLE:
        print("Loading RoBERTa model...")
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment",
            top_k=None,
            device=-1  # CPU
        )
        print("Calculating RoBERTa sentiment scores...")
        for r in rows:
            r["roberta_tone"] = get_roberta_sentiment(r["article_headline"], sentiment_pipeline)
    else:
        print("RoBERTa not available, using placeholder values")
        for r in rows:
            r["roberta_tone"] = r["vader_tone"]  # Use VADER as placeholder
    
    df = pd.DataFrame(rows)
    
    # Calculate variance for each event using both methods
    print("\nCalculating variance for each event...")
    
    event_variances = []
    for event_id, group in df.groupby("event_id"):
        vader_tones = group["vader_tone"].tolist()
        roberta_tones = group["roberta_tone"].tolist()

        vader_variance = sentiment_variance(vader_tones)
        roberta_variance = sentiment_variance(roberta_tones)
     

        event_variances.append({
            "event_id": event_id,
            "event_name": group["event_name"].iloc[0],
            "vader_variance": vader_variance,
            "vader_std": np.sqrt(vader_variance),
            "roberta_variance": roberta_variance,
            "roberta_std": np.sqrt(roberta_variance),
           
            "vader_min": min(vader_tones),
            "vader_max": max(vader_tones),
            "roberta_min": min(roberta_tones),
            "roberta_max": max(roberta_tones),
        })
    
    # Sort by VADER variance
    event_variances.sort(key=lambda x: x["vader_variance"], reverse=True)
    
    # Calculate statistics
    vader_vars = [e["vader_variance"] for e in event_variances]
    roberta_vars = [e["roberta_variance"] for e in event_variances]
    
    arr_vader = np.array(vader_vars)
    arr_roberta = np.array(roberta_vars)
    
    # Print comparison
   
    arr_vader_std = np.sqrt(arr_vader)
    arr_roberta_std = np.sqrt(arr_roberta)

    print("VADER SENTIMENT VARIANCE STATISTICS")
    print(f"Mean variance: {arr_vader.mean():.4f} (SD: {arr_vader_std.mean():.4f})")
    print(f"Median variance: {np.median(arr_vader):.4f} (SD: {np.median(arr_vader_std):.4f})")
    print(f"Std Dev of variances: {arr_vader.std():.4f}")
    print(f"Min variance: {arr_vader.min():.4f} (SD: {arr_vader_std.min():.4f})")
    print(f"Max variance: {arr_vader.max():.4f} (SD: {arr_vader_std.max():.4f})")

    print("ROBERTA SENTIMENT VARIANCE STATISTICS")
    print(f"Mean variance: {arr_roberta.mean():.4f} (SD: {arr_roberta_std.mean():.4f})")
    print(f"Median variance: {np.median(arr_roberta):.4f} (SD: {np.median(arr_roberta_std):.4f})")
    print(f"Std Dev of variances: {arr_roberta.std():.4f}")
    print(f"Min variance: {arr_roberta.min():.4f} (SD: {arr_roberta_std.min():.4f})")
    print(f"Max variance: {arr_roberta.max():.4f} (SD: {arr_roberta_std.max():.4f})")
    
    # Correlation analysis
    correlation = np.corrcoef(vader_vars, roberta_vars)[0, 1]
    print("CORRELATION ANALYSIS")
    print(f"Correlation between VADER and RoBERTa variance: {correlation:.4f}")
    
    # Threshold comparison
    print("THRESHOLD COMPARISON (0.15)")

    #counts flagged events for each method
    vader_flagged = sum(1 for v in vader_vars if v >= 0.15)
    roberta_flagged = sum(1 for v in roberta_vars if v >= 0.15)
    
    print(f"VADER: {vader_flagged} events flagged ({vader_flagged/len(event_variances)*100:.1f}%)")
    print(f"RoBERTa: {roberta_flagged} events flagged ({roberta_flagged/len(event_variances)*100:.1f}%)")
    
    # Find disagreements
    print("EVENTS WHERE METHODS DISAGREE ON THRESHOLD")

    
    disagreements = []
    for e in event_variances:
        vader_flag = e["vader_variance"] >= 0.15
        roberta_flag = e["roberta_variance"] >= 0.15
        if vader_flag != roberta_flag:
            disagreements.append({
                "event_name": e["event_name"],
                "vader_variance": e["vader_variance"],
                "roberta_variance": e["roberta_variance"],
                "vader_flagged": vader_flag,
                "roberta_flagged": roberta_flag,
            })
    
    if disagreements:
        print(f"\nFound {len(disagreements)} events where methods disagree:")
        for d in disagreements:
            print(f"\n  {d['event_name']}:")
            print(f"    VADER variance: {d['vader_variance']:.4f} (SD: {np.sqrt(d['vader_variance']):.4f}, flagged: {d['vader_flagged']})")
            print(f"    RoBERTa variance: {d['roberta_variance']:.4f} (SD: {np.sqrt(d['roberta_variance']):.4f}, flagged: {d['roberta_flagged']})")
    print("COMPARISON TABLE")
    print(f"{'Event':<50} | {'VADER Var':>10} | {'VADER Range':>15} | {'RoBERTa Var':>12} | {'RoBERTa Range':>17} | {'Diff':>8}")

    for e in event_variances[:10]:  # Top 10
        diff = e["vader_variance"] - e["roberta_variance"]
        vader_range = f"{e['vader_min']:+.2f} to {e['vader_max']:+.2f}"
        roberta_range = f"{e['roberta_min']:+.2f} to {e['roberta_max']:+.2f}"
        print(f"{e['event_name'][:48]:<50} | {e['vader_variance']:>10.4f} | {vader_range:>15} | {e['roberta_variance']:>12.4f} | {roberta_range:>17} | {diff:>8.4f}")

    print("\n... (showing top 10 of 44 events)")
    print("Note: Variance is in squared sentiment units; SD is on the original [-1, +1] sentiment scale.")
    
    # Summary
   
    print("SUMMARY")
   
    print(f"Correlation: {correlation:.4f}")
    print(f"VADER flags: {vader_flagged} events (11.4%)")
    print(f"RoBERTa flags: {roberta_flagged} events ({roberta_flagged/len(event_variances)*100:.1f}%)")
    print(f"Disagreements: {len(disagreements)} events")
    
    if correlation > 0.9:
        print("\nStrong agreement between methods - VADER results are robust")
    elif correlation > 0.7:
        print("\nModerate agreement - results are reasonably consistent")
    else:
        print("\nWeak agreement - methods produce different results")
    
    # Show 5 lowest-variance events
   
    # print("5 LOWEST-VARIANCE EVENTS (Sources Mostly Agree)")
    # print("=" * 70)
    # event_variances_sorted = sorted(event_variances, key=lambda x: x["vader_variance"])
    # for i in range(5):
    #     e = event_variances_sorted[i]
    #     print(f"\n{i+1}. {e['event_name']}")
    #     print(f"   VADER variance: {e['vader_variance']:.4f}")
    #     print(f"   VADER score range: {e['vader_min']:.2f} to {e['vader_max']:.2f}")
    #     print(f"   RoBERTa variance: {e['roberta_variance']:.4f}")
    #     print(f"   RoBERTa score range: {e['roberta_min']:.2f} to {e['roberta_max']:.2f}")
    
 


if __name__ == "__main__":
    main()