# Library Service

Welcome to the Library Service documentation! This API is designed to address the 
existing challenges in the manual book borrowing and payment system of the city library. By implementing this online management system, we aim to streamline the process for both library administrators and users, providing a user-friendly experience while improving overall efficiency.

## Table of Contents
1. [Features](#features)
2. [Getting Started](#getting-started)
   * [Installation](#installation)
3. [API Endpoints](#api-endpoints)
   * [Authentication](#authentication)
   * [Users](#users)
   * [Books](#books)
   * [Borrowings](#borrowings)
   * [Payments](#payments)
4. [Error Handling](#error-handling)
5. [Contributing](#contributing)
6. [License](#license)

## Features
* User registration and authentication
* Browse available books and their details
* Borrow and return books
* Track borrowing history and due dates
* Make payments for overdue books using card
* Administer books and users
* Generate reports on borrowings and payments

# Installation
Clone this repository

`git clone https://github.com/erikagayan/Library-Service-Project.git`

Navigate to the project directory: 

`cd library-management-api`

Create and activate a virtual environment:

`python -m venv venv`

On Linux/Mac: `source venv/bin/activate`

On Windows: `venv\Scripts\activate`

Install the required packages: 

`pip install -r requirements.txt`

Run migrations: 

`python manage.py migrate`

Install fixture with data: 

`python manage.py loaddatautf8 fixture_data_library.json`

Start the development server:

`python manage.py runserver`

# API Endpoints
## Authentication
POST /api/token/ - Obtain an access token using email and password (JWT 
authentication).
## Users
POST: /api/users/ - Register a new user

POST: /api/users/token/refresh/ - refresh JWT token 

GET: /api/users/me/ - get my profile info 

PUT/PATCH: users/me/ - update profile info 

## Books
POST: books/ - Add new book.

GET: books/ - Retrieve a list of available books.

GET: books/{book_id}/ - Retrieve details of a specific book.

PUT/PATCH: books/{book_id}/ - Update book (also manage inventory).

DELETE: books/{book_id}/ - Delete book.
## Borrowings

POST: /api/borrowings/ - Add new borrowing

GET: /api/borrowings/?user_id=...&is_active=...  - get borrowings by user id 
and whether is borrowing still active or not.

GET: /api/borrowings/{book_id}/ - Get specific borrowing 

POST: /api/borrowings/{book_id}/return/ - Set actual return date


## Payments
GET: success/ - Check successful stripe payment
GET: cancel/ - Return payment paused message



# Error Handling
The API follows RESTful conventions for error responses. It returns appropriate status codes and error messages in case of invalid requests or failures.

# Contributing
We welcome contributions to enhance the functionality and usability of this API.

# License
This project is licensed under the MIT License. Feel free to use and modify the codebase as needed.
