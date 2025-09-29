import openai
from scipaper.config import settings
import json

client = openai.AsyncOpenAI(api_key=settings.openai_api_key)

async def analyze_paper(title: str, abstract: str) -> dict:
    """Analyzes a paper's title and abstract using GPT-4 to extract structured data."""
    prompt = f"""
    Analyze the following scientific paper and extract the specified information in JSON format.

    **Title:** {title}
    **Abstract:** {abstract}

    **Instructions:**
    Based on the abstract and title, provide a structured analysis covering the following points.
    If a section cannot be determined from the text, use an empty list or a null value.

    **JSON Output Structure:**
    {{
        "findings": ["List of key findings and results."],
        "methods": ["List of methodologies, techniques, or approaches used."],
        "datasets": ["List of datasets used or created."],
        "gaps": ["List of identified research gaps or open questions."],
        "limitations": ["List of the study's limitations."],
        "suggested_experiments": ["List of potential future experiments or research directions."]
    }}
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert scientific research assistant. Your goal is to provide structured analysis of academic papers in JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            timeout=300  # 5-minute timeout as per requirements
        )
        analysis_content = response.choices[0].message.content
        return json.loads(analysis_content)
    except Exception as e:
        # In a real application, you'd have more robust logging and error handling
        print(f"An error occurred during OpenAI API call: {e}")
        raise
