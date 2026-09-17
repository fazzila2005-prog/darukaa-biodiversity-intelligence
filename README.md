# 🌱 Darukaa Biodiversity Intelligence

An AI-powered biodiversity intelligence chatbot that provides evidence-grounded environmental recommendations by combining **Retrieval-Augmented Generation (RAG)**, environmental reasoning, and a scientific knowledge base.

## 🚀 Live Demo

https://darukaa-biodiversity-intelligence-9gwycxxjezz7d8oaytkrp5.streamlit.app/

## 💻 GitHub Repository

https://github.com/fazzila2005-prog/darukaa-biodiversity-intelligence

---

## 📌 Overview

Darukaa Biodiversity Intelligence is designed as an AI environmental scientist that helps users understand biodiversity and environmental problems using multiple environmental variables together.

The system considers factors such as:

* Soil organic carbon
* Soil moisture
* Rainfall
* Soil pH
* Temperature
* Land use
* Habitat diversity
* Species richness
* Pollution
* Deforestation

Instead of generating recommendations using an LLM alone, the system retrieves relevant scientific knowledge and combines it with a rule-based environmental reasoning layer before generating the final response.

---

## 🏗️ System Architecture

```text
                    USER
                      │
                      ▼
             Streamlit Chat Interface
                      │
                      ▼
          Environmental State Extraction
                      │
                      ▼
             Environmental Data
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
   Reasoning Engine          RAG Engine
          │                       │
          │                Sentence Transformers
          │                all-MiniLM-L6-v2
          │                       │
          │                    ChromaDB
          │                       │
          │                Scientific Knowledge
          │                       │
          └───────────┬───────────┘
                      ▼
             Evidence + Reasoning
                      │
                      ▼
              OpenRouter LLM
                      │
                      ▼
       Evidence-Grounded Recommendation
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   What to do      Why it helps    Metrics
                                      │
                                      ▼
                              Time Horizon
                              + Confidence
```

---

## 🧠 Key Features

### 1. Retrieval-Augmented Generation (RAG)

The chatbot retrieves relevant information from a biodiversity knowledge base before generating an answer.

The knowledge base contains information covering:

* Soil organic carbon
* Soil moisture
* Rainfall
* Soil pH
* Temperature
* Land use
* Habitat diversity
* Species richness
* Pollution
* Deforestation

Documents are embedded using:

**Sentence Transformers — `all-MiniLM-L6-v2`**

The embeddings are stored and searched using:

**ChromaDB**

---

### 2. Multi-Metric Environmental Reasoning

The reasoning engine does not treat environmental variables independently.

For example:

```text
Low Soil Organic Carbon
          +
Low Rainfall
          +
Monoculture
          +
Low Species Richness
          ↓
Combined Soil–Water–Habitat Pressure
```

This allows the system to reason about relationships such as:

* Soil carbon ↔ water retention
* Rainfall ↔ soil moisture
* Soil conditions ↔ soil organisms
* Land use ↔ habitat diversity
* Habitat diversity ↔ species richness
* Temperature ↔ water stress
* Pollution ↔ biodiversity
* Deforestation ↔ habitat loss and fragmentation

---

## 🔬 Scientific Knowledge Base

The project contains 10 knowledge documents:

| Knowledge File           | Main Topic                        |
| ------------------------ | --------------------------------- |
| `soil_organic_carbon.md` | Soil organic carbon               |
| `soil_moisture.md`       | Soil moisture                     |
| `rainfall.md`            | Rainfall and water availability   |
| `species_richness.md`    | Biodiversity indicator            |
| `soil_ph.md`             | Soil pH                           |
| `land_use.md`            | Land use and habitat              |
| `temperature.md`         | Temperature and ecological stress |
| `habitat_diversity.md`   | Habitat diversity                 |
| `pollution.md`           | Pollution and biodiversity        |
| `deforestation.md`       | Forest loss and fragmentation     |

The knowledge base is based on established environmental science concepts and references organizations and assessment sources such as **FAO, IPCC, IPBES, and UNEP**.

---

## 🗄️ Database / Data Schema

The project uses **ChromaDB** as its vector database.

Each knowledge document is stored with:

```text
Document
├── ID
├── Document text
├── Embedding
└── Metadata
     ├── source
     └── topic
```

Example metadata:

```python
{
    "source": "soil_organic_carbon.md",
    "topic": "soil_organic_carbon"
}
```

The system retrieves the most relevant documents for the user's environmental question.

---

