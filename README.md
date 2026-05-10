# Smart Task Management System

A data-driven, real-time task orchestration platform built with **Flask**, **PostgreSQL**, and **WebSockets**. This system features advanced productivity analytics powered by **Pandas** and **NumPy**, providing users with instant feedback and deep insights into their workflow.

## 🌟 Key Features

-   **Real-time Synchronization:** Utilizing **Socket.io Rooms**, the dashboard updates instantly across multiple devices without page refreshes.
    
-   **Data-Driven Insights:** A dedicated analytics engine using **Pandas** and **NumPy** to process task data and generate productivity metrics.
    
-   **Secure Authentication:** User session management and secure password hashing via **Flask-Login**.
    
-   **Priority-Based CRUD:** Full task lifecycle management (Create, Read, Update, Delete) with color-coded priority levels.
    
-   **Responsive Design:** A clean, modern UI designed for efficiency and ease of use.
    

## 🛠️ Technical Stack

-   **Backend:** Python (Flask, Flask-RESTful)
    
-   **Database:** PostgreSQL (SQLAlchemy ORM)
    
-   **Real-Time:** Flask-SocketIO (Event-driven architecture)
    
-   **Data Science:** Pandas, NumPy
    
-   **Frontend:** JavaScript (ES6+), HTML5, CSS3
   

## 🚀 Getting Started

### 1. Prerequisites

-   Python 3.8+
    
-   PostgreSQL installed and running
    
-   A terminal/command prompt
    

### 2. Installation

Clone the repository and navigate to the project directory:

Bash

```
git clone https://github.com/manjinder-27/Smart-Task-Management-System.git
cd Smart-Task-Management-System

```

### 3. Setup Virtual Environment

Bash

```
# Windows
python -m venv venv
venv\Scripts\activate

# MacOS/Linux
python3 -m venv venv
source venv/bin/activate

```

### 4. Install Dependencies

Bash

```
pip install -r requirements.txt

```

### 5. Database Configuration

Create a PostgreSQL database and update `app.py`.

Python

```
# Example URI format:
# postgresql://username:password@localhost/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_postgres_uri'

```

### 6. Run the Application

Bash

```
python main.py

```

The application will be available at `http://127.0.0.1:5000`.

## 📊 API Documentation

**Endpoint** | **Method** | **Description** | **Auth Required**
---- | ---- | ---- | ----
|`/api/register`|POST|Register a new user|No
|`/api/login`|POST|Authenticate user|No
|`/api/tasks`|GET|Fetch all user tasks|Yes
|`/api/tasks`|POST|Create a new task|Yes
|`/api/tasks/<task_id>`|PUT|Update an existing task|Yes
|`/api/tasks/<task_id>`|DELETE|Remove a task|Yes
|`/api/analytics`|GET|Fetch Pandas-computed stats|Yes

## 🧠 Smart Logic Implementation

### Real-Time Sync (WebSockets)

The system uses **Socket.io Rooms** to isolate data streams. When a task is modified, an event is emitted specifically to the `user_id` room, ensuring only the relevant client triggers a UI refresh.

### Analytics Pipeline

Unlike traditional SQL counting, this project extracts data into a **Pandas DataFrame**. This allows for scalable data manipulation and the potential for future integration of machine learning or trend forecasting using **NumPy**'s computational power.

