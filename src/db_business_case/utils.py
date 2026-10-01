import sqlite3
from fpdf import FPDF
from PyPDF2 import PdfReader, PdfWriter
import io

def db_connection():
  while True:
    try:
      conn = sqlite3.connect(database="src\db_business_case\inventario_prod.db")
      cur = conn.cursor()
      print("Conexión a la DB lograda con éxito\n")
      break
    except Exception as e:
      print(f"Error al conectarse a la DB: {e}")
  return conn, cur

def crear_producto():
  """_summary_
  Solicita los datos del producto al usuario y los agrega a la base de datos del inventario
  Garantiza que la cantidad y el precio sean números válidos
  """
  
  conn, cur = db_connection()
  
  while True:
    try:
      producto = input("Ingrese el nombre del producto: ").strip().title()
      if not producto.isalpha():
        raise ValueError(f"El nombre del producto no puede contener núermos. Nombre de producto ingresado {producto}")
    except Exception as e:
      print(f"ERROR, {e}")
    else:
      break
    
  while True:
    try:
      cantidad = input("Ingrese la cantidad inicial en el inventario: ")
      if not cantidad.isdigit():
        raise ValueError(f"La cantidad de inventario inicial debe ser un número entero positivo. Cantidad ingresada: {cantidad}")
    except Exception as e:
      print(f"ERROR, {e}")
    else:
      cantidad = int(cantidad)
      break
    
  while True:
    try:
      precio_unitario = input("Ingrese el precio unitario del producto: ")
      if not (precio_unitario.replace(".", "").isdigit() or precio_unitario.replace(",", ".").isdigit()):
        raise ValueError(f"El precio unitario debe ser un número positivo (ej: 10.50s). Precio ingresado: {precio_unitario}")
    except Exception as e:
      print(f"ERROR, {e}")
    else:
      if precio_unitario.__contains__(","):
        precio_unitario = float(precio_unitario.replace(",", "."))
      else:
        precio_unitario = float(precio_unitario)
      break
    
  producto_dict = {
    "nombre": producto,
    "cantidad": cantidad,
    "precio_unitario": precio_unitario,
    "valor_total": precio_unitario * cantidad
  }
  
  try:
    cur.execute(
    """
      INSERT INTO 
        productos (nombre, cantidad, precio_unitario, valor_total)
      VALUES
        (?,?,?,?)
    """,
    (
      producto_dict["nombre"], 
      producto_dict["cantidad"], 
      producto_dict["precio_unitario"], 
      producto_dict["valor_total"])
    )
    conn.commit()
    print("\nEl producto fue agregado con éxito al inventario")
  except Exception as e:
    print(f"Error al crear el producto. {e}")

def leer_productos():
  _, cur = db_connection()
  
  try:
    
    datos = cur.execute(
    """
      SELECT * FROM productos
    """
    ).fetchall()
    
    if not datos:
      print("\n El inventario está vacío")
      return
    
    for dato in datos:
      print(f"ID                     : {dato[0]}")
      print(f"Fecha                  : {dato[1]}")
      print(f"Producto               : {dato[2]}")
      print(f"Cantidad               : {dato[3]}")
      print(f"Precio unitario        : {dato[4]:.2f}")
      print(f"Valor total            : {dato[5]:.2f}")
      print("-" * 40)
  except Exception as e:
    print(f"Error al leer los productos del inventario {e}")

def leer_producto(id: int):
  
  _, cur = db_connection()
  
  try:
    
    dato = cur.execute(
    """
      SELECT * FROM productos WHERE id = ?
    """,
    (id)
    ).fetchone()
    
    if not dato:
      print(f"\n El producto no con ID {id} no existe en el inventario")
      return
    
    print(f"ID                     : {dato[0]}")
    print(f"Fecha                  : {dato[1]}")
    print(f"Producto               : {dato[2]}")
    print(f"Cantidad               : {dato[3]}")
    print(f"Precio unitario        : {dato[4]:.2f}")
    print(f"Valor total            : {dato[5]:.2f}")
    print("-" * 40)
  except Exception as e:
      print(f"Error al leer el producto en el inventario {e}")

