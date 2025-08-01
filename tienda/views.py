from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Producto, Categoria, Carrito, ItemCarrito, Pedido, ItemPedido
from .forms import PedidoForm
import json

def home(request):
    """Vista principal con productos destacados"""
    productos_destacados = Producto.objects.filter(destacado=True, activo=True)[:6]
    categorias = Categoria.objects.filter(activo=True)
    context = {
        'productos_destacados': productos_destacados,
        'categorias': categorias,
    }
    return render(request, 'tienda/home.html', context)

def lista_productos(request):
    """Lista de todos los productos con filtros"""
    productos = Producto.objects.filter(activo=True)
    categoria_id = request.GET.get('categoria')
    busqueda = request.GET.get('q')
    orden = request.GET.get('orden', 'nombre')

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | 
            Q(descripcion__icontains=busqueda) |
            Q(categoria__nombre__icontains=busqueda)
        )

    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nuevos':
        productos = productos.order_by('-fecha_creacion')
    else:
        productos = productos.order_by('nombre')

    # Paginación
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.filter(activo=True)
    
    context = {
        'page_obj': page_obj,
        'categorias': categorias,
        'categoria_actual': categoria_id,
        'busqueda': busqueda,
        'orden': orden,
    }
    return render(request, 'tienda/lista_productos.html', context)

def detalle_producto(request, producto_id):
    """Vista detallada de un producto"""
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, 
        activo=True
    ).exclude(id=producto.id)[:4]
    
    context = {
        'producto': producto,
        'productos_relacionados': productos_relacionados,
    }
    return render(request, 'tienda/detalle_producto.html', context)

def obtener_carrito(request):
    """Obtiene o crea el carrito del usuario"""
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    else:
        # Para usuarios anónimos, usar sesión
        carrito_id = request.session.get('carrito_id')
        if carrito_id:
            carrito = Carrito.objects.filter(id=carrito_id).first()
        else:
            carrito = Carrito.objects.create()
            request.session['carrito_id'] = carrito.id
    return carrito

def carrito(request):
    """Vista del carrito de compras"""
    carrito = obtener_carrito(request)
    context = {
        'carrito': carrito,
    }
    return render(request, 'tienda/carrito.html', context)

def agregar_al_carrito(request):
    """Agregar producto al carrito via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad', 1)
        
        producto = get_object_or_404(Producto, id=producto_id, activo=True)
        carrito = obtener_carrito(request)
        
        # Verificar stock
        if producto.stock < cantidad:
            return JsonResponse({
                'success': False,
                'message': f'Solo hay {producto.stock} unidades disponibles'
            })
        
        # Agregar o actualizar item en carrito
        item, created = ItemCarrito.objects.get_or_create(
            carrito=carrito,
            producto=producto,
            defaults={'cantidad': cantidad}
        )
        
        if not created:
            item.cantidad += cantidad
            item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{producto.nombre} agregado al carrito',
            'carrito_total': carrito.total,
            'carrito_cantidad': carrito.cantidad_items
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def actualizar_carrito(request):
    """Actualizar cantidad en carrito via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        cantidad = data.get('cantidad')
        
        item = get_object_or_404(ItemCarrito, id=item_id)
        
        if cantidad <= 0:
            item.delete()
        else:
            if item.producto.stock < cantidad:
                return JsonResponse({
                    'success': False,
                    'message': f'Solo hay {item.producto.stock} unidades disponibles'
                })
            item.cantidad = cantidad
            item.save()
        
        carrito = item.carrito
        return JsonResponse({
            'success': True,
            'carrito_total': carrito.total,
            'carrito_cantidad': carrito.cantidad_items,
            'item_subtotal': item.subtotal if cantidad > 0 else 0
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

def eliminar_del_carrito(request):
    """Eliminar item del carrito via AJAX"""
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        item = get_object_or_404(ItemCarrito, id=item_id)
        carrito = item.carrito
        item.delete()
        
        return JsonResponse({
            'success': True,
            'carrito_total': carrito.total,
            'carrito_cantidad': carrito.cantidad_items
        })
    
    return JsonResponse({'success': False, 'message': 'Método no permitido'})

@login_required
def checkout(request):
    """Proceso de checkout"""
    carrito = obtener_carrito(request)
    
    if carrito.cantidad_items == 0:
        messages.warning(request, 'Tu carrito está vacío')
        return redirect('carrito')
    
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.total = carrito.total
            pedido.pagado = True
            pedido.save()
            
            # Crear items del pedido
            for item in carrito.items.all():
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio,
                    subtotal=item.subtotal
                )
                
                # Actualizar stock
                item.producto.stock -= item.cantidad
                item.producto.save()
            
            # Limpiar carrito
            carrito.items.all().delete()
            if 'carrito_id' in request.session:
                del request.session['carrito_id']
            
            messages.success(request, f'Pedido #{pedido.id} creado exitosamente')
            return redirect('detalle_pedido', pedido_id=pedido.id)
    else:
        form = PedidoForm()
    
    context = {
        'form': form,
        'carrito': carrito,
    }
    return render(request, 'tienda/checkout.html', context)

@login_required
def mis_pedidos(request):
    """Lista de pedidos del usuario"""
    pedidos = Pedido.objects.filter(usuario=request.user)
    context = {
        'pedidos': pedidos,
    }
    return render(request, 'tienda/mis_pedidos.html', context)

@login_required
def detalle_pedido(request, pedido_id):
    """Detalle de un pedido específico"""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    context = {
        'pedido': pedido,
    }
    return render(request, 'tienda/detalle_pedido.html', context)
