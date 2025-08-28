import streamlit as st
import pandas as pd
import requests
from io import StringIO
import os

# Load questions from a CSV URL
def load_questions(file_url, local_filename):
    # If local corrected file exists, load it instead of URL
    if os.path.exists(local_filename):
        return pd.read_csv(local_filename)
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, quotechar='"', skipinitialspace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Fetch list of quiz sets
def get_quiz_sets():
    quiz_sets = {
         "Set 1": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february.csv",
         "Set 2": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/ca4_set2.csv",
         "Set 3": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/ca4_set3.csv",
         "Set 4": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/ca4_set4.csv"
    }
    return quiz_sets

# Main function to display the quiz
def main():
    st.title("Current Affairs Quiz")

    quiz_sets = get_quiz_sets()
    selected_set = st.selectbox("Select a quiz set to practice:", list(quiz_sets.keys()))

    if selected_set:
        st.write(f"**You selected: {selected_set}**")
        local_filename = f"{selected_set.lower().replace(' ', '_')}.csv"
        df = load_questions(get_quiz_sets()[selected_set], local_filename)

        if df.empty:
            st.write("No data available for the selected quiz set.")
            return
        
        total_questions = len(df)
        score = 0
        user_answers = []

        st.write("**Please answer the following questions:**")

        for index, row in df.iterrows():
            st.write(f"**Q{index+1}: {row['question']}**")
            options = [row['1'], row['2'], row['3'], row['4']]
            user_answer = st.radio(f"Select your answer for Q{index+1}:", options, key=index)
            user_answers.append(user_answer)

        if st.button("Submit"):
            # If no correct answers exist → save first attempt as correct
            if "correct_ans" not in df.columns or df["correct_ans"].isnull().all() or (df["correct_ans"] == "").all():
                df["correct_ans"] = user_answers
                df.to_csv(local_filename, index=False, encoding="utf-8-sig")
                st.success(f"✅ First attempt saved! Correct answers stored in {local_filename}. Please rerun to test yourself.")
                return

            incorrect_answers = []
            for i, row in df.iterrows():
                correct_option = row['correct_ans']
                if user_answers[i] == correct_option:
                    score += 1
                else:
                    incorrect_answers.append((row['question'], correct_option))

            st.write(f"Your total score: {score}/{total_questions}")

            if incorrect_answers:
                st.write("**Questions you got wrong:**")
                for question, correct in incorrect_answers:
                    st.write(f"**Question:** {question}")
                    st.write(f"**Correct Answer:** {correct}")
            else:
                st.write("🎉 Congratulations! All your answers are correct!")

if __name__ == "__main__":
    main()
