import streamlit as st
import pandas as pd
import os

# Load questions from CSV file
def load_questions(file_path):
    df = pd.read_csv(file_path)
    return df

# Fetch list of quiz sets
def get_quiz_sets():
    # You can replace this list with a dynamic fetch from your GitHub repo if needed
    quiz_sets = {
        #"Set 1": "https://raw.githubusercontent.com/your-username/your-repo/main/set1.csv",
        #"Set 2": "https://raw.githubusercontent.com/your-username/your-repo/main/set2.csv",
        "Set 3": "https://github.com/its0su0rj/owspracticeits-suraj/main/current_affairs_questions.csv",
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
