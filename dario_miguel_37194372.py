lista_de_productos = []

posicion_numeracion = 0
posicion_precio = 1
posicion_nombre = 2
posicion_categoria = 3

ya_selecciono_alguna_opcion = False 

menu_principal = "Sistema de Gestión Básica de Productos\n1. Agregar Producto\n2. Mostrar Productos\n3. Buscar Producto\n4. Buscar Producto por fragmento de nombre\n5. Eliminar Producto\n6. Salir"
borrar_pantalla = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
separador = "" + "-" * 84


print(borrar_pantalla + menu_principal)
opcion_seleccionada = input("\nSeleccione una opción luego presione Enter:")
opcion_es_valida = opcion_seleccionada.isdigit()

while not opcion_es_valida:
    print(f"\n{borrar_pantalla}{menu_principal}\nError!: La opción debe ser un número entero del 1 al 6.")
    opcion_seleccionada = input("\nSeleccione una opción luego presione Enter:")
    opcion_es_valida = opcion_seleccionada.isdigit()

opcion_seleccionada = int(opcion_seleccionada)


while opcion_seleccionada != 6:


    if ya_selecciono_alguna_opcion:
        print(borrar_pantalla + menu_principal)
        opcion_seleccionada = input("\nSeleccione una opción luego presione Enter:")
        opcion_es_valida = opcion_seleccionada.strip().isdigit()
    
        while not opcion_es_valida:
            print(f"\n{borrar_pantalla}{menu_principal}\nError!: La opción debe ser un número entero del 1 al 6.")
            opcion_seleccionada = input("\nSeleccione una opción luego presione Enter:")
            opcion_es_valida = opcion_seleccionada.strip().isdigit()

        opcion_seleccionada = int(opcion_seleccionada)


    match opcion_seleccionada:


        case 1:
            producto = [0,0,"", ""] #Posición,Precio, Nombre, Categoria
            print(f"{borrar_pantalla}Agregar un nuevo producto")
            print(separador)


            nombre = input("Ingrese el nombre del producto: ")
            nombre_valido = nombre.strip() != "" and nombre.isdigit() == False
            while not nombre_valido:
                print(f"\n{borrar_pantalla}{menu_principal}\nError!: El nombre del producto no puede estar vacío o ser solo números.")
                nombre = input("Ingrese el nombre del producto: ")
                nombre_valido = nombre.strip() != "" and nombre.isdigit() == False


            categoria = input("Ingrese la categoría del producto: ")
            categoria_valida = categoria.strip() != "" and categoria.isdigit() == False
            while not categoria_valida:
                print(f"\n{borrar_pantalla}{menu_principal}\nError!: La categoría del producto no puede estar vacío o ser solo números.")
                categoria = input("Ingrese la categoría del producto: ")
                categoria_valida = categoria.strip() != "" and categoria.isdigit() == False

            precio = input("Ingrese el precio del producto: ")
            precio_valido = precio.isdigit()
            while not precio_valido:
                print(f"\n{borrar_pantalla}{menu_principal}\nError!: El precio debe ser un número entero.")
                precio = input("Ingrese el precio del producto: ")
                precio_valido = precio.isdigit()  

            producto[posicion_numeracion] = len(lista_de_productos) + 1 
            producto[posicion_precio] = int(precio)
            producto[posicion_nombre] = nombre.title()
            producto[posicion_categoria] = categoria.title()

            lista_de_productos.append(producto)
            ya_selecciono_alguna_opcion = True

            print(f"\n{separador}\nProducto agregado exitosamente!!!\n{separador}")
            input("Presione Enter para continuar...")


        case 2:
            print(borrar_pantalla + "Lista de productos:")

            if len(lista_de_productos) == 0:       
                print("No hay productos para mostrar.")
            else:
                print(separador)
                print(f"|  Item  |   Precio   |            Nombre           |           Categoría          | ")
                print(separador)
                for i in range(len(lista_de_productos)):
                    producto = lista_de_productos[i]
                    print(f"|{producto[posicion_numeracion]:^8}|${producto[posicion_precio]:<10} | {producto[posicion_nombre]:^27} | {producto[posicion_categoria]:^29}|")

            ya_selecciono_alguna_opcion = True
            print(f"\n{separador}\n")
            input("Presione Enter para continuar...")


        case 3:
            print(borrar_pantalla  + "Buscar un producto por su nombre")
            nombre_a_buscar = input("Ingrese el nombre del producto a buscar: ")
            encontrado = False
            print(f"|  Item  |   Precio   |            Nombre           |           Categoría          | ")
            print(separador)

            for producto in lista_de_productos:
                if producto[posicion_nombre].lower() == nombre_a_buscar.lower() :
                    print(f"|{producto[posicion_numeracion]:^8}|${producto[posicion_precio]:<10} | {producto[posicion_nombre]:^27} | {producto[posicion_categoria]:^29}|")
                    encontrado = True

            if not encontrado:
                print("Producto no encontrado.")

            ya_selecciono_alguna_opcion = True
            print(f"\n{separador}\n")
            input("Presione Enter para continuar...")


        case 4:
                
            print(borrar_pantalla  + "Buscar un producto por fragmento de nombre")
            fragmento_a_buscar = input("Ingrese el nombre del producto a buscar: ")
            encontrado = False
            print(f"|  Item  |   Precio   |            Nombre           |           Categoría          | ")
            print(separador)

            for producto in lista_de_productos:
                if producto[posicion_nombre].lower().find(fragmento_a_buscar.lower()) != -1:
                    print(f"|{producto[posicion_numeracion]:^8}|${producto[posicion_precio]:<10} | {producto[posicion_nombre]:^27} | {producto[posicion_categoria]:^29}|")
                    encontrado = True

            if not encontrado:
                print("Producto no encontrado.")

            ya_selecciono_alguna_opcion = True
            print(f"\n{separador}\n")
            input("Presione Enter para continuar...")


        case 5:
            print(borrar_pantalla  + "Eliminar un producto por su nombre")
            print(separador)
            posicion_a_borrar = input("Ingrese el la posición del producto a eliminar: ")

            eliminado = False

            for producto in lista_de_productos:
                if producto[posicion_numeracion] == int(posicion_a_borrar):
                    lista_de_productos.remove(producto)
                    print("Producto eliminado exitosamente.")
                    eliminado = True

            if not eliminado:
                print("Producto no encontrado.")   

            ya_selecciono_alguna_opcion = True
            print(f"\n{separador}\n")
            input("Presione Enter para continuar...")


        case 6:
            print("Saliendo del sistema. ¡Hasta luego!")
            break


        case _:
            print(borrar_pantalla)
            print("Opción no válida. Por favor, seleccione una opción del 1 al 6.")
            ya_selecciono_alguna_opcion = True
            print(f"\n{separador}\n")
            input("Presione Enter para continuar...")