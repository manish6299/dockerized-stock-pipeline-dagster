
# 📈 Dockerized Stock Data Pipeline using Dagster & PostgreSQL

This project implements a data pipeline using **Dagster** for orchestration and **PostgreSQL** for storage. It fetches stock market data from **Yahoo Finance (via `yfinance`)**, parses it, and stores it in a PostgreSQL database.

---

## 🚀 Features

- ✅ Uses **Dagster** for pipeline orchestration
- ✅ Fetches stock data (default: AAPL) via **Yahoo Finance API**
- ✅ Stores data in a **PostgreSQL** database
- ✅ Uses **Docker Compose** for end-to-end containerization
- ✅ Robust error handling and retry logic
- ✅ Secrets managed via `.env` file

---

## 🗂️ Project Structure

```
project/
│
├── dagster_pipeline/
│   ├── repository.py         # Dagster repository definition
│   └── ops.py               # fetch the data and save into database 
|   |__ jobs.py           # Data fetching and storing ops
│
├── .env                      # Secrets & configuration
├── Dockerfile                # Builds the Dagster service
├── docker-compose.yml        # Defines Dagster + Postgres services
├── requirements.txt          # Python dependencies
└── README.md
|__ workspace.yaml
|__ myproject.toml               # You're here!
```

---

## 🧪 Requirements

- To build and run this project, you’ll need the following installed:

- Docker Destop – containerization platform

- Docker Compose – for managing multi-container Docker apps

- Python 3.10+ – for running scripts locally (if needed outside Docker)

- pgAdmin – optional, for managing and inspecting the PostgreSQL database via GUI

---<img width="951" height="463" alt="image5" src="https://github.com/user-attachments/assets/cbe9a97c-eebc-48fa-a047-f9ca8f755758" />


## ⚙️ Setup & Run

### 1. Clone the Repo

```bash
git clone <your-repo-url>
cd project
```

### 2. Create and Configure the `.env` File

```env
# .env
POSTGRES_USER=stockuser
POSTGRES_PASSWORD="your password"
POSTGRES_DB=stockdb
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

STOCK_SYMBOL=AAPL
```

---

### 3. Build and Run the Pipeline

```bash
docker-compose up --build
```

- Dagster UI: [http://localhost:3000](http://localhost:3000)

---

### 4. Trigger the Job in Dagster UI

1. Open `http://localhost:3000`
2. Navigate to your repository
3. Launch the job manually (or schedule it)

---

## 🗄️ Inspecting the Database

Open a terminal and run:

```bash
docker exec -it project-postgres-1 psql -U stockuser -d stockdb
```

Then inside PostgreSQL CLI:

```sql
\dt;
SELECT * FROM stocks;
\q
```

---

## 🔄 Updating the Stock Symbol

Just edit the `STOCK_SYMBOL` in the `.env` file and restart:

```bash
docker-compose down
docker-compose up --build
```

---

## 📌 Tech Stack

- [Dagster](https://dagster.io/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [yfinance](https://pypi.org/project/yfinance/)
- [psycopg2](https://pypi.org/project/psycopg2/)

---

## 🧹 Cleanup

To stop and remove containers, run:

```bash
docker-compose down
```

---

## 📬 Author

- **Your Name** – *Manish kumar Yadav *


