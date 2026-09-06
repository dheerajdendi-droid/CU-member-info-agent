# Credit Union Member Information Agent

A proof-of-concept retrieval-augmented generation (RAG) assistant for Penny Post Credit Union public information.

The project explores whether a conversational assistant can make published information about membership, loans, savings, rates, and applications easier to find while maintaining clear financial-services boundaries. It was built as a GenAI course project around a real Credit Union use case.

## What the agent does

- Answers general questions from approved, publicly available Credit Union website content.
- Uses retrieval to ground responses instead of relying on unsupported model knowledge.
- Refuses requests for personalised financial advice or individual credit decisions.
- Does not access balances, transactions, applications, accounts, or other member records.
- Escalates to the Credit Union when public information cannot support a reliable answer.

## Architecture

```text
User question
    |
    v
Lyzr Agent Studio
    |
    v
RAG retrieval -> Qdrant vector store -> approved public website content
    |
    v
Grounded, member-friendly response
```

The prototype uses Lyzr Agent Studio, an OpenAI model, Qdrant-backed retrieval, and Penny Post Credit Union public webpages. The evaluation harness calls the deployed agent and records results in LangSmith.

## Repository contents

| File | Purpose |
| --- | --- |
| `eval_runner.py` | Calls the deployed Lyzr agent with an isolated session and captures latency. |
| `evaluators.py` | Rule-based and LLM-as-judge evaluators for safety, escalation, relevance, faithfulness, and latency. |
| `run_eval.py` | Runs the representative 10-case LangSmith evaluation. |
| `cu_member_agent_golden_v1.csv` | Full 40-case golden evaluation dataset. |
| `cu_member_agent_golden_v2 _judge_10.csv` | Representative 10-case dataset for LLM judging under provider rate limits. |
| `CU_Member_Agent_Week4_Final_Evaluation_Report.docx` | Final evaluation report and deployment assessment. |
| `Credit_Union_Member_Information_Agent_Project_Documentation.docx` | Project scope, architecture, safety controls, and rollout proposal. |
| `EVALUATION_README.md` | Plain-language explanation of the evaluation goal, method, results, and lessons. |

## Evaluation coverage

The golden dataset contains happy-path, edge-case, known/difficult, and adversarial prompts. It tests factual public-information answers as well as boundaries around:

- ambiguous eligibility;
- personalised product or pricing recommendations;
- credit approval predictions;
- private member and application data;
- prompt injection and unrelated requests;
- unsupported facts, escalation, and response latency.

The datasets contain test questions and public reference facts only. The account reference used in a refusal test is an explicit synthetic placeholder and is not associated with a real member.

See [EVALUATION_README.md](EVALUATION_README.md) for the findings and their interpretation.

## Running the evaluation

1. Create and activate a Python virtual environment.
2. Install dependencies:

   ```bash
   pip install -r Requirements.txt
   ```

3. Set the required credentials and deployment configuration in a local `.env` file: `OPENAI_API_KEY`, `LANGSMITH_API_KEY`, `LYZR_API_KEY`, `LYZR_AGENT_ID`, and `LYZR_ENDPOINT`. Optionally set `JUDGE_MODEL`; it defaults to `gpt-5`.
4. Run:

   ```bash
   python run_eval.py
   ```

The `.env` file and generated Python cache files are ignored by Git. Do not commit credentials, exported production traces, or member information.

## Current status

The final evaluation supports a controlled pilot after targeted improvements, not an unrestricted production launch. Core Q&A, relevance, escalation, and personal-data boundaries were strong. The main remaining work is tightening ambiguous eligibility handling, cleaning retrieval sources, calibrating automated judges, validating high-value answers with business owners, and rerunning focused regression tests.

Authenticated member servicing is intentionally outside the MVP and would require a separate security, privacy, permissions, audit, vendor-governance, and human-escalation workstream.
