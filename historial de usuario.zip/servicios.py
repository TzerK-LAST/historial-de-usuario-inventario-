
def agregar_producto(inventario, nombre, precio, cantidad):
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return False

    inventario.append({
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    })
    return True


def mostrar_inventario(inventario):
    if not inventario:
        print("\n  El inventario está vacío.\n")
        return

    print("\n" + "="*70)
    print(f"{'NOMBRE':<25} {'PRECIO':>15} {'CANTIDAD':>15} {'SUBTOTAL':>13}")
    print("="*70)

    for p in inventario:
        subtotal = p["precio"] * p["cantidad"]
        print(f"{p['nombre']:<25} ${p['precio']:>14.2f} {p['cantidad']:>15} ${subtotal:>12.2f}")

    print("="*70 + "\n")


def buscar_producto(inventario, nombre):
    for producto in inventario:
        if producto["nombre"].lower() == nombre.lower():
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    producto = buscar_producto(inventario, nombre)
    if not producto:
        return False

    if nuevo_precio is not None:
        producto["precio"] = nuevo_precio

    if nueva_cantidad is not None:
        producto["cantidad"] = nueva_cantidad

    return True


def eliminar_producto(inventario, nombre):
    producto = buscar_producto(inventario, nombre)
    if not producto:
        return False

    inventario.remove(producto)
    return True


def calcular_estadisticas(inventario):
    if not inventario:
        return None

    subtotal = lambda p: p["precio"] * p["cantidad"]

    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)

    mas_caro = max(inventario, key=lambda p: p["precio"])
    mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": (mas_caro["nombre"], mas_caro["precio"]),
        "producto_mayor_stock": (mayor_stock["nombre"], mayor_stock["cantidad"])
    }
