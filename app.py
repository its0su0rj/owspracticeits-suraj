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
        "Jan2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025ans.csv"
        },
        "Feb2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025ans.csv"
        },
        "March2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025ans.csv"
        },
        "April2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025ans.csv"
        },
        "May2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025ans.csv"
        },
        "July2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025ans.csv"
        },
        "Aug2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025ans.csv"
        }
    }

# Quiz Runner
def run_quiz(selected_set, quiz_sets):
    df_q = load_questions(quiz_sets[selected_set]["questions"])
    df_a = load_answers(quiz_sets[selected_set]["answers"])

    if df_q.empty or df_a.empty:
        st.warning("⚠️ Data not available for this set.")
        return

    # Back button at TOP
    if st.button("⬅️ Back to Home"):
        st.query_params.clear()
        st.experimental_rerun()

    st.subheader("Answer the questions:")
    total_questions = len(df_q)
    score = 0
    user_answers = []

    for index, row in df_q.iterrows():
        st.write(f"**Q{index+1}: {row['question']}**")
        options = [row['1'], row['2'], row['3'], row['4']]
        user_answer = st.radio(f"Your answer for Q{index+1}:", options, key=f"{selected_set}_{index}")
        user_answers.append(user_answer)

    if st.button("Submit"):
        incorrect = []
        for i, row in df_q.iterrows():
            correct_option_number = df_a.iloc[i]["correct_ans"]
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

# Main App
def main():
    st.title("📘 Current Affairs Quiz by Suraj")
    quiz_sets = get_quiz_sets()

    # Read query param
    query_params = st.query_params
    selected_set = query_params.get("set", None)

    if not selected_set:
        # Home Page
        st.subheader("Choose a Quiz Set:")

        with st.container():
            st.markdown("### Monthly CA")
            cols = st.columns(3)
            if cols[0].button("Jan 2025 - Set 1", key="jan"):
                st.query_params["set"] = "Jan2025-Set1"
                st.experimental_rerun()
            if cols[1].button("Feb 2025 - Set 1", key="feb"):
                st.query_params["set"] = "Feb2025-Set1"
                st.experimental_rerun()
            if cols[2].button("March 2025 - Set 1", key="mar"):
                st.query_params["set"] = "March2025-Set1"
                st.experimental_rerun()

        with st.container():
            cols = st.columns(3)
            if cols[0].button("April 2025 - Set 1", key="apr"):
                st.query_params["set"] = "April2025-Set1"
                st.experimental_rerun()
            if cols[1].button("May 2025 - Set 1", key="may"):
                st.query_params["set"] = "May2025-Set1"
                st.experimental_rerun()
            if cols[2].button("July 2025 - Set 1", key="jul"):
                st.query_params["set"] = "July2025-Set1"
                st.experimental_rerun()

        with st.container():
            cols = st.columns(3)
            if cols[0].button("Aug 2025 - Set 1", key="aug"):
                st.query_params["set"] = "Aug2025-Set1"
                st.experimental_rerun()

    else:
        run_quiz(selected_set, quiz_sets)


if __name__ == "__main__":
    main()
