
from config import (
    TITLE_KEYWORDS,
    EXCLUDED_TITLE_KEYWORDS,
    LOCATION_KEYWORDS,
    EXCLUDED_COMPANIES
)


def matches_title(job):
    title = job.get("title", "").lower()

    included = any(
        keyword in title
        for keyword in TITLE_KEYWORDS
    )

    excluded = any(
        keyword in title
        for keyword in EXCLUDED_TITLE_KEYWORDS
    )

    return included and not excluded


def matches_location(job):
    location = job.get("location", "").lower()

    return any(
        keyword in location
        for keyword in LOCATION_KEYWORDS
    )


def matches_company(job):
    company = job.get("company", "").strip().casefold()

    excluded = {
        name.strip().casefold()
        for name in EXCLUDED_COMPANIES
    }

    return company not in excluded

#def filter_jobs(jobs):
#    return [
#        job
#        for job in jobs
#        if matches_title(job) and matches_location(job)
#    ]

def filter_jobs(jobs):
    return [
        job
        for job in jobs
        if (
            matches_title(job)
            and matches_location(job)
            and matches_company(job)
        )
    ]


def deduplicate_jobs(jobs):
    unique_jobs = {}

    for job in jobs:
        # Prefer the application URL as a unique key.
        key = job.get("url") or job.get("id")

        if key:
            unique_jobs[key] = job

    return list(unique_jobs.values())


def debug_filters(jobs):
    """Explain how many jobs pass each filtering stage."""

    title_matches = [
        job for job in jobs
        if matches_title(job)
    ]

    location_matches = [
        job for job in jobs
        if matches_location(job)
    ]

    both_matches = [
        job for job in jobs
        if matches_title(job) and matches_location(job)
    ]

    print("\n========== FILTER DIAGNOSTICS ==========")
    print(f"Total jobs: {len(jobs)}")
    print(f"Title matches: {len(title_matches)}")
    print(f"Location matches: {len(location_matches)}")
    print(f"Both conditions: {len(both_matches)}")

    print("\nJobs matching our target titles:")

    for job in title_matches:
        print(
            f"  {job['title']} | "
            f"{job['company']} | "
            f"{job['location']}"
        )

    print("========================================")
