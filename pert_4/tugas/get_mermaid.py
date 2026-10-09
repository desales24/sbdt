import base64
import urllib.request
import json
import zlib

mermaid_code = """graph TD
    U((Pengguna)) -- "1. Request Data" --> A[Aplikasi Pusat]
    A -- "6. Response Data" --> U
    A -- "2. Query / Insert (Lokasi Jakarta)" --> DB1[(Database Node Jakarta)]
    DB1 -- "3. Result Set Jakarta" --> A
    A -- "4. Query / Insert (Lokasi Bandung)" --> DB2[(Database Node Bandung)]
    DB2 -- "5. Result Set Bandung" --> A"""

compressed = zlib.compress(mermaid_code.encode('utf-8'))
encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
url = f"https://kroki.io/mermaid/png/{encoded}"

req = urllib.request.Request(
    url, 
    data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
)

with urllib.request.urlopen(req) as response, open('praktikum/diagram.png', 'wb') as out_file:
    data = response.read()
    out_file.write(data)
print("Downloaded diagram.png")
