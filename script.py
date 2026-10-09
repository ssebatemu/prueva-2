import re
import urllib.request

url_pagina = "http://alwaysdata.net"

try:
    print("Conectando con la página...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9'
    }
    
    req = urllib.request.Request(url_pagina, headers=headers)
    
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8')
    
    # NUEVA ESTRATEGIA: Buscar cualquier texto continuo que contenga cvattv.com.ar
    # Captura la URL completa sin importar el subdominio con el que comience
    match = re.search(r'https://[^\s"\'<>`]+cvattv\.com\.ar[^\s"\'<>`]+', html)
    
    if match:
        token = match.group(0).strip()
        print("¡Token localizado con la nueva regla!")
        
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(token)
            
        print("El token ha sido guardado dentro de token.txt")
    else:
        print("ERROR: No se encontró la cadena 'cvattv.com.ar' dentro del código HTML.")
        # Guardamos los primeros 500 caracteres del HTML en token.txt para diagnosticar qué lee el script
        fragmento_html = html[:500].replace('\n', ' ')
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(f"Error: Estructura no reconocida. Inicio del HTML recibido: {fragmento_html}")

except Exception as e:
    print(f"Error de conexión: {e}")
    with open("token.txt", "w", encoding="utf-8") as f:
        f.write(f"Error al intentar acceder a la web: {e}")
