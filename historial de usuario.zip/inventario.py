
import servicios
import archivos


def validar_numero_positivo(mensaje, tipo=float):
  
   # Valida que el input sea un número positivo
    
    #Parámetros:mensaje (str): Mensaje a mostrar al usuariotipo (type): Tipo de dato esperado (int o float)Retorna: int o float: Número validado
    while True:
        try:
            valor = tipo(input(mensaje))
            if valor > 0:
                return valor
            else:
                print(" Error: El valor debe ser mayor que cero")
        except ValueError:
            print(f" Error: Debe ingresar un número válido")


def opcion_agregar(inventario):
    #Opción 1: Agregar un nuevo producto al inventario
    print("\n" + "="*50)
    print("AGREGAR PRODUCTO")
    print("="*50)
    
    # Validar nombre
    while True:
        nombre = input("Nombre del producto: ").strip()
        if nombre == "":
            print("Error: El nombre no puede estar vacío")
        elif nombre.isdigit():
            print("Error: El nombre no puede ser solo números")
        else:
            break
    
    # Validar precio
    precio = validar_numero_positivo("Precio: $", float)
    
    # Validar cantidad
    cantidad = validar_numero_positivo("Cantidad: ", int)
    
    # Agregar producto
    if servicios.agregar_producto(inventario, nombre, precio, cantidad):
        print(f"\nProducto '{nombre}' agregado exitosamente.\n")
    else:
        print(f"\n El producto '{nombre}' ya existe en el inventario.\n")

def opcion_mostrar(inventario):
    #Opción 2: Mostrar todos los productos del inventario
    print("\n" + "="*50)
    print("INVENTARIO COMPLETO")
    print("="*50)
    servicios.mostrar_inventario(inventario)


def opcion_buscar(inventario):
    #Opción 3: Buscar un producto por nombre
    print("\n" + "="*50)
    print("BUSCAR PRODUCTO")
    print("="*50)
    
    nombre = input("Nombre del producto a buscar: ").strip()
    producto = servicios.buscar_producto(inventario, nombre)
    
    if producto:
        print(f"\nProducto encontrado:")
        print(f"   Nombre: {producto['nombre']}")
        print(f"   Precio: ${producto['precio']:.2f}")
        print(f"   Cantidad: {producto['cantidad']}")
        print(f"   Subtotal: ${producto['precio'] * producto['cantidad']:.2f}\n")
    else:
        print(f"\n No se encontró el producto '{nombre}'.\n")


def opcion_actualizar(inventario):
    #Opción 4: Actualizar precio o cantidad de un producto
    print("\n" + "="*50)
    print("ACTUALIZAR PRODUCTO")
    print("="*50)
    
    nombre = input("Nombre del producto a actualizar: ").strip()
    producto = servicios.buscar_producto(inventario, nombre)
    
    if not producto:
        print(f"\n No se encontró el producto '{nombre}'.\n")
        return
    
    print(f"\nProducto actual: {producto['nombre']}")
    print(f"Precio actual: ${producto['precio']:.2f}")
    print(f"Cantidad actual: {producto['cantidad']}")
    
    print("\n¿Qué deseas actualizar?")
    print("1. Solo precio")
    print("2. Solo cantidad")
    print("3. Ambos")
    
    opcion = input("Opción: ").strip()
    
    nuevo_precio = None
    nueva_cantidad = None
    
    if opcion in ['1', '3']:
        nuevo_precio = validar_numero_positivo("Nuevo precio: $", float)
    
    if opcion in ['2', '3']:
        nueva_cantidad = validar_numero_positivo("Nueva cantidad: ", int)
    
    if servicios.actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad):
        print(f"\n Producto '{nombre}' actualizado exitosamente.\n")
    else:
        print("\n Error al actualizar el producto.\n")


def opcion_eliminar(inventario):
    #Opción 5: Eliminar un producto del inventario
    print("\n" + "="*50)
    print("ELIMINAR PRODUCTO")
    print("="*50)
    
    nombre = input("Nombre del producto a eliminar: ").strip()
    
    confirmacion = input(f"¿Está seguro de eliminar '{nombre}'? (SI/NO): ").strip().upper()
    
    if confirmacion == 'SI':
        if servicios.eliminar_producto(inventario, nombre):
            print(f"\n Producto '{nombre}' eliminado exitosamente.\n")
        else:
            print(f"\n No se encontró el producto '{nombre}'.\n")
    else:
        print("\n  Operación cancelada.\n")


