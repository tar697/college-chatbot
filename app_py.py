import streamlit as st
import pandas as pd
import random
import difflib
import ast

# Load and process data
@st.cache_data
def load_data():
    df = pd.read_csv("chatbot_training_data.csv")
    df['responses'] = df['responses'].apply(ast.literal_eval)
    return df

df = load_data()

# Fuzzy matching response function
def get_response(user_input):
    best_match = None
    highest_score = 0
    for _, row in df.iterrows():
        score = difflib.SequenceMatcher(None, user_input.lower(), row['text'].lower()).ratio()
        if score > highest_score:
            highest_score = score
            best_match = row
    if highest_score > 0.6:
        return random.choice(best_match['responses'])
    return "Sorry, I didn't understand that."

# Streamlit interface
st.title("🎓 College Admission Enquiry Chatbot")
st.write("Ask me about courses, fees, admission process, and more!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", key="input")

if user_input:
    response = get_response(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", response))

# Display chat history
for speaker, message in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {message}")
