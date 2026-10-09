import re
import urllib.request

# URL de la página que contiene el token
url_pagina = "http://alwaysdata.net"

try:
    # Configurar un User-Agent para evitar bloqueos básicos
    req = urllib.request.Request(
        url_pagina, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Expresión regular para buscar la URL específica del token cvattv
    match = re.search(r'https://[^\s"\']+\.cvattv\.com\.ar:[0-9]+/[^\s"\']+', html)
    
    if match:
        token = match.group(0)
        # Guardar el token en el archivo txt
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(token)
        print("Token extraído y guardado correctamente.")
    else:
        print("No se encontró el formato del token en la página.")

except Exception as e:
    print(f"Error al obtener el token: {e}")
