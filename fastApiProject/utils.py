import joblib
import re

# Load the pre-trained model
model = joblib.load('logistic_regression_sentiment_model.pkl')

def clean_text(text):
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'\W', ' ', text)
    return text.lower()

def predict_sentiment(text):
    cleaned_text = clean_text(text)
    prediction = model.predict([cleaned_text])[0]
    return "Good" if prediction == 1 else "Poor"