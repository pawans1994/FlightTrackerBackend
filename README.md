Here's a `README.md` for your backend project:

---

# FlightTrackerBackend

This is the backend application for tracking flight prices. It handles user inputs through a REST API, tracks flight prices, and sends email notifications when prices fall below a user-defined threshold. The backend uses Flask, Celery, and Redis, and is fully dockerized.

## Features

- **REST API**: Receives flight details from the frontend.
- **Price Tracking**: Schedules tasks to track flight prices.
- **Email Notifications**: Sends email alerts when flight prices drop below the threshold.
- **Dockerized Setup**: The application, Redis, and Celery worker run inside Docker containers.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework.
- **Celery**: An asynchronous task queue/job queue based on distributed message passing.
- **Redis**: An in-memory data structure store, used as a message broker.
- **Docker**: A platform for developing, shipping, and running applications inside containers.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Docker (v20 or above)
- Docker Compose (v1.27 or above)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/pawans1994/FlightTrackerBackend.git
   cd FlightTrackerBackend
   ```

2. **Build and run the Docker containers:**

   ```sh
   docker-compose up --build
   ```

   This command will start the Flask app, Redis server, and Celery worker.

### Configuration

Set up environment variables by creating a `.env` file in the root directory with the following content:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
MAIL_SERVER=smtp.your-email-provider.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

Replace the placeholders with your actual configuration values.

## Usage

1. **Run the application:**

   ```sh
   docker-compose up
   ```

2. **Access the API:**

   The Flask app will be running at `http://localhost:5000`. You can use a tool like Postman or curl to interact with the API endpoints.

3. **API Endpoints:**

   - **POST /track-flight**: Accepts flight details and threshold price, and schedules the price tracking task.
   - **GET /check-status**: Returns the status of the scheduled tasks.

## Contributing

We welcome contributions to improve the project. To contribute, follow these steps:

1. **Fork the repository.**
2. **Create a new branch:**

   ```sh
   git checkout -b feature-branch
   ```

3. **Make your changes.**
4. **Commit your changes:**

   ```sh
   git commit -m 'Add feature'
   ```

5. **Push to the branch:**

   ```sh
   git push origin feature-branch
   ```

6. **Open a pull request.**

## Contact

For questions or support, contact:

- **Pawandeep Singh Mendiratta**
- **Email**: pawan.p.121@gmail.com

---

Feel free to adjust any details or add additional sections as needed.