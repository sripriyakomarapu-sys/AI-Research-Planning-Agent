import json
import os

import streamlit as st
from groq import Groq


MODEL = "llama-3.1-8b-instant"


# ============================================================
# GET GROQ API KEY
# ============================================================

def get_groq_api_key():
    """
    Get the Groq API key.

    Works both:
    1. Locally using environment variable
    2. On Streamlit Cloud using st.secrets
    """

    # Local environment variable
    api_key = os.getenv("GROQ_API_KEY")

    # Streamlit Cloud secrets
    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = None

    return api_key


# ============================================================
# GENERATE AI RESEARCH PLAN
# ============================================================

def generate_ai_plan(data):

    api_key = get_groq_api_key()

    if not api_key:
        return {
            "error": "GROQ_API_KEY is not configured."
        }

    try:

        client = Groq(api_key=api_key)

        prompt = f"""
You are an AI Research Planning Agent.

Your task is to PLAN research, NOT perform the research.

Convert the following broad research objective into a concise,
logical and executable research plan.

RESEARCH OBJECTIVE:
{data['objective']}

TARGET AUDIENCE:
{data['audience']}

GEOGRAPHIC SCOPE:
{data['geography']}

TIME PERIOD:
{data['time_period']}

DESIRED DEPTH:
{data['depth']}

OUTPUT FORMAT:
{data['output_format']}

CURRENT OR HISTORICAL REQUIREMENT:
{data['current_historical']}

PREFERRED / RESTRICTED SOURCE TYPES:
{data['sources']}

ADDITIONAL CONSTRAINTS:
{data['constraints']}


PLANNING REQUIREMENTS:

1. Break the objective into meaningful research questions.
2. Avoid unnecessary research tasks.
3. Identify information required for every task.
4. Recommend appropriate source types or tools.
5. Identify dependencies between tasks.
6. Identify tasks that can be performed in parallel.
7. Define the expected result of every task.
8. Separate evidence-gathering tasks from synthesis.
9. Create a final synthesis task.
10. Check that every important part of the original objective is covered.
11. Consider whether current information is required.
12. Keep the final plan concise enough to execute.


Return ONLY valid JSON.

Use EXACTLY this structure:

{{
    "research_objective": "...",

    "research_questions": [
        {{
            "id": "T1",
            "question": "...",
            "information_required": [
                "...",
                "..."
            ],
            "source_types": [
                "...",
                "..."
            ],
            "depends_on": [],
            "parallelizable": true,
            "expected_result": "..."
        }}
    ],

    "task_sequence": [
        "T1",
        "T2"
    ],

    "dependencies": [
        {{
            "task": "T2",
            "depends_on": [
                "T1"
            ],
            "reason": "..."
        }}
    ],

    "parallel_tasks": [
        [
            "T1",
            "T2"
        ]
    ],

    "synthesis_task": {{
        "id": "S1",
        "description": "...",
        "depends_on": [
            "T1",
            "T2"
        ],
        "expected_result": "..."
    }},

    "validation": {{
        "coverage": "...",
        "missing_areas": [],
        "status": "PASS"
    }},

    "final_research_structure": [
        "...",
        "..."
    ]
}}
"""

        # ====================================================
        # CALL GROQ
        # ====================================================

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert research planning specialist. "
                        "Return ONLY valid JSON. "
                        "Do not include markdown or explanations outside JSON."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=3500
        )

        result = response.choices[0].message.content

        # ====================================================
        # CLEAN RESPONSE
        # ====================================================

        result = result.strip()

        if result.startswith("```json"):
            result = result[7:]

        elif result.startswith("```"):
            result = result[3:]

        if result.endswith("```"):
            result = result[:-3]

        result = result.strip()

        # ====================================================
        # CONVERT JSON STRING TO PYTHON DICTIONARY
        # ====================================================

        return json.loads(result)

    except Exception as e:

        return {
            "error": str(e)
        }


# ============================================================
# FALLBACK PLAN
# ============================================================

def fallback_plan(data):

    objective = data["objective"]

    return {

        "research_objective": objective,

        "research_questions": [

            {
                "id": "T1",

                "question":
                    "What is the background and current context of the research topic?",

                "information_required": [
                    "Background",
                    "Definitions",
                    "Current context",
                    "Historical context"
                ],

                "source_types": [
                    "Government reports",
                    "Academic papers",
                    "Industry reports"
                ],

                "depends_on": [],

                "parallelizable": True,

                "expected_result":
                    "Background and context of the topic"
            },

            {
                "id": "T2",

                "question":
                    "Who are the major stakeholders, organizations or competitors?",

                "information_required": [
                    "Major organizations",
                    "Stakeholders",
                    "Competitors",
                    "Market participants"
                ],

                "source_types": [
                    "Company websites",
                    "Industry reports",
                    "Market research"
                ],

                "depends_on": [],

                "parallelizable": True,

                "expected_result":
                    "Stakeholder and competitor landscape"
            },

            {
                "id": "T3",

                "question":
                    "What are the major trends, opportunities and challenges?",

                "information_required": [
                    "Major trends",
                    "Opportunities",
                    "Risks",
                    "Challenges"
                ],

                "source_types": [
                    "Research reports",
                    "News sources",
                    "Academic publications"
                ],

                "depends_on": [
                    "T1"
                ],

                "parallelizable": False,

                "expected_result":
                    "Trend, opportunity and challenge analysis"
            }
        ],

        "task_sequence": [
            "T1",
            "T2",
            "T3",
            "S1"
        ],

        "dependencies": [

            {
                "task": "T3",

                "depends_on": [
                    "T1"
                ],

                "reason":
                    "Trend analysis requires background context."
            },

            {
                "task": "S1",

                "depends_on": [
                    "T1",
                    "T2",
                    "T3"
                ],

                "reason":
                    "Synthesis requires outputs from research tasks."
            }
        ],

        "parallel_tasks": [
            [
                "T1",
                "T2"
            ]
        ],

        "synthesis_task": {

            "id": "S1",

            "description":
                "Combine the findings from all research tasks into a final structured synthesis.",

            "depends_on": [
                "T1",
                "T2",
                "T3"
            ],

            "expected_result":
                "Final research synthesis"
        },

        "validation": {

            "coverage":
                "The plan covers background, stakeholders, trends, challenges and synthesis.",

            "missing_areas": [],

            "status": "PASS"
        },

        "final_research_structure": [

            "1. Introduction and background",

            "2. Current landscape",

            "3. Stakeholder or competitor analysis",

            "4. Trends and opportunities",

            "5. Challenges and risks",

            "6. Final synthesis and conclusion"
        ]
    }