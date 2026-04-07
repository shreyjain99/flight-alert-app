Claude Instructions (STRICT RULES)



Project Description:

We are building a simple Flight Price Tracker web application.

Users enter flight details (from, to, date, email), and the system tracks flight prices daily using the Amadeus API.

If prices change, the system sends email alerts (price drop, lowest price, increase, or reminder).

The goal is to build a minimal, working MVP that is clean, simple, and resume-ready.



1\. Keep everything SIMPLE

\- Do not over-engineer

\- Do not add unnecessary features

\- Focus only on MVP



2\. Tech Stack (DO NOT CHANGE)

\- Frontend: React

\- Backend: FastAPI (Python)

\- Database: SQLite

\- Flight API: Amadeus

\- Email: Gmail SMTP

\- Hosting: Render



3\. Code Style

\- Write clean, beginner-friendly code

\- Add comments for clarity

\- Avoid complex patterns

\- No advanced architecture (no microservices, no Docker unless asked)



4\. Backend Rules

\- Use FastAPI only

\- Use SQLite (no other DB)

\- Keep all logic simple and readable

\- Use APScheduler for daily tasks



5\. Frontend Rules

\- Use basic React (no heavy UI libraries)

\- Keep UI minimal

\- One page only (no routing unless asked)

\- Use mock data initially (no backend integration in first step)



6\. API Rules

\- Do not mock data (backend)

\- Show real integration with Amadeus API

\- Clearly mark where API keys go



7\. Security

\- Do NOT hardcode secrets

\- Use environment variables



8\. Output Format

\- Always provide:

&#x20; - File structure

&#x20; - Full working code

&#x20; - Step-by-step explanation



9\. Iteration

\- Build step-by-step

\- Do not dump entire project unless asked

\- Wait for confirmation before moving to next step



10\. Goal

\- This is a working MVP + resume-quality project

\- Prioritize functionality over perfection

