
#Módulo para manejo de persistencia de datos en archivos CSV
#Proporciona funciones para guardar y cargar inventario

import csv
import os


def guardar_csv(inventario, ruta, incluir_header=True):
    # Validar que el inventario no esté vacío
    if not inventario:
        print("\n  El inventario está vacío. No hay nada que guardar.\n")
        return False
    
    try:
        # Crear el directorio si no existe
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Escribir el archivo CSV
        with open(ruta, 'w', newline='', encoding='utf-8') as archivo:
            campos = ['nombre', 'precio', 'cantidad']
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            
            # Escribir encabezado si se solicita
            if incluir_header:
                escritor.writeheader()
            
            # Escribir cada producto
            for producto in inventario:
                escritor.writerow({
                    "nombre": producto["nombre"],
                    "precio": producto["precio"],
                    "cantidad": producto["cantidad"]
                })
        
        print(f"\n Inventario guardado en: {ruta}\n")
        return True
    
    except PermissionError:
        print(f"\n Error: No tiene permisos para escribir en '{ruta}'.\n")
        return False
    
    except Exception as e:
        print(f"\n Error al guardar el archivo: {e}\n")
        return False


def cargar_csv(ruta):

    # Validar que el archivo existe
    if not os.path.exists(ruta):
        print(f"\n El archivo '{ruta}' no existe.\n")
        return [], 0
    
    productos = []
    filas_invalidas = 0
    
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            
            # Leer y validar encabezado
            try:
                encabezado = next(lector)
                
                # Validar que tenga el formato correcto
                if len(encabezado) != 3 or encabezado != ['nombre', 'precio', 'cantidad']:
                    print(f"\n  Advertencia: El encabezado no coincide con el formato esperado.")
                    print(f"   Esperado: nombre,precio,cantidad")
                    print(f"   Encontrado: {','.join(encabezado)}\n")
            
            except StopIteration:
                print("\n  El archivo está vacío.\n")
                return [], 0
            
            # Procesar cada fila
            for i, fila in enumerate(lector, start=2):
                if len(fila) != 3:
                    print(f"  Línea {i}: fila inválida, columnas insuficientes.")
                    filas_invalidas += 1
                    continue


                
                try:
                    nombre = fila[0].strip()
                    
                    # Validar nombre no vacío
                    if not nombre:
                        filas_invalidas += 1
                        continue
                    
                    # Convertir y validar precio
                    precio = float(fila[1])
                    if precio < 0:
                        filas_invalidas += 1
                        continue
                    
                    # Convertir y validar cantidad
                    cantidad = int(fila[2])
                    if cantidad < 0:
                        filas_invalidas += 1
                        continue
                    
                    # Agregar producto válido
                    productos.append({
                        "nombre": nombre,
                        "precio": precio,
                        "cantidad": cantidad
                    })
                
                except ValueError:
                    # Error al convertir precio o cantidad
                    filas_invalidas += 1
                    continue
                
                except Exception:
                    # Cualquier otro error
                    filas_invalidas += 1
                    continue
        
        return productos, filas_invalidas
    
    except FileNotFoundError:
        print(f"\n El archivo '{ruta}' no se encontró.\n")
        return [], 0
    
    except UnicodeDecodeError:
        print(f"\n Error: El archivo '{ruta}' tiene un formato de codificación no válido.\n")
        print("   Asegúrese de que el archivo esté en formato UTF-8.\n")
        return [], 0
    
    except PermissionError:
        print(f"\n Error: No tiene permisos para leer el archivo '{ruta}'.\n")
        return [], 0
    
    except Exception as e:
        print(f"\n Error inesperado al cargar el archivo: {e}\n")
        return [], 0