import streamlit as st
import requests

st.set_page_config(page_title="PDF Chatbot")

st.title("📄 PDF Chatbot – Ask Your File Anything")

if "chat" not in st.session_state:
    st.session_state.chat = []

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
if uploaded_file:
    with st.spinner("Processing file..."):
        res = requests.post("http://localhost:8000/upload/", files={"file": uploaded_file})
        if res.ok:
            st.success("✅ File processed successfully!")
        else:
            st.error("❌ Failed to process file.")

query = st.text_input("Ask a question:")
if st.button("Send") and query:
    st.session_state.chat.append(("user", query))
    with st.spinner("Generating response..."):
        res = requests.post("http://localhost:8000/ask/", data={"query": query})
        answer = res.json().get("response", "Sorry, something went wrong.")
        st.session_state.chat.append(("bot", answer))

st.divider()
for role, msg in st.session_state.chat:
    st.chat_message("user" if role == "user" else "assistant").markdown(msg)
