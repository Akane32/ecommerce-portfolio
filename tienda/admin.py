from django.contrib import admin
from .models import Categoria, Producto, Carrito, ItemCarrito, Pedido, ItemPedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre']
    list_editable = ['activo']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'stock', 'activo', 'destacado']
    list_filter = ['categoria', 'activo', 'destacado', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo', 'destacado']

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha_creacion', 'total', 'cantidad_items']
    list_filter = ['fecha_creacion']
    search_fields = ['usuario__username']

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['carrito', 'producto', 'cantidad', 'subtotal']
    list_filter = ['fecha_agregado']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_pedido', 'estado', 'total', 'pagado']
    list_filter = ['estado', 'pagado', 'fecha_pedido']
    search_fields = ['usuario__username', 'nombre_completo', 'email']
    list_editable = ['estado', 'pagado']
    readonly_fields = ['fecha_pedido', 'total']

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['pedido__estado']
