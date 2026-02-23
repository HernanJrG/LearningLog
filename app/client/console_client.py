import os
import sys
import time
from datetime import date
from typing import Any, Dict, Optional

import requests


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        response = self.session.request(method=method, url=url, timeout=20, **kwargs)
        if response.status_code >= 400:
            detail = response.text
            try:
                detail = response.json()
            except ValueError:
                pass
            raise RuntimeError(f"{method} {path} failed ({response.status_code}): {detail}")

        if not response.content:
            return None
        return response.json()


def prompt_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def print_json(title: str, payload: Any):
    print(f"\n{title}")
    print("-" * len(title))
    print(payload)


def run_full_smoke_test(client: ApiClient):
    timestamp = int(time.time())
    suffix = str(timestamp)

    created_ids: Dict[str, Optional[str]] = {
        "user_id": None,
        "topic_id": None,
        "resource_id": None,
        "session_id": None,
        "reflection_id": None,
    }

    print("\nRunning full CRUD smoke test...")

    try:
        user_email = f"project2.user.{suffix}@example.com"
        user = client.request(
            "POST",
            "/users",
            json={"full_name": f"Project2 User {suffix}", "email": user_email},
        )
        created_ids["user_id"] = user["id"]
        print_json("Created user", user)

        print_json("Get user by id", client.request("GET", f"/users/{created_ids['user_id']}"))
        print_json("Get user by email", client.request("GET", "/users/by-email", params={"email": user_email}))
        print_json("List users", client.request("GET", "/users"))

        user = client.request(
            "PUT",
            f"/users/{created_ids['user_id']}",
            json={"full_name": f"Project2 User Updated {suffix}", "email": user_email},
        )
        print_json("Updated user", user)

        topic = client.request(
            "POST",
            "/topics",
            json={
                "user_id": created_ids["user_id"],
                "name": f"Project2 Topic {suffix}",
                "description": "Created by smoke test",
            },
        )
        created_ids["topic_id"] = topic["id"]
        print_json("Created topic", topic)
        print_json("Get topic by id", client.request("GET", f"/topics/{created_ids['topic_id']}"))
        print_json("List all topics", client.request("GET", "/topics"))
        print_json(
            "List topics by user",
            client.request("GET", "/topics", params={"user_id": created_ids["user_id"]}),
        )

        topic = client.request(
            "PUT",
            f"/topics/{created_ids['topic_id']}",
            json={
                "name": f"Project2 Topic Updated {suffix}",
                "description": "Updated by smoke test",
            },
        )
        print_json("Updated topic", topic)

        resource = client.request(
            "POST",
            "/resources",
            json={
                "topic_id": created_ids["topic_id"],
                "title": f"Project2 Resource {suffix}",
                "url": "https://example.com/project2-resource",
                "resource_type": "article",
            },
        )
        created_ids["resource_id"] = resource["id"]
        print_json("Created resource", resource)
        print_json(
            "Get resource by id",
            client.request("GET", f"/resources/{created_ids['resource_id']}"),
        )
        print_json(
            "List resources by topic",
            client.request("GET", "/resources", params={"topic_id": created_ids["topic_id"]}),
        )

        resource = client.request(
            "PUT",
            f"/resources/{created_ids['resource_id']}",
            json={
                "title": f"Project2 Resource Updated {suffix}",
                "url": "https://example.com/project2-resource-updated",
                "resource_type": "video",
            },
        )
        print_json("Updated resource", resource)

        session = client.request(
            "POST",
            "/sessions",
            json={
                "user_id": created_ids["user_id"],
                "topic_id": created_ids["topic_id"],
                "session_date": date.today().isoformat(),
                "duration_minutes": 45,
                "notes": "Smoke-test learning session",
            },
        )
        created_ids["session_id"] = session["id"]
        print_json("Created learning session", session)
        print_json(
            "Get session by id",
            client.request("GET", f"/sessions/{created_ids['session_id']}"),
        )
        print_json(
            "List sessions by user",
            client.request("GET", "/sessions", params={"user_id": created_ids["user_id"]}),
        )
        print_json(
            "List sessions by topic",
            client.request("GET", "/sessions", params={"topic_id": created_ids["topic_id"]}),
        )

        session = client.request(
            "PUT",
            f"/sessions/{created_ids['session_id']}",
            json={
                "session_date": date.today().isoformat(),
                "duration_minutes": 60,
                "notes": "Updated smoke-test learning session",
            },
        )
        print_json("Updated session", session)

        reflection = client.request(
            "POST",
            "/reflections",
            json={
                "session_id": created_ids["session_id"],
                "rating": 5,
                "summary": "Smoke test reflection",
            },
        )
        created_ids["reflection_id"] = reflection["id"]
        print_json("Created reflection", reflection)
        print_json(
            "Get reflection by id",
            client.request("GET", f"/reflections/{created_ids['reflection_id']}"),
        )
        print_json(
            "List reflections by session",
            client.request("GET", "/reflections", params={"session_id": created_ids["session_id"]}),
        )
        print_json(
            "List reflections by topic",
            client.request("GET", "/reflections", params={"topic_id": created_ids["topic_id"]}),
        )

        reflection = client.request(
            "PUT",
            f"/reflections/{created_ids['reflection_id']}",
            json={"rating": 4, "summary": "Updated smoke test reflection"},
        )
        print_json("Updated reflection", reflection)

        print("\nSmoke test finished successfully.")
    finally:
        # Cleanup runs in reverse order so relational constraints are satisfied.
        cleanup_steps = [
            ("reflection_id", "/reflections"),
            ("session_id", "/sessions"),
            ("resource_id", "/resources"),
            ("topic_id", "/topics"),
            ("user_id", "/users"),
        ]
        for key, path in cleanup_steps:
            record_id = created_ids.get(key)
            if not record_id:
                continue
            try:
                result = client.request("DELETE", f"{path}/{record_id}")
                print_json(f"Cleanup {key}", result)
            except Exception as exc:  # noqa: BLE001
                print(f"Cleanup warning for {key}: {exc}")


def create_user(client: ApiClient):
    full_name = prompt_non_empty("Full name: ")
    email = prompt_non_empty("Email: ")
    result = client.request("POST", "/users", json={"full_name": full_name, "email": email})
    print_json("Created user", result)


def list_users(client: ApiClient):
    result = client.request("GET", "/users")
    print_json("Users", result)


def main():
    default_url = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    if len(sys.argv) > 1:
        default_url = sys.argv[1]

    base_url = input(f"Service URL [{default_url}]: ").strip() or default_url
    client = ApiClient(base_url)

    while True:
        print(
            """
Console Service Client
======================
1. Run full CRUD smoke test (all entities)
2. List users
3. Create user
0. Exit
"""
        )
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            return
        try:
            if choice == "1":
                run_full_smoke_test(client)
            elif choice == "2":
                list_users(client)
            elif choice == "3":
                create_user(client)
            else:
                print("Invalid option.")
        except Exception as exc:  # noqa: BLE001
            print(f"Error: {exc}")


if __name__ == "__main__":
    main()

