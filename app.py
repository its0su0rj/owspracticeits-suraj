import streamlit as st
import pandas as pd

# Load the CSV file
questions_df = pd.read_csv('owsqa.csv')

# Initialize session state variables
if 'index' not in st.session_state:
    st.session_state.index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answer' not in st.session_state:
    st.session_state.answer = ""

# Function to load the next question
def next_question():
    if st.session_state.index < len(questions_df) - 1:
        st.session_state.index += 1
        st.session_state.answer = ""

# Function to check the answer
def check_answer():
    correct_answer = questions_df.iloc[st.session_state.index]['Answer']
    if st.session_state.answer == correct_answer:
        st.session_state.score += 1
        st.success("Correct!")
    else:
        st.error("Incorrect.")
    next_question()

# Display the current question
if 'index' in st.session_state:
    current_question = questions_df.iloc[st.session_state.index]
    st.write(f"Question {st.session_state.index + 1}: {current_question['Question']}")
    st.radio("Options", ['a', 'b', 'c', 'd'], key='answer')

    if st.button("Submit"):
        check_answer()

    st.write(f"Score: {st.session_state.score}")

    if st.session_state.index >= len(questions_df):
        st.write("You've completed the quiz!")
    else:
        st.write("Next question will appear after submitting the current one.")
else:
    st.write("Initializing...")
