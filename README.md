# AI Job Search

A multi-source job aggregation and ranking engine that collects opportunities from multiple job providers, removes duplicate listings, normalizes search queries, and ranks results using a custom relevance scoring system.

The system is designed to improve job discovery by combining multiple sources into a single searchable dataset and prioritizing the most relevant opportunities.

---

## Overview

Searching for internships and entry-level opportunities often requires browsing multiple job platforms independently.

This project automates that process by:

* Aggregating jobs from multiple providers
* Standardizing user queries
* Removing duplicate listings
* Ranking opportunities based on relevance
* Displaying the best matches directly in the terminal

The application runs locally and does not require databases, schedulers, cloud deployment, or external storage.

---

## Key Features

### Multi-Source Job Aggregation

Collects opportunities from:

* JSearch (RapidAPI)
* RemoteOK
* Remotive

All results are combined into a unified search dataset.

---

### Query-Based Search

Users can search for positions such as:

* Data Science Intern
* Machine Learning Engineer
* AI Engineer
* Python Developer
* Backend Developer

The query is processed and used across all providers.

---

### Query Normalization

To improve search quality, common variations are normalized.

| User Input  | Normalized              |
| ----------- | ----------------------- |
| internships | intern                  |
| internship  | intern                  |
| scientists  | scientist               |
| engineers   | engineer                |
| developers  | developer               |
| analysts    | analyst                 |
| ai          | artificial intelligence |
| ml          | machine learning        |

This allows broader matching across job providers.

---

### Duplicate Removal

Jobs collected from multiple providers may overlap.

Duplicate listings are identified using:

* Job Title
* Company Name
* Location

This produces cleaner and more meaningful search results.

---

### Relevance Scoring

Each opportunity receives a relevance score based on:

* Title keyword matches
* Company keyword matches
* Location matches
* Remote-work preference

Higher scores indicate stronger alignment with the user's intent.

---

### Intelligent Ranking

Search results pass through the following pipeline:

```text
User Query
     │
     ▼
Query Normalization
     │
     ▼
Provider Search
     │
     ▼
Aggregation
     │
     ▼
Deduplication
     │
     ▼
Relevance Scoring
     │
     ▼
Ranking
     │
     ▼
Final Results
```

The highest scoring jobs are displayed first.

---

## Project Structure

```text
AI-Job_Search/
│
├── main.py
├── jobs.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### main.py

Handles:

* User input
* Search execution
* Result presentation

### jobs.py

Contains:

* Provider implementations
* Aggregation logic
* Deduplication logic
* Query normalization
* Relevance scoring
* Ranking algorithms

---

## Technologies Used

### Programming Language

* Python

### APIs

* JSearch API
* RemoteOK API
* Remotive API

### Libraries

* Requests
* Python-dotenv

### Concepts

* Information Retrieval
* Search Systems
* Ranking Algorithms
* Data Aggregation
* API Integration
* Object-Oriented Programming

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Surya-Kotipalli/AI-Job_Search.git
cd AI-Job_Search
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
RAPID_API_KEY=your_jsearch_api_key
```

---

## Running the Application

```bash
python main.py
```

Example query:

```text
Remote Data Science Internship
```

Example output:

```text
1. [Score: 24] [JSearch]
   Data Science Intern

2. [Score: 18] [RemoteOK]
   Machine Learning Intern

3. [Score: 16] [Remotive]
   AI Research Intern
```

---

## Provider Statistics

During execution the application reports:

```text
JSearchProvider: 10 jobs
RemoteOKProvider: 22 jobs
RemotiveProvider: 16 jobs

Total fetched: 48
After deduplication: 39
After ranking: 29
```

This provides visibility into provider performance and ranking effectiveness.

---

## Current Limitations

* Sequential provider fetching
* Basic keyword-based ranking
* No negative keyword filtering
* No CSV export
* No search history
* Limited JSearch pagination

---

## Future Improvements

Planned enhancements include:

* Concurrent API fetching
* Advanced ranking engine
* Positive and negative keyword scoring
* Exact phrase matching
* CSV export
* Rich CLI table output
* Search analytics
* Provider balancing
* Extended pagination support

---

## Learning Outcomes

This project demonstrates practical experience with:

* API Integration
* Data Aggregation
* Search Systems
* Information Retrieval
* Ranking Algorithms
* Query Processing
* Data Deduplication
* Python Application Architecture
* Object-Oriented Programming

---

## Status

Version: v1.0

Type: Local CLI Application

Stage: Functional MVP

---

## Author

**Surya Teja**

Aspiring Data Scientist and AI Developer interested in Machine Learning, Search Systems, Analytics, Automation, and Intelligent Applications.
