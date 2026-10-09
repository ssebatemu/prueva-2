import re
import urllib.request

url_pagina = "http://alwaysdata.net"

try:
    print("Conectando con el servidor simulando un navegador Chrome real...")
    
    # Encabezados completos para evitar bloqueos por parte de Alwaysdata
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }
    
    req = urllib.request.Request(url_pagina, headers=headers)
    
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8')
    
    # Expresión regular robusta para capturar la URL completa del token
    match = re.search(r'https://[^\s"\'<>]+cvattv\.com\.ar[^\s"\'<>]+', html)
    
    if match:
        token = match.group(0).strip()
        print("¡Token localizado exitosamente!")
        
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(token)
            
        print("El token ha sido guardado dentro de token.txt")
    else:
        print("ERROR: No se encontró la estructura de transmisión en el HTML.")
        # Inspección por si la estructura cambió
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write("Error: Estructura de la página no reconocida o modificada.")

except Exception as e:
    print(f"Error de conexión: {e}")
    with open("token.txt", "w", encoding="utf-8") as f:
        f.write(f"Error al intentar acceder a la web: {e}")
