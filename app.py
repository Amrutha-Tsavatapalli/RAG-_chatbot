# ui/app.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import streamlit as st
import requests
from modules.resume_parser import parse_resume
from modules.evaluator import evaluate_answer

# LLM-based question generation using Together AI
def generate_questions_with_llm(profile):
    api_url = "https://api.together.xyz/v1/completions"
    headers = {"Authorization": ""}
    prompt = (
        f"You are an HR interviewer. Generate 5 technical interview questions for a candidate "
        f"with the stream '{profile['stream']}' and skills: {', '.join(profile['skills'])}. "
        f"Return only the questions as a numbered list."
    )
    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 256,
        "temperature": 0.7,
        "top_p": 0.9,
        "stop": None,
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        text = response.json()["choices"][0]["text"]
        questions = [line.lstrip("1234567890. ").strip() for line in text.split('\n') if line.strip()]
        questions = [q for q in questions if len(q) > 10]
        return questions[:5]
    else:
        return [f"Failed to generate questions. API response: {response.text}"]

st.title("🤖 HR Interview Chatbot")


uploaded = st.file_uploader("Upload your resume (PDF/DOCX)", type=["pdf", "docx"])

if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'profile' not in st.session_state:
    st.session_state.profile = None

if uploaded and not st.session_state.interview_started:
    st.write("Saving uploaded resume...")
    with open(f"data/resumes/{uploaded.name}", "wb") as f:
        f.write(uploaded.read())
    st.write("Resume saved. Parsing resume...")

    profile = parse_resume(f"data/resumes/{uploaded.name}")
    st.session_state.profile = profile
    st.write("Resume parsed:", profile)
    st.success(f"Detected Stream: {profile['stream']}")
    st.info(f"Skills: {', '.join(profile['skills'])}")

    if st.button("Start Interview"):
        st.write("Generating questions using LLM...")
        questions = generate_questions_with_llm(profile)
        st.session_state.questions = questions
        st.session_state.interview_started = True

# If interview started, show questions and answer boxes
if st.session_state.interview_started:
    profile = st.session_state.profile
    questions = st.session_state.questions
    st.write(f"Questions generated: {questions}")
    for idx, q in enumerate(questions):
        st.subheader(f"Q{idx+1}: {q}")
        user_ans = st.text_area("Your Answer:", key=f"answer_{idx}")
        if user_ans:
            st.write(f"Evaluating answer for: {q}")
            feedback = evaluate_answer(q, user_ans)
            st.markdown(f"**Feedback:** {feedback}")

    if st.button("End Interview"):
        st.session_state.interview_started = False
        st.session_state.questions = []
        st.session_state.profile = None
