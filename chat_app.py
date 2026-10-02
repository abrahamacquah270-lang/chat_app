import os

import streamlit as st  # type: ignore
from openai import OpenAI  # type: ignore


st.set_page_config(page_title="ChatAKA", page_icon="💬")
st.title("💬 ChatAKA")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    if st.button("＋ New chat", use_container_width=True):
        st.session_state.messages = []

# Show the conversation so far.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Keep the input at the bottom of the chat.
if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            token = "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"  # Replace with your Hugging Face token

            if not token or token == "":
                st.error("Add your Hugging Face token to HF_TOKEN in this file.")
            else:
                try:
                    client = OpenAI(
                        base_url="https://router.huggingface.co/v1",
                        api_key=token,
                    )

                    completion = client.chat.completions.create(
                        model="meta-llama/Llama-3.1-8B-Instruct:novita",
                        messages=st.session_state.messages,
                    )

                    answer = completion.choices[0].message.content or ""
                    st.markdown(answer)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception:
                    st.error("Could not get a response. Check your token and connection.")
