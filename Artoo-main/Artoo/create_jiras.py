import os
import requests
from requests.auth import HTTPBasicAuth

JIRA_URL = "https://anandinfinity0007.atlassian.net"
JIRA_USER = "<email>"
JIRA_TOKEN = "<token>"
PROJECT_KEY = "IN"

auth = HTTPBasicAuth(JIRA_USER, JIRA_TOKEN)
headers = {"Accept": "application/json", "Content-Type": "application/json"}

# Fetch valid issue types for project
url = f"{JIRA_URL}/rest/api/3/project/{PROJECT_KEY}"
response = requests.get(url, headers=headers, auth=auth)
proj_data = response.json()
types = proj_data.get("issueTypes", [])
issue_type_id = types[0]["id"] if types else "10001"

def create_issue(summary, desc_text):
    payload = {
        "fields": {
           "project": {"key": PROJECT_KEY},
           "summary": summary,
           "description": {
               "type": "doc",
               "version": 1,
               "content": [
                   {
                       "type": "paragraph",
                       "content": [
                           {"type": "text", "text": desc_text}
                       ]
                   }
               ]
           },
           "issuetype": {"id": issue_type_id}
        }
    }
    resp = requests.post(f"{JIRA_URL}/rest/api/3/issue", json=payload, headers=headers, auth=auth)
    print(resp.status_code, resp.text)

desc_12 = """The GET /todos endpoint currently returns all todos regardless of their due_date.
We need to add optional query parameters to filter todos by due date range.

Users should be able to:
- Filter todos due before a specific date (due_before=2025-12-31)
- Filter todos due after a specific date (due_after=2025-01-01)
- Combine both filters to get todos in a date range

The filters should be optional — if not provided, return all todos as before.
Date format should follow ISO 8601 (YYYY-MM-DD).

Acceptance Criteria:
- GET /todos?due_before=2025-12-31 returns only todos with due_date <= 2025-12-31
- GET /todos?due_after=2025-01-01 returns only todos with due_date >= 2025-01-01
- Both filters can be combined in the same request
- If no filter is provided, all todos are returned (existing behaviour preserved)
- Invalid date formats return HTTP 422 with a clear error message
- Unit tests cover all three filter combinations"""

desc_13 = """Currently the Todo API has no authentication — any user can read and modify all todos.
We need to add JWT-based authentication so each user only sees their own todos.

Implementation required:
- Add a User model with email and hashed password fields
- POST /auth/register — create a new user account
- POST /auth/login — returns a JWT access token
- All /todos endpoints must require a valid Bearer token
- Each todo should have an owner_id foreign key linking to the User table
- Users can only read and modify their own todos

Acceptance Criteria:
- POST /auth/register with email + password creates a user and returns HTTP 201
- POST /auth/login with valid credentials returns {"access_token": "...", "token_type": "bearer"}
- POST /auth/login with wrong password returns HTTP 401
- GET /todos without a token returns HTTP 401
- GET /todos with a valid token returns only that user's todos
- Passwords are stored as bcrypt hashes, never as plain text"""

desc_14 = """We need search."""

create_issue("Add due date filtering to the Todo list endpoint", desc_12)
create_issue("Add user authentication to the Todo API", desc_13)
create_issue("Add search functionality", desc_14)
