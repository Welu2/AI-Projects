import streamlit as st
from transformers import pipeline

# 1. Set up the title of your website
st.title("🌐 My AI Language Translator")
st.write("Type a sentence in English to translate it into Amharic!")

# 2. Create a text input box for the user
user_input = st.text_input("Enter your text here:", "I love learning AI!")

# 3. Load the AI model
@st.cache_resource
def load_translation_model():
    return pipeline("text-generation", model="Atnafu/English-Amharic-MT")

translator = load_translation_model()

# 4. Create a button to trigger the AI
if st.button("Translate"):
    with st.spinner("Translating..."):
        translation = translator(user_input)
        translated_text = translation[0]['translation_text']
        st.success(f"Amharic Translation: {translated_text}")



#day3 :)
