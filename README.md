# Django User Authentication API

A Django REST Framework based authentication system providing JWT-based authentication with features like user registration, login, logout, and password management.

## Features

- User Registration with email validation
- JWT Authentication (Login/Logout)
- Token Refresh
- Password Change for authenticated users
- API versioning support
- Standardized API responses

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- virtualenv (recommended)

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd mysite
```

2. Create and activate a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply database migrations:

```bash
python manage.py migrate
```

5. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

## API Endpoints

All endpoints are prefixed with `/api/v1/auth/`

### User Registration

```http
POST /api/v1/auth/register/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "StrongPass@123",
    "confirm_password": "StrongPass@123",
    "first_name": "John",  // Optional
    "last_name": "Doe"     // Optional
}
```

### Login

```http
POST /api/v1/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "StrongPass@123"
}
```

### Refresh Token

```http
POST /api/v1/auth/refresh/
Content-Type: application/json

{
    "refresh": "<your-refresh-token>"
}
```

### Logout

```http
POST /api/v1/auth/logout/
Content-Type: application/json

{
    "refresh": "<your-refresh-token>"
}
```

### Change Password

```http
POST /api/v1/auth/change-password/
Content-Type: application/json
Authorization: Bearer <your-access-token>

{
    "current_password": "CurrentPass@123",
    "new_password": "NewPass@123",
    "confirm_password": "NewPass@123"
}
```

### Update Profile
Update the logged-in user's profile information.

**URL**: `/api/v1/auth/profile/`
**Method**: `PUT`
**Auth required**: Yes
**Required Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
    "first_name": "John",
    "last_name": "Doe"
}
```

**Success Response**:
```json
{
    "message": "Profile updated successfully",
    "status_code": 200,
    "data": {
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    }
}
```

**Notes**:
- Email address cannot be changed
- Both first_name and last_name are optional
- Partial updates are supported (you can update just first_name or just last_name)

## API Response Format

All API endpoints follow a consistent response format:

### Success Response

```json
{
  "message": "Success message",
  "status_code": 200,
  "error": null,
  "data": {
    // Response data if any
  }
}
```

### Error Response

```json
{
  "message": "Error message",
  "status_code": 400,
  "error": {
    // Error details
  },
  "data": null
}
```

## Password Requirements

- Minimum 8 characters long
- Must contain at least one uppercase letter
- Must contain at least one lowercase letter
- Must contain at least one number
- Must contain at least one special character

## Development

The project uses:

- Django REST Framework for API development
- Simple JWT for JWT authentication
- Django REST Framework versioning for API versioning

## Testing

Run the test suite:

```bash
pytest
```

For test coverage:

```bash
pytest --cov
```

## API Testing with REST Client

The project includes an `apis.rest` file that can be used to test the API endpoints directly from VS Code using the REST Client extension.

### Setup REST Client

1. Install the "REST Client" extension in VS Code
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "REST Client"
   - Install the extension by "Huachao Mao"

### Using apis.rest

The `apis.rest` file contains ready-to-use API requests. To use it:

1. Open `apis.rest` in VS Code
2. Click "Send Request" above any request to execute it
3. View the response in a split pane

Example requests in `apis.rest`:

```http
### Login ###
POST http://localhost:8000/api/v1/auth/login/
Content-Type: application/json

{
    "email": "user@example.com",
    "password": "your_password"
}

### User Registration ###
POST http://localhost:8000/api/v1/auth/register/
Content-Type: application/json

{
    "email": "test@example.com",
    "password": "Test@123",
    "confirm_password": "Test@123"
}
```

Tips for using apis.rest:
- Each request is separated by `###`
- You can save the response of one request and use it in subsequent requests
- Environment variables can be set at the top of the file
- The file supports dynamic variables and scripts
