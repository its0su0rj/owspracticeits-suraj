import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Load questions CSV
def load_questions(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, quotechar='"', skipinitialspace=True)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Load answers CSV
def load_answers(ans_url):
    try:
        response = requests.get(ans_url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        return df
    except Exception as e:
        st.error(f"Error loading answers: {e}")
        return pd.DataFrame()

# Quiz sets (questions + answers)
def get_quiz_sets():
    return {
         "jan2025": {
             "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025.csv",
             "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025ans.csv"
         },
         "feb2025": {
             "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025.csv",
             "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025ans.csv"
         },
         "march2025": {
             "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025.csv",
             "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025ans.csv"
         },
         "april2025": {
             "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025.csv",
             "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025ans.csv"
         },
         "may2025": {
             "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025.csv",
             "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025ans.csv"
         },
         "Set 6": {
             "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/june2025.csv",
             "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/june2025ans.csv"
         },
         "Set 7": {
             "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025.csv",
             "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025ans.csv"
         },
         "Set 8": {
             "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025.csv",
             "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025ans.csv"
         }
    }

def main():
    st.title("📘 Current Affairs Quiz by suraj")

    quiz_sets = get_quiz_sets()
    selected_set = st.selectbox("Select a quiz set:", list(quiz_sets.keys()))

    if selected_set:
        # Load questions and answers
        df_q = load_questions(quiz_sets[selected_set]["questions"])
        df_a = load_answers(quiz_sets[selected_set]["answers"])

        if df_q.empty or df_a.empty:
            st.warning("⚠️ Data not available for this set.")
            return

        total_questions = len(df_q)
        score = 0
        user_answers = []

        st.subheader("Answer the questions:")

        for index, row in df_q.iterrows():
            st.write(f"**Q{index+1}: {row['question']}**")
            options = [row['1'], row['2'], row['3'], row['4']]
            user_answer = st.radio(f"Your answer for Q{index+1}:", options, key=f"{selected_set}_{index}")
            user_answers.append(user_answer)

        if st.button("Submit"):
            incorrect = []
            for i, row in df_q.iterrows():
                correct_option_number = df_a.iloc[i]["correct_ans"]  # e.g., 1,2,3,4
                correct_option_text = row[str(correct_option_number)]
                if user_answers[i] == correct_option_text:
                    score += 1
                else:
                    incorrect.append((row['question'], correct_option_text))

            st.write(f"### ✅ Your Score: {score}/{total_questions}")
            if incorrect:
                st.error("❌ Incorrect Answers:")
                for q, correct in incorrect:
                    st.write(f"**Q:** {q}")
                    st.write(f"**Correct:** {correct}")
            else:
                st.balloons()
                st.success("🎉 Perfect! All answers correct.")

if __name__ == "__main__":
    main()
