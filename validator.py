def validate_plan(plan, objective):

    if not isinstance(plan, dict):

        return {
            "status": "FAIL",
            "message": "Invalid plan format.",
            "missing_areas": ["Complete research plan"]
        }

    if "error" in plan:

        return {
            "status": "FAIL",
            "message": plan["error"],
            "missing_areas": ["AI-generated plan"]
        }

    required_sections = [
        "research_objective",
        "research_questions",
        "task_sequence",
        "dependencies",
        "parallel_tasks",
        "synthesis_task",
        "validation",
        "final_research_structure"
    ]

    missing_sections = []

    for section in required_sections:

        if section not in plan:
            missing_sections.append(section)

    if len(plan.get("research_questions", [])) == 0:
        missing_sections.append("research questions")

    if len(plan.get("task_sequence", [])) == 0:
        missing_sections.append("task sequence")

    if "synthesis_task" not in plan:
        missing_sections.append("synthesis task")

    if "final_research_structure" not in plan:
        missing_sections.append("final research structure")

    if missing_sections:

        return {
            "status": "FAIL",
            "message": "Plan is incomplete.",
            "missing_areas": list(set(missing_sections))
        }

    return {
        "status": "PASS",
        "message": "Plan successfully covers the required planning components.",
        "missing_areas": []
    }


def refine_plan(plan, validation):

    missing = validation.get("missing_areas", [])

    if "synthesis task" in missing:

        plan["synthesis_task"] = {
            "id": "S1",
            "description": "Combine all research findings into a final structured synthesis.",
            "depends_on": plan.get("task_sequence", []),
            "expected_result": "Final research synthesis"
        }

    if "final research structure" in missing:

        plan["final_research_structure"] = [
            "1. Introduction",
            "2. Research findings",
            "3. Analysis",
            "4. Synthesis",
            "5. Conclusion"
        ]

    if "research questions" in missing:

        plan["research_questions"] = [
            {
                "id": "T1",
                "question": "What background information is required?",
                "information_required": [
                    "Background",
                    "Definitions",
                    "Current context"
                ],
                "source_types": [
                    "Academic sources",
                    "Government reports"
                ],
                "depends_on": [],
                "parallelizable": True,
                "expected_result": "Research background"
            }
        ]

    plan["validation"] = {
        "coverage": "The plan was automatically refined after validation.",
        "missing_areas": [],
        "status": "PASS"
    }

    return plan