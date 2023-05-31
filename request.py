import requests

# URL de la dirección de la API
url = 'http://192.168.0.10:18083/api/v4/acl/username'

# Credenciales de autenticación
username = 'amuracciole'
password = 'AjMv15293'

# Realizar una solicitud GET con las credenciales de autenticación
response = requests.get(url, auth=(username, password))

# Obtener el contenido de la respuesta
content = response.content

# Imprimir el contenido de la respuesta
print(f'Contenido de la respuesta: {content}')

