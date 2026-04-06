scrape:
	python3 pipeline/scrape_cheeses.py
	python3 pipeline/scrape_cheese_details.py

run:
	python3 pipeline/run_pipeline.py

preview:
	python3 pipeline/preview_staging.py

similarity:
	python3 notebooks/cheese_similarity.py

all:
	make scrape
	make run
	make preview

clean:
	rm -f data/cheese_analytics.db
	rm -f data/processed/*.csv