
import streamlit as st
import joblib
import os

st.set_page_config(
    page_title="Product Review Sentiment Analysis",
    page_icon="📱",
    layout="centered"
)

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "final_sentiment_model.pkl"
)

model = joblib.load(MODEL_PATH)

st.title("📱 Product Review Sentiment Analysis")

st.write(
    "Analyse customer reviews and identify "
    "whether the sentiment is Positive, Negative or Neutral."
)

review = st.text_area(
    "Enter your customer review:",
    placeholder="The camera is excellent and battery life is amazing."
)

if st.button("Analyse Sentiment"):

    if review.strip():

        prediction = model.predict([review])[0]

        if prediction == "Positive":
            st.success("Positive Sentiment 😊")

        elif prediction == "Negative":
            st.error("Negative Sentiment 😞")

        else:
            st.info("Neutral Sentiment 😐")

    else:
        st.warning("Please enter a customer review.")
