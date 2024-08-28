
# User Management API Documentation

## Overview
This is a User Management API that provides endpoints for user registration, authentication, and management. It also includes features like Google OAuth integration, user details management, subscription management, and a dynamic calendar system based on pregnancy due dates.

## API Endpoints

### Authentication and User Management

- **POST /register**
  - Register a new user.
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "password": "password123",
      "first_name": "John",
      "last_name": "Doe"
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "is_admin": false
    }
    ```

- **POST /login**
  - Authenticate a user and return a JWT token along with user's first and last name.
  - Request Body:
    ```json
    {
      "email": "user@example.com",
      "password": "password123"
    }
    ```
  - Response:
    ```json
    {
      "token": "jwt_token",
      "first_name": "John",
      "last_name": "Doe"
    }
    ```

- **GET /users/{id}**
  - Get user details by ID.
  - Headers: `Authorization: Bearer <token>`
  - Response:
    ```json
    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "is_admin": false
    }
    ```

- **PUT /users/{id}/admin**
  - Update a user to admin role.
  - Headers: `Authorization: Bearer <token>`
  - Response:
    ```json
    {
      "message": "User updated to admin"
    }
    ```

### Google OAuth

- **GET /login/google**
  - Redirects to Google OAuth login.

- **GET /login/google/callback**
  - Callback endpoint for Google OAuth.
  - Response:
    ```json
    {
      "token": "jwt_token",
      "first_name": "John",
      "last_name": "Doe"
    }
    ```

### User Details Management

- **POST /user-details**
  - Add or update user details.
  - Headers: `Authorization: Bearer <token>`
  - Request Body:
    ```json
    {
      "sex": "Male",
      "pronouns": "He/Him",
      "due_date": "2024-12-31",
      "first_pregnancy": true,
      "phone_number": "1234567890",
      "can_receive_texts": true
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "sex": "Male",
      "pronouns": "He/Him",
      "due_date": "2024-12-31",
      "first_pregnancy": true,
      "phone_number": "1234567890",
      "can_receive_texts": true,
      "user_id": 1
    }
    ```

- **GET /user-details/{user_id}**
  - Get user details by user ID.
  - Headers: `Authorization: Bearer <token>`
  - Response:
    ```json
    {
      "id": 1,
      "sex": "Male",
      "pronouns": "He/Him",
      "due_date": "2024-12-31",
      "first_pregnancy": true,
      "phone_number": "1234567890",
      "can_receive_texts": true,
      "user_id": 1
    }
    ```

### Subscription Management

- **POST /subscriptions**
  - Subscribe or unsubscribe a user to newsletters and texts.
  - Headers: `Authorization: Bearer <token>`
  - Request Body:
    ```json
    {
      "subscribe_to_newsletter": true,
      "subscribe_to_texts": true
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "subscribe_to_newsletter": true,
      "subscribe_to_texts": true,
      "user_id": 1
    }
    ```

- **GET /subscriptions/{user_id}**
  - Get user's subscription status.
  - Headers: `Authorization: Bearer <token>`
  - Response:
    ```json
    {
      "id": 1,
      "subscribe_to_newsletter": true,
      "subscribe_to_texts": true,
      "user_id": 1
    }
    ```

### Reference Calendar Management

- **POST /reference-calendar**
  - Add a reference calendar event.
  - Headers: `Authorization: Bearer <token>`
  - Request Body:
    ```json
    {
      "day": 50,
      "event": "Ultrasound"
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "day": 50,
      "event": "Ultrasound"
    }
    ```

- **GET /reference-calendar**
  - Get all reference calendar events.
  - Headers: `Authorization: Bearer <token>`
  - Response:
    ```json
    [
      {
        "id": 1,
        "day": 50,
        "event": "Ultrasound"
      },
      {
        "id": 2,
        "day": 100,
        "event": "Checkup"
      }
    ]
    ```

- **PUT /reference-calendar/{id}**
  - Update a reference calendar event by ID.
  - Headers: `Authorization: Bearer <token>`
  - Request Body:
    ```json
    {
      "day": 100,
      "event": "Checkup"
    }
    ```
  - Response:
    ```json
    {
      "id": 2,
      "day": 100,
      "event": "Checkup"
    }
    ```

- **DELETE /reference-calendar/{id}**
  - Delete a reference calendar event by ID.
  - Headers: `Authorization: Bearer <token>`
  - Response:
    ```json
    {
      "message": "Event deleted successfully"
    }
    ```

### User Calendar Management

- **GET /user-calendar/{user_id}**
  - Get all user-specific calendar events.
  - Headers: `Authorization: Bearer <token>`
  - Response:
    ```json
    [
      {
        "id": 1,
        "date": "2024-03-20",
        "event": "Ultrasound"
      },
      {
        "id": 2,
        "date": "2024-06-15",
        "event": "Checkup"
      }
    ]
    ```

- **POST /user-calendar**
  - Add a custom event to the user calendar.
  - Headers: `Authorization: Bearer <token>`
  - Request Body:
    ```json
    {
      "user_id": 1,
      "date": "2024-07-01",
      "event": "Yoga Class"
    }
    ```
  - Response:
    ```json
    {
      "id": 3,
      "user_id": 1,
      "date": "2024-07-01",
      "event": "Yoga Class"
    }
    ```

## Authorization

- All endpoints require a JWT token passed in the `Authorization` header:
  ```
  Authorization: Bearer <token>
  ```

## Error Handling

- **401 Unauthorized**
  - Returned when the JWT token is invalid or expired.

- **404 Not Found**
  - Returned when the requested resource is not found.

- **400 Bad Request**
  - Returned when the request body is malformed or missing required fields.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
