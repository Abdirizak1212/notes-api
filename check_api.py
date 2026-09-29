import urllib.request

for path in ['/', '/notes']:
    url = f'http://127.0.0.1:8000{path}'
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            body = r.read().decode()
            print(path, 'STATUS', r.status)
            print(body)
    except Exception as e:
        print(path, 'ERROR', e)