def opcion_estadisticas(inventario):
    #Opción 6: Mostrar estadísticas del inventario
    print("\n" + "="*50)
    print("ESTADÍSTICAS DEL INVENTARIO")
    print("="*50)
    
    stats = servicios.calcular_estadisticas(inventario)
    
    if not stats:
        print("\n  No hay productos para calcular estadísticas.\n")
        return
    
    print(f"\n Unidades totales: {stats['unidades_totales']}")
    print(f" Valor total del inventario: ${stats['valor_total']:.2f}")
    print(f" Producto más caro: {stats['producto_mas_caro'][0]} (${stats['producto_mas_caro'][1]:.2f})")
    print(f" Mayor stock: {stats['producto_mayor_stock'][0]} ({stats['producto_mayor_stock'][1]} unidades)\n")


def opcion_guardar(inventario):
    #Opción 7: Guardar inventario en archivo CSV
    print("\n" + "="*50)
    print("GUARDAR INVENTARIO")
    print("="*50)
    
    ruta = input("Ruta del archivo (ej: inventario.csv): ").strip()
    
    if not ruta:
        ruta = "inventario.csv"
    
    archivos.guardar_csv(inventario, ruta)


def opcion_cargar(inventario):
    #Opción 8: Cargar inventario desde archivo CSV
    print("\n" + "="*50)
    print("CARGAR INVENTARIO")
    print("="*50)
    
    ruta = input("Ruta del archivo CSV: ").strip()
    
    productos_cargados, filas_invalidas = archivos.cargar_csv(ruta)
    
    if not productos_cargados and filas_invalidas == 0:
        return
    
    if productos_cargados:
        print(f"\n Se encontraron {len(productos_cargados)} productos en el archivo.")
        
        if filas_invalidas > 0:
            print(f"  {filas_invalidas} filas inválidas fueron omitidas.")
        
        # Preguntar si sobrescribir o fusionar
        if inventario:
            opcion = input("\n¿Sobrescribir inventario actual? (SI/NO): ").strip().upper()
            
            if opcion == 'SI':
                inventario.clear()
                inventario.extend(productos_cargados)
                print(f"\n Inventario reemplazado. Total: {len(inventario)} productos.\n")
            else:
                # Fusionar inventarios
                agregados = 0
                actualizados = 0
                
                for nuevo in productos_cargados:
                    existente = servicios.buscar_producto(inventario, nuevo["nombre"])
                    
                    if existente:
                        # Actualizar: sumar cantidad y actualizar precio
                        existente["cantidad"] += nuevo["cantidad"]
                        existente["precio"] = nuevo["precio"]
                        actualizados += 1
                    else:
                        inventario.append(nuevo)
                        agregados += 1
                
                print(f"\n Fusión completada:")
                print(f"   - {agregados} productos nuevos agregados")
                print(f"   - {actualizados} productos existentes actualizados")
                print(f"   - Total en inventario: {len(inventario)} productos\n")
        else:
            inventario.extend(productos_cargados)
            print(f"\n {len(productos_cargados)} productos cargados exitosamente.\n")


def mostrar_menu():
    #Muestra el menú principal
    print("\n" + "="*50)
    print("SISTEMA DE GESTIÓN DE INVENTARIO")
    print("="*50)
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Estadísticas")
    print("7. Guardar CSV")
    print("8. Cargar CSV")
    print("9. Salir")
    print("="*50)


def main():
    #Función principal del programa
    inventario = []
    
    print("\n Bienvenido al Sistema de Gestión de Inventario")
    
    while True:
        try:
            mostrar_menu()
            opcion = input("Seleccione una opción: ").strip()
            
            match opcion:
                case '1':
                    opcion_agregar(inventario)
                
                case '2':
                    opcion_mostrar(inventario)
                
                case '3':
                    opcion_buscar(inventario)
                
                case '4':
                    opcion_actualizar(inventario)
                
                case '5':
                    opcion_eliminar(inventario)
                
                case '6':
                    opcion_estadisticas(inventario)
                
                case '7':
                    opcion_guardar(inventario)
                
                case '8':
                    opcion_cargar(inventario)
                
                case '9':
                    print("\n ¡Gracias por usar el sistema! Hasta pronto.\n")
                    break
                
                case _:
                    print("\n  Opción inválida. Por favor seleccione una opción del 1 al 9.\n")
        
        except KeyboardInterrupt:
            print("\n\n Programa interrumpido por el usuario. ¡Hasta pronto!\n")
            break
        
        except Exception as e:
            print(f"\n Error inesperado: {e}")
            print("El programa continuará ejecutándose.\n")

if __name__ == "__main__":
    main()