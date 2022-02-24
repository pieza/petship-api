conda create --name=petship-api python=3
conda activate petship-api

uvicorn app:app --port=5000 --reload