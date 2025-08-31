import streamlit as st
import pandas as pd
import requests
from io import StringIO

# -------------------
# Load Questions CSV
# -------------------
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

# -------------------
# Load Answers CSV
# -------------------
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

# -------------------
# Quiz Sets
# -------------------
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
        },
        "May 2025": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025ans.csv"
        },
        "June 2025": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/june2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/june2025ans.csv"
        },
        "July 2025": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025ans.csv"
        },
        "August 2025": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025ans.csv"
        }
    }

# -------------------
# Run Quiz Page
# -------------------
def run_quiz(selected_set, quiz_sets):
    st.markdown("### ⬅️ [Back to Home](?home=true)", unsafe_allow_html=True)

    st.subheader(f"📖 {selected_set} Quiz")

    # Load data
    df_q = load_questions(quiz_sets[selected_set]["questions"])
    df_a = load_answers(quiz_sets[selected_set]["answers"])

    if df_q.empty or df_a.empty:
        st.warning("⚠️ Data not available for this set.")
        return

    total_questions = len(df_q)

    # --- Initialize session state ---
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "results" not in st.session_state:
        st.session_state.results = None

    # --- Questions UI ---
    for index, row in df_q.iterrows():
        st.write(f"**Q{index+1}: {row['question']}**")
        options = [row['1'], row['2'], row['3'], row['4']]

        # Answer saving
        st.session_state.answers[index] = st.radio(
            f"Your answer for Q{index+1}:",
            options,
            key=f"{selected_set}_{index}"
        )

    # --- Submit button ---
    if st.button("✅ Submit"):
        score = 0
        incorrect = []
        for i, row in df_q.iterrows():
            correct_option_number = df_a.iloc[i]["correct_ans"]  # 1,2,3,4
            correct_option_text = row[str(correct_option_number)]
            user_answer = st.session_state.answers.get(i, None)
            if user_answer == correct_option_text:
                score += 1
            else:
                incorrect.append((row['question'], correct_option_text))

        # Save results in session_state
        st.session_state.results = {"score": score, "incorrect": incorrect, "total": total_questions}
        st.session_state.submitted = True

    # --- Show Results ---
    if st.session_state.submitted and st.session_state.results:
        score = st.session_state.results["score"]
        incorrect = st.session_state.results["incorrect"]
        total_questions = st.session_state.results["total"]

        st.success(f"### 🎯 Your Score: {score}/{total_questions}")
        if incorrect:
            st.error("❌ Incorrect Answers:")
            for q, correct in incorrect:
                st.markdown(f"- **Q:** {q}  \n  ✅ Correct: {correct}")
        else:
            st.balloons()
            st.success("🎉 Perfect! All answers correct.")



# -------------------
# Homepage Layout
# -------------------
def homepage():
    st.header("📘 Current Affairs Quiz by Suraj")
    quiz_sets = get_quiz_sets()

    st.subheader("📅 Monthly Quiz Sets")
    cols = st.columns(2)
    i = 0
    for set_name in quiz_sets.keys():
        if cols[i % 2].button(set_name, key=set_name):
            st.query_params["set"] = set_name
            st.rerun()
        i += 1

    st.markdown("---")
    st.subheader("🌍 BiharCA Section")
    st.info("👉 Here you will get quizzes related to Bihar Current Affairs (Coming soon).")

    st.markdown("---")
    st.subheader("📂 Topicwise Section")
    st.info("👉 Here you will get quizzes arranged topicwise (Coming soon).")

# -------------------
# Main
# -------------------
def main():
    quiz_sets = get_quiz_sets()
    selected_set = st.query_params.get("set", None)
    if isinstance(selected_set, list):
        selected_set = selected_set[0]

    if not selected_set:
        homepage()
    else:
        if selected_set in quiz_sets:
            run_quiz(selected_set, quiz_sets)
        else:
            st.error("⚠️ Invalid quiz set selected. Please go back to Home.")
            if st.button("⬅️ Back to Home"):
                st.query_params.clear()
                st.rerun()

if __name__ == "__main__":
    main()
