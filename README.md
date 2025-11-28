# Taquería Taco — Django demo app

**Características del proyecto**

- `manage.py`: Script de gestión de Django para ejecutar comandos (`runserver`, `migrate`, `createsuperuser`, etc.).
- `db.sqlite3`: Archivo de base de datos SQLite (usado si no se configura PostgreSQL vía env).
- `.env`: Variables de entorno usadas por Docker Compose y la configuración de Django (base de datos, correo, secret key, debug, etc.).
- `docker-compose.yml`: Define los servicios `web`, `db` y `pgadmin`. Carga las variables de `.env` y monta la aplicación en `/app` dentro del contenedor.
- `Dockerfile`: Imagen para el servicio web (con Python, dependencias y ejecución del servidor).
- `requirements.txt`: Dependencias Python necesarias para ejecutar la app.
- `scripts/entrypoint.sh`: Script que corre migraciones y arranca el servidor dentro del contenedor `web`.

- `backend/`: Contiene la configuración de Django (`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`).
	- `backend/settings.py` lee variables de entorno y configura la base de datos, archivos estáticos y la conexión de correo. Si `EMAIL_HOST` está presente, se configura SMTP, de lo contrario usa el backend de consola.

- `taqueria/`: Aplicación Django principal.
	- `models.py`: Define `Category`, `Product`, `Order`, `OrderItem`.
	- `admin.py`: Registro de modelos en el admin de Django (incluye vista de color para categorías).
	- `views.py`: Vistas para `home`, `register`, `signin`, `profile`, `cart` y `checkout`. El checkout crea la orden y llama a `send_order_confirmation_async`.
	- `cart.py`: Clase `Cart` que usa la sesión para almacenar artículos del carrito.
	- `email.py`: Funciones `send_order_confirmation` y `send_order_confirmation_async` que renderizan `templates/emails/order_confirmation.{html,txt}` y envían correo (usando `EmailMultiAlternatives`).
	- `templates/`: Plantillas HTML y los templates de correo (`templates/emails/order_confirmation.html` y `.txt`).
	- `management/commands/send_test_order_email.py`: Comando para crear una orden de prueba y enviar el correo (útil para smoke tests).

**Cómo ejecutar la aplicación**

Requisitos locales: Docker y Docker Compose.

1. Ajustar las variables necesarias del archivo `.env`:
	 - `POSTGRES_*` si se usa Postgres, o dejar la base SQLite por defecto.
	 - `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`.
	 - Para enviar correos por SMTP: `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`.

2. Construir y levantar los servicios (desde la raíz del proyecto donde está `docker-compose.yml`):
```cmd
docker compose up -d --build
```

3. Verificar que los contenedores estén corriendo:
```cmd
docker compose ps
```

4. Crear superusuario:
```cmd
docker compose exec web python manage.py createsuperuser
```

5. Acceder a la aplicación en: `http://localhost:8000/` y al admin en `http://localhost:8000/admin/`.

**Cómo funciona el archivo Docker / Docker Compose**

- `docker-compose.yml` define tres servicios principales:
	- `db`: Servicio PostgreSQL con volúmenes persistentes y variables `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` tomadas de `.env`.
	- `web`: Servicio que construye la imagen desde `Dockerfile`, monta el código (`.:/app`) y ejecuta `scripts/entrypoint.sh`. Está configurado para leer variables de entorno desde `.env` usando `env_file: .env` y además pasa `DB_HOST` y `DJANGO_SETTINGS_MODULE` directamente.
	- `pgadmin`: Interfaz web opcional para administrar la base de datos PostgreSQL.

- `Dockerfile`: instala dependencias de `requirements.txt`, copia el código (en el contexto del contenedor) y define el comando por defecto. El contenedor `web` ejecuta `scripts/entrypoint.sh`, que aplica migraciones y arranca el servidor de Django.

- Variables de entorno y recarga: `docker compose up -d --force-recreate web` o `--build` recrea el contenedor `web` para recoger cambios en `.env`. 


