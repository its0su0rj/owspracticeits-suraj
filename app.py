import streamlit as st
import time
import difflib
from datetime import datetime, timedelta

# Function to calculate WPM
def calculate_wpm(start_time, current_time, text_length):
    elapsed_time = (current_time - start_time) / 60  # Time in minutes
    wpm = text_length / 5 / elapsed_time if elapsed_time > 0 else 0
    return wpm

# Function to calculate errors
def calculate_errors(original_text, typed_text):
    differ = difflib.Differ()
    differences = list(differ.compare(original_text.split(), typed_text.split()))
    errors = [diff for diff in differences if diff.startswith('- ')]
    return len(errors), differences

# Function to display suggestions
def suggest_improvements(errors, total_words):
    error_rate = (errors / total_words) * 100
    suggestions = []
    if error_rate > 10:
        suggestions.append("Consider slowing down and focusing on accuracy.")
    if error_rate > 5 and error_rate <= 10:
        suggestions.append("You're doing well, but try to reduce the number of errors.")
    if error_rate <= 5:
        suggestions.append("Great job! Keep practicing to maintain your accuracy.")
    return suggestions

# Function to highlight errors in the typed text
def highlight_errors(differences):
    highlighted_text = []
    for diff in differences:
        if diff.startswith('- '):
            highlighted_text.append(f"<span style='color:red'>{diff[2:]}</span>")
        elif diff.startswith('+ '):
            highlighted_text.append(f"<span style='color:green'>{diff[2:]}</span>")
        else:
            highlighted_text.append(diff[2:])
    return ' '.join(highlighted_text)

st.title("Typing Practice App")

uploaded_file = st.file_uploader("Upload a text file to practice", type=["txt"])

if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")
    st.write("Here is the text you will be practicing:")
    st.write(text)

    start_time = None
    end_time = None
    typed_text = st.empty()

    if st.button("Start Typing"):
        start_time = datetime.now()
        time_limit = timedelta(minutes=20)
        
        while (datetime.now() - start_time) < time_limit:
            current_time = datetime.now()
            # Use a unique key based on timestamp
            user_input = st.text_area("Start typing the text here:", height=300, key=f"typing_area_{current_time.timestamp()}")
            
            text_length = len(user_input)
            wpm = calculate_wpm(start_time.timestamp(), current_time.timestamp(), text_length)
            
            st.write(f"**Real-Time Words Per Minute (WPM):** {wpm:.2f}")
            time.sleep(1)

        # Analysis after 20 minutes or when the user stops typing
        end_time = datetime.now()
        total_words = len(text.split())
        errors, differences = calculate_errors(text, user_input)
        error_percentage = (errors / total_words) * 100
        suggestions = suggest_improvements(errors, total_words)
        highlighted_text = highlight_errors(differences)
        
        st.write("### Typing Analysis")
        st.write(f"**Words Per Minute (WPM):** {wpm:.2f}")
        st.write(f"**Total Errors:** {errors}")
        st.write(f"**Error Percentage:** {error_percentage:.2f}%")
        
        st.write("### Suggestions for Improvement")
        for suggestion in suggestions:
            st.write(f"- {suggestion}")
        
        st.write("### Error Highlighting")
        st.markdown(highlighted_text, unsafe_allow_html=True)
    else:
        st.warning("Please start typing to begin the practice session.")
