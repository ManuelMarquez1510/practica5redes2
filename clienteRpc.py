import os
import xmlrpc.client


gestorFicheros = xmlrpc.client.ServerProxy('http://127.0.0.1:8080')

def SeleccionarFichero(ruta, accion, esCarpeta = False):
    archivos = gestorFicheros.ObtenerContenido(ruta)

    while(True):
        i = 0
        files = []
        carpetas = []
        print("Ficheros disponibles: ")
        for archivo in archivos:
            if( "." in archivo ):
                files.append(archivo)
            else:
                carpetas.append(archivo)

            if(not esCarpeta and "." in archivo):
                print( "\t" + str( len(files) ) + ". " + archivo)
            elif(esCarpeta and "." not in archivo):
                print( "\t" + str( len(carpetas) ) + ". " + archivo)

        if( (len(files) == 0 and not esCarpeta) or (len(carpetas) == 0 and esCarpeta) ):
            input ("\t No hay ficheros en esta carpeta. Pulsa enter para continuar ...")
            return ""

        if(esCarpeta):
            aux = carpetas
        else:
            aux = files

        opcion = input( "\t Ingresa el numero del fichero que deseas " + accion + ": ")
        if( opcion.isdigit() ):
            numArchivo = int(opcion)
            if(numArchivo > 0 and numArchivo <= len(aux)):
                if(esCarpeta):
                    return carpetas[numArchivo - 1]
                return ruta + files[numArchivo - 1]

        print("\t Selecciona una opción valida")

ruta = "/"
while(True):
    os.system("clear")
    aArchivos = []
    aDirectorio = []
    for archivo in gestorFicheros.ObtenerContenido(ruta):
        if( "." in archivo ):
            aArchivos.append(archivo)
        else:
            aDirectorio.append(archivo)
    
    print("Te encuentras en la ruta : " + ruta)
    for directorio in aDirectorio:
        print("\t" + directorio)           
    for archivo in aArchivos:
        print("\t" + archivo)

    print("\nOperaciones con ficheros:")
    print("\t1. Crear fichero")
    print("\t2. Ver fichero")
    print("\t3. Modificar contenido del fichero")
    print("\t4. Renombrar fichero")
    print("\t5. Borrar fichero")
    print("Operaciones con carpetas:")
    print("\t6. Crear carpeta")
    print("\t7. Abrir carpeta")
    print("\t8. Borrar carpeta")
    print("\t9. Renombrar carpeta")
    print("\t10. Carpeta anterior")
    print("11. Salir")
    
    opcion = input(" Seleccione una opción: ")

    if( opcion == "1"):
        nombre = input( "Ingresa el nombre del archivo de texto: ")
        input( gestorFicheros.CrearFichero(nombre.replace(" ", ""), ruta) )

    elif( opcion == "2"):
        archivo = SeleccionarFichero(ruta, "ver")
        if( archivo != ""):                    
            print( gestorFicheros.AbrirFichero(archivo) )
            input("\tPulsa enter para continuar ... ")

    elif( opcion == "3"):
        archivo = SeleccionarFichero(ruta, "modificar")
        if( archivo != ""):
            nuevoContenido = input("\t Ingresa el nuevo nombre para el fichero " + archivo + ": ")
            print( gestorFicheros.ModificarFichero(archivo, nuevoContenido) )

    elif( opcion == "4"):
        archivo = SeleccionarFichero(ruta, "renombrar")
        if( archivo != ""):
            nombre = input("\t Ingresa el nuevo nombre para el fichero " + archivo + ": ")
            print(gestorFicheros.RenombrarFichero(ruta, archivo, nombre))

    elif( opcion == "5"):
        archivo = SeleccionarFichero(ruta, "eliminar")
        if( archivo != ""):      
            opcion = input("\t Seguro que desea eliminar el fichero? s/n: ")
            if( opcion.lower() == "s"):
                gestorFicheros.BorrarFichero(archivo)

    elif( opcion == "6"):
        nombre = input( "\tIngresa el nombre de la carpeta: ")
        input( gestorFicheros.CrearCarpeta(ruta, nombre) )

    elif( opcion == "7"):
        directorio = SeleccionarFichero(ruta, "abrir", True)
        if(directorio != ""):
            ruta = ruta + directorio + "/"

    elif( opcion == "8"):
        directorio = SeleccionarFichero(ruta, "eliminar", True)

        if(directorio != ""):
            opcion = input("\t Seguro que desea eliminar la carpeta? s/n: ")
            if( opcion.lower() == "s"):
                gestorFicheros.BorrarCarpeta(ruta+directorio, True)

    elif( opcion == "9"):
        directorio = SeleccionarFichero(ruta, "renombrar", True)
        nuevoDirectorio = input( "\tIngresa el nuevo nombre para " + directorio + " : ")
        gestorFicheros.CrearCarpeta(ruta, nuevoDirectorio)
        gestorFicheros.RenombrarCarpeta(ruta + nuevoDirectorio, ruta + directorio, True)

    elif( opcion == "10"):
        ruta = gestorFicheros.RegresarCarpeta(ruta)
        print("Se ha regresado al directorio anterior con exito" + ruta)

    elif( opcion == "11"):
        break
    else:
        print("Ingresa una opción valida")
        input("Pulsa enter para continuar")
print("Saliendo")