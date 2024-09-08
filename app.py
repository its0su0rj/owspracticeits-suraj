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
        df = pd.read_csv(csv_data, quotechar='"', skipinitialspace=True)
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()
    except pd.errors.EmptyDataError:
        st.error("The data is empty or improperly formatted.")
        return pd.DataFrame()
    except pd.errors.ParserError:
        st.error("Error parsing the data. Ensure the CSV format is correct.")
        return pd.DataFrame()

# Fetch list of quiz sets
def get_quiz_sets():
    # Replace this list with actual URLs to your CSV files in the GitHub repo
    quiz_sets = {
         "Set 1": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/ca4_set1.csv",
         "Set 2": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/ca4_set2.csv",
         "Set 3": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/ca4_set3.csv",
         "Set 4": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/ca4_set4.csv"
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
            st.write("No data available for the selected quiz set.")
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
            # Debugging information
            st.write("Available columns:", df.columns)
            st.write("Example row:", row)
            st.write("Correct answer column:", row['correct_ans'])

            # Check answers and calculate score
            incorrect_answers = []
            for i, row in df.iterrows():
                correct_ans_col = row['correct_ans']
                # Check if the correct answer column exists
                if correct_ans_col in df.columns:
                    correct_option = row[correct_ans_col]
                    if user_answers[i] == correct_option:
                        score += 1
                    else:
                        incorrect_answers.append((row['question'], correct_option))
                else:
                    st.write(f"Warning: Correct answer column '{correct_ans_col}' not found.")
                    incorrect_answers.append((row['question'], 'Unknown'))

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
