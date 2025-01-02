# Bot Detection and Traffic Simulation Project

## Overview
This project simulates user traffic, evaluates heuristics to detect bot-like behavior, and integrates with a Django backend. The system processes human and bot-like behaviors, evaluates heuristics, and analyzes performance using PostgreSQL and Redis.

## Features
- **Traffic Simulation**: Simulate browser sessions for human-like and bot-like behaviors.
- **Heuristics Evaluation**: Detect suspicious activities using various heuristics like mismatched user agents, blacklisted IPs, etc.
- **Data Processing**: Queue data using Redis and analyze it with Django and Celery.
- **Performance Reporting**: Visualize logs and results using a Flask server with a PostgreSQL backend.

## Components
1. **Traffic Simulation**:
   - Simulate mouse movements and interactions.
   - Use Playwright and PyAutoGUI for realistic UI interactions.
2. **Django Backend**:
   - Queue data for analysis via Redis.
   - Process data asynchronously with Celery workers.
3. **PostgreSQL**:
   - Store and retrieve processed logs for reporting.
4. **Heuristics**:
   - Evaluate behaviors against known patterns and IP blocklists.

## Technology Stack
- **Backend**: Django, Redis, Celery, PostgreSQL
- **Frontend**: Flask for reports
- **Testing Tools**: Playwright, PyAutoGUI
- **Programming Languages**: Python, JavaScript
- **Tools**: Docker, Kubernetes

## Setup Instructions
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   npm install
