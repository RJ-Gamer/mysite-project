# Database Architecture for Matrimonial Site

## Overview
This document outlines the database architecture for the matrimonial site, including the design, relationships between tables, and key attributes.

## 1. Database Design
The matrimonial site will utilize a relational database management system (RDBMS) to manage user data, profiles, and interactions. The primary database will be PostgreSQL.

## 2. Entity-Relationship Diagram (ERD)

### 2.1. Entities
- **User**: Represents the users of the matrimonial site.
- **Profile**: Contains detailed information about each user.
- **Chat**: Stores messages exchanged between users.
- **Subscription**: Manages subscription plans and user payments.

### 2.2. Relationships
- **User to Profile**: One-to-One (Each user has one profile)
- **User to Chat**: One-to-Many (A user can have multiple chat messages)
- **User to Subscription**: One-to-Many (A user can have multiple subscriptions over time)

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

### 3.4. Subscription Table
| Column Name       | Data Type     | Description                    |
|-------------------|---------------|--------------------------------|
| `id`              | SERIAL        | Primary key                    |
| `user_id`        | INT           | Foreign key to User            |
| `plan_type`       | VARCHAR(50)   | Type of subscription plan      |
| `start_date`      | TIMESTAMP     | Subscription start date        |
| `end_date`        | TIMESTAMP     | Subscription end date          |
| `status`          | VARCHAR(20)   | Active, Inactive               |

## Summary
This document provides a comprehensive overview of the database architecture for the matrimonial site, detailing the tables, relationships, and attributes necessary for effective data management.
