import json
import os
import time

from openai import OpenAI


def analyze_transaction_with_llm(description: str) -> tuple[bool, str]:
    """Use an LLM to infer if a free-text description suggests fraud.

    Contract:
    - Input: transaction description string
    - Output: tuple (is_fraud: bool, reason: str)
    - Behavior: returns a conservative default if description is missing or API fails

    Notes:
    - The model and prompt are intentionally simple for the lab; production systems
      should add guardrails, schemas, and timeouts/retries.
    - Requires OPENAI_API_KEY in the environment (loaded via dotenv in main.py).
    """

    if not description:
        return False, "No description"

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        # Minimal prompt asking for strict JSON output to make parsing robust.
        response = client.responses.create(
            model="gpt-5-nano",
            input=(
                f'Is this transaction description fraudulent? "{description}" '
                'Return your answer exclusively in JSON format: '
                '{"is_fraud": true/false, "reason": "brief explanation"}'
            ),
        )
        result = response.output_text
        json_content = json.loads(result)
        return json_content.get("is_fraud", False), json_content.get("reason", "Unknown")

    except Exception as e:
        # Fail closed: don't block the pipeline due to AI service hiccups.
        print("Error calling OpenAI API:", e)
        return False, "API error"

# Todo: incorporate previous fraud tactics or few-shot exemplars for better guidance