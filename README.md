
# 📈 Dockerized Stock Data Pipeline using Dagster & PostgreSQL

This project implements a data pipeline using **Dagster** for orchestration and **PostgreSQL** for storage. It fetches stock market data from **Yahoo Finance (via `yfinance`)**, parses it, and stores it in a PostgreSQL database.

---

## 🚀 Features

- ✅ **Dagster** for modular and maintainable pipeline orchestration  
- ✅ **Automated schedule** — runs every 2 hours via Dagster scheduler  
- ✅ **Fetch stock data** from **Yahoo Finance API** (default: AAPL)  
- ✅ **Validate stock data** to ensure correctness before processing  
- ✅ **Normalize data** into a consistent format  
- ✅ **Analyze stock data** — calculate price changes & insights  
- ✅ **Log data to CSV** for local record-keeping  
- ✅ **Summarize stock data** for quick insights  
- ✅ **Send alerts** (e.g., significant price changes)  
- ✅ **Store results** in **PostgreSQL** with upsert logic  
- ✅ **Export results to JSON** for API or sharing  
- ✅ **Generate HTML reports** for human-friendly review  
- ✅ **Backup PostgreSQL database** automatically before new runs  
- ✅ **Environment variables** managed securely via `.env` file  
- ✅ **Docker Compose** setup — runs PostgreSQL + Dagster webserver  
- ✅ **Database auto-creation** if it doesn't exist  
- ✅ **Fully containerized** — no local Python/PostgreSQL setup needed  
- ✅ **Scalable architecture** — easy to add new data sources or steps  

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

## Output 
<img width="960" height="382" alt="image1" src="https://github.com/user-attachments/assets/9c2d3c9c-866d-44ca-af07-d62ed45b84ba" />
<img width="960" height="327" alt="image2" src="https://github.com/user-attachments/assets/8ac6f5c4-819b-45b3-a222-ebb4b38ef403" />
<img width="951" height="536" alt="image3" src="https://github.com/user-attachments/assets/f70a51f4-08a2-446b-9612-24910a2e703b" />
<img width="757" height="463" alt="image4" src="https://github.com/user-attachments/assets/28833255-ac78-459d-bfb7-6b841d73f4b4" />
<img width="953" height="471" alt="image6 png" src="https://github.com/user-attachments/assets/5e262130-f339-4fb6-abfa-83154384671b" />

<img width="819" height="249" alt="container" src="https://github.com/user-attachments/assets/21a9013d-d6bc-4250-b50e-93d72d8a8eeb" />
<img width="940" height="407" alt="{0781ADEB-C75E-4D8B-AFD8-0A92847B4B6C}" src="https://github.com/user-attachments/assets/2b54e9f0-d680-4f46-bed5-7afb4b799876" />




## 📬 Author

 – *Manish kumar Yadav*


