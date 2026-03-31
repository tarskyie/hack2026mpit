# Server Interaction Manual

This guide provides instructions on how to run the Django server and interact with its API endpoints using `curl.exe` on Windows.

## 1. Running the Server

To start the server, run the following command in your project's root directory. By default, the server will be accessible at `http://127.0.0.1:8000`.

```shell
python manage.py runserver
```

---

## 2. Making API Requests with curl.exe

The following examples demonstrate how to interact with the server's API.

**Note on Windows `curl.exe`:** When sending JSON data with `curl.exe` on Windows, you must escape the double quotes inside the JSON string with backslashes (`"`).

### Example 1: Listing News (Public Endpoint)

This endpoint does not require authentication.

```shell
curl.exe -X GET http://127.0.0.1:8000/news/list
```

### Example 2: Obtaining an Authentication Token

To access protected endpoints, you first need to obtain a JWT (JSON Web Token) by providing user credentials.

**Prerequisite:** You must have a user account (a superuser or a regular user). You can create one using the following command:
`python manage.py createsuperuser`

Replace `your_username` and `your_password` with your actual credentials.

```shell
curl.exe -X POST -H "Content-Type: application/json" -d "{"username": "your_username", "password": "your_password"}" http://127.0.0.1:8000/auth/jwt/create/
```

The server will respond with a JSON object containing `access` and `refresh` tokens. Copy the `access` token for use in subsequent requests.

### Example 3: Listing Your Rooms (Protected Endpoint)

To access this endpoint, you must include the `access` token in the `Authorization` header.

Replace `<YOUR_ACCESS_TOKEN>` with the token you obtained in the previous step.

```shell
curl.exe -X GET -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" http://127.0.0.1:8000/smarthome/rooms/
```

### Example 4: Creating a New Room (Protected Endpoint)

This example sends a `POST` request to create a new room named "Living Room".

```shell
curl.exe -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" -d "{"name": "Living Room"}" http://127.0.0.1:8000/smarthome/rooms/
```

### Example 5: Setting an Appliance Status (Custom Action)

This example demonstrates how to call a custom action on an appliance. This `POST` request sets the status of the appliance with ID `1` to "active" for 60 minutes.

Replace `<YOUR_ACCESS_TOKEN>` and adjust the appliance ID (`1`) as needed.

```shell
curl.exe -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" -d "{"status": "active", "active_for": 60}" http://127.0.0.1:8000/smarthome/appliances/1/set_status/
```
