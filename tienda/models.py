from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_anterior = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/')
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre

    @property
    def tiene_descuento(self):
        return self.precio_anterior and self.precio_anterior > self.precio
    
    @property
    def precio_formateado(self):
        """Retorna el precio formateado con puntos de miles"""
        return f"{int(self.precio):,}".replace(",", ".")
    
    @property
    def precio_anterior_formateado(self):
        """Retorna el precio anterior formateado con puntos de miles"""
        if self.precio_anterior:
            return f"{int(self.precio_anterior):,}".replace(",", ".")
        return ""
    
    @property
    def ahorro_formateado(self):
        """Retorna el ahorro formateado con puntos de miles"""
        if self.tiene_descuento:
            ahorro = self.precio_anterior - self.precio
            return f"{int(ahorro):,}".replace(",", ".")
        return ""

    @property
    def porcentaje_descuento(self):
        if self.tiene_descuento:
            return int(((self.precio_anterior - self.precio) / self.precio_anterior) * 100)
        return 0

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username if self.usuario else 'Anónimo'}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.all())
    
    @property
    def total_formateado(self):
        """Retorna el total formateado con puntos de miles"""
        return f"{int(self.total):,}".replace(",", ".")

    @property
    def cantidad_items(self):
        return sum(item.cantidad for item in self.items.all())

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_agregado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['carrito', 'producto']

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad
    
    @property
    def subtotal_formateado(self):
        """Retorna el subtotal formateado con puntos de miles"""
        return f"{int(self.subtotal):,}".replace(",", ".")

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Información de envío
    nombre_completo = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)
    
    # Información de pago
    METODO_PAGO_CHOICES = [
        ('transferencia', 'Transferencia bancaria'),
        ('tarjeta', 'Tarjeta de crédito/débito'),
        ('paypal', 'PayPal'),
    ]
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO_CHOICES, default='transferencia')
    pagado = models.BooleanField(default=False)
    fecha_pago = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-fecha_pedido']

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
    
    @property
    def total_formateado(self):
        """Retorna el total formateado con puntos de miles"""
        return f"{int(self.total):,}".replace(",", ".")

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"

    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
    
    @property
    def precio_unitario_formateado(self):
        """Retorna el precio unitario formateado con puntos de miles"""
        return f"{int(self.precio_unitario):,}".replace(",", ".")
    
    @property
    def subtotal_formateado(self):
        """Retorna el subtotal formateado con puntos de miles"""
        return f"{int(self.subtotal):,}".replace(",", ".")
