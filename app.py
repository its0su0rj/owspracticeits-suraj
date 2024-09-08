import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Load questions from a CSV URL
def load_questions(file_url):
    try:
        # Fetch the CSV file content from the URL
        response = requests.get(file_url)
        response.raise_for_status()  # Raise an error for bad status codes
        # Convert the response content into a pandas-readable format
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Fetch list of quiz sets
def get_quiz_sets():
    # Replace this list with actual URLs to your CSV files in the GitHub repo
    quiz_sets = {
        "Set 1": "https://raw.githubusercontent.com/your-username/your-repo/main/set1.csv",
        "Set 2": "https://raw.githubusercontent.com/your-username/your-repo/main/set2.csv",
        "Set 3": "https://github.com/its0su0rj/owspracticeits-suraj/blob/8bcf1b36bedc3ef5dc4dc84f3dc6a07f388db68b/current_affairs_questions.csv",
    }
    return quiz_sets

# Main function to display the quiz
def main():
    st.title("Current Affairs Quiz")

    # Fetch available quiz sets
    quiz_sets = get_quiz_sets()

    # Select quiz set
    selected_set = st.selectbox("Select a quiz set to practice:", list(quiz_sets.keys()))

    # Load the selected quiz set
    if selected_set:
        st.write(f"**You selected: {selected_set}**")
        df = load_questions(quiz_sets[selected_set])
        if df.empty:
            return
        total_questions = len(df)
        score = 0
        user_answers = []

        st.write("**Please answer the following questions:**")

        # Loop through questions and display them
        for index, row in df.iterrows():
            st.write(f"**Q{index+1}: {row['question']}**")
            options = [row['1'], row['2'], row['3'], row['4']]
            user_answer = st.radio(f"Select your answer for Q{index+1}:", options, key=index)
            user_answers.append(user_answer)

        # Submit button
        if st.button("Submit"):
            # Check answers and calculate score
            incorrect_answers = []
            for i, row in df.iterrows():
                correct_option = row[f"{row['correct_ans']}"]
                if user_answers[i] == correct_option:
                    score += 1
                else:
                    incorrect_answers.append((row['question'], correct_option))

            # Display score
            st.write(f"Your total score: {score}/{total_questions}")

            # Display incorrect answers
            if incorrect_answers:
                st.write("**Questions you got wrong:**")
                for question, correct in incorrect_answers:
                    st.write(f"**Question:** {question}")
                    st.write(f"**Correct Answer:** {correct}")
            else:
                st.write("Congratulations! All your answers are correct!")

if __name__ == "__main__":
    main()
