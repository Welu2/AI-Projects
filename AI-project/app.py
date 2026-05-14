import streamlit as st
import ollama

st.title("🦙 My Private Local AI Engine")
st.write("This app communicates directly with the LLM running on your local hardware.")

# 1. Capture user prompt input
user_prompt = st.text_area("Ask your private AI something:", "Write a short poem about a programmer.")

# 2. Trigger the local model generation
if st.button("Generate Response"):
    with st.spinner("Processing locally on your device..."):
        try:
            # Send the text directly to your background Ollama engine
            response = ollama.chat(model='llama3.2:1b', messages=[
                {
                    'role': 'user',
                    'content': user_prompt,
                },
            ])
            # Display the generated content
            st.success("Generation Complete!")
            st.write(response['message']['content'])
        except Exception as e:
            st.error(f"Failed to connect to local AI server: {e}")
