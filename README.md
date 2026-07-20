# AI-HCP CRM

AI-HCP CRM is an AI-first Customer Relationship Management system designed for managing Healthcare Professionals (HCPs) and their interactions.

The application combines traditional CRM functionality with an AI assistant powered by LangGraph and Groq, allowing users to manage CRM activities using natural language.

## Features

### HCP Management
- Create Healthcare Professional profiles
- View all HCPs
- Update HCP information
- Delete HCP records
- Duplicate email validation

### Interaction Management
- Log HCP interactions
- View interaction history
- Track visits, calls, emails, meetings, and follow-ups

### AI CRM Assistant

The AI assistant supports five core capabilities:

1. Log Interaction
2. Edit Interaction
3. Search Interactions
4. Generate Meeting/Interaction Summaries
5. Recommend Follow-up Actions

Natural-language requests are routed to the appropriate CRM tool using LangGraph.

Example:

> Summarize all interactions for HCP ID 1.

The system retrieves the relevant interaction history from PostgreSQL and uses the LLM to generate a professional summary.

## Tech Stack

### Frontend
- React
- Vite
- Axios
- React Router

### Backend
- FastAPI
- Python
- SQLAlchemy
- Pydantic

### Database
- PostgreSQL

### AI
- Groq LLM API
- LangGraph

## Architecture

User
↓
React Frontend
↓
FastAPI REST API
↓
LangGraph AI Agent
↓
CRM Tools
↓
PostgreSQL / Groq LLM

## Project Structure

AI-HCP-CRM/

    backend/
        app/
            agents/
            api/
            core/
            database/
            models/
            schemas/
            services/
            tools/
        main.py
        requirements.txt

    frontend/
        src/
            components/
            pages/
            services/

    .gitignore
    README.md

## Backend Setup

Navigate to the backend:

    cd backend

Create and activate a virtual environment:

    python -m venv venv

Windows:

    .\venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

Create a `.env` file and configure the required environment variables:

    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    GROQ_API_KEY=your_groq_api_key

Run the backend:

    uvicorn main:app --reload

FastAPI documentation will be available at:

    http://127.0.0.1:8000/docs

## Frontend Setup

Navigate to the frontend:

    cd frontend

Install dependencies:

    npm install

Start the development server:

    npm run dev

The frontend will typically run at:

    http://localhost:5173

## AI Assistant Example Commands

Log an interaction:

    Log a Call interaction for HCP ID 1. The doctor requested product information.

Edit an interaction:

    Edit interaction ID 1. Change the type to Follow-up Call and update the notes.

Search interactions:

    Search for Follow-up Call interactions.

Generate a summary:

    Summarize all interactions for HCP ID 1.

Generate a follow-up recommendation:

    Recommend the next follow-up action for HCP ID 1.

## Security

Environment variables and API credentials are stored in `.env` and excluded from version control through `.gitignore`.

Never commit database passwords or API keys to a public repository.

## Future Improvements

- Authentication and role-based access control
- Advanced HCP search and filtering
- Interaction analytics
- AI conversation memory
- Deployment with managed PostgreSQL
- Automated testing

## Author

Sofia Naushad