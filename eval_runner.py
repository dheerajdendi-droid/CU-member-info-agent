import os
import time
import uuid
import requests

from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

LYZR_API_KEY = os.getenv("LYZR_API_KEY")
LYZR_AGENT_ID = os.getenv("LYZR_AGENT_ID")
LYZR_ENDPOINT = os.getenv("LYZR_ENDPOINT")


@traceable(
    name="cu_member_agent",
    project_name="CU-MEMBER-AGENT-EVAL"
)
def run_cu_agent(inputs: dict) -> dict:
    question = inputs["question"]

    start = time.time()

    response = requests.post(
        LYZR_ENDPOINT,
        headers={
            "Content-Type": "application/json",
            "x-api-key": LYZR_API_KEY,
        },
        json={
            "user_id": "week4_eval_user",
            "agent_id": LYZR_AGENT_ID,
            "session_id": str(uuid.uuid4()),
            "message": question,
        },
        timeout=60,
    )

    latency = time.time() - start

    response.raise_for_status()
    data = response.json()

    return {
        "answer": data,
        "latency_seconds": latency,
    }


if __name__ == "__main__":
    result = run_cu_agent({
        "question": "Who can join Penny Post Credit Union?"
    })

    print(result)
