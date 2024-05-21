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
if 'submitted' not in st.session_state:
    st.session_state.submitted = False

# Function to load the next question
def next_question():
    if st.session_state.index < len(questions_df) - 1:
        st.session_state.index += 1
        st.session_state.answer = ""
        st.session_state.submitted = False

# Function to check the answer
def check_answer():
    correct_answer = questions_df.iloc[st.session_state.index]['Correct Answer'].strip().lower()
    selected_option = st.session_state.answer.split(".")[0].strip().lower()  # Extract the letter and convert to lowercase
    if selected_option == correct_answer:
        st.session_state.score += 1
        st.success("Correct!")
    else:
        st.error(f"Incorrect. The correct answer is {correct_answer.upper()}.")
    st.session_state.submitted = True

# Display the current question
current_question = questions_df.iloc[st.session_state.index]
st.write(f"Question {st.session_state.index + 1}: {current_question['Question']}")

# Display radio options
options = [
    current_question['Option A'],
    current_question['Option B'],
    current_question['Option C'],
    current_question['Option D']
]
st.radio("Options", options, key='answer')

# Submit button
if st.button("Submit"):
    check_answer()

# Only show the "Next Question" button if the answer has been submitted
if st.session_state.submitted:
    if st.button("Next Question"):
        next_question()

st.write(f"Score: {st.session_state.score}")

# End of quiz message
if st.session_state.index >= len(questions_df):
    st.write("You've completed the quiz!")
