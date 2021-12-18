import os
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

HOME = os.getcwd() + "/Home"

with SimpleXMLRPCServer(('127.0.0.1', 8080),requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    def CrearFichero(nombre, r):
        ruta = HOME + r
        print("Crear fichero: " + r + nombre)
        try:
            with open(ruta + nombre + ".txt", "x") as archivo:
                return("\t" + "El fichero " + nombre + " se ha creado")
        except:
            return("\t" + "Error al crear el fichero" + nombre )

    def ObtenerContenido(r):
        try:
            ruta = HOME + r
            return os.listdir(ruta)
        except:
            return os.listdir(HOME)
    
    def RenombrarFichero(r, nombreArchivo, nuevoNombre):
        nombreArchivo = HOME + nombreArchivo        
        return CopiarFichero(nombreArchivo, HOME + r + "/" + nuevoNombre + ".txt", "renombrado")

    def ModificarFichero(r, nuevoContenido):
        nombreArchivo = HOME + r
        try:
            with open(nombreArchivo, "w") as archivo:
                archivo.write(nuevoContenido)
                response = "El fichero se ha modificado correctamente"
        except:
            response = "Error al modificar el fichero"
        return response

    def BorrarFichero(r):
        nombreArchivo = HOME + r
        os.remove(nombreArchivo)
        return "El fichero se ha eliminado"

    def CrearCarpeta(r, nombre):
        ruta = HOME + r
        if( not os.path.exists(ruta + nombre + "/") ):
            os.mkdir(ruta + nombre + "/")
            return( "\t" + "La carpeta " + nombre + " se ha creado")
        else:
            return( "\t" + "Error al crear la carpeta " + nombre)

    def BorrarCarpeta(r, borrar = False):
        if(borrar):
            ruta = HOME + r
        else:
            ruta = r
        print(ruta)
        contenidos = os.listdir(ruta)
        
        for contenido in contenidos:
            if("." in contenido):
                os.remove(ruta + "/" + contenido)
            else:            
                BorrarCarpeta(ruta + "/" + contenido)
        os.rmdir(ruta)
        return "Carpeta eliminada"

    def RenombrarCarpeta(nuevoDirectorio, r, borrar = False):
        if(borrar):
            nuevo = HOME + nuevoDirectorio
        else:
            nuevo = nuevoDirectorio
        contenidos = os.listdir(HOME + r)

        for contenido in contenidos:
            if("." in contenido):
                print( CopiarFichero(HOME + r + "/" + contenido, nuevo + "/" + contenido, "renombrado") )
            else:
                CrearCarpeta( nuevo.replace(HOME,"") + "/",contenido)
                RenombrarCarpeta(nuevo + "/" + contenido, r + "/" + contenido)
        os.rmdir(HOME + r)
        return "Carpeta renombrada"

    def CopiarFichero(original, copia, accion = ""):
        contenido = ""
        try:
            with open(original, "r") as archivo1:
                contenido = archivo1.read()

            with open(copia, "w") as archivo2:
                archivo2.write(contenido)
            os.remove(original)
            response = "El fichero " + copia + " se ha " + accion
        except:
            response = "Error al " + accion + " el fichero " + original
        return response

    def ListarCarpetas(r):
        ruta = HOME + r
        print( "Ficheros en la carpeta " + ( ruta.replace(HOME, "") ) )
        return( "\t" + str(os.listdir(ruta)) )

    def AbrirFichero(ruta):
        nombreArchivo = HOME + ruta
        try:
            with open(nombreArchivo, "r") as archivo:
                contenido = archivo.read()
                response  = ( "\tContenido: " + "\n\t\t'" + contenido.replace("\n","\n\t")+ "'")
        except:
            response = "\tError al abrir el fichero: " + nombreArchivo
        return response

    def RegresarCarpeta(ruta):
        print("Regresar")    
        if( ruta.replace(HOME,"") != "/"):
            arrayRuta = ruta.replace(HOME,"").split("/")
            rActual = ""
            for i in range(0, len(arrayRuta) - 2):
                rActual = rActual + arrayRuta[i] + "/"
            return rActual
        return "/"

    def SeleccionarFichero(archivos, accion, esDirectorio = False):
        while(True):
            i = 0
            files = []
            directorios = []
            
            for archivo in archivos:            
                if( "." in archivo ):
                    files.append(archivo)
                else:
                    directorios.append(archivo)

                if(not esDirectorio and "." in archivo):
                    print( "\t" + str( len(files) ) + ". " + archivo)
                elif(esDirectorio and "." not in archivo):
                    print( "\t" + str( len(directorios) ) + ". " + archivo)

            if( (len(files) == 0 and not esDirectorio) or (len(directorios) == 0 and esDirectorio) ):
                return ""

            if(esDirectorio):
                aux = directorios
            else:
                aux = files

            opcion = input( "\t Ingresa el numero del fichero que deseas " + accion + ": ")
            if( opcion.isdigit() ):
                numArchivo = int(opcion)
                if(numArchivo > 0 and numArchivo <= len(aux)):
                    if(esDirectorio):
                        return directorios[numArchivo - 1]
                    return files[numArchivo - 1]
            print("\t Selecciona una opción valida")
    
    server.register_function(ObtenerContenido, 'ObtenerContenido')
    server.register_function(CrearFichero, 'CrearFichero')
    server.register_function(RenombrarFichero, 'RenombrarFichero')
    server.register_function(ModificarFichero, 'ModificarFichero')
    server.register_function(BorrarFichero, 'BorrarFichero')
    server.register_function(CrearCarpeta, 'CrearCarpeta')
    server.register_function(BorrarCarpeta, 'BorrarCarpeta')
    server.register_function(RenombrarCarpeta, 'RenombrarCarpeta')
    server.register_function(CopiarFichero, 'CopiarFichero')
    server.register_function(ListarCarpetas, 'ListarCarpetas')
    server.register_function(AbrirFichero, 'AbrirFichero')
    server.register_function(RegresarCarpeta, 'RegresarCarpeta')
    server.register_function(SeleccionarFichero, 'SeleccionarFichero')

    server.serve_forever()
