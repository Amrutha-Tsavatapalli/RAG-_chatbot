# main.py
import os
from modules.resume_parser import parse_resume
from modules.retriever import retrieve_questions
from modules.evaluator import evaluate_answer
from modules.embedder import build_faiss_index

def main():
    print("=== HR RAG Chatbot (Terminal Version) ===")
    resume_path = input("Enter path to your resume (PDF or DOCX): ")

    if not os.path.exists(resume_path):
        print("❌ File does not exist. Exiting.")
        return

    print("✅ Parsing resume...")
    profile = parse_resume(resume_path)
    print(f"Stream: {profile['stream']}")
    print(f"Skills: {', '.join(profile['skills'])}")

    print("📚 Building question index...")
    build_faiss_index(profile["stream"])

    print("🔍 Retrieving questions...")
    questions = retrieve_questions(profile)

    print("\n🧠 Starting Interview Simulation:")
    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q}")
        answer = input("Your Answer: ")
        feedback = evaluate_answer(q, answer)
        print(f"💬 Feedback:\n{feedback}")

    print("\n🎉 Interview session completed!")

if __name__ == "__main__":
    main()
