from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='user').exists():
    User.objects.create_superuser('user', 'user@example.com', 'p6#B9!vL2*wZ4@qN')
    print("Superuser 'user' created.")
else:
    print("Superuser 'user' already exists.")
