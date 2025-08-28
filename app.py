import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Load questions
def load_questions(file_url):
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data, quotechar='"', skipinitialspace=True)
        if "correct_ans" not in df.columns:
            df["correct_ans"] = ""
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Quiz sets
def get_quiz_sets():
    return {
         "Set 1": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025.csv",
         "Set 2": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025.csv",
         "Set 3": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025.csv",
         "Set 4": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025.csv",
         "Set 5": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025.csv",
         "Set 6": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/june2025.csv",
         "Set 7": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025.csv",
         "Set 8": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025.csv"
    }

def main():
    st.title("📘 Current Affairs Quiz")

    quiz_sets = get_quiz_sets()
    selected_set = st.selectbox("Select a quiz set:", list(quiz_sets.keys()))

    if selected_set:
        df = load_questions(quiz_sets[selected_set])

        if df.empty:
            st.warning("⚠️ No data available for this quiz set.")
            return

        if "answer_keys" not in st.session_state:
            st.session_state.answer_keys = {}

        total_questions = len(df)
        score = 0
        user_answers = []

        st.subheader("Answer the questions:")

        for index, row in df.iterrows():
            st.write(f"**Q{index+1}: {row['question']}**")
            options = [row['1'], row['2'], row['3'], row['4']]
            user_answer = st.radio(f"Your answer for Q{index+1}:", options, key=f"{selected_set}_{index}")
            user_answers.append(user_answer)

        if st.button("Submit"):
            # First attempt → save as session answer key
            if selected_set not in st.session_state.answer_keys:
                st.session_state.answer_keys[selected_set] = user_answers
                st.success("✅ First attempt saved as answer key (session only). Rerun to evaluate.")
                return

            # Next attempts → evaluate
            correct_answers = st.session_state.answer_keys[selected_set]
            incorrect = []
            for i, user_ans in enumerate(user_answers):
                if user_ans == correct_answers[i]:
                    score += 1
                else:
                    incorrect.append((df.iloc[i]['question'], correct_answers[i]))

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
