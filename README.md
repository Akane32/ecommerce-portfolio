# 🛒 Mi Ecommerce - Django

Un ecommerce completo desarrollado en Django para portafolio de programador. Incluye todas las funcionalidades esenciales de una tienda online moderna.

## ✨ Características

- **Sistema de Autenticación**: Registro, login y logout de usuarios
- **Catálogo de Productos**: Con categorías, filtros y búsqueda
- **Carrito de Compras**: Funcionalidad AJAX para agregar/eliminar productos
- **Sistema de Pedidos**: Proceso completo de checkout
- **Panel de Administración**: Gestión completa de productos, categorías y pedidos
- **Interfaz Responsive**: Diseño moderno con Bootstrap 5
- **Sistema de Descuentos**: Productos con precios rebajados
- **Gestión de Stock**: Control de inventario automático

## 🚀 Instalación

### Prerrequisitos

- Python 3.8+
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repositorio>
   cd ecommerce-portfolio
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   ```bash
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install django pillow django-crispy-forms crispy-bootstrap5
   ```

5. **Ejecutar migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crear superusuario**
   ```bash
   python manage.py createsuperuser
   ```

7. **Crear datos de ejemplo (opcional)**
   ```bash
   python crear_datos_ejemplo.py
   ```

8. **Ejecutar el servidor**
   ```bash
   python manage.py runserver
   ```

## 📱 Uso

### Acceso a la Aplicación

- **Frontend**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **Usuario admin**: admin
- **Contraseña**: admin

### Funcionalidades Principales

#### Para Usuarios
1. **Navegación**: Explorar productos por categorías
2. **Búsqueda**: Buscar productos por nombre o descripción
3. **Carrito**: Agregar productos con cantidades
4. **Checkout**: Proceso de compra con información de envío
5. **Pedidos**: Historial y seguimiento de pedidos

#### Para Administradores
1. **Gestión de Productos**: Crear, editar y eliminar productos
2. **Categorías**: Organizar productos por categorías
3. **Pedidos**: Ver y gestionar el estado de los pedidos
4. **Stock**: Control automático de inventario

## 🏗️ Estructura del Proyecto

```
ecommerce-portfolio/
├── ecommerce/              # Configuración principal
│   ├── settings.py        # Configuraciones del proyecto
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuración WSGI
├── tienda/               # Aplicación principal
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Lógica de negocio
│   ├── forms.py          # Formularios
│   ├── admin.py          # Panel de administración
│   └── urls.py           # URLs de la aplicación
├── templates/            # Plantillas HTML
│   ├── base.html         # Plantilla base
│   └── tienda/          # Plantillas específicas
├── static/              # Archivos estáticos
├── media/               # Archivos subidos
├── manage.py            # Script de gestión Django
└── README.md           # Este archivo
```

## 🎨 Tecnologías Utilizadas

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, jQuery
- **Base de Datos**: SQLite (desarrollo)
- **Formularios**: Django Crispy Forms
- **Imágenes**: Pillow

## 📊 Modelos de Datos

### Categoria
- nombre, descripcion, imagen, activo, fecha_creacion

### Producto
- nombre, descripcion, precio, precio_anterior, categoria, imagen, stock, activo, destacado

### Carrito & ItemCarrito
- Gestión del carrito de compras con cantidades

### Pedido & ItemPedido
- Proceso completo de pedidos con información de envío

## 🔧 Configuración Avanzada

### Variables de Entorno
Crear archivo `.env`:
```
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Base de Datos
Para producción, cambiar a PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tu_db',
        'USER': 'tu_usuario',
        'PASSWORD': 'tu_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Despliegue

### Heroku
1. Crear `requirements.txt`
2. Configurar `Procfile`
3. Configurar variables de entorno
4. Desplegar con Git

### VPS
1. Configurar servidor web (Nginx)
2. Configurar WSGI (Gunicorn)
3. Configurar base de datos PostgreSQL
4. Configurar archivos estáticos

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- LinkedIn: [Tu Perfil](https://linkedin.com/in/tu-perfil)

## 🙏 Agradecimientos

- Django Documentation
- Bootstrap Team
- Font Awesome
- Comunidad Django

---

⭐ Si este proyecto te ayuda, dale una estrella en GitHub! 