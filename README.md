# AI Lead Processing System (KeaBuilder)

## Overview
This project demonstrates an AI-powered lead processing system:
- Classifies leads into hot/warm/cold
- Generates personalized responses
- Handles incomplete inputs

## Architecture
Form Input → LLM Classification → LLM Response → JSON Output

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload