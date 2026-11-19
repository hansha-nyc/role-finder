# codebase for a python tool to find criteria-based roles
# Antman - Earth - Milkyway - Galaxy


import json
from pathlib import Path
from datetime import datetime, timezone

from jobs import fetch_jobs
from greenhouse_jobs import fetch_greenhouse_jobs
from job_filters import filter_jobs, deduplicate_jobs, debug_filters


def normalize_remotive_jobs(jobs):
    normalized = []

    for job in jobs:
        normalized.append({
            "id": f"remotive:{job.get('id')}",
            "source": "Remotive",
            "company": job.get("company_name", ""),
            "title": job.get("title", ""),
            "location": job.get(
                "candidate_required_location", ""
            ),
            "url": job.get("url", ""),
            "description": job.get("description", ""),
            "published": job.get("publication_date"),
            "updated": None,
            "salary": job.get("salary"),
        })

    return normalized


def main():
    print("=" * 55)
    print("AI Agents Jobs - MULTI-SOURCE JOB DISCOVERY")
    print("=" * 55)

    print(
        f"Started: {datetime.now(timezone.utc).isoformat()}"
    )

    # Source 1: Remotive
    remotive_raw = fetch_jobs() or []
    remotive_jobs = normalize_remotive_jobs(remotive_raw)

    # Source 2: Greenhouse
    greenhouse_jobs = fetch_greenhouse_jobs()

    # Combine results.
    all_jobs = remotive_jobs + greenhouse_jobs

    debug_filters(all_jobs)

    print(f"\nTotal jobs collected: {len(all_jobs)}")

    # Filter by title and location.
    matching_jobs = filter_jobs(all_jobs)

    # Remove duplicates.
    matching_jobs = deduplicate_jobs(matching_jobs)

    print(f"Matching jobs: {len(matching_jobs)}")

    # Display results.
    for index, job in enumerate(matching_jobs, start=1):
        print("\n" + "-" * 55)
        print(f"JOB #{index}")
        print(f"Company: {job['company']}")
        print(f"Title: {job['title']}")
        print(f"Location: {job['location']}")
        print(f"Source: {job['source']}")
        print(f"Apply: {job['url']}")

    # Save results.
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "jobs.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(
            matching_jobs,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(f"\nSaved results to {output_file}")


if __name__ == "__main__":
    main()



