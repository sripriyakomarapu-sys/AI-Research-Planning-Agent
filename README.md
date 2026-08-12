# AI Research Planning Agent

## Overview

The AI Research Planning Agent converts a broad research objective into a structured and executable research plan.

The system focuses on research planning rather than directly generating a research report.

It identifies:

- Research questions
- Information requirements
- Task sequence
- Dependencies
- Parallel tasks
- Source/tool types
- Expected results
- Synthesis requirements
- Coverage validation
- Plan refinement

## Architecture

User
↓
Research Objective
↓
AI Planning Agent
↓
Task Decomposition
↓
Information Requirements
↓
Source/Tool Classification
↓
Dependency Analysis
↓
Parallel Task Identification
↓
Validation
↓
Refinement
↓
Final Research Plan

## Technology Stack

- Python
- Streamlit
- Groq API
- Llama 3.1 8B Instant
- JSON

## Why Groq?

The project uses Groq Cloud instead of a locally hosted LLM.

This reduces the processing load on the user's computer and provides fast AI inference through a cloud API.

## Planning Logic

### 1. Goal Definition

The user provides a broad research objective together with audience, geographic scope, time period, depth and constraints.

### 2. Task Decomposition

The AI breaks the objective into meaningful research questions.

### 3. Information Requirements

Each task identifies the information required to answer the research question.

### 4. Source Selection

The AI recommends suitable source categories such as:

- Government reports
- Academic papers
- Industry reports
- Company websites
- News sources
- Market research

### 5. Dependency Analysis

The system identifies which tasks depend on earlier tasks.

### 6. Parallelization

Independent research tasks are identified as parallelizable.

### 7. Synthesis

A final synthesis task is created to combine the outputs of the research tasks.

### 8. Validation

The validation module checks whether the plan contains:

- Research objective
- Research questions
- Task sequence
- Dependencies
- Parallel tasks
- Synthesis
- Final research structure

### 9. Refinement

If validation finds missing components, the system automatically adds the missing components and produces a refined plan.

## Test Scenarios

### Scenario 1

Indian electric two-wheeler market from 2020-2026.

Focus:

- Market growth
- Competitors
- Government policy
- Consumer adoption
- Challenges

### Scenario 2

AI in healthcare.

Focus:

- Applications
- Benefits
- Risks
- Regulations
- Ethics
- Future trends

### Scenario 3

Online education market.

Focus:

- Market growth
- Competitors
- Consumer behavior
- Technology trends
- Challenges

## Incomplete Plan Testing

### Case 1

Initial plan:

- Market overview
- Competitor analysis
- Synthesis

Missing:

- Government policy
- Consumer adoption
- Industry challenges

Validation detects the missing areas and refinement adds them.

### Case 2

Initial plan:

- AI applications
- Benefits
- Synthesis

Missing:

- Risks
- Regulations
- Ethical considerations
- Future trends

Validation detects the missing areas and refinement adds them.

## Limitations

- The system plans research but does not perform complete research.
- Recommended source types are categories, not verified sources.
- AI output depends on the selected language model.
- Internet access is required for Groq API.
- API availability can affect AI generation.
- Validation checks structural coverage but does not verify factual correctness.

## Future Enhancements

- Web search integration
- Automatic source collection
- Citation verification
- Research execution agents
- Research progress tracking
- Vector databases
- Automatic report generation
- Multi-agent research workflows

## Conclusion

The AI Research Planning Agent demonstrates agentic planning by converting broad goals into smaller tasks, identifying dependencies and parallel work, validating coverage and refining incomplete plans.

The system separates research planning from research execution and produces an executable research structure.