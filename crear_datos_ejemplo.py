#!/usr/bin/env python
import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from tienda.models import Categoria, Producto
from django.contrib.auth.models import User

def crear_datos_ejemplo():
    print("Creando datos de ejemplo...")
    
    # Crear categorías
    categorias = [
        {
            'nombre': 'Electrónicos',
            'descripcion': 'Los mejores productos electrónicos con la última tecnología'
        },
        {
            'nombre': 'Ropa',
            'descripcion': 'Moda actual y tendencias para todas las edades'
        },
        {
            'nombre': 'Hogar',
            'descripcion': 'Todo para decorar y equipar tu hogar'
        },
        {
            'nombre': 'Deportes',
            'descripcion': 'Equipamiento deportivo para todos los niveles'
        }
    ]
    
    categorias_creadas = []
    for cat_data in categorias:
        categoria, created = Categoria.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults=cat_data
        )
        categorias_creadas.append(categoria)
        if created:
            print(f"Categoría creada: {categoria.nombre}")
    
    # Crear productos de ejemplo
    productos = [
        # Electrónicos
        {
            'nombre': 'Smartphone Galaxy S23',
            'descripcion': 'El último smartphone de Samsung con cámara de 108MP y procesador de última generación',
            'precio': Decimal('899.99'),
            'precio_anterior': Decimal('999.99'),
            'stock': 50,
            'destacado': True,
            'categoria': categorias_creadas[0]
        },
        {
            'nombre': 'Laptop HP Pavilion',
            'descripcion': 'Laptop ideal para trabajo y estudio con procesador Intel i5 y 8GB RAM',
            'precio': Decimal('699.99'),
            'stock': 25,
            'destacado': True,
            'categoria': categorias_creadas[0]
        },
        {
            'nombre': 'Auriculares Sony WH-1000XM4',
            'descripcion': 'Auriculares inalámbricos con cancelación de ruido activa',
            'precio': Decimal('349.99'),
            'precio_anterior': Decimal('399.99'),
            'stock': 30,
            'categoria': categorias_creadas[0]
        },
        {
            'nombre': 'Smart TV LG 55"',
            'descripcion': 'Televisor inteligente 4K con webOS y acceso a streaming',
            'precio': Decimal('599.99'),
            'stock': 15,
            'categoria': categorias_creadas[0]
        },
        
        # Ropa
        {
            'nombre': 'Camiseta Básica',
            'descripcion': 'Camiseta de algodón 100% cómoda y transpirable',
            'precio': Decimal('19.99'),
            'stock': 100,
            'categoria': categorias_creadas[1]
        },
        {
            'nombre': 'Jeans Clásicos',
            'descripcion': 'Jeans de alta calidad con elástico para mayor comodidad',
            'precio': Decimal('49.99'),
            'precio_anterior': Decimal('59.99'),
            'stock': 75,
            'destacado': True,
            'categoria': categorias_creadas[1]
        },
        {
            'nombre': 'Sudadera con Capucha',
            'descripcion': 'Sudadera abrigada perfecta para el invierno',
            'precio': Decimal('39.99'),
            'stock': 60,
            'categoria': categorias_creadas[1]
        },
        {
            'nombre': 'Zapatillas Running',
            'descripcion': 'Zapatillas deportivas con tecnología de amortiguación avanzada',
            'precio': Decimal('89.99'),
            'stock': 40,
            'categoria': categorias_creadas[1]
        },
        
        # Hogar
        {
            'nombre': 'Lámpara de Mesa LED',
            'descripcion': 'Lámpara moderna con luz ajustable y diseño minimalista',
            'precio': Decimal('29.99'),
            'stock': 80,
            'categoria': categorias_creadas[2]
        },
        {
            'nombre': 'Juego de Sábanas',
            'descripcion': 'Sábanas de algodón egipcio suaves y duraderas',
            'precio': Decimal('45.99'),
            'precio_anterior': Decimal('55.99'),
            'stock': 50,
            'destacado': True,
            'categoria': categorias_creadas[2]
        },
        {
            'nombre': 'Cafetera Automática',
            'descripcion': 'Cafetera programable con molinillo integrado',
            'precio': Decimal('129.99'),
            'stock': 20,
            'categoria': categorias_creadas[2]
        },
        {
            'nombre': 'Almohadas Memory Foam',
            'descripcion': 'Almohadas ortopédicas para un descanso perfecto',
            'precio': Decimal('34.99'),
            'stock': 65,
            'categoria': categorias_creadas[2]
        },
        
        # Deportes
        {
            'nombre': 'Pelota de Fútbol',
            'descripcion': 'Pelota oficial de competición con tecnología avanzada',
            'precio': Decimal('24.99'),
            'stock': 90,
            'categoria': categorias_creadas[3]
        },
        {
            'nombre': 'Yoga Mat Premium',
            'descripcion': 'Mat de yoga antideslizante con diseño ecológico',
            'precio': Decimal('19.99'),
            'stock': 120,
            'categoria': categorias_creadas[3]
        },
        {
            'nombre': 'Pesas Ajustables',
            'descripcion': 'Set de pesas ajustables de 2.5kg a 25kg',
            'precio': Decimal('199.99'),
            'stock': 15,
            'destacado': True,
            'categoria': categorias_creadas[3]
        },
        {
            'nombre': 'Bicicleta Estática',
            'descripcion': 'Bicicleta de spinning para entrenamiento cardiovascular',
            'precio': Decimal('299.99'),
            'stock': 10,
            'categoria': categorias_creadas[3]
        }
    ]
    
    for prod_data in productos:
        # Crear imagen dummy (en un proyecto real, subirías imágenes reales)
        from django.core.files.base import ContentFile
        from PIL import Image
        import io
        
        # Crear una imagen dummy
        img = Image.new('RGB', (300, 300), color='lightgray')
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG')
        img_io.seek(0)
        
        producto, created = Producto.objects.get_or_create(
            nombre=prod_data['nombre'],
            defaults={
                'descripcion': prod_data['descripcion'],
                'precio': prod_data['precio'],
                'precio_anterior': prod_data.get('precio_anterior'),
                'stock': prod_data['stock'],
                'destacado': prod_data.get('destacado', False),
                'categoria': prod_data['categoria'],
                'activo': True
            }
        )
        
        if created:
            # Guardar imagen dummy
            producto.imagen.save(f"{prod_data['nombre'].replace(' ', '_').lower()}.jpg", 
                               ContentFile(img_io.getvalue()), save=True)
            print(f"Producto creado: {producto.nombre}")
    
    print("\n¡Datos de ejemplo creados exitosamente!")
    print(f"- {len(categorias_creadas)} categorías")
    print(f"- {len(productos)} productos")
    print("\nPuedes acceder al admin en: http://localhost:8000/admin/")
    print("Usuario: admin")
    print("Contraseña: admin")

if __name__ == '__main__':
    crear_datos_ejemplo() 