# MST - Puch AI Hackathon Project

## 💡 Project Introduction
Welcome to the official repository for the MST team's project for the Puch AI Hackathon! Our project is a demonstration of our skills in leveraging artificial intelligence and machine learning to build a solution to a real-world problem.

### Project Focus
- **What it does**: Resume Checker: An AI tool that analyzes and improves resumes by checking for ATS compatibility, keywords, and common writing errors.
                    Emotional Music Suggestor: An AI tool that recommends music based on a user's emotional state to help them find the perfect song for their mood.
  
- **Main Goal**:This repository hosts an MCP Server built with FastAPI for the Puch AI Hackathon. It explores the creation and deployment of AI-powered tools as a service. The project showcases two key AI-driven tools: a resume analyzer and an emotional music suggestor. This provides a practical example of how to build and manage custom AI tools for an agent.

This repository serves as both a practice ground and a final showcase of our work, encapsulating our journey from ideation to implementation.

## ✨ Features
This section highlights the key functionalities of our project:

**Resume Checker**
-An AI-powered tool that provides expert feedback on resume content and formatting.

-ATS Compatibility Score: Analyzes the resume's structure and keywords to predict its performance with Applicant Tracking Systems.

-Keyword Optimization: Identifies and suggests keywords from job descriptions to improve relevance.

-Action Verb Analysis: Evaluates the use of strong action verbs to create a more impactful professional summary.

**Emotional Music Suggestor**
-A smart music recommendation engine that curates playlists based on a user's emotional state.

-Mood-Based Curation: Takes emotional input (e.g., "calm," "energetic") and matches it with songs from a diverse music database.

-Genre Filtering: Allows users to refine suggestions by their preferred music genre (e.g., pop, lo-fi, classical).

-Personalized Suggestions: Returns specific song titles, artists, and descriptions to provide immediate, actionable recommendations.

## 🚀 Getting Started
This guide will help you set up the project locally for development or testing.

### Prerequisites
You will need the following software installed on your machine:
- **Python 3.8 or higher**
- **Git**
- **AI Framework**: **spaCy** and **TextBlob**

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/mayu2989/puch-7B07951D.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd puch-7B07951D
   ```
3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Usage
To run the project, execute the following command from the project root:
```bash
python main.py
```

### Application Instructions
- **Chatbot**: Open your browser and navigate to `http://localhost:5000` to interact with the chatbot.
- **API**: Make a POST request to `http://localhost:5000/api/predict` with your input.

## 🤝 Team MST
This project was a collaborative effort by the following team members:
- **Tushar Tiple**
- **Mayuresh Itankar**
- **Smit Patil**
