
import requests
import json

# Replace with your actual username and password
username = 'superuser'
password = 'superuser'

# 1. Authenticate and get token
auth_url = 'http://127.0.0.1:8000/auth/jwt/create/'
auth_data = {'username': username, 'password': password}
response = requests.post(auth_url, data=auth_data)

if response.status_code != 200:
    print(f'Authentication failed: {response.text}')
    exit()

token = response.json()['access']
headers = {'Authorization': f'Bearer {token}'}

# 2. Create a Room
room_url = 'http://127.0.0.1:8000/smarthome/rooms/'
room_data = {'name': 'Living Room'}
response = requests.post(room_url, data=room_data, headers=headers)

if response.status_code != 201:
    print(f'Failed to create room: {response.text}')
    exit()

room = response.json()
print(f'Successfully created room: {room["name"]}')

# 3. Create an Appliance Category
category_url = 'http://127.0.0.1:8000/smarthome/appliance-categories/'
category_data = {'name': 'Lighting'}
# This endpoint requires superuser privileges, which we have.
response = requests.post(category_url, data=category_data, headers=headers)

# If category already exists, get it
if response.status_code == 400 and 'unique' in response.text:
    response = requests.get(category_url, headers=headers)
    category = next((c for c in response.json() if c['name'] == 'Lighting'), None)
    if not category:
        print(f'Failed to get appliance category: {response.text}')
        exit()
else:
    if response.status_code != 201:
        print(f'Failed to create appliance category: {response.text}')
        exit()
    category = response.json()

print(f'Using appliance category: {category["name"]}')


# 4. Create an Appliance
appliance_url = 'http://127.0.0.1:8000/smarthome/appliances/'
appliance_data = {
    'name': 'Living Room Lamp',
    'category': category['id'],
    'room': room['id']
}
response = requests.post(appliance_url, data=appliance_data, headers=headers)

if response.status_code != 201:
    print(f'Failed to create appliance: {response.text}')
    exit()

appliance = response.json()
print(f'Successfully created appliance: {appliance["name"]}')

# 5. Verify the appliance is in the room
response = requests.get(f'{room_url}{room["id"]}/', headers=headers)
room_details = response.json()

response = requests.get(f'{appliance_url}{appliance["id"]}/', headers=headers)
appliance_details = response.json()

if appliance_details['room'] == room['id']:
    print(f'Successfully assigned appliance {appliance["name"]} to room {room["name"]}.')
else:
    print(f'Failed to assign appliance to room.')

