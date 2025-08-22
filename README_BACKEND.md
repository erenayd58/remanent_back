
# Remanent Backend (FastAPI + SQLModel)

## Run (local)
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API: http://localhost:8000/docs

## Quick start (HTTP)
1) Create a location:
```bash
curl -X POST http://localhost:8000/locations -H "Content-Type: application/json" -d '{"code":"S-B2-03-04","zone":"S","rack":"B2","row":"03","bin":"04"}'
```

2) Create a remanent:
```bash
curl -X POST http://localhost:8000/remanents -H "Content-Type: application/json" -d '{"id":"REM-2025-08-001","material":"AISI304","thickness_mm":1.5,"width_mm":1200,"height_mm":800,"location_code":"S-B2-03-04"}'
```

3) Generate label (PNG):
```bash
curl -X POST http://localhost:8000/labels/REM-2025-08-001
```
Output path is returned (./labels/REM-2025-08-001.png).

## Settings
- `.env` (optional): DATABASE_URL, LABEL_OUTPUT_DIR, thresholds.
- Thresholds default: min short edge 200 mm, min area 0.06 m², tolerance 5 mm.

## Deploy with Docker
```bash
docker compose up --build
```


## Export CSV
- Endpoint: `GET /export/remanents.csv`
- Dönen dosya: `text/csv` (Content-Disposition: attachment)
Örnek kolonlar: id, material, thickness_mm, width_mm, height_mm, location_code, created_at
