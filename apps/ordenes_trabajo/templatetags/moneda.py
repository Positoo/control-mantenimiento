from django import template

register = template.Library()


@register.filter
def moneda_ar(valor):
    if valor is None:
        return "—"

    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return valor

    return f"$ {valor:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")