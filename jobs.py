
import requests

API_URL = "https://remotive.com/api/remote-jobs"

TARGET_TITLES = [
    "cloud engineer",
    "devops engineer",
    "platform engineer",
    "site reliability engineer",
    "infrastructure engineer",
    "cloud architect",
    "devops",
    "sre",
]

EXCLUDED_TITLES = [
    "sales engineer",
    "data engineer",
    "frontend engineer",
    "front end engineer",
]

def fetch_jobs():
    """Retrieve job listings from Remotive."""

    print("\nConnecting to Remotive API...")

    try:
        response = requests.get(
            API_URL,
            timeout=30,
            headers={"User-Agent": "JobHunterAI/0.1"},
        )

        response.raise_for_status()

        print(f"HTTP Status Code: {response.status_code}")
        print(f"Response URL: {response.url}")

        data = response.json()
        jobs = data.get("jobs", [])

        if not isinstance(jobs, list):
            raise ValueError("Unexpected API response")

        print(f"Successfully retrieved {len(jobs)} job listings.")

        # Debugging: inspect the returned job titles.
        print("\nDEBUG: Jobs returned by Remotive")

        for job in jobs:
            print(
                f"Title: {job.get('title', 'Unknown')} | "
                f"Company: {job.get('company_name', 'Unknown')}"
            )

        return jobs

    except (requests.RequestException, ValueError) as error:
        print(f"Error retrieving jobs: {error}")
        return None


    except (requests.RequestException, ValueError) as error:
        print(f"Error retrieving jobs: {error}")
        return None


def filter_jobs(jobs):
    """Filter jobs by relevant engineering titles."""

    matching_jobs = []

    for job in jobs:
        title = job.get("title", "").lower()

        relevant = any(
            keyword in title for keyword in TARGET_TITLES
        )

        excluded = any(
            keyword in title for keyword in EXCLUDED_TITLES
        )

        if relevant and not excluded:
            matching_jobs.append(job)

    return matching_jobs


def display_jobs(jobs):
    """Display job opportunities in the terminal."""

    print(f"\nFound {len(jobs)} matching positions.\n")

    for index, job in enumerate(jobs, start=1):
        print("-" * 60)
        print(f"JOB #{index}")
        print(f"Title: {job.get('title', 'Unknown')}")
        print(f"Company: {job.get('company_name', 'Unknown')}")
        print(
            "Location: "
            f"{job.get('candidate_required_location', 'Not specified')}"
        )
        print(f"Salary: {job.get('salary') or 'Not listed'}")
        print(f"Published: {job.get('publication_date', 'Unknown')}")
        print(f"Source: Remotive")
        print(f"Apply: {job.get('url', '')}")
