from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
import functools

@functools.lru_cache(maxsize=1)
def load_sentiment_model():
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    return tokenizer, config, model

# def preprocess(text):
#     return text

def sentiment_analysis(txt):
    tokenizer, config, model = load_sentiment_model()  # Load the model using caching
    text = txt
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output.logits[0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)[::-1]
    sentiment = {config.id2label[ranking[i]]: np.round(float(scores[ranking[i]]), 4) for i in range(scores.shape[0])}
    max_key = max(sentiment, key=sentiment.get).title()
    return max_key




