from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import json
import re
import os

from prompts import CLASSIFICATION_PROMPT, RESPONSE_PROMPT

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
app = FastAPI()


class LeadInput(BaseModel):
    name: str | None = None
    email: str | None = None
    budget: str | None = None
    message: str | None = None


def call_llm(prompt):
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)

        if not response or not response.text:
            return "Error: Empty response from model"

        return response.text

    except Exception as e:
        return f"Error: {str(e)}"



def extract_json(text):
    try:
        # Remove markdown/code blocks if present
        text = text.strip()
        text = re.sub(r"```json|```", "", text)

        # Extract JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            clean_json = match.group()

            # Fix common issues
            clean_json = clean_json.replace("\n", "").replace("\t", "")

            return json.loads(clean_json)

    except Exception as e:
        print("JSON parsing error:", e)
        print("RAW TEXT:", text)

    return {
        "lead_type": "unknown",
        "reason": "Parsing failed"
    }


def classify_lead(lead_data):
    prompt = CLASSIFICATION_PROMPT.format(lead_data=lead_data)
    result = call_llm(prompt)

    print("\nRAW CLASSIFICATION:", result)

    return extract_json(result)


def generate_response(lead_data, lead_type):
    prompt = RESPONSE_PROMPT.format(
        lead_data=lead_data,
        lead_type=lead_type
    )

    result = call_llm(prompt)

    print("\n💬 RESPONSE RESULT:\n", result)

    if result.startswith("Error"):
        return "Sorry, something went wrong."

    return result.strip()

@app.get("/test")
def test():
    return call_llm("Say hello")


@app.post("/process-lead")
def process_lead(lead: LeadInput):
    try:
        lead_dict = lead.dict()

        if not lead_dict.get("message"):
            return {
                "error": "Insufficient data",
                "message": "Please provide more details."
            }

        classification = classify_lead(lead_dict)

        response = generate_response(
            lead_dict,
            classification.get("lead_type")
        )

        return {
            "input": lead_dict,
            "classification": classification,
            "response": response
        }

    except Exception as e:
        print("🔥 FULL ERROR:", e)
        return {
            "error": "Internal failure",
            "details": str(e)
        }