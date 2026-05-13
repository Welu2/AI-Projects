import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# 1. Set up the title of your website
st.title("🌐 My AI Language Translator")
st.write("Type a sentence in English to translate it into Amharic!")

# 2. Create a text input box for the user
user_input = st.text_input("Enter your text here:", "I love learning AI!")

# 3. Load the AI model
@st.cache_resource
def load_translation_model():
    model_name = "Atnafu/English-Amharic-MT"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

tokenizer, model = load_translation_model()

if st.button("Translate to Amharic"):
    with st.spinner("Translating..."):
        # Convert text to model inputs
        inputs = tokenizer(user_input, return_tensors="pt", padding=True)
        
        # Generate translation tokens
        generated_tokens = model.generate(**inputs)
        
        # Convert tokens back to readable Amharic string
        result = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        
        st.success(f"Amharic Translation: {result}")

#day 5 :)