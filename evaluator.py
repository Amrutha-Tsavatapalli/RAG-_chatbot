# modules/evaluator.py

import requests

def evaluate_answer(question, answer):
    api_url = "https://api.together.xyz/v1/completions"
    headers = {"Authorization": "Bearer aaaef45831bd088ba6b7f24819ec8fc8f27800e17cf649d0001246df48042254"}
    prompt = f"""You are an HR expert. Evaluate the candidate's answer to this question.\n\nQuestion: {question}\n\nAnswer: {answer}\n\nGive a score out of 10 and suggest how it can be improved."""
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
        return text.strip()
    else:
        return f"Failed to evaluate answer. API response: {response.text}"
