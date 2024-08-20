import streamlit as st
import difflib
from datetime import datetime, timedelta

# Function to calculate WPM
def calculate_wpm(start_time, end_time, text_length):
    elapsed_time = (end_time - start_time).total_seconds() / 60  # Time in minutes
    wpm = text_length / 5 / elapsed_time if elapsed_time > 0 else 0
    return wpm

# Function to calculate errors
def calculate_errors(original_text, typed_text):
    differ = difflib.Differ()
    differences = list(differ.compare(original_text.split(), typed_text.split()))
    errors = [diff for diff in differences if diff.startswith('- ')]
    return len(errors), differences

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

# Streamlit app title
st.title("Typing Practice App")

# Upload text file to practice
uploaded_file = st.file_uploader("Upload a text file to practice", type=["txt"])

if uploaded_file is not None:
    # Display the original text to be typed
    text = uploaded_file.read().decode("utf-8")
    
    # Start button to initiate the timer
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None

    if st.button("Start"):
        st.session_state.start_time = datetime.now()

    if st.session_state.start_time:
        # Calculate the remaining time
        time_remaining = timedelta(minutes=15) - (datetime.now() - st.session_state.start_time)
        if time_remaining.total_seconds() > 0:
            st.write(f"**Time Remaining:** {str(time_remaining).split('.')[0]}")
        else:
            st.session_state.start_time = None
            st.write("**Time's up!** Automatically submitting your typing.")

        # Display the original text and typing area in two equal halves
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Text")
            st.write(f"<div style='height:400px; overflow:auto;'>{text}</div>", unsafe_allow_html=True)

        with col2:
            st.subheader("Type Here")
            user_input = st.text_area("Start typing the text here:", height=400, key="typing_area")

        # Automatically submit if the timer runs out
        if time_remaining.total_seconds() <= 0 or st.button("Submit"):
            end_time = datetime.now()

            # Calculate WPM based on the elapsed time and the length of the typed text
            text_length = len(user_input)
            wpm = calculate_wpm(st.session_state.start_time, end_time, text_length)

            # Calculate errors by comparing the original text and typed text
            total_words = len(text.split())
            errors, differences = calculate_errors(text, user_input)
            error_percentage = (errors / total_words) * 100
            highlighted_text = highlight_errors(differences)

            # Display the results: WPM, total errors, error percentage, and highlighted text
            st.write("### Typing Analysis")
            st.write(f"**Words Per Minute (WPM):** {wpm:.2f}")
            st.write(f"**Total Errors:** {errors}")
            st.write(f"**Error Percentage:** {error_percentage:.2f}%")

            st.write("### Error Highlighting")
            st.markdown(highlighted_text, unsafe_allow_html=True)

            # Reset the start time for a new session
            st.session_state.start_time = None
