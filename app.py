import streamlit as st
import pandas as pd
import time
import glob

# Function to load questions from CSV files
def load_questions(set_name):
    df = pd.read_csv(f"{set_name}.csv")
    return df

# Function to calculate score and generate results
def calculate_results(df, answers):
    score = 0
    results = []
    for i, row in df.iterrows():
        correct_answer = row['correct_answer']
        user_answer = answers.get(row['question_no'])
        if user_answer == correct_answer:
            score += 1
        else:
            results.append((row['question'], user_answer, correct_answer))
    return score, results

# Streamlit app
st.title("OWS Question Practice")

# Get all available sets
sets = glob.glob("set*.csv")
sets = [set_name.split(".csv")[0] for set_name in sets]

# Dropdown to select set
set_name = st.selectbox("Select a set to practice:", sets)

if set_name:
    df = load_questions(set_name)
    num_questions = len(df)
    time_limit = num_questions / 5 * 60  # Time limit in seconds

    st.write(f"Total questions: {num_questions}")
    st.write(f"Time limit: {time_limit / 60:.2f} minutes")

    # Timer
    start_time = st.empty()
    timer = time.time()

    # Form to display questions
    with st.form("questions_form"):
        answers = {}
        for i, row in df.iterrows():
            question = row['question']
            options = [row['option1'], row['option2'], row['option3'], row['option4']]
            st.write(f"Q{i+1}: {question}")
            answers[row['question_no']] = st.radio(f"Options for Q{i+1}", options)

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            end_time = time.time()
            time_taken = end_time - timer

            score, results = calculate_results(df, answers)
            st.write(f"Your score: {score}/{num_questions}")
            st.write(f"Time taken: {time_taken / 60:.2f} minutes")

            if results:
                st.write("Questions you got wrong:")
                for question, user_answer, correct_answer in results:
                    st.write(f"Question: {question}")
                    st.write(f"Your answer: {user_answer}")
                    st.write(f"Correct answer: {correct_answer}")

            start_time.empty()
else:
    st.write("Please select a set to start practicing.")
