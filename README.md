# AI Lead Processing System (KeaBuilder)

## Overview
This project demonstrates an AI-powered lead processing system:
- Classifies leads into hot/warm/cold
- Generates personalized responses
- Handles incomplete inputs


**Link to Loom Video**
loom.com/share/5c03de8e414f44c7805cf17c707f4b09


## Architecture
Form Input → LLM Classification → LLM Response → JSON Output

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app:app --reload