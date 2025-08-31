import streamlit as st
import pandas as pd
import requests
from io import StringIO

# ---------- Loaders ----------
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

# ---------- Quiz Sets ----------
def get_quiz_sets():
    return {
        "January 2025": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025ans.csv"
        },
        "February 2025": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025ans.csv"
        },
        "March 2025": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025ans.csv"
        },
        "April 2025": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025ans.csv"
        }
    }

# ---------- Quiz Page ----------
def run_quiz(selected_set, quiz_sets):
    st.subheader(f"📖 {selected_set} Quiz")

    df_q = load_questions(quiz_sets[selected_set]["questions"])
    df_a = load_answers(quiz_sets[selected_set]["answers"])

    if df_q.empty or df_a.empty:
        st.warning("⚠️ Data not available for this set.")
        return

    total_questions = len(df_q)

    # Session state init
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "results" not in st.session_state:
        st.session_state.results = None

    # Show questions
    for index, row in df_q.iterrows():
        st.write(f"**Q{index+1}: {row['question']}**")
        options = [row['1'], row['2'], row['3'], row['4']]
        st.session_state.answers[index] = st.radio(
            f"Your answer for Q{index+1}:",
            options,
            key=f"{selected_set}_{index}"
        )

    # Submit button
    if st.button("✅ Submit"):
        score = 0
        incorrect = []
        for i, row in df_q.iterrows():
            correct_option_number = df_a.iloc[i]["correct_ans"]
            correct_option_text = row[str(correct_option_number)]
            user_answer = st.session_state.answers.get(i, None)
            if user_answer == correct_option_text:
                score += 1
            else:
                incorrect.append((row['question'], correct_option_text))

        st.session_state.results = {"score": score, "incorrect": incorrect, "total": total_questions}
        st.session_state.submitted = True

    # Results
    if st.session_state.submitted and st.session_state.results:
        score = st.session_state.results["score"]
        incorrect = st.session_state.results["incorrect"]

        st.success(f"### 🎯 Your Score: {score}/{total_questions}")
        if incorrect:
            st.error("❌ Incorrect Answers:")
            for q, correct in incorrect:
                st.markdown(f"- **Q:** {q}  \n  ✅ Correct: {correct}")
        else:
            st.balloons()
            st.success("🎉 Perfect! All answers correct.")

    # Back button
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.session_state.submitted = False
        st.session_state.results = None

# ---------- Home Page ----------
def home_page():
    st.title("📘 Current Affairs Quiz by Suraj")
    st.write("👉 Select a quiz set to start practice!")

    quiz_sets = get_quiz_sets()
    cols = st.columns(2)

    for i, set_name in enumerate(quiz_sets.keys()):
        with cols[i % 2]:
            if st.button(set_name, use_container_width=True):
                st.session_state.selected_set = set_name
                st.session_state.page = "quiz"

# ---------- Main ----------
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "selected_set" not in st.session_state:
        st.session_state.selected_set = None

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "quiz":
        run_quiz(st.session_state.selected_set, get_quiz_sets())

if __name__ == "__main__":
    main()
