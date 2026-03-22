from google import genai
import json
import time
import csv
from pydantic import BaseModel, Field


class EvaluationScore(BaseModel):
    tone: int = Field(description="Score from 1 to 5 grading the tone of the response.")
    relevance: int = Field(description="Score from 1 to 5 grading how relevant the response is to the question.")

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client()

doc_data = {
  "doc_title": "ChronoSync App Strategy",
  "author": "Engineering Lead",
  "updated": "2026-03-25",
  "objective": "Release the MVP of the ChronoSync time-tracking application using a unified codebase.",
  "tech_stack": "Kotlin Multiplatform (KMP), SQLite",
  "target_audience": "Freelancers and contractors",
  "milestones": [
    {"phase": "Architecture", "date": "April 10"},
    {"phase": "Core Logic", "date": "May 15"},
    {"phase": "UI Integration", "date": "June 1"}
  ],
  "budget": {"dev": 15000, "cloud": 2000, "marketing": 3000}
}

questions = [
  "What is the main objective of the ChronoSync project?",
  "Who is the stated author of this document?",
  "What specific technology stack is being used for the app?",
  "When was this document last updated?",
  "What is the deadline for the UI Integration phase?",
  "How much of the budget is allocated specifically to cloud infrastructure?",
  "Who is the target audience for this application?",
  "If you add up all the categories, what is the total budget?",
  "When is the Architecture phase scheduled to be completed?",
  "Based on the budget, which area is getting the most funding?"
]

responses = []

for question in questions:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview", contents="Document: " + json.dumps(doc_data) + "\n\nQuestion: " + question
    )

    responses.append(response.text)
    print("Finished a response")
    time.sleep(5)


csv_data = []


for i,response in enumerate(responses):
    content = f"Document: {json.dumps(doc_data)}\n\nQuestion: {questions[i]}\nThe response from an assistant is: {response}\nGrade it on a scale of 1 to 5."    
    gemini_response = client.models.generate_content(
        model="gemini-3.1-flash-lite-preview", contents= content,
        config= {
            "response_mime_type": "application/json",
            "response_json_schema": EvaluationScore.model_json_schema(),
        }
    )

    scores = EvaluationScore.model_validate_json(gemini_response.text)

    csv_data.append({
        "Question": questions[i],
        "Response": response,
        "Tone_score": scores.tone,
        "Relevance_score": scores.relevance
    })

    print(f"Evaluated: Tone={scores.tone}, Relevance={scores.relevance}")
    time.sleep(5)


csv_filename = "eval_results.csv"

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:

    fieldnames = ["Question", "Response", "Tone_score", "Relevance_score"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(csv_data)

print(f"Success, saved to {csv_filename}")