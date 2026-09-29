import requests, json

base = "http://127.0.0.1:8002"

r1 = requests.post(f"{base}/notes", json={"title": "FastAPI Week 4", "content": "Building Notes API with SQLite and Pydantic validation"})
try:
	j = r1.json()
except Exception:
	j = r1.text
print("POST /notes (1):", r1.status_code, j)

r2 = requests.post(f"{base}/notes", json={"title": "SQLite Persistence", "content": "Data survives server restarts"})
try:
	j = r2.json()
except Exception:
	j = r2.text
print("POST /notes (2):", r2.status_code, j)

r3 = requests.get(f"{base}/notes")
try:
	j = r3.json()
except Exception:
	j = r3.text
print("GET /notes:", r3.status_code, j)

r4 = requests.get(f"{base}/notes/1")
try:
	j = r4.json()
except Exception:
	j = r4.text
print("GET /notes/1:", r4.status_code, j)

r5 = requests.put(f"{base}/notes/1", json={"title": "FastAPI Week 4 - Complete", "content": "Notes API with full CRUD working"})
try:
	j = r5.json()
except Exception:
	j = r5.text
print("PUT /notes/1:", r5.status_code, j)

r6 = requests.delete(f"{base}/notes/2")
print("DELETE /notes/2:", r6.status_code)

r7 = requests.get(f"{base}/notes")
try:
	j = r7.json()
except Exception:
	j = r7.text
print("GET /notes (final):", r7.status_code, j)
