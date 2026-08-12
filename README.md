# 🚕 Ride ETL Pipeline

An end-to-end Data Engineering project that extracts ride-sharing data from CSV files, loads it into MySQL staging tables, performs data-quality checks, and transforms the data into an analytics-ready table.

## Architecture

CSV Files
   ↓
Python Extraction
   ↓
MySQL Staging Tables
   ↓
Data Quality Checks
   ↓
SQL Transformation
   ↓
ride_analytics

## Tech Stack

- Python
- MySQL
- SQL
- mysql-connector-python
- python-dotenv
- Git & GitHub

## Project Structure

```text
ride-etl-pipeline/
│
├── data/
│   ├── customers.csv
│   ├── drivers.csv
│   ├── rides.csv
│   └── payments.csv
│
├── src/
│   ├── generate_data.py
│   ├── extract.py
│   ├── load.py
│   ├── data_quality.py
│   └── transform.py
│
├── logs/
├── .gitignore
└── README.md