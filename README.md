# Smart Home Control Backend

This project is a Django-based backend for a smart home control application. It provides a RESTful API for managing smart home devices, rooms, and appliance categories.

## Features

*   User authentication with JWT (djoser)
*   Create, Read, Update, Delete (CRUD) operations for:
    *   Rooms
    *   Appliance Categories
    *   Appliances
    *   Air Conditioners
*   Set appliance status (active/inactive) with an optional timer
*   Set air conditioner temperature
*   User-specific configurations: each user can only see and manage their own smart home configuration.

## Project Structure

The project consists of two main Django apps:

*   `news`: A simple news app.
*   `smarthome`: The core app for the smart home functionality.

## Getting Started

### Prerequisites

*   Python 3.10+
*   pip
*   SQL Server

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the database:**

    Open `mpityakutiazhgutbackend/settings.py` and update the `DATABASES` setting with your SQL Server credentials.

5.  **Apply the database migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/`.

## API Documentation

The API is protected and requires authentication. You need to obtain a JWT token to access the endpoints.

### Authentication

*   **Register a new user:** `POST /auth/users/`
*   **Get a JWT token:** `POST /auth/jwt/create/`
*   **Refresh a JWT token:** `POST /auth/jwt/refresh/`

### Smart Home API

All endpoints are prefixed with `/smarthome/`.

#### Rooms

*   `GET /smarthome/rooms/`: List all rooms for the current user.
*   `POST /smarthome/rooms/`: Create a new room.
*   `GET /smarthome/rooms/{id}/`: Retrieve a specific room.
*   `PUT /smarthome/rooms/{id}/`: Update a specific room.
*   `DELETE /smarthome/rooms/{id}/`: Delete a specific room.

#### Appliance Categories

*   `GET /smarthome/appliance-categories/`: List all appliance categories for the current user.
*   `POST /smarthome/appliance-categories/`: Create a new appliance category.
*   `GET /smarthome/appliance-categories/{id}/`: Retrieve a specific appliance category.
*   `PUT /smarthome/appliance-categories/{id}/`: Update a specific appliance category.
*   `DELETE /smarthome/appliance-categories/{id}/`: Delete a specific appliance category.

#### Appliances

*   `GET /smarthome/appliances/`: List all appliances for the current user.
*   `POST /smarthome/appliances/`: Create a new appliance.
*   `GET /smarthome/appliances/{id}/`: Retrieve a specific appliance.
*   `PUT /smarthome/appliances/{id}/`: Update a specific appliance.
*   `DELETE /smarthome/appliances/{id}/`: Delete a specific appliance.
*   `POST /smarthome/appliances/{id}/set_status/`: Set the status of an appliance.
    *   **Body:** `{"status": "active" | "inactive", "active_for": <minutes>}` (optional)

#### Air Conditioners

*   `GET /smarthome/air-conditioners/`: List all air conditioners for the current user.
*   `POST /smarthome/air-conditioners/`: Create a new air conditioner.
*   `GET /smarthome/air-conditioners/{id}/`: Retrieve a specific air conditioner.
*   `PUT /smarthome/air-conditioners/{id}/`: Update a specific air conditioner.
*   `DELETE /smarthome/air-conditioners/{id}/`: Delete a specific air conditioner.
*   `POST /smarthome/air-conditioners/{id}/set_temperature/`: Set the temperature of an air conditioner.
    *   **Body:** `{"temperature": <float>}`

## Running Tests

To run the tests, use the following command:

```bash
python manage.py test
```
