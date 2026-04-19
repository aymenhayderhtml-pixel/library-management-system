import os
import json
import urllib.request

api_key = os.getenv('AGENTMAIL_API_KEY')
base_url = 'https://api.agentmail.to/v0'

def api_request(method, path, data=None):
    url = base_url + path
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }
    if data:
        body = json.dumps(data).encode('utf-8')
    else:
        body = None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            resp_body = response.read().decode('utf-8')
            return json.loads(resp_body), response.status
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        return {'error': error_body}, e.code

# Create inbox
create_data = {
    'username': 'openclaw-assistant',
    'display_name': 'OpenClaw Assistant',
    'client_id': 'openclaw-assistant-inbox'
}
result, status = api_request('POST', '/inboxes', create_data)
if status != 201:
    # Creation failed, likely because inbox is taken or another issue.
    # List inboxes and pick the first one available.
    list_result, list_status = api_request('GET', '/inboxes?limit=10')
    if list_status == 200:
        inboxes = list_result.get('inboxes', [])
        if not inboxes:
            print('No inboxes found.')
            exit(1)
        # Use the first inbox
        inbox_id = inboxes[0]['inbox_id']
        print('Using existing inbox: ' + inbox_id)
    else:
        print('Failed to list inboxes.')
        exit(1)
else:
    inbox_id = result['inbox_id']
    print('Created inbox: ' + inbox_id)

# Send email
send_data = {
    'to': 'hayderaymen.html@gmail.com',
    'subject': 'Test from OpenClaw',
    'text': 'AgentMail skill is now working perfectly \u2729'  # using unicode escape for the emoji
}
send_resp, send_status = api_request('POST', '/inboxes/' + inbox_id + '/messages', send_data)
if send_status == 201:
    msg = send_resp
    print('Email sent! Message ID: ' + msg['message_id'])
else:
    print('Failed to send email: ' + str(send_status) + ' ' + json.dumps(send_resp))
