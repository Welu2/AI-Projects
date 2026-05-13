import streamlit as st
from transformers import pipeline

# 1. Set up the title of your website
st.title("🎬 My First AI Sentiment Web App")
st.write("Type a sentence below to see if the AI thinks it is Happy or Sad!")

# 2. Create a text input box for the user
user_input = st.text_input("Enter your text here:", "I love learning AI!")

# 3. Load the AI model
@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis")

classifier = load_model()

# 4. Create a button to trigger the AI
if st.button("Analyze Sentiment"):
    result = classifier(user_input)
    label = result[0]['label']
    score = result[0]['score']
    
    # Show the result on screen
    st.success(f"Result: {label} (Confidence: {score:.2%})")
    


#day3 :)
