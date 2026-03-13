from huggingface_hub import InferenceClient

# Create HF client
client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token="API KEY"
)


def ask_llm(prompt):
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"LLM Error: {str(e)}"


def run_security_audit(code):

    prompt = f"""
You are a cybersecurity auditor.

Analyze this code and return:

1. Programming language
2. Vulnerabilities found
3. Secure fixes
4. Security score out of 100

Code:
{code}
"""

    result = ask_llm(prompt)

    return f"""

{result}
"""