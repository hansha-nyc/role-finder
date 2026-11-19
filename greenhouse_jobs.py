
import json
from pathlib import Path

import requests


def load_company_boards():
    """Load configured employer job boards."""

    config_path = (
        Path(__file__).resolve().parent
        / "company_boards.json"
    )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = json.load(file)

    return [
        board
        for board in config.get("greenhouse", [])
        if board.get("enabled", False)
    ]


def fetch_greenhouse_jobs():
    """Retrieve jobs from enabled Greenhouse boards."""

    all_jobs = []

    boards = load_company_boards()

    for board in boards:
        company = board["company"]
        token = board["board_token"]

        url = (
            "https://boards-api.greenhouse.io/v1/"
            f"boards/{token}/jobs"
        )

        print(f"\nSearching Greenhouse: {company}")

        try:
            response = requests.get(
                url,
                params={"content": "true"},
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()
            jobs = data.get("jobs", [])

            if not isinstance(jobs, list):
                raise ValueError("Invalid jobs response")

            print(f"Retrieved {len(jobs)} positions")

            for job in jobs:
                if job.get("internal_job_id") is None:
                    continue

                all_jobs.append({
                    "id": f"greenhouse:{token}:{job['id']}",
                    "source": "Greenhouse",
                    "company": company,
                    "title": job.get("title", ""),
                    "location": (
                        job.get("location") or {}
                    ).get("name", ""),
                    "url": job.get("absolute_url", ""),
                    "description": job.get("content", ""),
                    "published": None,
                    "updated": job.get("updated_at"),
                    "salary": None,
                })

        except (
            requests.RequestException,
            ValueError,
            KeyError,
        ) as error:
            print(f"Error retrieving {company}: {error}")

    return all_jobs

