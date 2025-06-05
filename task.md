# **RESTful Payment Gateway API for Small Businesses**

## **Objective**

Create a basic RESTful API that enables small businesses to accept payments from customers using payment gateways such as PayPal, Paystack, or Flutterwave. The API should focus on minimal customer information, including:

- Name
- Email
- Payment amount

## Key Requirements

- No user authentication: The API should function without requiring user authentication.
- Versioning: Implement API versioning for better maintainability.
- CI/CD: Automate testing and deployment using Continuous Integration and Continuous Deployment pipelines.

## **Endpoints**

The API should follow RESTful best practices and include versioning.

### 1. Initiate a Payment

Endpoint: `POST /api/v1/payments`

Description: Initiates a payment.

Request Body:

```json
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "amount": 50.00
}

```

### 2. Retrieve Payment Status

Endpoint: `GET /api/v1/payments/{id}`

Description: Retrieves the status of a specific payment transaction.

Example Response:

```json
{
    "payment": {
        "id": "PAY-123",
        "customer_name": "John Doe",
        "customer_email": "john@example.com",
        "amount": 50.00,
        "status": "completed"
    },
    "status": "success",
    "message": "Payment details retrieved successfully."
}

```

### Notes

- Ensure the API adheres to RESTful principles.
- Use proper HTTP status codes for responses.
- Include automated tests to validate functionality.
- Implement CI/CD pipelines for seamless deployment.
- Focus on simplicity and usability for small businesses.

## **Task Details**

### Backend Setup

- Develop using Django REST Framework.
- Use a payment gateway plugin or manually integrate the payment API.

### CI/CD Pipeline

- Test: Use Django's testing framework or `pytest-django` to verify payment processing and status checks.
- Build: Ensure the application builds and all dependencies are installed.
- Deploy: Deploy to platforms like Netlify, Vercel, Render, or similar.

Sample `.github/workflows/django.yml`

```yaml
name: Django CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      max-parallel: 4
      matrix:
        python-version: [3.8]
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run Tests
      run: |
        python manage.py test

```

## **Deliverables**

A functional RESTful API for processing payments with:

- Versioning
- No user authentication
- Clear status messages
- A CI/CD pipeline setup in GitHub Actions for automated testing and deployment.

Documentation detailing:

- How to run the service locally
- How to understand the tests
- How to deploy using the CI/CD pipeline