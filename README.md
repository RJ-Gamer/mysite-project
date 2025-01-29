# Django Authentication API 🔐

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![DRF](https://img.shields.io/badge/DRF-3.14+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A robust Django REST API for user authentication with JWT tokens, featuring secure password management and comprehensive testing.

## ✨ Features

- 🔒 JWT Authentication
- 🔑 Secure Password Change
- 🔄 Token Refresh
- 📝 Type Hints & Documentation
- ✅ Comprehensive Tests
- 🎯 API Response Standardization

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- virtualenv (recommended)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd mysite
```

2. Create and activate virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows, use: env\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp env.sample .env
# Edit .env with your configuration
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser (optional)
```bash
python manage.py createsuperuser
```

7. Run the development server
```bash
python manage.py runserver
```

## 🔗 API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login/` | POST | User login |
| `/api/v1/auth/refresh/` | POST | Refresh access token |
| `/api/v1/auth/logout/` | POST | User logout |
| `/api/v1/auth/change-password/` | POST | Change user password |

### Request/Response Examples

#### Login
```json
// Request
POST /api/v1/auth/login/
{
    "email": "user@example.com",
    "password": "your_password"
}

// Response
{
    "message": "Login successful",
    "status_code": 200,
    "error": null,
    "data": {
        "access": "your.access.token",
        "refresh": "your.refresh.token"
    }
}
```

#### Change Password
```json
// Request
POST /api/v1/auth/change-password/
{
    "current_password": "old_password",
    "new_password": "new_password",
    "confirm_password": "new_password"
}

// Response
{
    "message": "Password changed successfully",
    "status_code": 200,
    "error": null,
    "data": null
}
```

## 🧪 Running Tests

The project uses pytest for testing. Run the tests with:

```bash
pytest
```

For test coverage report:
```bash
pytest --cov=.
```

## 📝 Code Style

This project follows PEP 8 style guide and uses type hints. Code formatting is maintained using:
- Black (code formatter)
- isort (import sorter)
- mypy (type checker)

## 🛡️ Security Features

- JWT token-based authentication
- Password complexity validation
- Token refresh mechanism
- Secure password storage using Django's password hashing
- Protection against common attacks (CSRF, XSS)

## 🏗️ Project Structure

```
mysite/
├── users/              # User authentication app
├── utils/              # Shared utilities
├── tests/              # Test suite
├── requirements/       # Environment-specific requirements
├── mysite/            # Project settings
├── manage.py
├── README.md
└── .gitignore
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

**Your Name**
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django Rest Framework
- SimpleJWT
- Factory Boy
- pytest

---

Made with ❤️ and ☕
