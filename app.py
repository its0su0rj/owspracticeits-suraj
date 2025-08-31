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
        "January 2025  196Q": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025ans.csv"
        },
        "February 2025coming": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025ans.csv"
        },
        "March 2025  140Q": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/march2025ans.csv"
        },
        "April 2025  155Q": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/april2025ans.csv"
        },
        "May 2025  155Q": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/may2025ans.csv"
        },
        "June 2025coming": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/june2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/june2025ans.csv"
        },
        "July 2025coming": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/july2025ans.csv"
        },
        "August 2025coming": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/august2025ans.csv"
        }
    }

# -------------------
# Run Quiz Page
# -------------------
def run_quiz(selected_set, quiz_sets):
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.session_state.results = None
        return

    st.subheader(f"📖 {selected_set} Quiz")

    df_q = load_questions(quiz_sets[selected_set]["questions"])
    df_a = load_answers(quiz_sets[selected_set]["answers"])

    if df_q.empty or df_a.empty:
        st.warning("⚠️ Data not available for this set.")
        return

    total_questions = len(df_q)

    # --- Session state init ---
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
    if "results" not in st.session_state:
        st.session_state.results = None

    # --- If not submitted: show quiz ---
    if not st.session_state.submitted:
        for index, row in df_q.iterrows():
            st.write(f"**Q{index+1}: {row['question']}**")
            options = [row['1'], row['2'], row['3'], row['4']]
            st.session_state.answers[index] = st.radio(
                f"Your answer for Q{index+1}:",
                options,
                key=f"{selected_set}_{index}"
            )

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

            st.session_state.results = {
                "score": score,
                "incorrect": incorrect,
                "total": total_questions
            }
            st.session_state.submitted = True

    # --- If submitted: show results ---
    
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
         # ✅ Extra Back to Home button at end
        if st.button("⬅️ Back to Home", key="back_home_after_results"):
           st.session_state.page = "home"
           st.session_state.answers = {}
           st.session_state.submitted = False
           st.session_state.results = None
   

# -------------------
# Homepage Layout
# -------------------
def homepage():
    st.header("📘 Current Affairs Quiz by Suraj")

    # Gradient Colorful Buttons
    st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;  /* ✅ Full width button */
        background: linear-gradient(135deg, #4CAF50, #2196F3);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.6em 1.2em;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #45a049, #1976D2);
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

    quiz_sets = get_quiz_sets()
    #st.subheader("📅 Monthly Quiz Sets")
    st.subheader("📅 Monthly Quiz Sets: (source KGS)")
    st.markdown("<p style='color:red; font-weight:bold;'>**CLIK 2 TIMES ON EACH SET</p>", unsafe_allow_html=True)


    # ✅ Keep buttons in correct order & full width
    for set_name in quiz_sets.keys():
        if st.button(set_name, key=set_name):
            st.session_state.page = "quiz"
            st.session_state.selected_set = set_name
            st.session_state.answers = {}
            st.session_state.submitted = False
            st.session_state.results = None

    st.markdown("---")
    st.subheader("🌍 BiharCA Section")
    st.info("👉 Bihar Current Affairs quizzes coming soon.")

    st.markdown("---")
    st.subheader("📂 Topicwise Section")
    st.info("👉 Topicwise quizzes coming soon.")



# -------------------
# Main
# -------------------
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "selected_set" not in st.session_state:
        st.session_state.selected_set = None

    quiz_sets = get_quiz_sets()

    if st.session_state.page == "home":
        homepage()
    elif st.session_state.page == "quiz" and st.session_state.selected_set:
        run_quiz(st.session_state.selected_set, quiz_sets)
    else:
        homepage()

if __name__ == "__main__":
    main()
