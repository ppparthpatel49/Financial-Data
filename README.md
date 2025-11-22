# 🌸 AuraCycle: AI-Powered Menstrual Health Assistant

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

An intelligent, multi-agent AI system built with Streamlit and Google Gemini to provide personalized menstrual health guidance, symptom tracking, and cycle predictions.

## 🎯 Project Overview

AuraCycle is a capstone project demonstrating **Agentic AI** principles where multiple specialized AI agents collaborate to provide comprehensive health guidance:

- 🤖 **Coordinator Agent**: Orchestrates all other agents and manages user interactions
- 🧘 **Wellness Agent**: Provides yoga and exercise recommendations
- 🥗 **Nutrition Agent**: Suggests vegetarian foods and recipes
- 🔮 **Prediction Agent**: Predicts next cycle and detects irregularities

## ✨ Features

### Core Functionality
- ✅ **Cycle Tracking**: Log period dates and flow intensity
- ✅ **Symptom Logging**: Track physical and emotional symptoms daily
- ✅ **AI Chat**: Conversational interface for health questions
- ✅ **Cycle Prediction**: ML-based prediction of next period
- ✅ **Irregularity Detection**: Smart alerts for unusual patterns
- ✅ **Dashboard**: Visual analytics of health data
- ✅ **Personalized Recommendations**: Context-aware yoga, exercise, and nutrition advice

### Technical Highlights
- 🏗️ **Multi-Agent Architecture**: Specialized agents working in coordination
- 🧠 **LLM-Powered**: Google Gemini API for natural language understanding
- 💾 **Simple Storage**: JSON-based database (no complex setup)
- 🎨 **Beautiful UI**: Streamlit with custom CSS styling
- 📊 **Data Visualization**: Interactive charts with Plotly

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Google Gemini API key ([Get it free here](https://makersuite.google.com/app/apikey))
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/auracycle.git
   cd auracycle
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, manually navigate to that URL

## 📖 Usage Guide

### Getting Started

1. **Track Your First Cycle**
   - Navigate to "📅 Track Cycle"
   - Select your period start date
   - Choose flow intensity
   - Click "Log Cycle"

2. **Log Symptoms**
   - Go to "😊 Log Symptoms"
   - Select physical symptoms (cramps, bloating, etc.)
   - Select emotional symptoms (mood swings, anxiety, etc.)
   - Rate your energy and pain levels
   - Save to get instant AI recommendations

3. **Chat with AI**
   - Navigate to "💬 Chat with AI"
   - Ask any question like:
     - "What foods help with cramps?"
     - "Which yoga poses are good for bloating?"
     - "When is my next period?"
   - The AI agents will collaborate to provide comprehensive answers

4. **View Dashboard**
   - Check "📊 My Dashboard" for:
     - Cycle timeline visualization
     - Symptom pattern analysis
     - Energy and pain trends

5. **Get Predictions**
   - Visit "🔮 Predictions" to:
     - See predicted next cycle date
     - Check for irregularities
     - View cycle statistics

## 🏗️ Architecture

### Multi-Agent System

```
┌─────────────────────────────────────────────────────┐
│              User Interface (Streamlit)             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            Coordinator Agent (Main)                 │
│  • Interprets user intent                           │
│  • Routes to appropriate agents                     │
│  • Synthesizes final response                       │
└────┬──────────────┬──────────────┬─────────────────┘
     │              │              │
     ▼              ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────────┐
│ Wellness │  │Nutrition │  │ Prediction   │
│  Agent   │  │  Agent   │  │   Agent      │
└────┬─────┘  └────┬─────┘  └──────┬───────┘
     │             │                │
     ▼             ▼                ▼
┌──────────┐  ┌──────────┐  ┌──────────────┐
│Knowledge │  │Knowledge │  │  User Data   │
│   Base   │  │   Base   │  │  Analysis    │
└──────────┘  └──────────┘  └──────────────┘
     │             │                │
     └─────────────┴────────────────┘
                   │
                   ▼
           ┌───────────────┐
           │ Gemini LLM    │
           │ (Synthesis)   │
           └───────┬───────┘
                   │
                   ▼
           Final Response to User
```

### Data Flow

```
User Input
    ↓
Streamlit UI
    ↓
Coordinator Agent
    ├→ Analyzes Intent
    ├→ Retrieves User History (Database)
    ├→ Calls Relevant Agents:
    │   ├→ Wellness Agent → Knowledge Base → Recommendations
    │   ├→ Nutrition Agent → Knowledge Base → Recipes/Foods
    │   └→ Prediction Agent → Data Analysis → Predictions
    ├→ Sends All Context to Gemini LLM
    └→ Synthesizes Comprehensive Response
        ↓
    Saves to Database
        ↓
    Displays in UI
```

## 📚 Project Structure Details

### Core Files

- **`app.py`**: Main Streamlit application with UI components
- **`agents.py`**: Multi-agent system implementation
  - `CoordinatorAgent`: Main orchestrator
  - `WellnessAgent`: Yoga and exercise specialist
  - `NutritionAgent`: Diet and nutrition specialist
  - `PredictionAgent`: Cycle prediction and analysis
- **`database.py`**: Simple JSON-based data persistence
- **`knowledge.py`**: Static knowledge base for health information

### Configuration Files

- **`requirements.txt`**: Python dependencies
- **`.env`**: Environment variables (API keys) - **DO NOT COMMIT**
- **`.env.example`**: Template for environment variables
- **`.gitignore`**: Files to exclude from version control

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **AI/LLM** | Google Gemini API |
| **Language** | Python 3.9+ |
| **Data Storage** | JSON (local files) |
| **Visualization** | Plotly |
| **Date/Time** | Python datetime, pandas |

## 🔒 Privacy & Security

- **Local Storage**: All data stored locally in JSON files
- **No External Database**: Your health data never leaves your machine
- **API Security**: API keys stored in `.env` (never committed to git)
- **Data Encryption**: Consider encrypting `auracycle_data.json` for production use

## ⚠️ Medical Disclaimer

**IMPORTANT**: AuraCycle is an educational project and proof-of-concept.

- ❌ **NOT** a substitute for professional medical advice
- ❌ **NOT** FDA-approved or clinically validated
- ❌ **NOT** intended for diagnosing medical conditions

**Always consult a qualified healthcare provider for:**
- Severe symptoms
- Irregular cycles lasting >3 months
- Any health concerns or questions

## 🧪 Testing

Run tests (when implemented):
```bash
pytest tests/
```


## 🗺️ Roadmap

- [x] Multi-agent system implementation
- [x] Streamlit UI
- [x] Cycle prediction
- [x] Symptom tracking
- [ ] Enhanced ML models (LSTM for prediction)
- [ ] User authentication
- [ ] PostgreSQL database option
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Export data to PDF/CSV
- [ ] Integration with health wearables


## 🙏 Acknowledgments

- Google Gemini team for the LLM API
- Streamlit team for the amazing framework
- Health information sourced from reputable medical websites
- Inspired by the need for accessible women's health technology



If you find this project helpful, please consider giving it a ⭐!

---

**Made with ❤️ for women's health empowerment**
