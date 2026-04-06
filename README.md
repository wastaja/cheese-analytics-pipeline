# 🧀 Cheese Analytics Pipeline

End-to-end data pipeline that scrapes, transforms, and analyzes cheese data to build a simple recommendation system based on product similarity.

---

## 🚀 Project Overview

This project demonstrates a full analytics workflow:

- Web scraping of cheese products and their attributes  
- Data modeling using a layered architecture (raw → staging → mart)  
- Data cleaning & standardization  
- Similarity scoring model for cheese recommendations  
- Pipeline orchestration using Python and Makefile  

---

## 🏗️ Architecture

data/
  raw/        # scraped raw data (CSV)
  processed/  # cleaned & transformed data (exported)
  
pipeline/
  scrape_cheeses.py
  scrape_cheese_details.py
  run_pipeline.py
  preview_staging.py

sql/
  staging/
  marts/
  analysis/

notebooks/
  cheese_similarity.py

Makefile
README.md

---

## 🔄 Data Pipeline

1. Scraping
- Scrapes cheese list from multiple pages  
- Extracts product URLs  
- Fetches detailed attributes (country, milk type, strength, etc.)

2. Raw Layer
- Stores scraped data as CSV  
- No transformations applied  

3. Staging Layer
- Cleans and standardizes:
  - milk types (e.g. cow / goat)
  - cheese styles (hard / soft / blue)
  - strength levels → numeric scores  
- Handles missing values  

4. Mart Layer
- Final analytical dataset  
- Ready for scoring and analysis  

5. Similarity Model
- Scores similarity between cheeses based on:
  - milk type  
  - style  
  - pasteurisation  
  - country  
  - organic flag  
  - strength  

---

## 🧠 Example Output

Top similar cheeses to: Aettis

candidate_cheese                similarity_score
-----------------------------------------------
Alpine Meadows                  10
Blackbomber Extra Mature         8
Bleu des Causses AOC             7

---

## ⚙️ How to Run

make scrape      # scrape data
make run         # build pipeline
make preview     # preview transformed data
make similarity  # run similarity model
make all         # full pipeline

---

## 🛠️ Tech Stack

- Python (requests, BeautifulSoup, pandas)
- DuckDB
- SQL
- Makefile

---

## 📈 What This Project Demonstrates

- Building end-to-end data pipelines  
- Layered data modeling (raw → staging → mart)  
- Web scraping in production-like workflow  
- Feature engineering for similarity models  
- Combining SQL + Python in analytics engineering  

---

## 💡 Future Improvements

- Add text-based similarity (tasting notes NLP)  
- Introduce dbt for transformation layer  
- Schedule pipeline (Airflow / Prefect)  
- Store data in cloud (S3 + warehouse)  

---

## 👩‍💻 Author

Taja Vasilevich  
Analytics Engineer / Data Analyst