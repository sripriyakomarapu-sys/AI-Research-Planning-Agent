import os
import json
import streamlit as st


# ============================================================
# LOAD GROQ API KEY FROM STREAMLIT CLOUD SECRETS
# ============================================================

try:
    if "GROQ_API_KEY" in st.secrets:
        os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
except Exception:
    pass


# Import project modules AFTER loading the secret
from planner import generate_ai_plan, fallback_plan
from validator import validate_plan, refine_plan


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Research Planning Agent",
    page_icon="🔬",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🔬 AI Research Planning Agent")

st.write(
    "Convert a broad research objective into a structured, "
    "validated and executable research plan."
)

st.caption(
    "Powered by Groq Cloud AI • Planning + Validation + Refinement"
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.header("Research Configuration")


objective = st.sidebar.text_area(
    "Research Topic / Objective",
    placeholder=(
        "Example: Understand the Indian electric two-wheeler "
        "market from 2020-2026."
    ),
    height=120
)


audience = st.sidebar.text_input(
    "Target Audience",
    value="Management"
)


geography = st.sidebar.text_input(
    "Geographic Scope",
    value="India"
)


time_period = st.sidebar.text_input(
    "Time Period",
    value="2020-2026"
)


depth = st.sidebar.selectbox(
    "Desired Depth",
    [
        "Quick overview",
        "Moderate",
        "Detailed",
        "Deep research"
    ]
)


output_format = st.sidebar.selectbox(
    "Output Format",
    [
        "Research report",
        "Management briefing",
        "Presentation",
        "Academic report"
    ]
)


current_historical = st.sidebar.selectbox(
    "Information Requirement",
    [
        "Current information",
        "Historical information",
        "Current + historical"
    ]
)


sources = st.sidebar.text_input(
    "Preferred / Restricted Source Types",
    value=(
        "Government reports, academic papers, "
        "industry reports, company websites"
    )
)


constraints = st.sidebar.text_area(
    "Additional Constraints",
    placeholder="Example: Avoid unsupported claims."
)


# ---------------------------------------------------------
# SAMPLE SCENARIOS
# ---------------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.header("Quick Scenarios")


scenario = st.sidebar.selectbox(
    "Choose a Scenario",
    [
        "Custom",
        "Indian Electric Two-Wheeler Market",
        "AI in Healthcare",
        "Online Education Market"
    ]
)


if scenario == "Indian Electric Two-Wheeler Market":

    objective = (
        "Understand the Indian electric two-wheeler market "
        "from 2020-2026 for a management audience. "
        "Focus on market growth, competitors, government "
        "policy, consumer adoption and challenges."
    )

    audience = "Management"
    geography = "India"
    time_period = "2020-2026"


elif scenario == "AI in Healthcare":

    objective = (
        "Analyze the adoption of artificial intelligence "
        "in healthcare, including applications, benefits, "
        "risks, regulations and future trends."
    )

    audience = "Healthcare management"
    geography = "Global"
    time_period = "2020-2026"


elif scenario == "Online Education Market":

    objective = (
        "Study the growth of online education platforms, "
        "major competitors, consumer behavior, technology "
        "trends and challenges."
    )

    audience = "Business strategy team"
    geography = "Global"
    time_period = "2020-2026"


# ---------------------------------------------------------
# GENERATE PLAN
# ---------------------------------------------------------

if st.button(
    "🚀 Generate Research Plan",
    type="primary",
    use_container_width=True
):

    if not objective.strip():

        st.error(
            "Please enter a research objective."
        )

        st.stop()


    data = {
        "objective": objective,
        "audience": audience,
        "geography": geography,
        "time_period": time_period,
        "depth": depth,
        "output_format": output_format,
        "current_historical": current_historical,
        "sources": sources,
        "constraints": constraints
    }


    # -----------------------------------------------------
    # AI PLANNING
    # -----------------------------------------------------

    with st.spinner(
        "🤖 AI is decomposing the research objective..."
    ):

        plan = generate_ai_plan(data)


    # -----------------------------------------------------
    # ERROR HANDLING
    # -----------------------------------------------------

    if "error" in plan:

        st.warning(
            "Groq API could not generate the plan."
        )

        st.error(
            plan["error"]
        )

        st.info(
            "Using the built-in fallback planning logic "
            "so the application can continue running."
        )

        plan = fallback_plan(data)


    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    validation = validate_plan(
        plan,
        objective
    )


    st.subheader("✅ Plan Validation")


    if validation["status"] == "PASS":

        st.success(
            "VALIDATION PASSED — "
            "The research plan covers the required components."
        )

    else:

        st.warning(
            "Validation detected missing components."
        )

        st.write(
            "**Missing areas:**"
        )

        for item in validation["missing_areas"]:

            st.write(
                f"- {item}"
            )


        plan = refine_plan(
            plan,
            validation
        )


        st.info(
            "🔄 Plan automatically refined after validation."
        )


    # -----------------------------------------------------
    # RESEARCH OBJECTIVE
    # -----------------------------------------------------

    st.subheader("🎯 Research Objective")

    st.info(
        plan["research_objective"]
    )


    # -----------------------------------------------------
    # RESEARCH QUESTIONS
    # -----------------------------------------------------

    st.subheader(
        "❓ Research Questions / Tasks"
    )


    for task in plan["research_questions"]:

        with st.expander(
            f"{task['id']} — {task['question']}"
        ):

            col1, col2 = st.columns(2)


            with col1:

                st.markdown(
                    "**Information Required**"
                )

                for item in task[
                    "information_required"
                ]:

                    st.write(
                        f"• {item}"
                    )


                st.markdown(
                    "**Suggested Source / Tool Types**"
                )

                for source in task[
                    "source_types"
                ]:

                    st.write(
                        f"• {source}"
                    )


            with col2:

                st.markdown(
                    "**Dependencies**"
                )

                dependencies = task[
                    "depends_on"
                ]


                if dependencies:

                    st.write(
                        ", ".join(dependencies)
                    )

                else:

                    st.write(
                        "None"
                    )


                st.markdown(
                    "**Parallelizable**"
                )

                if task["parallelizable"]:

                    st.success("Yes")

                else:

                    st.info("No")


                st.markdown(
                    "**Expected Result**"
                )

                st.write(
                    task["expected_result"]
                )


    # -----------------------------------------------------
    # TASK SEQUENCE
    # -----------------------------------------------------

    st.subheader(
        "🔢 Task Execution Sequence"
    )


    for index, task_id in enumerate(
        plan["task_sequence"],
        start=1
    ):

        st.write(
            f"**Step {index} → {task_id}**"
        )


    # -----------------------------------------------------
    # DEPENDENCIES
    # -----------------------------------------------------

    st.subheader(
        "🔗 Dependencies"
    )


    if plan["dependencies"]:

        for dependency in plan["dependencies"]:

            depends_on = dependency.get(
                "depends_on",
                []
            )

            st.write(
                f"**{dependency['task']}** "
                f"depends on "
                f"**{', '.join(depends_on)}**"
            )

            st.caption(
                dependency.get(
                    "reason",
                    ""
                )
            )

    else:

        st.write(
            "No explicit dependencies."
        )


    # -----------------------------------------------------
    # PARALLEL TASKS
    # -----------------------------------------------------

    st.subheader(
        "⚡ Parallelizable Tasks"
    )


    if plan["parallel_tasks"]:

        for group in plan[
            "parallel_tasks"
        ]:

            st.success(
                "Can run in parallel: "
                + " + ".join(group)
            )

    else:

        st.write(
            "No parallel tasks identified."
        )


    # -----------------------------------------------------
    # SYNTHESIS
    # -----------------------------------------------------

    st.subheader(
        "🧩 Final Synthesis"
    )


    synthesis = plan[
        "synthesis_task"
    ]


    st.write(
        f"**{synthesis['id']} — "
        f"{synthesis['description']}**"
    )


    st.write(
        "**Depends on:** "
        + ", ".join(
            synthesis["depends_on"]
        )
    )


    st.write(
        "**Expected Result:** "
        + synthesis["expected_result"]
    )


    # -----------------------------------------------------
    # COVERAGE VALIDATION
    # -----------------------------------------------------

    st.subheader(
        "🔍 Coverage Validation"
    )


    validation_data = plan[
        "validation"
    ]


    status = validation_data.get(
        "status",
        "UNKNOWN"
    )


    st.write(
        f"**Status:** {status}"
    )


    st.write(
        "**Coverage:** "
        + validation_data.get(
            "coverage",
            "Not available"
        )
    )


    missing = validation_data.get(
        "missing_areas",
        []
    )


    if missing:

        st.warning(
            "Missing Areas: "
            + ", ".join(missing)
        )

    else:

        st.success(
            "No critical research areas are missing."
        )


    # -----------------------------------------------------
    # FINAL RESEARCH STRUCTURE
    # -----------------------------------------------------

    st.subheader(
        "📑 Final Research Structure"
    )


    for section in plan[
        "final_research_structure"
    ]:

        st.write(
            f"• {section}"
        )


    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    st.subheader(
        "💾 Export Plan"
    )


    json_data = json.dumps(
        plan,
        indent=4
    )


    st.download_button(
        label="Download Research Plan JSON",
        data=json_data,
        file_name="research_plan.json",
        mime="application/json",
        use_container_width=True
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")

st.caption(
    "AI Research Planning Agent • "
    "Goal Definition → Task Decomposition → "
    "Planning → Validation → Refinement"
)