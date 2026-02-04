from datetime import datetime
from typing import Optional

from app.daos.learning_sessions import LearningSessionDAO
from app.daos.reflections import ReflectionDAO
from app.daos.resources import ResourceDAO
from app.daos.topics import TopicDAO
from app.daos.users import UserDAO


MENU = """
Personal Knowledge & Learning Tracker
====================================
1. View all topics
2. Add a new topic
3. Add a resource to a topic
4. Log a learning session
5. Add a reflection to a session
6. View reflections for a topic
7. Update a topic
8. Delete a topic
9. Update a resource
10. Delete a resource
11. Update a learning session
12. Delete a learning session
13. Update a reflection
14. Delete a reflection
0. Exit
"""


def prompt_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def prompt_optional(prompt: str):
    value = input(prompt).strip()
    return value if value else None


def prompt_int(prompt: str, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("Please enter a number.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("Please enter a valid number.")
            continue
        if min_value is not None and value < min_value:
            print(f"Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value must be at most {max_value}.")
            continue
        return value


def prompt_date(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Please use YYYY-MM-DD.")


def prompt_date_optional(prompt: str, current_value: str) -> str:
    value = input(prompt).strip()
    if value == "":
        return current_value
    while True:
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            value = input("Please use YYYY-MM-DD: ").strip()


def prompt_int_optional(
    prompt: str,
    current_value: int,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    value = input(prompt).strip()
    if value == "":
        return current_value
    while True:
        try:
            parsed = int(value)
        except ValueError:
            value = input("Please enter a valid number: ").strip()
            continue
        if min_value is not None and parsed < min_value:
            value = input(f"Value must be at least {min_value}: ").strip()
            continue
        if max_value is not None and parsed > max_value:
            value = input(f"Value must be at most {max_value}: ").strip()
            continue
        return parsed


def choose_from_list(items, label_fn, allow_cancel: bool = True):
    if not items:
        print("No records found.")
        return None
    for idx, item in enumerate(items, start=1):
        print(f"{idx}. {label_fn(item)}")
    if allow_cancel:
        print("0. Cancel")
    max_choice = len(items)
    choice = prompt_int("Select an option: ", 0 if allow_cancel else 1, max_choice)
    if allow_cancel and choice == 0:
        return None
    return items[choice - 1]


def select_user(user_dao: UserDAO):
    while True:
        users = user_dao.list_all()
        if not users:
            print("No users found. Create one to get started.")
            return create_user(user_dao)

        print("\nChoose a user:")
        for idx, user in enumerate(users, start=1):
            print(f"{idx}. {user['full_name']} ({user['email']})")
        print("0. Exit")
        print("C. Create a new user")

        raw = input("Select an option: ").strip()
        if raw == "0":
            return None
        if raw.lower() in ("c", "n", "new"):
            return create_user(user_dao)
        try:
            choice = int(raw)
        except ValueError:
            print("Please enter a number, or 'C' to create a new user.")
            continue
        if 1 <= choice <= len(users):
            return users[choice - 1]
        print("Please choose a valid option.")


def create_user(user_dao: UserDAO):
    full_name = prompt_non_empty("Full name: ")
    email = prompt_non_empty("Email: ")
    user_id = user_dao.create(full_name, email)
    return user_dao.get_by_id(user_id)


def view_topics(topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    if not topics:
        print("No topics found.")
        return
    print("\nTopics:")
    for topic in topics:
        description = topic["description"] or "(no description)"
        print(f"- {topic['name']}: {description} [id={topic['id']}]")


def add_topic(topic_dao: TopicDAO, user_id):
    name = prompt_non_empty("Topic name: ")
    description = prompt_optional("Description (optional): ")
    topic_id = topic_dao.create(user_id, name, description)
    print(f"Created topic with id {topic_id}.")


def add_resource(resource_dao: ResourceDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    title = prompt_non_empty("Resource title: ")
    url = prompt_non_empty("Resource URL: ")
    resource_type = prompt_non_empty("Resource type (article, video, book, etc.): ")
    resource_id = resource_dao.create(topic["id"], title, url, resource_type)
    print(f"Created resource with id {resource_id}.")


def log_session(session_dao: LearningSessionDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    session_date = prompt_date("Session date (YYYY-MM-DD): ")
    duration = prompt_int("Duration in minutes: ", 1)
    notes = prompt_optional("Notes (optional): ")
    session_id = session_dao.create(user_id, topic["id"], session_date, duration, notes)
    print(f"Logged session with id {session_id}.")


def add_reflection(reflection_dao: ReflectionDAO, session_dao: LearningSessionDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    sessions = session_dao.list_by_topic(topic["id"])
    session = choose_from_list(
        sessions,
        lambda s: f"{s['session_date']} ({s['duration_minutes']} min)",
    )
    if not session:
        return
    rating = prompt_int("Rating (1-5): ", 1, 5)
    summary = prompt_non_empty("Reflection summary: ")
    reflection_id = reflection_dao.create(session["id"], rating, summary)
    print(f"Added reflection with id {reflection_id}.")


def view_reflections(reflection_dao: ReflectionDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    reflections = reflection_dao.list_by_topic(topic["id"])
    if not reflections:
        print("No reflections found for this topic.")
        return
    print("\nReflections:")
    for reflection in reflections:
        print(f"- Rating {reflection['rating']}: {reflection['summary']} (session {reflection['session_id']})")


def update_topic(topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    name = input(f"New name [{topic['name']}]: ").strip() or topic["name"]
    description_input = input(
        f"New description [{topic['description'] or 'none'}] (use '-' to clear): "
    ).strip()
    if description_input == "-":
        description = None
    elif description_input == "":
        description = topic["description"]
    else:
        description = description_input
    if topic_dao.update(topic["id"], name, description):
        print("Topic updated.")
    else:
        print("Topic update failed.")


def delete_topic(topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    confirm = input("Type DELETE to confirm topic deletion: ").strip()
    if confirm != "DELETE":
        print("Deletion cancelled.")
        return
    if topic_dao.delete(topic["id"]):
        print("Topic deleted (related resources/sessions/reflections removed).")
    else:
        print("Topic deletion failed.")


def update_resource(resource_dao: ResourceDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    resources = resource_dao.list_by_topic(topic["id"])
    resource = choose_from_list(resources, lambda r: r["title"])
    if not resource:
        return
    title = input(f"New title [{resource['title']}]: ").strip() or resource["title"]
    url = input(f"New URL [{resource['url']}]: ").strip() or resource["url"]
    resource_type = (
        input(f"New type [{resource['resource_type']}]: ").strip() or resource["resource_type"]
    )
    if resource_dao.update(resource["id"], title, url, resource_type):
        print("Resource updated.")
    else:
        print("Resource update failed.")


def delete_resource(resource_dao: ResourceDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    resources = resource_dao.list_by_topic(topic["id"])
    resource = choose_from_list(resources, lambda r: r["title"])
    if not resource:
        return
    confirm = input("Type DELETE to confirm resource deletion: ").strip()
    if confirm != "DELETE":
        print("Deletion cancelled.")
        return
    if resource_dao.delete(resource["id"]):
        print("Resource deleted.")
    else:
        print("Resource deletion failed.")


def update_session(session_dao: LearningSessionDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    sessions = session_dao.list_by_topic(topic["id"])
    session = choose_from_list(
        sessions,
        lambda s: f"{s['session_date']} ({s['duration_minutes']} min)",
    )
    if not session:
        return
    session_date = prompt_date_optional(
        f"New date [{session['session_date']}] (YYYY-MM-DD): ",
        session["session_date"],
    )
    duration = prompt_int_optional(
        f"New duration [{session['duration_minutes']}]: ",
        session["duration_minutes"],
        1,
    )
    notes_input = input(
        f"New notes [{session['notes'] or 'none'}] (use '-' to clear): "
    ).strip()
    if notes_input == "-":
        notes = None
    elif notes_input == "":
        notes = session["notes"]
    else:
        notes = notes_input
    if session_dao.update(session["id"], session_date, duration, notes):
        print("Learning session updated.")
    else:
        print("Learning session update failed.")


def delete_session(session_dao: LearningSessionDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    sessions = session_dao.list_by_topic(topic["id"])
    session = choose_from_list(
        sessions,
        lambda s: f"{s['session_date']} ({s['duration_minutes']} min)",
    )
    if not session:
        return
    confirm = input("Type DELETE to confirm session deletion: ").strip()
    if confirm != "DELETE":
        print("Deletion cancelled.")
        return
    if session_dao.delete(session["id"]):
        print("Learning session deleted (related reflections removed).")
    else:
        print("Learning session deletion failed.")


def update_reflection(reflection_dao: ReflectionDAO, session_dao: LearningSessionDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    sessions = session_dao.list_by_topic(topic["id"])
    session = choose_from_list(
        sessions,
        lambda s: f"{s['session_date']} ({s['duration_minutes']} min)",
    )
    if not session:
        return
    reflections = reflection_dao.list_by_session(session["id"])
    reflection = choose_from_list(
        reflections,
        lambda r: f"Rating {r['rating']}: {r['summary']}",
    )
    if not reflection:
        return
    rating = prompt_int("New rating (1-5): ", 1, 5)
    summary = prompt_non_empty("New summary: ")
    if reflection_dao.update(reflection["id"], rating, summary):
        print("Reflection updated.")
    else:
        print("Reflection update failed.")


def delete_reflection(reflection_dao: ReflectionDAO, session_dao: LearningSessionDAO, topic_dao: TopicDAO, user_id):
    topics = topic_dao.list_by_user(user_id)
    topic = choose_from_list(topics, lambda t: t["name"])
    if not topic:
        return
    sessions = session_dao.list_by_topic(topic["id"])
    session = choose_from_list(
        sessions,
        lambda s: f"{s['session_date']} ({s['duration_minutes']} min)",
    )
    if not session:
        return
    reflections = reflection_dao.list_by_session(session["id"])
    reflection = choose_from_list(
        reflections,
        lambda r: f"Rating {r['rating']}: {r['summary']}",
    )
    if not reflection:
        return
    confirm = input("Type DELETE to confirm reflection deletion: ").strip()
    if confirm != "DELETE":
        print("Deletion cancelled.")
        return
    if reflection_dao.delete(reflection["id"]):
        print("Reflection deleted.")
    else:
        print("Reflection deletion failed.")


def run():
    try:
        user_dao = UserDAO()
        topic_dao = TopicDAO()
        resource_dao = ResourceDAO()
        session_dao = LearningSessionDAO()
        reflection_dao = ReflectionDAO()

        current_user = select_user(user_dao)
        if not current_user:
            print("Goodbye.")
            return
        print(f"\nWelcome, {current_user['full_name']}!\n")

        while True:
            print(MENU)
            choice = prompt_int("Choose an option: ", 0, 14)
            if choice == 0:
                print("Goodbye.")
                return
            if choice == 1:
                view_topics(topic_dao, current_user["id"])
            elif choice == 2:
                add_topic(topic_dao, current_user["id"])
            elif choice == 3:
                add_resource(resource_dao, topic_dao, current_user["id"])
            elif choice == 4:
                log_session(session_dao, topic_dao, current_user["id"])
            elif choice == 5:
                add_reflection(reflection_dao, session_dao, topic_dao, current_user["id"])
            elif choice == 6:
                view_reflections(reflection_dao, topic_dao, current_user["id"])
            elif choice == 7:
                update_topic(topic_dao, current_user["id"])
            elif choice == 8:
                delete_topic(topic_dao, current_user["id"])
            elif choice == 9:
                update_resource(resource_dao, topic_dao, current_user["id"])
            elif choice == 10:
                delete_resource(resource_dao, topic_dao, current_user["id"])
            elif choice == 11:
                update_session(session_dao, topic_dao, current_user["id"])
            elif choice == 12:
                delete_session(session_dao, topic_dao, current_user["id"])
            elif choice == 13:
                update_reflection(reflection_dao, session_dao, topic_dao, current_user["id"])
            elif choice == 14:
                delete_reflection(reflection_dao, session_dao, topic_dao, current_user["id"])
    except KeyboardInterrupt:
        print("\nGoodbye.")
        return
