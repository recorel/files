import base64
import getpass
import json
import requests

URL = "https://ossindex.sonatype.org/api/v3/component-report"

# Prompt for credentials
username = input("Username (email): ")
password = getpass.getpass("Password / API token: ")

# Generate HTTP Basic Authentication token
credentials = f"{username}:{password}"
token = base64.b64encode(credentials.encode("utf-8")).decode("ascii")

# Prepare request
headers = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Components to scan
payload = {
    "coordinates": [
        "pkg:maven/org.apache.commons/commons-lang3@3.12.0"
    ]
}

try:
    response = requests.post(
        URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    response.raise_for_status()

    report = response.json()

    with open("ossindex_report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("Report saved to ossindex_report.json")

except requests.exceptions.RequestException as error:
    print(f"Request failed: {error}")
