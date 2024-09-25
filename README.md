# CompleteApi

**CompleteApi** is an example of a RESTful API implemented with **FastAPI** that demonstrates basic CRUD operations (Create, Read, Update, Delete) on a database. This project is ideal for understanding how to efficiently create and manage endpoints using FastAPI, a Python framework known for its high performance and simplicity.

## Features

- **Full CRUD operations**: Support for creating, reading, updating, and deleting resources.
- **Database connection**: Uses PostgreSQL as a relational database.
- **Modular structure**: The code is organized in a way that makes it scalable and maintainable.
- **Data validation**: Implemented with Pydantic to ensure data integrity for incoming and outgoing requests.
- **Interactive documentation**: Automatically generates API documentation using Swagger and OpenAPI.

## Requirements

- **Python 3.8+**
- **Docker** (optional, if you prefer to run the project in containers)
- **PostgreSQL**

## Installation


1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/CompleteApi.git
   cd CompleteApi

2. Start the application and database containers:
    ````
    docker-compose up --build

3. Access the API at: http://localhost:8000

## Usage

You can access the automatically generated interactive API documentation at http://localhost:8000/docs.
You can test the endpoints using tools like cURL or Postman.

## Main Endpoints

- POST /items/: Create a new item.
- GET /items/{id}: Get details of a specific item.
- GET /items/: Get details of all items saved on db
- PUT /items/{id}: Update an existing item.
- DELETE /items/{id}: Delete an item.