import streamlit as st
import pandas as pd
import time
import glob
import os

# Function to load questions from a CSV file
def load_questions(set_name):
    df = pd.read_csv(f"{set_name}.csv")
    return df

# Function to calculate the user's score and identify incorrect answers
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

# Function to save results to a CSV file
def save_results(candidate_name, set_name, score, num_questions, time_taken):
    results_file = f"{candidate_name}_results.csv"
    
    # Check if the results file already exists
    if os.path.exists(results_file):
        results_df = pd.read_csv(results_file)
    else:
        results_df = pd.DataFrame(columns=["Set", "Score", "Total Questions", "Time Taken (minutes)"])
    
    # Create a new entry with the current results
    new_entry = pd.DataFrame([[set_name, score, num_questions, time_taken / 60]], 
                             columns=["Set", "Score", "Total Questions", "Time Taken (minutes)"])
    results_df = pd.concat([results_df, new_entry], ignore_index=True)
    
    # Save the updated results back to the CSV file
    results_df.to_csv(results_file, index=False)

# Function to load and display results for a specific candidate
def load_results(candidate_name):
    results_file = f"{candidate_name}_results.csv"
    if os.path.exists(results_file):
        results_df = pd.read_csv(results_file)
        return results_df
    else:
        return None

# Function to check if the candidate credentials are valid
def check_credentials(candidate_name, candidate_password):
    if os.path.exists("candidates.csv"):
        candidates_df = pd.read_csv("candidates.csv")
        candidate_row = candidates_df[candidates_df['name'] == candidate_name]
        if not candidate_row.empty and candidate_row.iloc[0]['password'] == candidate_password:
            return True
    return False

# Function to add a new candidate
def add_candidate(candidate_name, candidate_password):
    if os.path.exists("candidates.csv"):
        candidates_df = pd.read_csv("candidates.csv")
    else:
        candidates_df = pd.DataFrame(columns=["name", "password"])

    new_entry = pd.DataFrame([[candidate_name, candidate_password]], columns=["name", "password"])
    candidates_df = pd.concat([candidates_df, new_entry], ignore_index=True)
    candidates_df.to_csv("candidates.csv", index=False)

# Streamlit app
st.title("OWS Question Practice")

# Input for viewing results
view_name = st.text_input("Enter your name to view results:")

if st.button("View Results"):
    results_df = load_results(view_name)
    if results_df is not None:
        st.write(f"Results for {view_name}:")
        st.dataframe(results_df)
    else:
        st.write("No results found for this name.")

# Get all available sets (CSV files)
sets = glob.glob("set*.csv")
sets = [set_name.split(".csv")[0] for set_name in sets]

# Section to add a new candidate
st.header("Add New Candidate")
new_candidate_name = st.text_input("Enter new candidate name:")
new_candidate_password = st.text_input("Enter new candidate password:", type="password")
if st.button("Add Candidate"):
    add_candidate(new_candidate_name, new_candidate_password)
    st.write(f"Candidate {new_candidate_name} added successfully.")

# Section to practice
st.header("Practice Questions")
candidate_name = st.text_input("Enter your name to practice:")
candidate_password = st.text_input("Enter your password:", type="password")

# Dropdown to select a set
set_name = st.selectbox("Select a set to practice:", sets)

if set_name and candidate_name and candidate_password:
    # Check if the entered name and password match
    if check_credentials(candidate_name, candidate_password):
        df = load_questions(set_name)
        num_questions = len(df)
        time_limit = num_questions / 5 * 60  # Time limit in seconds

        st.write(f"Total questions: {num_questions}")
        st.write(f"Time limit: {time_limit / 60:.2f} minutes")

        # Initialize timer
        if "start_time" not in st.session_state:
            st.session_state.start_time = time.time()

        # Form to display questions and options
        with st.form("questions_form"):
            answers = {}
            for i, row in df.iterrows():
                question = row['question']
                options = [row['option1'], row['option2'], row['option3'], row['option4']]
                st.write(f"Q{i+1}: {question}")
                answers[row['question_no']] = st.radio(f"Options for Q{i+1}", options)

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                # Calculate time taken
                end_time = time.time()
                time_taken = end_time - st.session_state.start_time

                # Calculate score and show results
                score, results = calculate_results(df, answers)
                st.write(f"Your score: {score}/{num_questions}")
                st.write(f"Time taken: {time_taken / 60:.2f} minutes")

                if results:
                    st.write("Questions you got wrong:")
                    for question, user_answer, correct_answer in results:
                        st.write(f"Question: {question}")
                        st.write(f"Your answer: {user_answer}")
                        st.write(f"Correct answer: {correct_answer}")

                # Save results to the candidate's CSV file
                save_results(candidate_name, set_name, score, num_questions, time_taken)
    else:
        st.write("Invalid name or password. Please try again.")

else:
    st.write("Please enter your name, password, and select a set to start practicing.")
