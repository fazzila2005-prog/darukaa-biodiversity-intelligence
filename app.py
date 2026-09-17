import streamlit as st
from dotenv import load_dotenv
import os
import json

from openai import OpenAI

from rag.rag_engine import load_knowledge, search_knowledge
from reasoning.reasoning_engine import (
    analyze_environment,
    check_missing_data
)


# ==========================================================
# LOAD API KEY
# ==========================================================

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    st.error("OPENROUTER_API_KEY was not found in your .env file.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Darukaa Biodiversity Intelligence",
    page_icon="🌱",
    layout="wide"
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "environmental_data" not in st.session_state:
    st.session_state.environmental_data = {}


# ==========================================================
# LOAD KNOWLEDGE BASE
# ==========================================================

load_knowledge()


# ==========================================================
# HEADER
# ==========================================================

st.title("🌱 Darukaa Biodiversity Intelligence")

st.write(
    "AI-powered environmental decision support grounded in "
    "scientific knowledge and environmental data."
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("🌍 Environmental Data")

st.sidebar.caption(
    "Provide environmental measurements for more specific "
    "recommendations."
)


# ==========================================================
# SOIL ORGANIC CARBON
# ==========================================================

soc_provided = st.sidebar.checkbox(
    "I have Soil Organic Carbon data",
    value=True
)

if soc_provided:
    soc = st.sidebar.number_input(
        "Soil Organic Carbon (%)",
        min_value=0.0,
        max_value=10.0,
        value=0.7,
        step=0.1
    )
else:
    soc = None


# ==========================================================
# RAINFALL
# ==========================================================

rainfall_provided = st.sidebar.checkbox(
    "I have Rainfall data",
    value=True
)

if rainfall_provided:
    rainfall = st.sidebar.number_input(
        "Annual Rainfall (mm)",
        min_value=0.0,
        max_value=5000.0,
        value=450.0,
        step=10.0
    )
else:
    rainfall = None


# ==========================================================
# SPECIES RICHNESS
# ==========================================================

richness_provided = st.sidebar.checkbox(
    "I have Species Richness data",
    value=True
)

if richness_provided:
    species_richness = st.sidebar.number_input(
        "Species Richness",
        min_value=0,
        max_value=1000,
        value=6,
        step=1
    )
else:
    species_richness = None


# ==========================================================
# LAND USE
# ==========================================================

land_use_provided = st.sidebar.checkbox(
    "I have Land Use data",
    value=True
)

if land_use_provided:
    land_use = st.sidebar.selectbox(
        "Land Use",
        [
            "Monoculture",
            "Diversified Cropping",
            "Forest",
            "Grassland"
        ]
    )
else:
    land_use = None


# ==========================================================
# JSON INPUT
# ==========================================================

st.sidebar.divider()

st.sidebar.subheader("📦 Structured JSON")

json_input = st.sidebar.text_area(
    "Optional environmental JSON",
    placeholder="""{
  "soil_organic_carbon": 0.7,
  "rainfall": 450,
  "species_richness": 6,
  "land_use": "Monoculture"
}"""
)

st.sidebar.caption(
    "JSON values override the corresponding sidebar values."
)


# ==========================================================
# CLEAR CHAT
# ==========================================================

if st.sidebar.button("🗑️ Clear Conversation"):

    st.session_state.chat_history = []
    st.session_state.environmental_data = {}

    st.rerun()


# ==========================================================
# BUILD ENVIRONMENTAL STATE
# ==========================================================

environmental_data = {
    "soil_organic_carbon": soc,
    "rainfall": rainfall,
    "species_richness": species_richness,
    "land_use": land_use
}


# ==========================================================
# JSON OVERRIDE
# ==========================================================

if json_input.strip():

    try:

        json_data = json.loads(json_input)

        if not isinstance(json_data, dict):

            st.sidebar.error(
                "JSON must contain an object of environmental fields."
            )

        else:

            environmental_data.update(json_data)

            st.sidebar.success("✅ JSON loaded")

    except json.JSONDecodeError:

        st.sidebar.error("❌ Invalid JSON format.")


# ==========================================================
# SAVE ENVIRONMENTAL STATE
# ==========================================================

st.session_state.environmental_data = environmental_data


# ==========================================================
# CURRENT ENVIRONMENTAL STATE
# ==========================================================

with st.expander("🌍 Current Environmental State"):

    st.json(environmental_data)


# ==========================================================
# PREVIOUS CHAT
# ==========================================================

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================================
# CHAT INPUT
# ==========================================================

question = st.chat_input(
    "Ask an environmental question..."
)


# ==========================================================
# PROCESS QUESTION
# ==========================================================

if question:

    # ------------------------------------------------------
    # Display user question
    # ------------------------------------------------------

    with st.chat_message("user"):

        st.markdown(question)


    # ------------------------------------------------------
    # Missing data
    # ------------------------------------------------------

    missing_data = check_missing_data(
        environmental_data
    )


    # ------------------------------------------------------
    # Rule-based reasoning
    # ------------------------------------------------------

    findings = analyze_environment(
        environmental_data
    )


    # ------------------------------------------------------
    # Previous conversation
    # ------------------------------------------------------

    previous_context = ""

    if st.session_state.chat_history:

        previous_messages = []

        for message in st.session_state.chat_history[-6:]:

            previous_messages.append(
                f"{message['role']}: {message['content']}"
            )

        previous_context = "\n".join(
            previous_messages
        )


    # ------------------------------------------------------
    # Contextual retrieval
    # ------------------------------------------------------

    retrieval_query = f"""
Environmental context:

Soil Organic Carbon:
{environmental_data.get("soil_organic_carbon")}

Annual Rainfall:
{environmental_data.get("rainfall")}

Species Richness:
{environmental_data.get("species_richness")}

Land Use:
{environmental_data.get("land_use")}

Previous conversation:
{previous_context}

Current user question:
{question}
"""

    results = search_knowledge(
        retrieval_query,
        n_results=4
    )


    # ------------------------------------------------------
    # Retrieved documents
    # ------------------------------------------------------

    retrieved_documents = results["documents"][0]

    knowledge_text = "\n\n---\n\n".join(
        retrieved_documents
    )


    # ------------------------------------------------------
    # Sources
    # ------------------------------------------------------

    sources = results["metadatas"][0]


    # ------------------------------------------------------
    # Findings text
    # ------------------------------------------------------

    if findings:

        findings_text = "\n".join(
            f"- {finding}"
            for finding in findings
        )

    else:

        findings_text = (
            "- No specific rule-based environmental finding "
            "was detected."
        )


    # ------------------------------------------------------
    # Missing data text
    # ------------------------------------------------------

    if missing_data:

        missing_text = ", ".join(
            missing_data
        )

    else:

        missing_text = "None"


    # ======================================================
    # GENERIC GROUNDED AI PROMPT
    # ======================================================

    prompt = f"""
You are Darukaa.Earth's AI Biodiversity Intelligence
decision-support assistant.

Your task is to answer the user's current environmental
question using the provided environmental data, retrieved
scientific knowledge, rule-based reasoning, and previous
conversation context.

The system must work GENERICALLY across environmental topics.
Do not assume that the question is about any particular
environmental variable.

The user may ask about biodiversity, soil, water, land use,
climate, pollution, deforestation, habitat, species, or
another environmental issue.

Determine what is relevant from the CURRENT QUESTION and
the RETRIEVED KNOWLEDGE.

==========================================================
ENVIRONMENTAL DATA
==========================================================

Soil Organic Carbon:
{environmental_data.get("soil_organic_carbon")}

Annual Rainfall:
{environmental_data.get("rainfall")}

Species Richness:
{environmental_data.get("species_richness")}

Land Use:
{environmental_data.get("land_use")}

Missing data:
{missing_text}

==========================================================
RULE-BASED ENVIRONMENTAL REASONING
==========================================================

{findings_text}

==========================================================
RETRIEVED SCIENTIFIC KNOWLEDGE
==========================================================

{knowledge_text}

==========================================================
PREVIOUS CONVERSATION
==========================================================

{previous_context}

==========================================================
CURRENT USER QUESTION
==========================================================

{question}

==========================================================
RESPONSE REQUIREMENTS
==========================================================

First, directly answer the CURRENT question.

Do not merely repeat or summarize the environmental data.

If the question asks what should be done, provide 1–3
specific practical actions supported by the retrieved
evidence.

If the question asks what happens to something, directly
explain the expected relationship or effect using the
retrieved evidence.

Adapt the answer to whatever environmental topic the user
actually asks about.

Where relevant, connect multiple environmental variables.
For example:

soil condition → soil moisture → vegetation → biodiversity

land use → habitat diversity → species richness

rainfall → soil moisture → vegetation → biodiversity

Do not force these relationships when they are not relevant
to the user's question.

Use the following structure:

### 🌱 Recommendation
OR
### 🌱 Answer

Give the direct answer first.

### 🔬 Why

Explain the scientific reasoning using the retrieved
knowledge.

Clearly distinguish direct effects from indirect effects.

### 📊 Metrics to monitor

List environmental metrics relevant to the user's question
and the recommended action.

### ⏳ Time horizon

Only provide a specific timeline if supported by the
retrieved evidence.

Otherwise write:

"No fixed timeline can be established from the available
evidence."

### 🎯 Confidence

Give High, Medium, or Low confidence and briefly explain why.

### 📚 Scientific evidence

Mention the relevant retrieved scientific source topics.

==========================================================
SCIENTIFIC SAFETY RULES
==========================================================

- Use retrieved knowledge as the scientific evidence base.
- Do not invent studies.
- Do not invent citations.
- Do not invent percentages.
- Do not invent numerical improvement estimates.
- Do not invent timelines.
- Do not claim that an intervention definitely improves a
  metric unless the retrieved evidence supports that claim.
- Use "may", "can potentially", or similar language when
  appropriate.
- Outcomes depend on local soil, climate, species and
  management conditions.
- Do not claim that land management can change rainfall.
- Distinguish direct effects from indirect effects.
- If evidence is insufficient, explicitly say so.
- Treat previous conversation as context, not scientific
  evidence.
- Answer the CURRENT question rather than repeating previous
  answers.
- Do not force unrelated environmental variables into the
  answer.
- Do not assume a specific question type.
- Do not use hard-coded topic-specific answers.

MOST IMPORTANT:

The response must be useful to the user and directly answer
their current environmental question.
"""


    # ======================================================
    # OPENROUTER MESSAGES
    # ======================================================

    messages = [
        {
            "role": "system",
            "content": (
                "You are an evidence-grounded biodiversity "
                "decision-support assistant. "
                "Answer environmental questions generically "
                "using retrieved scientific knowledge and "
                "provided environmental data. "
                "Never invent scientific evidence."
            )
        }
    ]


    for message in st.session_state.chat_history:

        messages.append(
            {
                "role": message["role"],
                "content": message["content"]
            }
        )


    messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # ======================================================
    # CALL OPENROUTER
    # ======================================================

    try:

        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0.2,
            max_tokens=1400
        )

        answer = response.choices[0].message.content

        if not answer or not answer.strip():

            raise ValueError(
                "The AI model returned an empty response."
            )


    except Exception as e:

        # --------------------------------------------------
        # GENERIC FALLBACK
        # --------------------------------------------------

        answer = f"""
### 🌱 Answer

The environmental analysis identified the following
conditions that may be relevant to your question:

{findings_text}

A complete question-specific recommendation could not be
generated because the language model was temporarily
unavailable.

### 🔬 Why

The system uses environmental measurements, rule-based
reasoning, and retrieved scientific knowledge to connect
environmental variables and identify relevant management
options.

### 📊 Metrics to monitor

- Soil organic carbon
- Soil moisture
- Species richness
- Habitat diversity
- Land-use / land-cover
- Relevant climate indicators

### ⏳ Time horizon

No fixed timeline can be established from the available
evidence.

### 🎯 Confidence

**Low** — the AI model response could not be generated, so
this fallback should not be treated as a full
question-specific recommendation.

### 📚 Scientific evidence

Relevant scientific knowledge was retrieved from the
biodiversity knowledge base.

Model error:
{str(e)}
"""


    # ======================================================
    # SAVE CONVERSATION
    # ======================================================

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


    # ======================================================
    # DISPLAY RESPONSE
    # ======================================================

    with st.chat_message("assistant"):

        st.markdown(answer)


        # --------------------------------------------------
        # Environmental reasoning
        # --------------------------------------------------

        with st.expander("🧠 Environmental Reasoning"):

            if findings:

                for finding in findings:

                    st.write(
                        "•",
                        finding
                    )

            else:

                st.write(
                    "No specific rule-based environmental "
                    "finding was detected."
                )


        # --------------------------------------------------
        # Retrieved scientific knowledge
        # --------------------------------------------------

        with st.expander(
            "📚 Retrieved Scientific Knowledge"
        ):

            st.write(
                "The response was grounded using retrieved "
                "scientific knowledge from the biodiversity "
                "knowledge base."
            )

            for source in sources:

                st.markdown(
                    f"**Source:** {source['source']}"
                )

                st.markdown(
                    f"**Topic:** "
                    f"{source['topic'].replace('_', ' ').title()}"
                )

                st.divider()