import streamlit as st
from openai import OpenAI
import ollama

st.title("🦙 My Private Local AI Engine")
st.write("This app communicates directly with the LLM running on your local hardware.")

user_prompt = st.text_area("Ask your private AI something:", "Write a short poem about Abay river.")

# Safely check for cloud secrets without throwing an error if the file is missing locally
try:
    IS_DEPLOYED = "GROQ_API_KEY" in st.secrets
except st.errors.StreamlitSecretNotFoundError:
    IS_DEPLOYED = False

if st.button("Generate Response"):
    with st.spinner("Processing..."):
        try:
            if IS_DEPLOYED:
                # Cloud Mode: Corrected Groq routing endpoint
                client = OpenAI(
                    base_url="https://api.groq.com/openai/v1",  # Fixed: Added accurate complete path
                    api_key=st.secrets["GROQ_API_KEY"]
                )
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": user_prompt}]
                )
                # Fixed: Added index element mapping array 0
                st.write(response.choices[0].message.content)
            else:
                # Local Mode: Communicates with your laptop's Ollama engine
                response = ollama.chat(model='llama3.2:1b', messages=[
                    {'role': 'user', 'content': user_prompt}
                ])
                st.write(response['message']['content'])

            st.success("Generation Complete!")
        except Exception as e:
            st.error(f"Failed to connect to AI server: {e}")
