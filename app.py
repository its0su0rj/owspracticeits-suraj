import streamlit as st
import pandas as pd
import requests
from io import StringIO

# ----------------------
# Helpers
# ----------------------
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

# ----------------------
# Quiz sets dictionary
# ----------------------
def get_quiz_sets():
    base = "https://raw.githubusercontent.com/its0su0rj/owspracticeits-suraj/main/"

    return {
        # Monthly CA
        "Feb2025-Set1": {"questions": base+"february2025.csv", "answers": base+"february2025ans.csv"},
        "Feb2025-Set2": {"questions": base+"february2025.csv", "answers": base+"february2025ans.csv"},
        "Feb2025-Set3": {"questions": base+"february2025.csv", "answers": base+"february2025ans.csv"},

        "March2025-Set1": {"questions": base+"march2025.csv", "answers": base+"march2025ans.csv"},
        "March2025-Set2": {"questions": base+"march2025.csv", "answers": base+"march2025ans.csv"},
        "March2025-Set3": {"questions": base+"march2025.csv", "answers": base+"march2025ans.csv"},

        "April2025-Set1": {"questions": base+"april2025.csv", "answers": base+"april2025ans.csv"},
        "April2025-Set2": {"questions": base+"april2025.csv", "answers": base+"april2025ans.csv"},
        "April2025-Set3": {"questions": base+"april2025.csv", "answers": base+"april2025ans.csv"},

        "May2025-Set1": {"questions": base+"may2025.csv", "answers": base+"may2025ans.csv"},
        "May2025-Set2": {"questions": base+"may2025.csv", "answers": base+"may2025ans.csv"},
        "May2025-Set3": {"questions": base+"may2025.csv", "answers": base+"may2025ans.csv"},

        "July2025-Set1": {"questions": base+"july2025.csv", "answers": base+"july2025ans.csv"},
        "July2025-Set2": {"questions": base+"july2025.csv", "answers": base+"july2025ans.csv"},
        "July2025-Set3": {"questions": base+"july2025.csv", "answers": base+"july2025ans.csv"},

        "Aug2025-Set1": {"questions": base+"august2025.csv", "answers": base+"august2025ans.csv"},
        "Aug2025-Set2": {"questions": base+"august2025.csv", "answers": base+"august2025ans.csv"},
        "Aug2025-Set3": {"questions": base+"august2025.csv", "answers": base+"august2025ans.csv"},

        # Bihar CA
        "Bihar-Set1": {"questions": base+"biharca.csv", "answers": base+"biharcaans.csv"},
        "Bihar-Set2": {"questions": base+"biharca.csv", "answers": base+"biharcaans.csv"},
        "Bihar-Set3": {"questions": base+"biharca.csv", "answers": base+"biharcaans.csv"},

        # Topic Wise
        "Topic-Set1": {"questions": base+"topicwise.csv", "answers": base+"topicwiseans.csv"},
        "Topic-Set2": {"questions": base+"topicwise.csv", "answers": base+"topicwiseans.csv"},
        "Topic-Set3": {"questions": base+"topicwise.csv", "answers": base+"topicwiseans.csv"},
    }

# ----------------------
# Quiz runner
# ----------------------
def run_quiz(selected_set, quiz_sets):
    df_q = load_questions(quiz_sets[selected_set]["questions"])
    df_a = load_answers(quiz_sets[selected_set]["answers"])

    if df_q.empty or df_a.empty:
        st.warning("⚠️ Data not available for this set.")
        return

    if st.button("⬅️ Back to Home"):
        st.query_params.clear()
        st.rerun()

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

# ----------------------
# Homepage
# ----------------------
def homepage():
    st.subheader("Monthly CA")

    # February to March row
    with st.container():
        st.write("**Feb 2025**")
        cols = st.columns(3)
        for i in range(1, 4):
            if cols[i-1].button(f"Set-{i}", key=f"Feb{i}"):
                st.query_params["set"] = f"Feb2025-Set{i}"
                st.rerun()

    with st.container():
        st.write("**March 2025**")
        cols = st.columns(3)
        for i in range(1, 4):
            if cols[i-1].button(f"Set-{i}", key=f"Mar{i}"):
                st.query_params["set"] = f"March2025-Set{i}"
                st.rerun()

    with st.container():
        st.write("**April 2025**")
        cols = st.columns(3)
        for i in range(1, 4):
            if cols[i-1].button(f"Set-{i}", key=f"Apr{i}"):
                st.query_params["set"] = f"April2025-Set{i}"
                st.rerun()

    with st.container():
        st.write("**May 2025**")
        cols = st.columns(3)
        for i in range(1, 4):
            if cols[i-1].button(f"Set-{i}", key=f"May{i}"):
                st.query_params["set"] = f"May2025-Set{i}"
                st.rerun()

    with st.container():
        st.write("**July 2025**")
        cols = st.columns(3)
        for i in range(1, 4):
            if cols[i-1].button(f"Set-{i}", key=f"Jul{i}"):
                st.query_params["set"] = f"July2025-Set{i}"
                st.rerun()

    with st.container():
        st.write("**Aug 2025**")
        cols = st.columns(3)
        for i in range(1, 4):
            if cols[i-1].button(f"Set-{i}", key=f"Aug{i}"):
                st.query_params["set"] = f"Aug2025-Set{i}"
                st.rerun()

    # Bihar CA
    st.subheader("Bihar CA")
    cols = st.columns(3)
    for i in range(1, 4):
        if cols[i-1].button(f"Set-{i}", key=f"Bihar{i}"):
            st.query_params["set"] = f"Bihar-Set{i}"
            st.rerun()

    # Topic Wise
    st.subheader("Topic Wise")
    cols = st.columns(3)
    for i in range(1, 4):
        if cols[i-1].button(f"Set-{i}", key=f"Topic{i}"):
            st.query_params["set"] = f"Topic-Set{i}"
            st.rerun()

# ----------------------
# Main
# ----------------------
def main():
    st.title("📘 Current Affairs Quiz by Suraj")
    quiz_sets = get_quiz_sets()

    selected_set = st.query_params.get("set", None)

    if not selected_set:
        homepage()
    else:
        run_quiz(selected_set, quiz_sets)


if __name__ == "__main__":
    main()
