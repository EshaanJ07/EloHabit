# EloHabit

EloHabit is a future web habit-tracking application that prioritizes users' **discipline, consistency, and long-term performance**. The app is intended to encourage users to participate in long-term habit goals by introducing an Elo-based ranking ladder system.

Unlike traditional habit trackers, EloHabit is designed to:
- Measure habit consistency over time
- Penalize inactivity and slacking intelligently via the ranking system
- Allow grace periods and rest days at the user's discretion
- Prevent common “gaming” behaviors that inflate rankings
- Enable future social mechanics (leaderboard, friend groups, etc.)

This repository currently contains a **FastAPI backend skeleton** (in progress), with core infrastructure in place.

---

## 🚀 Tech Stack

- **Backend:** FastAPI (Python)
- **API Server:** Uvicorn
- **Data Models:** Pydantic
- **Version Control:** Git + GitHub
- **Environment Management:** Python virtual environments

---

## 📁 Project Structure

```text
EloHabit/
├── backend/          # FastAPI application (in progress)
│   ├── main.py       # App entry point (in progress)
│   ├── routers/      # API route definitions (planned)
│   ├── models/       # Data models (planned)
│   ├── schemas/      # Request/response schemas (planned)
│   └── services/     # Business logic (planned)
├── .gitignore
├── README.md

