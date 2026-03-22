# LLM-as-a-Judge Local Test

I wrote this script just to figure out how the "LLM-as-a-judge" concept works under the hood. It's a quick local demo based on the paper [Judging LLM-as-a-judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685).

It uses Gemini to generate answers to some hardcoded questions, and then uses a second prompt to grade those answers on a scale of 1 to 5 for tone and relevance. 

## Setup

You just need the GenAI SDK and Pydantic:

```bash
pip install google-genai pydantic
```

## Running it

Before running the script, make sure your API key is exported in your terminal so the SDK can pick it up automatically:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

Then, execute the file:

Bash
python eval.py