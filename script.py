import re
import urllib.request

# CAMBIO CLAVE: Se añade la 's' a https:// para ingresar a la web correcta
url_pagina = "https://alwaysdata.net"

try:
    print("Conectando con la página segura...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9'
    }
    
    req = urllib.request.Request(url_pagina, headers=headers)
    
    with urllib.request.urlopen(req, timeout=15) as response:
        html = response.read().decode('utf-8')
    
    # Buscar el enlace de transmisión que contiene cvattv.com.ar
    match = re.search(r'https://[^\s"\'<>`]+cvattv\.com\.ar[^\s"\'<>`]+', html)
    
    if match:
        token = match.group(0).strip()
        print("¡Token localizado con éxito en la página correcta!")
        
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(token)
            
        print("El token ha sido guardado dentro de token.txt")
    else:
        print("ERROR: No se encontró la cadena 'cvattv.com.ar' dentro del código HTML.")
        fragmento_html = html[:500].replace('\n', ' ')
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(f"Error: Estructura no reconocida. Inicio del HTML recibido: {fragmento_html}")

except Exception as e:
    print(f"Error de conexión: {e}")
    with open("token.txt", "w", encoding="utf-8") as f:
        f.write(f"Error al intentar acceder a la web: {e}")
