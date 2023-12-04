import streamlit as st
from transformers import pipeline
from textSummerizerEnglish.pipeline.prediction_pipeline import PredictionPipeline

# Load the summarization model
obj = PredictionPipeline()

def main():
    st.title("Text Summarizer App")

    # Get user input
    user_input = st.text_area("Enter text to summarize:")

    # Button to trigger summarization
    if st.button("Summarize"):
        if user_input:
            # Summarize the user input using the model
            summary = obj.predict(user_input)

            # Display the summarized output
            st.subheader("Summary:")
            st.write(summary)
        else:
            st.warning("Please enter text before summarizing.")

if __name__ == "__main__":
    main()
