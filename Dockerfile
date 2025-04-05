# Imagen base de Python
FROM python:3.8

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (si es necesario)
RUN apt-get update && apt-get install -y netcat

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script de entrada (si lo usas)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer el puerto (ajusta según el puerto en settings.py)
EXPOSE 8000

# Comando de arranque
ENTRYPOINT ["/entrypoint.sh"]