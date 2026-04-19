from agentmail import AgentMail
import os

client = AgentMail(api_key=os.getenv('AGENTMAIL_API_KEY'))
response = client.inboxes.messages.send(
    inbox_id='openclaw11@agentmail.to',
    to='hayderaymen.html@gmail.com',
    subject='Test from OpenClaw',
    text='AgentMail skill is now working perfectly \u2729'
)
print('Email sent! Message ID:', response.message_id)
