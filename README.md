# Credit Union Member Information Agent

A GenAI/RAG agent built using Lyzr Agent Studio.

## Problem
Credit Union members frequently need to find information about
membership, savings, loans and application processes.

## Solution
An AI agent retrieves information from the publicly available
Credit Union website and provides grounded conversational answers.

## Architecture

User
 ↓
Lyzr Agent
 ↓
RAG Retrieval
 ↓
Qdrant Vector Store
 ↓
Penny Post Credit Union Public Website

## Scope

- Public information only
- No member account access
- No personalised financial advice
- No credit decisions
- No transactions

## Model
OpenAI GPT-5.4-mini

## Knowledge Base
Public Penny Post Credit Union website pages

## Safety Controls
- Scope restriction
- No personalised financial advice
- No personal account access
- No hallucination of unsupported CU information
- Human escalation where information cannot be confirmed

## Test Examples

1. Who can join Penny Post Credit Union?
2. What personal loans are available?
3. How do I apply for a loan?
4. Should I take out a £10,000 loan?
5. Can you check my loan application status?
