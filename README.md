# Micro servicio de rutas

Repositorio con código base con la implementación del micro servicio de rutas usando el patrón Event Sourcing.

## AlpesOnline
### Ejecutar Base de datos
Desde el directorio principal ejecute el siguiente comando.

```bash
docker-compose --profiles db up
```

Este comando descarga las imágenes e instala las dependencias de la base datos.

### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/alpesonline/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/alpesonline/api --debug run
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f alpesonline.Dockerfile -t alpesonline/flask
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 5000:5000 alpesonline/flask
```

### Consultar tópicos
Abrir en una terminal:

```bash
docker exec -it broker bash
```

Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-admin topics list public/default
```

### Cambiar retención de tópicos
Abrir en una terminal:

```bash
docker exec -it broker bash
```
Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1
```

Para poder ver que los cambios fueron efectivos ejecute el siguiente comando:

```bash
./bin/pulsar-admin namespaces get-retention public/default
```

## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose up
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose up -d
```

## Comandos útiles

### Listar contenedoras en ejecución
```bash
docker ps
```

### Listar todas las contenedoras
```bash
docker ps -a
```

### Parar contenedora
```bash
docker stop <id_contenedora>
```

### Eliminar contenedora
```bash
docker rm <id_contenedora>
```

### Listar imágenes
```bash
docker images
```

### Eliminar imágenes
```bash
docker images rm <id_imagen>
```

### Acceder a una contendora
```bash
docker exec -it <id_contenedora> sh
```

### Kill proceso que esta usando un puerto
```bash
fuser -k <puerto>/tcp
```

### Correr docker-compose usando profiles
```bash
docker-compose --profile <db|pulsar|alpesonline> up
```