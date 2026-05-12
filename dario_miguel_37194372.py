lista_de_productos = []

menu_principal = "Sistema de Gestión Básica de Productos\n1. Agregar Producto\n2. Mostrar Productos\n3. Buscar Producto\n4. Eliminar Producto\n5. Salir"
titulo_agregar_producto = "Agregar un nuevo producto"
titulo_mostrar_productos = "Lista de productos"
titulo_buscar_producto = "Buscar un producto por su nombre"
titulo_eliminar_producto = "Eliminar un producto por su nombre"
mensaje_producto_agregado = "Producto agregado exitosamente."
mensaje_producto_no_encontrado = "Producto no encontrado."
mensaje_producto_eliminado = "Producto eliminado exitosamente!"

print("\n\n\n\n" + menu_principal)
opcion_seleccionada = input("\nSeleccione una opción luego presione Enter:")
opcion_es_valida = opcion_seleccionada.isdigit()
while not opcion_es_valida:
    print("Error: La opción debe ser un número entero.")
    opcion_seleccionada = input("\nSeleccione una opción luego presione Enter:")
    opcion_es_valida = opcion_seleccionada.isdigit()

opcion_seleccionada = int(opcion_seleccionada)
while opcion_seleccionada != 5:

    match opcion_seleccionada:
        case 1:
            print("\n\n\n\n" + titulo_agregar_producto)
            nombre = input("Ingrese el nombre del producto: ")
            precio = int(input("Ingrese el precio del producto: "))
            precioValido = type(precio) == int
            if not precioValido:
                while not precioValido:
                    print("Error: El precio debe ser un número entero.")
                    precio = int(input("Ingrese el precio del producto: "))
                    precioValido = type(precio) == int   

            producto = {"nombre": nombre, "precio": precio}
            lista_de_productos.append(producto)
            print(mensaje_producto_agregado)

        case 2:
            print("\n" + titulo_mostrar_productos)
            if not lista_de_productos:       
                print("No hay productos para mostrar.")
            else:
                for producto in lista_de_productos:
                    print(f"Nombre: {producto['nombre']}, Precio: {producto['precio']}")
                    print("\n\n\n\n" + menu_principal)
                    opcion_seleccionada = int(input("\nSeleccione una opción luego presione Enter:"))
        case 3:
            print("\n" + titulo_buscar_producto)
            nombre = input("Ingrese el nombre del producto a buscar: ")
            encontrado = False
            for producto in lista_de_productos:
                if producto['nombre'] == nombre:
                    print(f"Producto encontrado: Nombre: {producto['nombre']}, Precio: {producto['precio']}")
                    encontrado = True
                    break
            if not encontrado:
                print(mensaje_producto_no_encontrado)
        case 4:
            print("\n" + titulo_eliminar_producto)
            nombre = input("Ingrese el nombre del producto a eliminar: ")
            eliminado = False
            for i, producto in enumerate(lista_de_productos):
                if producto['nombre'] == nombre:
                    lista_de_productos.pop(i)
                    print(mensaje_producto_eliminado)
                    eliminado = True
                    break
            if not eliminado:
                print(mensaje_producto_no_encontrado)   
        case 5:
            print("Saliendo del sistema. ¡Hasta luego!")
        case _:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 5.")