import streamlit as st
from api import predict_spam

st.title("📧 Spam Detection App")
st.markdown("Enter a message below to check if it's spam or ham (not spam).")

# Text input
message = st.text_area("Enter your message:", height=100, placeholder="Type your message here...")

# Predict button
if st.button("🔍 Check Message", type="primary"):
    if message.strip():
        with st.spinner("Analyzing message..."):
            result = predict_spam(message)
        
        if result == 1:
            st.error("🚨 **SPAM DETECTED!** This message appears to be spam.")
            st.markdown("⚠️ *Please be cautious with this message.*")
        else:
            st.success("✅ **HAM (Not Spam)** This message appears to be legitimate.")
            st.markdown("👍 *This message seems safe.*")
    else:
        st.warning("⚠️ Please enter a message to analyze.")

# Footer
st.markdown("---")
st.markdown("*Built with Streamlit and Machine Learning*")