import re
import urllib.request
import os

url_pagina = "http://alwaysdata.net"

try:
    print("Iniciando la descarga de la página...")
    req = urllib.request.Request(
        url_pagina, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    # Expresión regular mejorada y más flexible para capturar el token
    match = re.search(r'https://edge[^\s"\']+', html)
    
    if match:
        token = match.group(0).strip()
        print(f"¡Token encontrado de forma exitosa!")
        
        # Sobrescribir o crear de cero el archivo de texto
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write(token)
            
        print("El token ha sido escrito dentro de token.txt")
    else:
        print("ERROR CRÍTICO: La página no contiene ningún token con formato 'https://edge...'")
        # Dejamos un mensaje de error dentro del txt para saber qué falló
        with open("token.txt", "w", encoding="utf-8") as f:
            f.write("Error: No se encontró el token en la página web.")

except Exception as e:
    print(f"Error durante la ejecución: {e}")
    with open("token.txt", "w", encoding="utf-8") as f:
        f.write(f"Error de conexión o lectura: {e}")