def actualizar_producto(id: int, nuevo_nombre: str = None, nueva_cantidad: int = None, nuevo_precio_unitario: float = None):
  conn, cur = db_connection()
  
  try:
    dato = cur.execute(
    """
      SELECT * FROM productos WHERE id = ?
    """,
    (id)
    ).fetchone()
    
    if not nueva_cantidad:
      cantidad = dato[3]
      
    if not nuevo_precio_unitario:
      precio_unitario = dato[4]
    
    if not dato:
      print(f"\n El producto con ID {id} no existe en el inventario")
      return
      
    if not nuevo_nombre and not nueva_cantidad and not nuevo_precio_unitario:
      print(f"No se ingresaron nuevos datos para el producto con el ID {id}")
      return
    elif nuevo_nombre and not nueva_cantidad and not nuevo_precio_unitario:
      cur.execute("""UPDATE productos SET nombre = ? WHERE id = ?""", (nuevo_nombre, id))
      conn.commit()
      print(f"\nEl producto con ID {id} fue actualizado con éxitos")  
    elif nuevo_nombre and nueva_cantidad and not nuevo_precio_unitario:
      cur.execute("""UPDATE productos SET nombre = ?, cantidad = ? WHERE id = ?""", (nuevo_nombre, nueva_cantidad, id))
      conn.commit()
      print(f"\nEl producto con ID {id} fue actualizado con éxitos")  
    elif nuevo_nombre and not nueva_cantidad and nuevo_precio_unitario:
      cur.execute("""UPDATE productos SET nombre = ?, precio_unitario = ?, valor_total = ? WHERE id = ?""", (nuevo_nombre, nuevo_precio_unitario, id, int(nueva_cantidad * precio_unitario)))
      conn.commit()
      print(f"\nEl producto con ID {id} fue actualizado con éxitos")  
    elif not nuevo_nombre and nueva_cantidad and nuevo_precio_unitario:
      cur.execute("""UPDATE productos SET cantidad = ?, precio_unitario = ? WHERE id = ?""", (nueva_cantidad, nuevo_precio_unitario, id))
      conn.commit()
      print(f"\nEl producto con ID {id} fue actualizado con éxitos")  
    elif not nuevo_nombre and nueva_cantidad and not nuevo_precio_unitario:
      cur.execute("""UPDATE productos SET cantidad = ? WHERE id = ?""", (nueva_cantidad, id))
      conn.commit()
      print(f"\nEl producto con ID {id} fue actualizado con éxitos")  
    elif not nuevo_nombre and not nueva_cantidad and nuevo_precio_unitario:
      cur.execute("""UPDATE productos SET precio_unitario = ? WHERE id = ?""", (nuevo_precio_unitario, id))
      conn.commit()
      print(f"\nEl producto con ID {id} fue actualizado con éxitos")
      
    
    dato = cur.execute(
    """
      SELECT * FROM productos WHERE id = ?
    """,
    (id)
    ).fetchone()
      
    print(f"ID                     : {dato[0]}")
    print(f"Fecha                  : {dato[1]}")
    print(f"Producto               : {dato[2]}")
    print(f"Cantidad               : {dato[3]}")
    print(f"Precio unitario        : {dato[4]:.2f}")
    print(f"Valor total            : {dato[5]:.2f}")
    print("-" * 40)
  except Exception as e:
      print(f"Error al actualizar el producto en el inventario {e}")

def eliminar_producto(id: int):
  
  conn, cur = db_connection()
  
  try:
    
    dato = cur.execute(
    """
      SELECT * FROM productos WHERE id = ?
    """,
    (id)
    ).fetchone()
    
    if not dato:
      print(f"\n El producto no con ID {id} no existe en el inventario")
      return
    
    cur.execute("""DELETE FROM productos WHERE id = ?""", (id))
    conn.commit()
    print(f"Producto {dato[2]} eliminado con éxito")
  except Exception as e:
    print(f"\nError al eliminar el producto con ID {id}")

def generar_informe():
  try:
    
    _, cur = db_connection()
    
    autor = input("Ingrese el nombre del quien genera el informe: ")
    revisor = input("Ingrese el nombre de quien revisa el informe: ")
    
    encabezado = ["ID", "Fecha Creación", "Producto", "Cantidad", "Precio Unitario", "Valor Total"]
    
    datos = cur.execute("SELECT * FROM productos").fetchall()
    
    productos = [list(producto) for producto in datos]
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=24, style="B")
    
    pdf.ln(40)
    pdf.cell(w=190, h=10, text="Sistema de Control de Inventario", align="C")
    pdf.ln(20)
    
    resumen = """
    Se muestra el inventario actual para todos los productos después de su gestión (añadir o eliminar). También se muestra el Total unificado del inventario en la tabla que se muestra a continuación:
    """
    
    pdf.set_font("helvetica", size=16)
    pdf.multi_cell(w=180, h=10, text=resumen.strip(), align="J")
    pdf.ln(10)
    
    ancho_cols = [20, 45, 25, 35, 40, 30]
    
    for i, nombre_col in enumerate(encabezado):
      pdf.set_font("helvetica", size=14, style="B")
      pdf.cell(w=ancho_cols[i], h=10, text=nombre_col, align="C", border=1)
      
    pdf.ln()
    
    for fila in productos:
      for i, item in enumerate(fila):
        if isinstance(item, float) or isinstance(item, int) and fila.index(item) != 0 and fila.index(item) != 3:
          pdf.set_font("helvetica", size=12)
          pdf.cell(w=ancho_cols[i], h=10, text=f"${item:.2f}", border=1, align="C")
        else:
          pdf.set_font("helvetica", size=12)
          pdf.cell(w=ancho_cols[i], h=10, text=str(item), border=1, align="C")
      pdf.ln()
      
    gran_total = sum(producto[-1] for producto in datos)
    pdf.set_font("helvetica", size=14, style="B")
    pdf.cell(w=sum(ancho_cols[:-1]), h=10, text="TOTAL", border=1)
    pdf.cell(w=ancho_cols[-1], h=10, text=f"${gran_total:.2f}", border=1, align="C")
    
    pdf.ln(60)
    
    pdf.cell(w=80, text=f"Autor: {autor.title()}", border="T", align="L")
    pdf.ln(30)
    pdf.cell(w=80, text=f"Revisor: {revisor.title()}", border="T", align="L")
  except Exception as e:
    print(f"Ocurrió un error generando el informe: {e}")
  else:
    
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    
    template_pdf = PdfReader("src\db_business_case\plantilla.pdf")
    overlay_pdf = PdfReader(buffer)
    writer = PdfWriter()
    
    template_page = template_pdf.pages[0]
    overlay_page = overlay_pdf.pages[0]
    template_page.merge_page(overlay_page)
    writer.add_page(template_page)
    
    with open("src\db_business_case\Informe Sistema de Gestión de inventario.pdf", "wb") as f:
      writer.write(f)
      
    print("\n Informe generado en formato PDF con éxito")