# main.py
import os
from dotenv import load_dotenv
from jobs import JobSearch

load_dotenv()

def main():
    query = input("Enter job search query: ").strip()
    if not query:
        print("Error: Search query cannot be empty.")
        return
    
    searcher = JobSearch()
    jobs = searcher.search_jobs(query)
    
    if not jobs:
        print("No jobs found.")
        return
    
    for idx, job in enumerate(jobs, 1):
        print(f"{idx}. [{job.get('source', 'Unknown')}] Score: {job.get('score', 0)}")
        print(f"   Title: {job.get('title', 'N/A')}")
        print(f"   Company: {job.get('company', 'N/A')}")
        print(f"   Location: {job.get('location', 'N/A')}")
        print(f"   Apply Link: {job.get('apply_link', 'N/A')}")
        print()

if __name__ == "__main__":
    main()