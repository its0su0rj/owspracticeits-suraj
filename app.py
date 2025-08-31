import streamlit as st
import pandas as pd
import requests
from io import StringIO

# ===========================
# Load Questions CSV
# ===========================
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

# ===========================
# Load Answers CSV
# ===========================
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

# ===========================
# Quiz Sets Dictionary
# ===========================
def get_quiz_sets():
    return {
        # JANUARY
        "Jan2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/january2025ans.csv"
        },
        "Jan2025-Set2": {
            "questions": "https://raw.githubusercontent.com/.../january2025_set2.csv",
            "answers":   "https://raw.githubusercontent.com/.../january2025_set2ans.csv"
        },
        "Jan2025-Set3": {
            "questions": "https://raw.githubusercontent.com/.../january2025_set3.csv",
            "answers":   "https://raw.githubusercontent.com/.../january2025_set3ans.csv"
        },

        # FEBRUARY
        "Feb2025-Set1": {
            "questions": "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025.csv",
            "answers":   "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/february2025ans.csv"
        },
        "Feb2025-Set2": {
            "questions": "https://raw.githubusercontent.com/.../february2025_set2.csv",
            "answers":   "https://raw.githubusercontent.com/.../february2025_set2ans.csv"
        },
        "Feb2025-Set3": {
            "questions": "https://raw.githubusercontent.com/.../february2025_set3.csv",
            "answers":   "https://raw.githubusercontent.com/.../february2025_set3ans.csv"
        },

        # Add March – August similar way...
        
        # BIHAR CA
        "BiharCA-Set1": {
            "questions": "https://raw.githubusercontent.com/.../biharca_set1.csv",
            "answers":   "https://raw.githubusercontent.com/.../biharca_set1ans.csv"
        },

        # TOPICWISE
        "Topicwise-Economy": {
            "questions": "https://raw.githubusercontent.com/.../topicwise_economy.csv",
            "answers":   "https://raw.githubusercontent.com/.../topicwise_economyans.csv"
        },
        "Topicwise-Sports": {
            "questions": "https://raw.githubusercontent.com/.../topicwise_sports.csv",
            "answers":   "https://raw.githubusercontent.com/.../topicwise_sportsans.csv"
        }
    }

# ===========================
# Run Quiz Page
# ===========================
def run_quiz(selected_set, quiz_sets):
    st.subheader(f"📝 {selected_set} Quiz")
    df_q = load_questions(quiz_sets[selected_set]["questions"])
    df_a = load_answers(quiz_sets[selected_set]["answers"])

    if df_q.empty or df_a.empty:
        st.warning("⚠️ Data not available for this set.")
        if st.button("⬅️ Back to Home"):
            st.query_params.clear()
            st.rerun()
        return

    total_questions = len(df_q)
    score = 0
    user_answers = []

    st.write("### Answer the questions:")

    for index, row in df_q.iterrows():
        st.write(f"**Q{index+1}: {row['question']}**")
        options = [row['1'], row['2'], row['3'], row['4']]
        user_answer = st.radio(
            f"Your answer for Q{index+1}:", options, key=f"{selected_set}_{index}"
        )
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

    # Back button
    if st.button("⬅️ Back to Home"):
        st.query_params.clear()
        st.rerun()

# ===========================
# Homepage Layout
# ===========================
def homepage():
    st.subheader("📌 Choose a Quiz Set")

    # Monthwise Layout
    months = ["Jan 2025", "Feb 2025", "Mar 2025", "Apr 2025", "May 2025", "Jun 2025", "Jul 2025", "Aug 2025"]

    for m in months:
        st.markdown(f"### {m}")
        cols = st.columns(3)
        for i in range(3):
            if cols[i].button(f"Set {i+1}", key=f"{m}_Set{i+1}"):
                st.query_params["set"] = f"{m.replace(' ', '')}-Set{i+1}"
                st.rerun()

    # Bihar CA Section
    st.markdown("### 🟢 Bihar Current Affairs")
    cols = st.columns(3)
    if cols[0].button("Bihar Set 1"):
        st.query_params["set"] = "BiharCA-Set1"
        st.rerun()

    # Topicwise Section
    st.markdown("### 🔵 Topicwise Current Affairs")
    cols = st.columns(3)
    if cols[0].button("Economy"):
        st.query_params["set"] = "Topicwise-Economy"
        st.rerun()
    if cols[1].button("Sports"):
        st.query_params["set"] = "Topicwise-Sports"
        st.rerun()

# ===========================
# Main Function
# ===========================
def main():
    st.title("📘 Current Affairs Quiz by Suraj")
    quiz_sets = get_quiz_sets()

    selected_set = st.query_params.get("set", None)
    if isinstance(selected_set, list):  # FIX for query params
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
