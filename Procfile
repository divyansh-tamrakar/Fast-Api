release: fastapi db upgrade
release: fastapi db stamp head


web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
