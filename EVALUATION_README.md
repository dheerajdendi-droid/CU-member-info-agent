# Credit Union Member Agent: Evaluation Overview

## What I was trying to do

I wanted to test whether the Week 3 Credit Union RAG assistant was accurate, relevant, safe, and responsive enough for a public-information-only use case.

The aim was not simply to show that the agent could answer easy questions. I wanted to establish whether it would stay grounded in approved Penny Post Credit Union website content, respect financial-services boundaries, handle ambiguous questions cautiously, resist adversarial instructions, and direct people to the Credit Union when it could not confirm an answer.

This evaluation was also intended to separate failures in the agent from failures in the evaluation method. Automated scores are useful, but a keyword rule or an under-calibrated LLM judge can mark a good response as wrong—or miss a genuine issue. Human review was therefore part of interpreting the results.

## System under test

The assistant was built in Lyzr Agent Studio and uses RAG over public Penny Post Credit Union content. Its intended scope covers:

- membership eligibility and joining;
- published loans, savings products, APRs, and rates;
- application guidance, general services, and contact information.

It is not intended to access member records, balances, transactions, or application status. It must not make credit decisions or provide personalised financial advice.

## Evaluation design

I created a 40-case golden dataset in LangSmith:

| Category | Cases | Purpose |
| --- | ---: | --- |
| Happy path | 20 | Check ordinary public-information answers. |
| Edge cases | 12 | Check ambiguity, uncertainty, and boundary handling. |
| Known/difficult | 6 | Re-test previously challenging behaviours. |
| Adversarial | 2 | Test prompt injection, private-data requests, and scope control. |

Each case defines the expected behaviour and reference facts, whether refusal or escalation is required, and content that must not appear.

The Python harness sends each question to the deployed Lyzr agent in a fresh session and records the output and latency. The full dataset was assessed with deterministic checks for guardrail compliance, escalation, prohibited content, and latency. A representative 10-case subset used OpenAI LLM-as-judge checks for answer relevance and faithfulness because of provider rate limits. Human spot-checking was used to calibrate the automated findings.

## Results from the final report

| Measure | Observed result | Interpretation |
| --- | ---: | --- |
| Full execution | 40/40 completed | Stable API execution. |
| Guardrail compliance | About 72% | Keyword-based scoring needs cautious interpretation. |
| Escalation accuracy | About 92% | Generally strong. |
| Latency under 8 seconds, latest full run | About 92% | Usable but variable. |
| Answer relevance, 10-case subset | 100% | Responses stayed on topic. |
| Faithfulness judge, 10-case subset | 20% | Materially under-calibrated; human review found false negatives. |
| Prohibited-content compliance, 10-case subset | 100% | No prohibited content detected in final answers. |
| Latency under 8 seconds, 10-case subset | 80% | Acceptable for a prototype, with room to optimise. |

The low automated faithfulness score should not be read as an 80% factual-failure rate. The final report documents false negatives from the judge, including a response that correctly refused to predict a member's personal rate and accurately stated the published APR range.

## What the evaluation found

One genuine faithfulness problem involved former Royal Mail employees. The agent inferred eligibility from related wording even though the public common bond did not clearly confirm that former employment alone qualified. The safer behaviour is to say that eligibility cannot be confirmed and direct the person to Penny Post.

The evaluation process itself also produced misleading results. An earlier prohibited-content check scanned the complete RAG payload rather than only the final user-facing response, so prohibited phrases in retrieved reference material caused false positives. That evaluator was corrected. The LLM faithfulness judge also needs better calibration against examples of acceptable cautious refusals.

Retrieval quality is another improvement area. Source pages can contain cookie notices, banners, and loosely related content. Responses were often still good, but cleaner ingestion should reduce noise and may improve latency.

## Priority improvements

1. Tighten the eligibility instruction so the agent never treats related but non-equivalent information as proof.
2. Limit answers to retrieved facts that directly address the current question.
3. Keep refusals concise and provide only a relevant next step.
4. Remove boilerplate-heavy or redundant knowledge-base sources.
5. Calibrate automated evaluators with human-reviewed pass and fail examples.
6. Business-validate high-value public answers and rerun a focused regression suite.

## Deployment conclusion

The issues found are targeted rather than architectural. The assistant is not ready for an unrestricted public production launch, but the report assesses it as suitable for a controlled pilot or limited beta after the eligibility rule is tightened, key answers are validated, and regression tests pass.

The proposed Day 1 scope should remain public information only, with clear escalation to existing Credit Union support channels. Any future authenticated member-data functionality should be treated as a separate phase with dedicated security, privacy, permissions, audit, vendor-governance, and human-escalation controls.

## Data and secret handling

This repository contains public reference information and synthetic evaluation cases only. It does not contain live member records or credential values. Runtime credentials are loaded from local environment variables and `.env` files are excluded from version control.
