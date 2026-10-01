from utils import actualizar_producto, crear_producto, eliminar_producto, generar_informe, leer_producto, leer_productos, db_connection

def menu():
  print("Sistema de Control de Inventario")
  
  while True:
    print("Opciones")
    print("1. Agregar producto")
    print("2. Mostrar inventario")
    print("3. Mostrar inventario de un producto por ID")
    print("4. Actualizar un producto")
    print("5. Eliminar un producto")
    print("6. Exportar informe inventario actual")
    print("7. Salir")
    
    opcion = input("Elija una opción: ")
    
    if opcion == "1":
      crear_producto()
    elif opcion == "2":
      leer_productos()
    elif opcion == "3":
      id = input("Ingrese el ID del producto a consultar: ")
      leer_producto(id)
    elif opcion == "4":
      id = input("Ingrese el ID del producto a actualizar: ")
      nuevo_nombre = input("Ingrese el nuevo nombre del producto. Si es el mismo presione Enter: ")
      nueva_cantidad = input("Ingrese la nueva cantidad del producto. Si es la misma presione Enter: ")
      nuevo_precio = input("Ingrese el nuevo precio del producto. Si es el mismo presione Enter: ")
      actualizar_producto(id, nuevo_nombre, nueva_cantidad, nuevo_precio)
    elif opcion == "5":
      id = input("Ingrese el ID del producto a eliminar: ")
      eliminar_producto(id)
    elif opcion == "6":
      generar_informe()
    elif opcion == "7":
      print("Saliendo del sistema...")
      break
    else:
      print("Opción no válida. Intentélo nuevamente con una opción del 1 al 7")
      
if __name__ == "__main__":
  
  _, cur = db_connection()
  try:
    cur.execute(
      """
      CREATE TABLE productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_creacion DATE NOT NULL DEFAULT(DATE('now')),
        nombre VARCHAR(100) NOT NULL,
        cantidad INTEGER NOT NULL,
        precio_unitario DECIMAL NOT NULL,
        valor_total DECIMAL
      );
      """
    )
    print("Tabla creado con éxito")
  except Exception as e:
    print(f"Error al crear la tabla {e}")
    
  menu()