import uuid
import random
import string
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

username = f'testuser_{uuid.uuid4().hex[:8]}'
password = generate_random_password()

try:
    User.objects.create_superuser(username, f'{username}@example.com', password)
    print(f"SUPERUSER_USERNAME:{username}")
    print(f"SUPERUSER_PASSWORD:{password}")
except Exception as e:
    print(f"Failed to create superuser: {e}")