## ⚙️ Technologies Used

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python 3.10           | Main programming language       |
| Streamlit             | Web application                 |
| ChromaDB              | Vector database                 |
| Sentence Transformers | Text embeddings                 |
| `all-MiniLM-L6-v2`    | Embedding model                 |
| OpenRouter            | LLM API                         |
| OpenAI Python SDK     | API client                      |
| python-dotenv         | Environment variable management |
| GitHub                | Version control                 |
| GitHub Actions        | CI/CD testing                   |

---

## 📁 Project Structure

```text
darukaa-biodiversity-intelligence/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── knowledge/
│   ├── soil_organic_carbon.md
│   ├── soil_moisture.md
│   ├── rainfall.md
│   ├── species_richness.md
│   ├── soil_ph.md
│   ├── land_use.md
│   ├── temperature.md
│   ├── habitat_diversity.md
│   ├── pollution.md
│   └── deforestation.md
│
├── rag/
│   └── rag_engine.py
│
├── reasoning/
│   └── reasoning_engine.py
│
├── test_rag.py
├── test_reasoning.py
├── test_openrouter.py
│
└── .github/
    └── workflows/
        └── tests.yml
```

---

## 🛠️ Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/fazzila2005-prog/darukaa-biodiversity-intelligence.git
cd darukaa-biodiversity-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the API key

Create a `.env` file:

```text
OPENROUTER_API_KEY=your_api_key_here
```

The API key should **never be committed to GitHub**.

The `.gitignore` file excludes `.env`.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in the browser.

---

## 🧪 Testing

The project includes tests for:

### RAG

```bash
python test_rag.py
```

Tests whether the scientific knowledge base loads and retrieves relevant documents.

### Environmental Reasoning

```bash
python test_reasoning.py
```

Tests the environmental reasoning rules and missing-data detection.

### LLM Connection

```bash
python test_openrouter.py
```

Tests connectivity with the configured OpenRouter model.

---

## 🔄 CI/CD

GitHub Actions automatically runs the reasoning test when code is pushed or a pull request is created.

Workflow:

```text
Git Push / Pull Request
          ↓
     GitHub Actions
          ↓
   Python 3.10 Setup
          ↓
 Install Requirements
          ↓
 Run Reasoning Tests
          ↓
      Test Result
```

Workflow file:

```text
.github/workflows/tests.yml
```

---

## 💬 Example Interaction

### User

> My farm has low soil organic carbon, low rainfall, and low species richness. What should I do?

### System

The chatbot combines the three environmental conditions and retrieves relevant scientific knowledge.

It can recommend a combined strategy involving:

* Crop diversification
* Maintaining soil cover
* Organic matter management
* Locally suitable native habitat
* Monitoring soil carbon, moisture, habitat diversity and biodiversity

The response also explains the scientific pathways connecting soil, water and habitat conditions.

---

## 🎯 Challenge Alignment

The system addresses the major requirements of the Darukaa.Earth challenge:

| Requirement                | Implementation                  |
| -------------------------- | ------------------------------- |
| AI conversational system   | Streamlit + LLM                 |
| Biodiversity knowledge     | Scientific knowledge base       |
| RAG                        | ChromaDB + embeddings           |
| Environmental metrics      | Structured environmental inputs |
| Multi-metric reasoning     | Environmental reasoning engine  |
| Scientific grounding       | Retrieved knowledge             |
| Actionable recommendations | Evidence-grounded LLM response  |
| Conversational context     | Session-based chat history      |
| Confidence                 | Generated confidence assessment |
| Testing                    | Python tests                    |
| CI/CD                      | GitHub Actions                  |
| Deployment                 | Streamlit Community Cloud       |

---

## ⚠️ Prototype Reasoning Note

Some environmental thresholds used by the reasoning engine are **screening heuristics for this prototype**, rather than universal ecological thresholds.

Actual ecological interpretation depends on factors such as:

* Soil type
* Local climate
* Ecosystem
* Species composition
* Land-management history
* Geographic location

The chatbot therefore presents recommendations as evidence-informed guidance rather than guaranteed outcomes.

---

## 🌍 Future Improvements

Potential future extensions include:

* Geospatial environmental data integration
* Structured JSON environmental inputs
* Real-time climate and rainfall datasets
* Satellite-derived land-use information
* More scientific papers and environmental reports
* Location-specific ecological recommendations
* More detailed biodiversity indicators
* Automated evaluation of recommendation quality

---

## 👩‍💻 Project

**Darukaa Biodiversity Intelligence**

Built for the **Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge**.
