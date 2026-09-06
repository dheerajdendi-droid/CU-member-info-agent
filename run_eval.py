from langsmith import Client

from eval_runner import run_cu_agent

from evaluators import (
    guardrail_evaluator,
    escalation_evaluator,
    prohibited_content_evaluator,
    latency_evaluator,
    answer_relevance_evaluator,
    faithfulness_evaluator,
)

client = Client()

results = client.evaluate(
    run_cu_agent,

    # Your 10-case LLM judge dataset
    data="cu_member_agent_golden_v2 _judge_10",

    evaluators=[
        guardrail_evaluator,
        escalation_evaluator,
        prohibited_content_evaluator,
        latency_evaluator,
        answer_relevance_evaluator,
        faithfulness_evaluator,
    ],

    experiment_prefix="baseline-llm-judge-10",

    # VERY IMPORTANT:
    # Prevent LangSmith firing several OpenAI judge requests in parallel.
    max_concurrency=1,
)

print(results)