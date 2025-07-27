#!/usr/bin/env python
import os
import sys
import django
from decimal import Decimal
from PIL import Image, ImageDraw, ImageFont
import io

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from tienda.models import Categoria, Producto

def crear_imagen_dummy(nombre, ancho=300, alto=300):
    """Crear una imagen dummy para el producto"""
    # Crear imagen con color de fondo
    imagen = Image.new('RGB', (ancho, alto), color=(240, 240, 240))
    draw = ImageDraw.Draw(imagen)
    
    # Agregar texto
    try:
        # Intentar usar una fuente del sistema
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        # Si no está disponible, usar la fuente por defecto
        font = ImageFont.load_default()
    
    # Centrar el texto
    bbox = draw.textbbox((0, 0), nombre, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (ancho - text_width) // 2
    y = (alto - text_height) // 2
    
    draw.text((x, y), nombre, fill=(100, 100, 100), font=font)
    
    # Guardar en buffer
    buffer = io.BytesIO()
    imagen.save(buffer, format='JPEG')
    buffer.seek(0)
    
    return buffer

def crear_datos_ejemplo():
    print("Creando datos de ejemplo...")
    
    # Limpiar datos existentes
    Producto.objects.all().delete()
    Categoria.objects.all().delete()
    
    # Crear categorías
    categorias = [
        {
            'nombre': 'Electrónicos',
            'descripcion': 'Productos electrónicos de última generación',
            'imagen': crear_imagen_dummy('Electrónicos')
        },
        {
            'nombre': 'Ropa',
            'descripcion': 'Ropa casual y deportiva',
            'imagen': crear_imagen_dummy('Ropa')
        },
        {
            'nombre': 'Hogar',
            'descripcion': 'Productos para el hogar y decoración',
            'imagen': crear_imagen_dummy('Hogar')
        },
        {
            'nombre': 'Deportes',
            'descripcion': 'Equipamiento deportivo y fitness',
            'imagen': crear_imagen_dummy('Deportes')
        }
    ]
    
    categorias_creadas = []
    for cat_data in categorias:
        categoria = Categoria.objects.create(
            nombre=cat_data['nombre'],
            descripcion=cat_data['descripcion'],
            activo=True
        )
        categoria.imagen.save(f"{cat_data['nombre'].lower()}.jpg", cat_data['imagen'], save=True)
        categorias_creadas.append(categoria)
    
    # Crear productos
    productos = [
        # Electrónicos
        {
            'nombre': 'Smartphone Galaxy S23',
            'descripcion': 'Smartphone Samsung Galaxy S23 con 128GB, 8GB RAM, cámara de 50MP',
            'precio': Decimal('599990'),
            'precio_anterior': Decimal('699990'),
            'categoria': categorias_creadas[0],
            'stock': 15,
            'destacado': True,
            'imagen': crear_imagen_dummy('Galaxy S23')
        },
        {
            'nombre': 'Laptop HP Pavilion',
            'descripcion': 'Laptop HP Pavilion 15.6" Intel Core i5, 8GB RAM, 512GB SSD',
            'precio': Decimal('449990'),
            'precio_anterior': Decimal('549990'),
            'categoria': categorias_creadas[0],
            'stock': 8,
            'destacado': True,
            'imagen': crear_imagen_dummy('HP Pavilion')
        },
        {
            'nombre': 'Auriculares Sony WH-1000XM4',
            'descripcion': 'Auriculares inalámbricos con cancelación de ruido activa',
            'precio': Decimal('249990'),
            'precio_anterior': Decimal('299990'),
            'categoria': categorias_creadas[0],
            'stock': 20,
            'destacado': False,
            'imagen': crear_imagen_dummy('Sony WH-1000XM4')
        },
        {
            'nombre': 'Smart TV LG 55"',
            'descripcion': 'Smart TV LG 55" 4K Ultra HD con WebOS',
            'precio': Decimal('399990'),
            'precio_anterior': Decimal('499990'),
            'categoria': categorias_creadas[0],
            'stock': 5,
            'destacado': True,
            'imagen': crear_imagen_dummy('LG Smart TV')
        },
        
        # Ropa
        {
            'nombre': 'Camiseta Básica',
            'descripcion': 'Camiseta 100% algodón, disponible en varios colores',
            'precio': Decimal('15990'),
            'precio_anterior': Decimal('19990'),
            'categoria': categorias_creadas[1],
            'stock': 50,
            'destacado': False,
            'imagen': crear_imagen_dummy('Camiseta Básica')
        },
        {
            'nombre': 'Jeans Clásicos',
            'descripcion': 'Jeans de alta calidad, corte clásico, disponible en varios talles',
            'precio': Decimal('39990'),
            'precio_anterior': Decimal('49990'),
            'categoria': categorias_creadas[1],
            'stock': 30,
            'destacado': False,
            'imagen': crear_imagen_dummy('Jeans Clásicos')
        },
        {
            'nombre': 'Chaqueta Deportiva',
            'descripcion': 'Chaqueta deportiva con tecnología de respiración',
            'precio': Decimal('59990'),
            'precio_anterior': Decimal('79990'),
            'categoria': categorias_creadas[1],
            'stock': 25,
            'destacado': True,
            'imagen': crear_imagen_dummy('Chaqueta Deportiva')
        },
        {
            'nombre': 'Zapatillas Running',
            'descripcion': 'Zapatillas para running con tecnología de amortiguación',
            'precio': Decimal('89990'),
            'precio_anterior': Decimal('109990'),
            'categoria': categorias_creadas[1],
            'stock': 15,
            'destacado': True,
            'imagen': crear_imagen_dummy('Zapatillas Running')
        },
        
        # Hogar
        {
            'nombre': 'Cafetera Automática',
            'descripcion': 'Cafetera automática con molinillo integrado',
            'precio': Decimal('129990'),
            'precio_anterior': Decimal('159990'),
            'categoria': categorias_creadas[2],
            'stock': 12,
            'destacado': False,
            'imagen': crear_imagen_dummy('Cafetera Automática')
        },
        {
            'nombre': 'Lámpara de Mesa LED',
            'descripcion': 'Lámpara de mesa LED con luz ajustable',
            'precio': Decimal('29990'),
            'precio_anterior': Decimal('39990'),
            'categoria': categorias_creadas[2],
            'stock': 35,
            'destacado': False,
            'imagen': crear_imagen_dummy('Lámpara LED')
        },
        {
            'nombre': 'Juego de Sábanas',
            'descripcion': 'Juego de sábanas 100% algodón egipcio, 300 hilos',
            'precio': Decimal('39990'),
            'precio_anterior': Decimal('49990'),
            'categoria': categorias_creadas[2],
            'stock': 40,
            'destacado': False,
            'imagen': crear_imagen_dummy('Sábanas')
        },
        {
            'nombre': 'Almohadas Memory Foam',
            'descripcion': 'Almohadas con memory foam para mejor descanso',
            'precio': Decimal('19990'),
            'precio_anterior': Decimal('24990'),
            'categoria': categorias_creadas[2],
            'stock': 60,
            'destacado': True,
            'imagen': crear_imagen_dummy('Almohadas Memory Foam')
        },
        
        # Deportes
        {
            'nombre': 'Bicicleta Estática',
            'descripcion': 'Bicicleta estática con monitor de ritmo cardíaco',
            'precio': Decimal('199990'),
            'precio_anterior': Decimal('249990'),
            'categoria': categorias_creadas[3],
            'stock': 8,
            'destacado': True,
            'imagen': crear_imagen_dummy('Bicicleta Estática')
        },
        {
            'nombre': 'Pesas Ajustables',
            'descripcion': 'Set de pesas ajustables de 2.5kg a 25kg',
            'precio': Decimal('89990'),
            'precio_anterior': Decimal('109990'),
            'categoria': categorias_creadas[3],
            'stock': 20,
            'destacado': False,
            'imagen': crear_imagen_dummy('Pesas Ajustables')
        },
        {
            'nombre': 'Pelota de Fútbol',
            'descripcion': 'Pelota de fútbol oficial, tamaño 5',
            'precio': Decimal('15990'),
            'precio_anterior': Decimal('19990'),
            'categoria': categorias_creadas[3],
            'stock': 45,
            'destacado': False,
            'imagen': crear_imagen_dummy('Pelota Fútbol')
        },
        {
            'nombre': 'Yoga Mat Premium',
            'descripcion': 'Mat de yoga premium, antideslizante, 6mm de grosor',
            'precio': Decimal('12990'),
            'precio_anterior': Decimal('15990'),
            'categoria': categorias_creadas[3],
            'stock': 30,
            'destacado': False,
            'imagen': crear_imagen_dummy('Yoga Mat')
        }
    ]
    
    for prod_data in productos:
        producto = Producto.objects.create(
            nombre=prod_data['nombre'],
            descripcion=prod_data['descripcion'],
            precio=prod_data['precio'],
            precio_anterior=prod_data['precio_anterior'],
            categoria=prod_data['categoria'],
            stock=prod_data['stock'],
            destacado=prod_data['destacado'],
            activo=True
        )
        producto.imagen.save(f"{prod_data['nombre'].lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')}.jpg", prod_data['imagen'], save=True)
    
    print("\n¡Datos de ejemplo creados exitosamente!")
    print(f"- {len(categorias_creadas)} categorías")
    print(f"- {len(productos)} productos")
    print("\nUsuario: admin")
    print("Contraseña: admin")

if __name__ == '__main__':
    crear_datos_ejemplo() 