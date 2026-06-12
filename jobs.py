# jobs.py
import os
import requests
from typing import List, Dict
from abc import ABC, abstractmethod
import re


class JobProvider(ABC):
    @abstractmethod
    def search(self, query: str) -> List[Dict]:
        pass

print("Starting provider initialization...")
class JSearchProvider(JobProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://jsearch.p.rapidapi.com/search"
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
    
    def search(self, query: str) -> List[Dict]:
        jobs = []
        params = {
            "query": query,
            "page": "1",
            "num_pages": "1"
        }
        
        try:
            response = requests.get(
                self.base_url,
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("data"):
                for job in data["data"]:
                    jobs.append({
                        "title": job.get("job_title", ""),
                        "company": job.get("employer_name", ""),
                        "location": self._format_location(job),
                        "apply_link": job.get("job_apply_link", ""),
                        "source": "JSearch"
                    })
        except requests.exceptions.RequestException as e:
            print(f"JSearch error: {e}")
        
        return jobs
    
    def _format_location(self, job: Dict) -> str:
        city = job.get("job_city", "")
        state = job.get("job_state", "")
        country = job.get("job_country", "")
        parts = [p for p in [city, state, country] if p]
        return ", ".join(parts) if parts else "Remote"

class RemoteOKProvider(JobProvider):
    def __init__(self):
        self.base_url = "https://remoteok.com/api"
    
    def search(self, query: str) -> List[Dict]:
        jobs = []
        try:
            response = requests.get(self.base_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 1:
                for job in data[1:]:
                    position = job.get("position", "")
                    company = job.get("company", "")
                    
                    search_text = f"{position} {company}".lower()

                    query_words = [
                        w for w in query.lower().split()
                        if len(w) > 2
                    ]
                    matches = sum(1 for word in query_words if word in search_text)
                    if matches >= 1:
                        jobs.append({
                            "title": position,
                            "company": company,
                            "location": job.get("location", "Remote"),
                            "apply_link": job.get("url", ""),
                            "source": "RemoteOK"
                        })
        except requests.exceptions.RequestException as e:
            print(f"RemoteOK error: {e}")
        
        return jobs

class RemotiveProvider(JobProvider):
    def __init__(self):
        self.base_url = "https://remotive.com/api/remote-jobs"
    
    def search(self, query: str) -> List[Dict]:
        jobs = []
        try:
            response = requests.get(self.base_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get("jobs"):
                for job in data["jobs"]:
                    title = job.get("title", "")
                    company = job.get("company_name", "")
                    
                    search_text = (
                        title.lower()
                        + " "
                        + company.lower()
                        + " "
                        + " ".join(job.get("tags", [])).lower()
                    )

                    query_words = [
                        w for w in query.lower().split()
                        if len(w) > 2
                    ]
                    matches = sum(1 for word in query_words if word in search_text)
                    if matches >= 1:
                        jobs.append({
                            "title": title,
                            "company": company,
                            "location": job.get("candidate_required_location", "Remote"),
                            "apply_link": job.get("url", ""),
                            "source": "Remotive"
                        })
        except requests.exceptions.RequestException as e:
            print(f"Remotive error: {e}")
        
        return jobs



class JobSearch:
    def __init__(self):
        self.jsearch_api_key = os.getenv("RAPID_API_KEY", "")
        self.providers = []
        
        if self.jsearch_api_key:
            self.providers.append(JSearchProvider(self.jsearch_api_key))
        
        self.providers.append(RemoteOKProvider())
        self.providers.append(RemotiveProvider())
        
    def remove_duplicates(self, jobs):
        unique_jobs = []
        seen = set()
        for job in jobs:
            key = (
                job["title"].strip().lower(),
                job["company"].strip().lower(),
                job["location"].strip().lower()
            )

            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)

        return unique_jobs
    
    def search_jobs(self, query: str):
        all_jobs = []

        for provider in self.providers:
            jobs = provider.search(query)
            print(f"{provider.__class__.__name__}: {len(jobs)} jobs")
            all_jobs.extend(jobs)

        unique_jobs = self.remove_duplicates(all_jobs)

        ranked_jobs = self.rank_jobs(
            unique_jobs,
            query
        )

        return ranked_jobs
    
    def calculate_relevance_score(self, job, query):

        role_words, location_words, remote = self.parse_query(query)

        title = job["title"].lower()
        company = job["company"].lower()
        location = job["location"].lower()

        score = 0

        # Title matches are most important
        for word in role_words:

            if word in title:
                score += 8

            elif word in company:
                score += 2

        # Location matching
        for word in location_words:

            if word in location:
                score += 5

        # Remote bonus
        if remote and "remote" in location:
            score += 6

        return score
    
    def rank_jobs(self, jobs, query):
        ranked_jobs = []

        for job in jobs:
            score = self.calculate_relevance_score(job, query)

            if score >= 5:
                job["score"] = score
                ranked_jobs.append(job)

        ranked_jobs.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked_jobs[:50]

    def normalize_words(self, text):
        words = re.findall(r'\w+', text.lower())

        replacements = {
            "internships": "intern",
            "internship": "intern",
            "scientists": "scientist",
            "engineers": "engineer",
            "analysts": "analyst",
            "developers": "developer",
            "datascience": "data science",
            "ml": "machine learning",
            "ai": "artificial intelligence"
        }

        normalized = []

        for word in words:
            normalized.append(
                replacements.get(word, word)
            )

        return normalized
    
    def parse_query(self, query):
        words = self.normalize_words(query)

        remote = "remote" in words

        locations = {
            "india",
            "hyderabad",
            "telangana",
            "bangalore",
            "bengaluru",
            "chennai",
            "pune",
            "mumbai",
            "delhi",
            "gurgaon",
            "noida",
            "kolkata",
            "ahmedabad",
            "kochi",
            "remote"
        }

        location_words = [
            w for w in words
            if w in locations
        ]

        role_words = [
            w for w in words
            if w not in locations
            and w != "remote"
        ]

        return role_words, location_words, remote
    

    
