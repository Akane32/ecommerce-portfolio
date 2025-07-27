from django.contrib import admin
from .models import Categoria, Producto, Carrito, ItemCarrito, Pedido, ItemPedido
from django.utils.html import format_html

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_editable = ['activo']

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'destacado', 'activo', 'imagen_preview')
    list_filter = ('categoria', 'activo', 'destacado')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'stock', 'destacado', 'activo')
    readonly_fields = ('imagen_preview',)

    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 60px; border-radius: 6px;" />', obj.imagen.url)
        return "(Sin imagen)"
    imagen_preview.short_description = 'Imagen'

admin.site.register(Producto, ProductoAdmin)

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha_creacion', 'fecha_actualizacion']
    search_fields = ['usuario__username']

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ['carrito', 'producto', 'cantidad', 'fecha_agregado']
    search_fields = ['producto__nombre', 'carrito__usuario__username']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_pedido', 'estado', 'total']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['usuario__username', 'id']

@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    search_fields = ['producto__nombre', 'pedido__usuario__username']
