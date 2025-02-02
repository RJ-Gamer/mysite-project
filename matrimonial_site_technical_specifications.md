# Technical Specifications for Matrimonial Site

## Overview
This document outlines the technical specifications for the development of the matrimonial site, including architecture, API endpoints, and database schema.

## 1. Architecture

### 1.1. System Architecture
- **Frontend**: React.js application served via CDN.
- **Backend**: Django REST framework for API development.
- **Database**: PostgreSQL for relational data storage.
- **Caching**: Redis for session management and caching frequently accessed data.
- **Storage**: AWS S3 for storing user-uploaded images and documents.
- **Communication**: WebSocket for real-time chat functionality.

### 1.2. Deployment Architecture
- **Containerization**: Docker for containerizing applications.
- **Orchestration**: Kubernetes for managing containerized applications.
- **Load Balancer**: NGINX for load balancing incoming traffic.
- **Monitoring**: Prometheus and Grafana for monitoring application performance.

## 2. API Endpoints

### 2.1. User Authentication
| Endpoint                | Method | Description                     |
|-------------------------|--------|---------------------------------|
| `/api/auth/register/`   | POST   | Register a new user            |
| `/api/auth/login/`      | POST   | User login                     |
| `/api/auth/logout/`     | POST   | User logout                    |
| `/api/auth/profile/`    | GET    | Get user profile               |
| `/api/auth/update/`     | PUT    | Update user profile            |

### 2.2. Profile Management
| Endpoint                  | Method | Description                     |
|---------------------------|--------|---------------------------------|
| `/api/profiles/`         | GET    | Get all profiles               |
| `/api/profiles/{id}/`    | GET    | Get profile by ID              |
| `/api/profiles/create/`  | POST   | Create a new profile           |
| `/api/profiles/update/{id}/` | PUT | Update profile by ID           |
| `/api/profiles/delete/{id}/` | DELETE | Delete profile by ID          |

### 2.3. Search and Match
| Endpoint                  | Method | Description                     |
|---------------------------|--------|---------------------------------|
| `/api/search/`           | POST   | Search for profiles             |
| `/api/matches/`          | GET    | Get matched profiles            |

### 2.4. Communication
| Endpoint                  | Method | Description                     |
|---------------------------|--------|---------------------------------|
| `/api/chat/`             | POST   | Send a message                  |
| `/api/chat/{id}/`        | GET    | Get chat history by ID          |

### 2.5. Social Login APIs
| Endpoint                   | Method | Description                     |
|----------------------------|--------|---------------------------------|
| `/api/auth/google/`        | POST   | Authenticate user via Google    |
| `/api/auth/facebook/`      | POST   | Authenticate user via Facebook  |
| `/api/auth/social/callback/` | GET  | Handle social login callback     |

#### 2.5.1. Google Login
- **Request Body**:  
  ```json
  {
    "id_token": "<Google ID Token>"
  }
  ```
- **Response**:  
  ```json
  {
    "token": "<JWT Token>",
    "user": {
      "id": "<User ID>",
      "username": "<Username>",
      "email": "<Email>"
    }
  }
  ```

#### 2.5.2. Facebook Login
- **Request Body**:  
  ```json
  {
    "access_token": "<Facebook Access Token>"
  }
  ```
- **Response**:  
  ```json
  {
    "token": "<JWT Token>",
    "user": {
      "id": "<User ID>",
      "username": "<Username>",
      "email": "<Email>"
    }
  }
  ```

## 3. Database Schema

### 3.1. User Table
| Column Name       | Data Type     | Description                    |
|-------------------|---------------|--------------------------------|
| `id`              | SERIAL        | Primary key                    |
| `username`        | VARCHAR(50)   | Unique username                |
| `email`           | VARCHAR(100)  | User email                     |
| `password`        | VARCHAR(255)  | Hashed password                |
| `created_at`      | TIMESTAMP     | Account creation date          |
| `updated_at`      | TIMESTAMP     | Last update date               |

### 3.2. Profile Table
| Column Name       | Data Type     | Description                    |
|-------------------|---------------|--------------------------------|
| `id`              | SERIAL        | Primary key                    |
| `user_id`        | INT           | Foreign key to User            |
| `bio`             | TEXT          | User bio                       |
| `location`        | VARCHAR(100)  | User location                  |
| `education`       | VARCHAR(100)  | User education                 |
| `profession`      | VARCHAR(100)  | User profession                |
| `created_at`      | TIMESTAMP     | Profile creation date          |
| `updated_at`      | TIMESTAMP     | Last update date               |

### 3.3. Chat Table
| Column Name       | Data Type     | Description                    |
|-------------------|---------------|--------------------------------|
| `id`              | SERIAL        | Primary key                    |
| `sender_id`      | INT           | Foreign key to User (sender)   |
| `receiver_id`    | INT           | Foreign key to User (receiver)  |
| `message`         | TEXT          | Message content                 |
| `timestamp`       | TIMESTAMP     | Message sent date               |

## Summary
These technical specifications provide a detailed overview of the architecture, API endpoints, and database schema for the matrimonial site. Further refinement can be done during the development phase.
