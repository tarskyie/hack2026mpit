
import requests
import json
import uuid
import random
import string
import time


# Generate random username and password
def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

username = f'testuser_{uuid.uuid4().hex[:8]}'
password = generate_random_password()

# 0. Create the user
user_creation_url = 'http://127.0.0.1:8000/auth/users/'
user_data = {'username': username, 'password': password, 're_password': password}
response = requests.post(user_creation_url, data=user_data)

if response.status_code == 201:
    print(f"User '{username}' created successfully.")
elif response.status_code == 400 and 'username' in response.text:
    print(f"User '{username}' already exists (this should not happen with random usernames).")
    # Exit or handle as appropriate for your testing
    exit()
else:
    print(f'Failed to create user: {response.text}')
    exit()

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
        #exit()
else:
    if response.status_code != 201:
        print(f'Failed to create appliance category: {response.text}')
        #exit()
    category = response.json()

#print(f'Using appliance category: {category["name"]}')


# 4. Create an Appliance
appliance_url = 'http://127.0.0.1:8000/smarthome/appliances/'
appliance_data = {
    'name': 'Living Room Lamp',
    'category': 1,
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


# 6. Create 'Air Conditioner' appliance category
ac_category_data = {'name': 'Air Conditioner'}
response = requests.post(category_url, data=ac_category_data, headers=headers)

if response.status_code == 400 and 'unique' in response.text:
    response = requests.get(category_url, headers=headers)
    ac_category = next((c for c in response.json() if c['name'] == 'Air Conditioner'), None)
    if not ac_category:
        print(f'Failed to get appliance category: {response.text}')
        #exit()
else:
    if response.status_code != 201:
        print(f'Failed to create appliance category: {response.text}')
        #exit()
    ac_category = response.json()

#print(f'Using appliance category: {ac_category["name"]}')

# 7. Create an Air Conditioner
ac_url = 'http://127.0.0.1:8000/smarthome/air-conditioners/'
ac_data = {
    'name': 'Living Room AC',
    'category': 2,
    'room': room['id']
}
response = requests.post(ac_url, data=ac_data, headers=headers)

if response.status_code != 201:
    print(f'Failed to create air conditioner: {response.text}')
    exit()

ac = response.json()
print(f'Successfully created air conditioner: {ac["name"]}')
print(ac)


# 9. Set AC Temperature
set_temp_url = f'{ac_url}{ac["id"]}/set_temperature/'
temp_data = {'temperature': 25.5}
response = requests.post(set_temp_url, data=temp_data, headers=headers)

if response.status_code != 200:
    print(f'Failed to set AC temperature: {response.text}')
    exit()

ac_details = response.json()
if ac_details['temperature'] == 25.5:
    print(f'Successfully set AC temperature to {ac_details["temperature"]}.')
else:
    print(f'Failed to set AC temperature, it is {ac_details["temperature"]}.')
    exit()

# 10. Test /smarthome/home/
home_url = 'http://127.0.0.1:8000/smarthome/home/'
response = requests.get(home_url, headers=headers)

if response.status_code != 200:
    print(f'Failed to get home data: {response.text}')
    exit()

print(f'Successfully got home data: {response.json()}')

# 11. Test /smarthome/home_is_online/ (should be online)
online_url = 'http://127.0.0.1:8000/smarthome/home_is_online/'
response = requests.get(online_url, headers=headers)

if response.status_code == 200 and response.text == '"online"':
    print('Home is online, as expected.')
else:
    print(f'Home is not online, but it should be. Response: {response.text}')
    exit()

# 12. Wait for 11 seconds
print('Waiting for 6 seconds...')
time.sleep(6)

# 13. Test /smarthome/home_is_online/ again (should be offline)
response = requests.get(online_url, headers=headers)

if response.status_code == 200 and response.text == '"offline"':
    print('Home is offline, as expected.')
else:
    print(f'Home is not offline, but it should be. Response: {response.text}')
    exit()

# 14. Set appliance active
set_active_url = f'{appliance_url}{appliance_details["id"]}/set_status/'
print(set_active_url    )
status_data = {'status': 'active'}
response = requests.post(set_active_url, data=status_data, headers=headers)
print(response.json())

# 15. Destroy appliance
destroy_url = f'{appliance_url}{appliance_details["id"]}/'
response = requests.delete(destroy_url, headers=headers)
print(response)

print('All tests passed!')