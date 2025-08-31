# modules/chatbot.py

from modules.resume_parser import parse_resume
from modules.evaluator import evaluate_answer


# LLM-based question generation using HuggingFace Inference API
import requests

def generate_questions_with_llm(profile):
    api_url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {"Authorization": "Bearer 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"}
    prompt = (
        f"You are an HR interviewer. Generate 5 technical interview questions for a candidate "
        f"with the stream '{profile['stream']}' and skills: {', '.join(profile['skills'])}. "
        f"Return only the questions as a numbered list."
    )
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 256, "temperature": 0.7},
    }
    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        content = response.json()
        # HuggingFace API returns a list of dicts with 'generated_text'
        if isinstance(content, list) and 'generated_text' in content[0]:
            text = content[0]['generated_text']
        elif isinstance(content, dict) and 'generated_text' in content:
            text = content['generated_text']
        elif isinstance(content, list) and 'text' in content[0]:
            text = content[0]['text']
        else:
            text = str(content)
        # Split by lines and remove numbering
        questions = [line.lstrip("1234567890. ").strip() for line in text.split('\n') if line.strip()]
        # Filter out empty lines and keep only reasonable questions
        questions = [q for q in questions if len(q) > 10]
        return questions[:5]
    else:
        return ["Failed to generate questions. Please check your API key or model."]

def interview_pipeline(resume_path):
    profile = parse_resume(resume_path)
    print(f"Stream: {profile['stream']}, Skills: {profile['skills']}")

    questions = generate_questions_with_llm(profile)

    results = []
    for q in questions:
        print("\nQuestion:", q)
        ans = input("Your Answer: ")
        feedback = evaluate_answer(q, ans)
        print("Feedback:", feedback)
        results.append({"question": q, "answer": ans, "feedback": feedback})

    return results
