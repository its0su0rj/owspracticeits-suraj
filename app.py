import streamlit as st
import pandas as pd

# ===========================
# Load Questions & Answers
# ===========================
def load_questions(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame()

def load_answers(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame()

# ===========================
# Define Quiz Sets
# ===========================
def get_quiz_sets():
    quiz_sets = {}

    months = ["Jan2025", "Feb2025", "Mar2025", "Apr2025",
              "May2025", "Jun2025", "Jul2025", "Aug2025"]

    for m in months:
        for i in range(1, 3+1):
            quiz_sets[f"{m}-Set{i}"] = {
                "questions": f"data/{m.lower()}_set{i}_q.csv",
                "answers": f"data/{m.lower()}_set{i}_a.csv"
            }

    # Bihar CA
    quiz_sets["BiharCA-Set1"] = {
        "questions": "data/bihar_set1_q.csv",
        "answers": "data/bihar_set1_a.csv"
    }

    # Topicwise
    quiz_sets["Topicwise-Economy"] = {
        "questions": "data/topicwise_economy_q.csv",
        "answers": "data/topicwise_economy_a.csv"
    }
    quiz_sets["Topicwise-Sports"] = {
        "questions": "data/topicwise_sports_q.csv",
        "answers": "data/topicwise_sports_a.csv"
    }

    return quiz_sets

# ===========================
# Homepage Layout (exact like screenshot)
# ===========================
def homepage():
    st.subheader("📌 Choose a Quiz Set")

    months = ["Jan 2025", "Feb 2025", "Mar 2025", "Apr 2025",
              "May 2025", "Jun 2025", "Jul 2025", "Aug 2025"]

    for m in months:
        st.markdown(f"**{m}**")   # month heading (bold)

        for i in range(1, 4):
            if st.button(f"Set {i}", key=f"{m}_Set{i}", use_container_width=True):
                st.session_state["page"] = "quiz"
                st.session_state["selected_set"] = f"{m.replace(' ', '')}-Set{i}"
                st.rerun()

    # Bihar CA Section
    st.markdown("**Bihar Current Affairs**")
    if st.button("Set 1", key="bihar1", use_container_width=True):
        st.session_state["page"] = "quiz"
        st.session_state["selected_set"] = "BiharCA-Set1"
        st.rerun()

    # Topicwise Section
    st.markdown("**Topicwise Current Affairs**")
    if st.button("Economy", key="eco", use_container_width=True):
        st.session_state["page"] = "quiz"
        st.session_state["selected_set"] = "Topicwise-Economy"
        st.rerun()
    if st.button("Sports", key="sports", use_container_width=True):
        st.session_state["page"] = "quiz"
        st.session_state["selected_set"] = "Topicwise-Sports"
        st.rerun()

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
            st.session_state["page"] = "home"
            st.rerun()
        return

    score = 0
    for idx, row in df_q.iterrows():
        q = row.get("Question", "")
        options = [row.get("Option1", ""), row.get("Option2", ""),
                   row.get("Option3", ""), row.get("Option4", "")]
        correct = df_a.iloc[idx].get("Answer", "")

        st.write(f"**Q{idx+1}. {q}**")
        user_ans = st.radio("Choose:", options, key=f"q{idx}")
        if st.button(f"Submit Q{idx+1}", key=f"submit{idx}"):
            if user_ans == correct:
                st.success("✅ Correct!")
                score += 1
            else:
                st.error(f"❌ Wrong! Correct: {correct}")

    st.info(f"Your Score: {score}/{len(df_q)}")

    if st.button("⬅️ Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()

# ===========================
# Main App
# ===========================
def main():
    st.title("📘 Current Affairs Quiz by Suraj")

    quiz_sets = get_quiz_sets()

    # initialize session state
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    if "selected_set" not in st.session_state:
        st.session_state["selected_set"] = None

    if st.session_state["page"] == "home":
        homepage()
    elif st.session_state["page"] == "quiz":
        if st.session_state["selected_set"] in quiz_sets:
            run_quiz(st.session_state["selected_set"], quiz_sets)
        else:
            st.error("⚠️ Invalid quiz set selected. Returning home.")
            st.session_state["page"] = "home"
            st.rerun()

if __name__ == "__main__":
    main()
