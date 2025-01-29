import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_review(text, stars):
    """
    Analyze the tone and sentiment of a review using OpenAI's ChatGPT API.
    Returns a dictionary with keys 'tone' and 'sentiment'.
    """
    prompt = f"""
    Analyze the following review and provide its tone and sentiment:
    Review: {text}
    Stars: {stars}

    Return the response in JSON format with the following keys:
    - tone (e.g., positive, negative, neutral)
    - sentiment (e.g., happy, angry, sad)
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=100,
        )

        result_text = response["choices"][0]["message"]["content"].strip()

        result = json.loads(result_text)
        return result

    except json.JSONDecodeError:
        raise ValueError("Failed to parse OpenAI response as JSON.")
    except Exception as e:
        raise RuntimeError(f"Error analyzing review: {e}")
