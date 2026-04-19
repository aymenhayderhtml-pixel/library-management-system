import os
from agentmail import AgentMail

api_key = "am_us_3d90eda14ab243b14dbaad64a877c5b265b76d7150eb4d2fab981ee9adf56328"
inbox_id = "openclaw11@agentmail.to"

client = AgentMail(api_key=api_key)

try:
    messages = client.inboxes.messages.list(inbox_id=inbox_id, limit=10)
    print(f"Found {len(messages.messages)} recent messages:\n")
    for msg in messages.messages:
        print(f"From: {msg.from_}")
        print(f"Subject: {msg.subject or '[No subject]'}")
        print(f"Date: {msg.created_at}")
        print(f"Preview: {msg.preview[:200] if msg.preview else '[No preview]'}")
        print(f"Labels: {msg.labels}")
        print("-" * 50)
except Exception as e:
    print(f"Error: {e}")
