import openai
import os

# Load your API key (You can also set it as an env variable)
openai.api_key = "your-api-key-here"

def generate_test_case(api_description):
    prompt = f"""
You are a Python automation tester. 
Generate a Pytest-based API test using the requests library.
API Description:
{api_description}

Make sure to include:
- Status code validation
- Response body check (if possible)
- Clear test function with docstring
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response['choices'][0]['message']['content']


# === USAGE EXAMPLE ===

if __name__ == "__main__":
    api_info = """
POST /login - Authenticates the user. Request body: { "username": string, "password": string }.
Returns 200 OK with { "token": string } or 401 Unauthorized.
"""

    print("Generating test case from description...")
    test_code = generate_test_case(api_info)

    # Save it to a test file
    with open("test_generated_login.py", "w") as f:
        f.write(test_code)

    print("✅ Test case saved to test_generated_login.py")
