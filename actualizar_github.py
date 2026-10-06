import base64
import requests

def actualizar_listas_github():
    # ========================================================
    # ⚠️ 1. CONFIGURACIÓN DE TU CUENTA DE GITHUB
    # ========================================================
    # REQUISITO: Pega aquí tu Token de Acceso Personal (PAT) con permisos 'repo'
    GITHUB_TOKEN = "tu_github_token_aquí"
    
    USUARIO = "ssebatemu"
    REPOSITORIO = "prueva-2"
    
    # Nombre de la carpeta que quieres crear/usar dentro de tu GitHub
    CARPETA_DESTINO = "mis_listas_m3u"
    
    # Escribe aquí los nombres exactos de los archivos M3U que tienes en tu PC
    ARCHIVOS_A_PROCESAR = [
        "MPD prueva.m3u"
    ]
    
    # URL que entrega el token en texto plano
    URL_WEB_TOKEN = "https://alwaysdata.net"

    # ========================================================
    # 2. CAPTURAR EL TOKEN DE LA PÁGINA WEB
    # ========================================================
    try:
        print(f"Conectando a {URL_WEB_TOKEN}...")
        respuesta_web = requests.get(URL_WEB_TOKEN, timeout=15)
        
        if respuesta_web.status_code == 200:
            nuevo_token = respuesta_web.text.strip()
            print(f"¡Token capturado con éxito de la web!\n" + "-"*50)
        else:
            print(f"Error: La web respondió con código {respuesta_web.status_code}")
            return
    except Exception as e:
        print(f"Error al conectar con la página del token: {e}")
        return

    # ========================================================
    # 3. PROCESAR Y SUBIR CADA ARCHIVO A GITHUB
    # ========================================================
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    for nombre_archivo in ARCHIVOS_A_PROCESAR:
        print(f"Procesando archivo local: {nombre_archivo}...")
        
        # Leer el archivo local de tu computadora
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                contenido_m3u = archivo.read()
            
            # Reemplazar todas las variantes posibles del marcador de token
            contenido_m3u = contenido_m3u.replace('{{TOKEN}}', nuevo_token)
            contenido_m3u = contenido_m3u.replace('TOKEN', nuevo_token)
            contenido_m3u = contenido_m3u.replace('token', nuevo_token)
            
            # Convertir el contenido a formato Base64 (obligatorio para la API de GitHub)
            bytes_m3u = contenido_m3u.encode('utf-8')
            base64_m3u = base64.b64encode(bytes_m3u).decode('utf-8')
            
        except FileNotFoundError:
            print(f"⚠️ Alerta: No se encontró el archivo '{nombre_archivo}' en esta carpeta. Se saltará.\n")
            continue
        except Exception as e:
            print(f"⚠️ Error al procesar '{nombre_archivo}': {e}\n")
            continue

        # Definir la ruta final de la carpeta y el archivo en GitHub (CON LA BARRA CORREGIDA)
        ruta_completa_github = f"{CARPETA_DESTINO}/{nombre_archivo}"
        url_api_github = f"https://github.com{USUARIO}/{REPOSITORIO}/contents/{ruta_completa_github}"

        # Verificar si el archivo ya existe dentro de la carpeta en GitHub para obtener su código SHA
        respuesta_github_get = requests.get(url_api_github, headers=headers)
        
        sha_archivo = None
        if respuesta_github_get.status_code == 200:
            sha_archivo = respuesta_github_get.json().get("sha")

        # Preparar los datos que se enviarán a GitHub
        datos_commit = {
            "message": f"Actualización automática de {nombre_archivo} con token dinámico web",
            "content": base64_m3u
        }
        
        # Si el archivo ya existía en la carpeta, le pasamos el SHA para sobrescribirlo
        if sha_archivo:
            datos_commit["sha"] = sha_archivo

        # Enviar los datos definitivos a tu repositorio
        respuesta_github_put = requests.put(url_api_github, headers=headers, json=datos_commit)

        # Si responde 200 (OK) o 201 (Creado), el proceso fue exitoso
        if respuesta_github_put.status_code == 200 or respuesta_github_put.status_code == 201:
            print(f"✅ ¡Éxito! Guardado en la carpeta de GitHub como: {ruta_completa_github}\n")
        else:
            print(f"❌ Error al subir {nombre_archivo}: Código {respuesta_github_put.status_code}")
            print(respuesta_github_put.json(), "\n")

    print("-"*50 + f"\nProceso finalizado. Puedes revisar tu carpeta directamente aquí:\nhttps://github.com{USUARIO}/{REPOSITORIO}/tree/main/{CARPETA_DESTINO}")

if __name__ == "__main__":
    actualizar_listas_github()
