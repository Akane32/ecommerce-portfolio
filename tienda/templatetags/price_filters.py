from django import template

register = template.Library()

@register.filter
def format_price(value):
    """
    Formatea un precio con separadores de miles en formato chileno
    Ejemplo: 599990 -> 599.990
    """
    try:
        # Convertir a entero y formatear con puntos
        price = int(float(value))
        return f"{price:,}".replace(",", ".")
    except (ValueError, TypeError):
        return value 