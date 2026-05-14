import streamlit as st
import os
from openai import OpenAI
import ollama

st.title("🦙 My Private Local AI Engine")
st.write("This app communicates directly with the LLM running on your local hardware.")

user_prompt = st.text_area("Ask your private AI something:", "Write a short poem about a programmer.")

# Check if the app is running in the cloud or locally
IS_DEPLOYED = os.environ.get("STREAMLIT_RUNTIME_ENVIRONMENT") == "server" or "STREAMLIT_SERVER_PORT" in os.environ

if st.button("Generate Response"):
    with st.spinner("Processing..."):
        try:
            if IS_DEPLOYED:
                # Cloud Mode: Uses an external API provider hosting open models
                # Ensure you add GROQ_API_KEY to your deployment secrets settings
                client = OpenAI(
                    base_url="groq.com",
                    api_key=st.secrets["GROQ_API_KEY"]
                )
                response = client.chat.completions.create(
                    model="llama-3.2-1b-preview",
                    messages=[{"role": "user", "content": user_prompt}]
                )
                st.write(response.choices[0].message.content)
            else:
                # Local Mode: Uses your laptop's background Ollama service
                response = ollama.chat(model='llama3.2:1b', messages=[
                    {'role': 'user', 'content': user_prompt}
                ])
                st.write(response['message']['content'])

            st.success("Generation Complete!")
        except Exception as e:
            st.error(f"Failed to connect to AI server: {e}")
