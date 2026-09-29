import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError

base = 'http://127.0.0.1:8000/notes'

def req(method, path='', data=None):
    url = base + path
    headers = {'Content-Type': 'application/json'}
    data_bytes = None
    if data is not None:
        data_bytes = json.dumps(data).encode('utf-8')
    req = Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8')
            print(body)
    except HTTPError as e:
        print(f'HTTPError {e.code}: {e.read().decode() if e.fp else e.reason}')
    except Exception as e:
        print('Error:', e)

print('--- POST 1 ---')
req('POST', '', {'title':'FastAPI Week 4','content':'Building Notes API with SQLite and Pydantic validation'})
print('--- POST 2 ---')
req('POST', '', {'title':'SQLite Persistence','content':'Data survives server restarts'})
print('--- GET /notes ---')
req('GET')
print('--- GET /notes/1 ---')
req('GET','/1')
print('--- PUT /notes/1 ---')
req('PUT','/1', {'title':'FastAPI Week 4 - Complete','content':'Notes API with full CRUD working'})
print('--- DELETE /notes/2 ---')
req('DELETE','/2')
print('--- GET /notes (final) ---')
req('GET')
