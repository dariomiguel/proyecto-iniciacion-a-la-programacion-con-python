import sqlite3
from colorama import init, Fore, Style

init(autoreset=True)

# VARIABLES
###########

NOMBRE_BASE_DE_DATOS = "inventario.db"

MENU_PRINCIPAL =  (
    Fore.MAGENTA + Style.BRIGHT +
    "Sistema de Gestión de Inventario\n" + Style.RESET_ALL +
    Fore.WHITE +
    "1. Agregar Producto\n"
    "2. Mostrar Productos\n"
    "3. Buscar Producto por ID\n"
    "4. Buscar Producto por nombre o categoría\n"
    "5. Actualizar Producto\n"
    "6. Eliminar Producto\n"
    "7. Reporte de stock bajo\n"
    "0. Salir" + Style.RESET_ALL
)

BORRAR_PANTALLA = "\n" * 16
SEPARADOR = Fore.CYAN + "-" * 84 + Style.RESET_ALL

ya_selecciono_alguna_opcion = False


# BASE DE DATOS
###############


def inicializar_db():
    """Crea la base de datos y la tabla productos si no existen."""
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT    NOT NULL,
                descripcion TEXT,
                cantidad    INTEGER NOT NULL
                            CHECK (cantidad >= 0),
                precio      REAL    NOT NULL
                            CHECK (precio >= 0),
                categoria   TEXT
            )
        """)
        conexion.commit()
        print(Fore.GREEN + "Base de datos lista.")
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudo inicializar la base de datos: {e}")
    finally:
        conexion.close()

def agregar_producto(nombre, descripcion, cantidad, precio, categoria):
    """Inserta un nuevo producto en la base de datos."""
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?, ?, ?, ?, ?)",
            (nombre, descripcion, cantidad, precio, categoria)
        )
        conexion.commit()
        print(Fore.GREEN + f"Producto agregado exitosamente!!! (ID asignado: {cursor.lastrowid})")
    except sqlite3.Error as e:
        conexion.rollback()
        print(Fore.RED + f"[ERROR] No se pudo agregar el producto: {e}")
    finally:
        conexion.close()

def mostrar_productos():
    """Muestra todos los productos registrados en formato tabla."""
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        if len(productos) == 0:
            print(Fore.YELLOW + "No hay productos para mostrar.")
        else:
            print(SEPARADOR)
            print(Fore.CYAN + Style.BRIGHT + f"|{'ID':^6}|{'Precio':^10}| {'Nombre':<21}| {'Descripción':<19}| {'Cant':^8}| {'Categoría':<18}|")
            print(SEPARADOR)
            for producto in productos:
                print(Fore.WHITE + f"|{producto[0]:^6}|${producto[4]:<9.2f}| {producto[1]:<21}| {producto[2] or '—':<19}| {producto[3]:^8}| {producto[5] or '—':<18}|")
            print(SEPARADOR)
            print(Fore.CYAN + f"Total: {len(productos)} producto(s).")
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] No se pudo obtener la lista de productos: {e}")
    finally:
        conexion.close()

def buscar_producto_por_id(id_producto):
    """Busca y muestra un producto por su ID."""
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id = ?", (id_producto,))
        producto = cursor.fetchone()

        print(SEPARADOR)
        print(Fore.CYAN + Style.BRIGHT + f"|{'ID':^6}|{'Precio':^10}| {'Nombre':<21}| {'Descripción':<19}| {'Cant':^8}| {'Categoría':<18}|")
        print(SEPARADOR)
        if producto:
            print(Fore.WHITE + f"|{producto[0]:^6}|${producto[4]:<9.2f}| {producto[1]:<21}| {producto[2] or '—':<19}| {producto[3]:^8}| {producto[5] or '—':<18}|")
        else:
            print(Fore.RED + "Producto no encontrado.")
        print(SEPARADOR)
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] Error al buscar el producto: {e}")
    finally:
        conexion.close()

def buscar_producto_por_texto(termino):
    """Busca productos cuyo nombre o categoría contengan el término ingresado."""
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM productos WHERE nombre LIKE ? OR categoria LIKE ?",
            (f"%{termino}%", f"%{termino}%")
        )
        productos = cursor.fetchall()

        print(SEPARADOR)
        print(Fore.CYAN + Style.BRIGHT + f"|{'ID':^6}|{'Precio':^10}| {'Nombre':<21}| {'Descripción':<19}| {'Cant':^8}| {'Categoría':<18}|")
        print(SEPARADOR)
        if len(productos) == 0:
            print(Fore.RED + f"No se encontraron productos para '{termino}'.")
        else:
            for producto in productos:
                print(Fore.WHITE + f"|{producto[0]:^6}|${producto[4]:<9.2f}| {producto[1]:<21}| {producto[2] or '—':<19}| {producto[3]:^8}| {producto[5] or '—':<18}|")
            print(SEPARADOR)
            print(Fore.CYAN + f"Se encontraron {len(productos)} resultado(s).")
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] Error en la búsqueda: {e}")
    finally:
        conexion.close()

def actualizar_producto(id_producto, nombre, descripcion, cantidad, precio, categoria):
    """Actualiza los datos de un producto identificado por su ID."""
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    try:
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE productos SET nombre=?, descripcion=?, cantidad=?, precio=?, categoria=? WHERE id=?",
            (nombre, descripcion, cantidad, precio, categoria, id_producto)
        )
        conexion.commit()
        if cursor.rowcount == 0:
            print(Fore.RED + "No se encontró ningún producto con ese ID.")
        else:
            print(Fore.GREEN + "Producto actualizado exitosamente!!!")
    except sqlite3.Error as e:
        conexion.rollback()
        print(Fore.RED + f"[ERROR] No se pudo actualizar el producto: {e}")
    finally:
        conexion.close()

def eliminar_producto(id_producto):
    """Elimina un producto de la base de datos por su ID."""
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conexion.commit()
        if cursor.rowcount == 0:
            print(Fore.RED + "No se encontró ningún producto con ese ID.")
        else:
            print(Fore.GREEN + "Producto eliminado exitosamente.")
    except sqlite3.Error as e:
        conexion.rollback()
        print(Fore.RED + f"[ERROR] No se pudo eliminar el producto: {e}")
    finally:
        conexion.close()

def reporte_stock_bajo(limite):
    """Muestra los productos cuya cantidad es menor o igual al límite dado."""
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE cantidad <= ? ORDER BY cantidad", (limite,))
        productos = cursor.fetchall()

        if len(productos) == 0:
            print(Fore.GREEN + f"No hay productos con stock menor o igual a {limite}.")
        else:
            print(Fore.RED + Style.BRIGHT + f"\n{len(productos)} producto(s) con stock menor o igual a {limite}:\n")
            print(SEPARADOR)
            print(Fore.CYAN + Style.BRIGHT + f"|{'ID':^6}|{'Precio':^10}| {'Nombre':<21}| {'Descripción':<19}| {'Cant':^8}| {'Categoría':<18}|")
            print(SEPARADOR)
            for producto in productos:
                print(Fore.WHITE + f"|{producto[0]:^6}|${producto[4]:<9.2f}| {producto[1]:<21}| {producto[2] or '—':<19}| {producto[3]:^8}| {producto[5] or '—':<18}|")
            print(SEPARADOR)
    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] Error al generar el reporte: {e}")
    finally:
        conexion.close()


# FUNCIONES DE MENÚ
####################


def agregar_producto_menu():
    """Interfaz para agregar un nuevo producto (case 1)."""
    print(BORRAR_PANTALLA + Fore.CYAN + Style.BRIGHT + "Agregar un nuevo producto" + Style.RESET_ALL)
    print(SEPARADOR)

    nombre = input(Fore.YELLOW + "Ingrese el nombre del producto: " + Style.RESET_ALL).strip()
    nombre_valido = nombre != "" and nombre.isdigit() == False
    while not nombre_valido:
        print(Fore.RED + "Error!: El nombre no puede estar vacío ni ser solo números.")
        nombre = input(Fore.YELLOW + "Ingrese el nombre del producto: " + Style.RESET_ALL).strip()
        nombre_valido = nombre != "" and nombre.isdigit() == False

    descripcion = input(Fore.YELLOW + "Ingrese una descripción (opcional): " + Style.RESET_ALL).strip()

    categoria = input(Fore.YELLOW + "Ingrese la categoría del producto: " + Style.RESET_ALL).strip()
    categoria_valida = categoria != "" and categoria.isdigit() == False
    while not categoria_valida:
        print(Fore.RED + "Error!: La categoría no puede estar vacía ni ser solo números.")
        categoria = input(Fore.YELLOW + "Ingrese la categoría del producto: " + Style.RESET_ALL).strip()
        categoria_valida = categoria != "" and categoria.isdigit() == False

    cantidad = input(Fore.YELLOW + "Ingrese la cantidad disponible: " + Style.RESET_ALL).strip()
    cantidad_valida = cantidad.isdigit()
    while not cantidad_valida:
        print(Fore.RED + "Error!: La cantidad debe ser un número entero.")
        cantidad = input(Fore.YELLOW + "Ingrese la cantidad disponible: " + Style.RESET_ALL).strip()
        cantidad_valida = cantidad.isdigit()

    precio = input(Fore.YELLOW + "Ingrese el precio del producto: " + Style.RESET_ALL).strip()
    precio_valido = False
    try:
        float(precio)
        precio_valido = True
    except ValueError:
        precio_valido = False
    while not precio_valido:
        print(Fore.RED + "Error!: El precio debe ser un número válido (ej: 1250.50).")
        precio = input(Fore.YELLOW + "Ingrese el precio del producto: " + Style.RESET_ALL).strip()
        try:
            float(precio)
            precio_valido = True
        except ValueError:
            precio_valido = False

    agregar_producto(nombre.title(), descripcion, int(cantidad), float(precio), categoria.title())

def mostrar_productos_menu():
    """Interfaz para listar todos los productos (case 2)."""
    print(BORRAR_PANTALLA + Fore.CYAN + Style.BRIGHT + "Lista de productos:" + Style.RESET_ALL)
    mostrar_productos()

def buscar_por_id_menu():
    """Interfaz para buscar un producto por ID (case 3)."""
    print(BORRAR_PANTALLA + Fore.CYAN + Style.BRIGHT + "Buscar un producto por su ID" + Style.RESET_ALL)

    id_buscar = input(Fore.YELLOW + "Ingrese el ID del producto a buscar: " + Style.RESET_ALL).strip()
    id_valido = id_buscar.isdigit()
    while not id_valido:
        print(Fore.RED + "Error!: El ID debe ser un número entero.")
        id_buscar = input(Fore.YELLOW + "Ingrese el ID del producto a buscar: " + Style.RESET_ALL).strip()
        id_valido = id_buscar.isdigit()

    buscar_producto_por_id(int(id_buscar))

def buscar_por_texto_menu():
    """Interfaz para buscar por nombre o categoría (case 4)."""
    print(BORRAR_PANTALLA + Fore.CYAN + Style.BRIGHT + "Buscar producto por nombre o categoría" + Style.RESET_ALL)

    termino = input(Fore.YELLOW + "Ingrese el término de búsqueda: " + Style.RESET_ALL).strip()
    while termino == "":
        print(Fore.RED + "Error!: El término de búsqueda no puede estar vacío.")
        termino = input(Fore.YELLOW + "Ingrese el término de búsqueda: " + Style.RESET_ALL).strip()

    buscar_producto_por_texto(termino)

def actualizar_producto_menu():
    """Interfaz para actualizar un producto existente (case 5)."""
    print(BORRAR_PANTALLA + Fore.CYAN + Style.BRIGHT + "Actualizar un producto" + Style.RESET_ALL)
    print(SEPARADOR)

    id_actualizar = input(Fore.YELLOW + "Ingrese el ID del producto a actualizar: " + Style.RESET_ALL).strip()
    id_valido = id_actualizar.isdigit()
    while not id_valido:
        print(Fore.RED + "Error!: El ID debe ser un número entero.")
        id_actualizar = input(Fore.YELLOW + "Ingrese el ID del producto a actualizar: " + Style.RESET_ALL).strip()
        id_valido = id_actualizar.isdigit()

    # Buscar y mostrar el producto actual antes de pedir los nuevos datos
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id_actualizar),))
    producto_actual = cursor.fetchone()
    conexion.close()

    if not producto_actual:
        print(Fore.RED + "No se encontró ningún producto con ese ID.")
        return

    print(Fore.CYAN + "\nDatos actuales:")
    print(SEPARADOR)
    print(Fore.CYAN + Style.BRIGHT + f"|{'ID':^6}|{'Precio':^10}| {'Nombre':<21}| {'Descripción':<19}| {'Cant':^8}| {'Categoría':<18}|")
    print(SEPARADOR)
    print(Fore.WHITE + f"|{producto_actual[0]:^6}|${producto_actual[4]:<9.2f}| {producto_actual[1]:<21}| {producto_actual[2] or '—':<19}| {producto_actual[3]:^8}| {producto_actual[5] or '—':<18}|")
    print(SEPARADOR)
    print(Fore.WHITE + "\nIngresá los nuevos datos (Enter para mantener el valor actual):\n")

    nombre_nuevo = input(Fore.YELLOW + f"  Nombre [{producto_actual[1]}]: " + Style.RESET_ALL).strip()
    if nombre_nuevo == "":
        nombre_nuevo = producto_actual[1]

    desc_nueva = input(Fore.YELLOW + f"  Descripción [{producto_actual[2] or '—'}]: " + Style.RESET_ALL).strip()
    if desc_nueva == "":
        desc_nueva = producto_actual[2]

    cant_nueva = input(Fore.YELLOW + f"  Cantidad [{producto_actual[3]}]: " + Style.RESET_ALL).strip()
    if cant_nueva == "":
        cant_nueva = producto_actual[3]
    else:
        try:
            cant_nueva = int(cant_nueva)
        except ValueError:
            print(Fore.YELLOW + "Valor inválido. Se mantuvo la cantidad anterior.")
            cant_nueva = producto_actual[3]

    precio_nuevo = input(Fore.YELLOW + f"  Precio [{producto_actual[4]:.2f}]: " + Style.RESET_ALL).strip()
    if precio_nuevo == "":
        precio_nuevo = producto_actual[4]
    else:
        try:
            precio_nuevo = float(precio_nuevo)
        except ValueError:
            print(Fore.YELLOW + "Valor inválido. Se mantuvo el precio anterior.")
            precio_nuevo = producto_actual[4]

    cat_nueva = input(Fore.YELLOW + f"  Categoría [{producto_actual[5] or '—'}]: " + Style.RESET_ALL).strip()
    if cat_nueva == "":
        cat_nueva = producto_actual[5]

    actualizar_producto(int(id_actualizar), nombre_nuevo, desc_nueva, cant_nueva, precio_nuevo, cat_nueva)

def eliminar_producto_menu():
    """Interfaz para eliminar un producto (case 6)."""
    print(BORRAR_PANTALLA + Fore.CYAN + Style.BRIGHT + "Eliminar un producto" + Style.RESET_ALL)
    print(SEPARADOR)

    id_eliminar = input(Fore.YELLOW + "Ingrese el ID del producto a eliminar: " + Style.RESET_ALL).strip()
    id_valido = id_eliminar.isdigit()
    while not id_valido:
        print(Fore.RED + "Error!: El ID debe ser un número entero.")
        id_eliminar = input(Fore.YELLOW + "Ingrese el ID del producto a eliminar: " + Style.RESET_ALL).strip()
        id_valido = id_eliminar.isdigit()

    # Buscar y mostrar el producto antes de confirmar la eliminación
    conexion = sqlite3.connect(NOMBRE_BASE_DE_DATOS)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (int(id_eliminar),))
    producto_encontrado = cursor.fetchone()
    conexion.close()

    if not producto_encontrado:
        print(Fore.RED + "No se encontró ningún producto con ese ID.")
        return

    print(Fore.CYAN + "\nProducto encontrado:")
    print(SEPARADOR)
    print(Fore.CYAN + Style.BRIGHT + f"|{'ID':^6}|{'Precio':^10}| {'Nombre':<21}| {'Descripción':<19}| {'Cant':^8}| {'Categoría':<18}|")
    print(SEPARADOR)
    print(Fore.WHITE + f"|{producto_encontrado[0]:^6}|${producto_encontrado[4]:<9.2f}| {producto_encontrado[1]:<21}| {producto_encontrado[2] or '—':<19}| {producto_encontrado[3]:^8}| {producto_encontrado[5] or '—':<18}|")
    print(SEPARADOR)

    confirmacion = input(Fore.RED + Style.BRIGHT + f"¿Confirmar eliminación? (s/N): " + Style.RESET_ALL).strip().lower()
    if confirmacion == "s":
        eliminar_producto(int(id_eliminar))
    else:
        print(Fore.YELLOW + "Operación cancelada.")

def reporte_stock_bajo_menu():
    """Interfaz para generar el reporte de stock bajo (case 7)."""
    print(BORRAR_PANTALLA + Fore.CYAN + Style.BRIGHT + "Reporte de stock bajo" + Style.RESET_ALL)
    print(SEPARADOR)

    limite = input(Fore.YELLOW + "Ingrese el límite de cantidad (inclusive): " + Style.RESET_ALL).strip()
    limite_valido = limite.isdigit()
    while not limite_valido:
        print(Fore.RED + "Error!: El límite debe ser un número entero.")
        limite = input(Fore.YELLOW + "Ingrese el límite de cantidad (inclusive): " + Style.RESET_ALL).strip()
        limite_valido = limite.isdigit()

    reporte_stock_bajo(int(limite))


#  MENÚ PRINCIPAL
#####################

inicializar_db()

print(BORRAR_PANTALLA + MENU_PRINCIPAL)
opcion_seleccionada = input(Fore.YELLOW + "\nSeleccione una opción luego presione Enter: " + Style.RESET_ALL)
opcion_es_valida = opcion_seleccionada.isdigit() and 0 <= int(opcion_seleccionada) <= 7

while not opcion_es_valida:
    print(Fore.RED + f"\nError!: La opción debe ser un número del 0 al 7.")
    print(BORRAR_PANTALLA + MENU_PRINCIPAL)
    opcion_seleccionada = input(Fore.YELLOW + "\nSeleccione una opción luego presione Enter: " + Style.RESET_ALL)
    opcion_es_valida = opcion_seleccionada.isdigit() and 0 <= int(opcion_seleccionada) <= 7

opcion_seleccionada = int(opcion_seleccionada)

while opcion_seleccionada != 0:

    if ya_selecciono_alguna_opcion:
        print(BORRAR_PANTALLA + MENU_PRINCIPAL)
        opcion_seleccionada = input(Fore.YELLOW + "\nSeleccione una opción luego presione Enter: " + Style.RESET_ALL)
        opcion_es_valida = opcion_seleccionada.isdigit() and 0 <= int(opcion_seleccionada) <= 7

        while not opcion_es_valida:
            print(Fore.RED + f"\nError!: La opción debe ser un número del 0 al 7.")
            print(BORRAR_PANTALLA + MENU_PRINCIPAL)
            opcion_seleccionada = input(Fore.YELLOW + "\nSeleccione una opción luego presione Enter: " + Style.RESET_ALL)
            opcion_es_valida = opcion_seleccionada.isdigit() and 0 <= int(opcion_seleccionada) <= 7

        opcion_seleccionada = int(opcion_seleccionada)

    match opcion_seleccionada:

        case 1:
            agregar_producto_menu()
            ya_selecciono_alguna_opcion = True
            print(SEPARADOR)
            input("Presione Enter para continuar...")

        case 2:
            mostrar_productos_menu()
            ya_selecciono_alguna_opcion = True
            print(f"\n{SEPARADOR}\n")
            input("Presione Enter para continuar...")

        case 3:
            buscar_por_id_menu()
            ya_selecciono_alguna_opcion = True
            print(f"\n{SEPARADOR}\n")
            input("Presione Enter para continuar...")

        case 4:
            buscar_por_texto_menu()
            ya_selecciono_alguna_opcion = True
            print(f"\n{SEPARADOR}\n")
            input("Presione Enter para continuar...")

        case 5:
            actualizar_producto_menu()
            ya_selecciono_alguna_opcion = True
            print(SEPARADOR)
            input("Presione Enter para continuar...")

        case 6:
            eliminar_producto_menu()
            ya_selecciono_alguna_opcion = True
            print(SEPARADOR)
            input("Presione Enter para continuar...")

        case 7:
            reporte_stock_bajo_menu()
            ya_selecciono_alguna_opcion = True
            print(f"\n{SEPARADOR}\n")
            input("Presione Enter para continuar...")

        case 0:
            print(Fore.CYAN + "\n¡Hasta luego!\n")
            break

        case _:
            print(Fore.RED + "Opción no válida. Por favor, seleccioná una opción del 0 al 7.")
            ya_selecciono_alguna_opcion = True
            print(f"\n{SEPARADOR}\n")
            input("Presione Enter para continuar...")


