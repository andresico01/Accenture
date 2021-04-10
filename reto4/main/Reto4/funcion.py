"""
En el perfil de facturación se pueden realizar las siguientes funciones: consultar un producto
mediante su código y elaborar una nueva factura con su respectiva numeración.
El programa debe permitir al usuario finalizar el proceso cuando así se le indique, en el caso
del perfil de facturación debe indicar el total vendido durante el día, así como el número de
la última factura.
La factura debe tener las siguientes características:
 Nombre y cedula del cliente
 Un listado de los productos adquiridos por el cliente con su respectiva cantidad, el
subtotal de cada producto y el valor de IVA que posee (el %)
 El valor total de la factura, el subtotal sin IVA, y los valores individuales para cada
IVA.
"""
import random
import pandas as pd 
from pandas import ExcelWriter

from subprocess import call
lista_diccionario = list()
CedulaCliente = list()
factura = list()
adminstrador = ('rangiro', 99999)
facturacion =('casimiro', 88888)
def ListaMercancia():
    archivo = pd.read_excel("/home/patyy/Documents/reto4/Productos/Productos.xlsx", names = ['CODIGO','DESCRIPCION','IVA','PRECIO'], engine='openpyxl')
    control  = ['CODIGO','DESCRIPCION','IVA','PRECIO']
    diccionario = {'CODIGO' : 0,'DESCRIPCION': 0,'IVA': 0,'PRECIO':0}
    global lista_diccionario
    posicion = 0
    for posicion in range(len(archivo)):
        for clave in control:
            diccionario[clave] = archivo[clave][posicion]
        
        lista_diccionario.append(diccionario.copy())
    print(archivo)


def Buscar(Numero):
    try:
        cont = 0
        print("si desea buscar un producto precione 1.\nsi en cambio desea buscar un cliente unda 2 ")
        opcion = int(input("esperando:\t"))
        if opcion == 2:
            for iterador in CedulaCliente:
                if Numero == iterador['Cedula']:
                    break
                cont+=1
        elif(opcion == 1):
            for iterador in factura:
                if Numero == iterador['Codigo']:
                    break
                cont+=1
        return cont
    except:
        print("paso algo...")
        return Buscar(Numero)
    
def ProductosCanasta():
    try :
        Producto = {'Codigo' : 0,'Producto' : 0,'Iva': 0,'Precio': 0,'Cantidad': 0}
        salida = True
        control = 0
        print("ingrese los codigos de los productos")
        while salida:
            cont = 0
            codigo = int(input("ingrese codigo:\t"))
            for item in lista_diccionario:
                if codigo == item['CODIGO']:
                    break
                cont+=1
            if codigo == item['CODIGO']:
                Producto['Codigo'] = lista_diccionario[cont]['CODIGO']
                Producto['Producto'] = lista_diccionario[cont]['DESCRIPCION']
                Producto['Iva'] = lista_diccionario[cont]['IVA']
                Producto['Precio'] = lista_diccionario[cont]['PRECIO']
                Producto['Cantidad'] = int(input("cantidad del producto:\t"))
                factura.append(Producto.copy())
            else:
                print("Codigo no identificado")
            control = str(input("...."))
            if control in ['s','S']:
                salida = False
            elif control in ['c','C']:  # eliminar producto de factura
                Admi()          
    except:
        print("ingreso un caracter")
        return ProductosCanasta()
            
def ListaClientes():
    try:
        Cliente = {'Nombre' : 0,'Cedula' : 0,'Direccion': 0,'PagoTotal': 0,'PagoSub' : 0}
        Nombre = str(input("ingrese nombre del cliente:\t")) 
        Cedula = int(input("ingrese la cedula el cliente:\t"))
        direccion = input("Ingrese direccion de cliente:\t")
        Cliente['Nombre'] = Nombre
        Cliente['Cedula'] = Cedula
        Cliente['Direccion'] = direccion
        ProductosCanasta()
        CedulaCliente.append(Cliente.copy())
        return Cliente
    except:
        print("ingreso un caracter invalido")
        return ListaClientes()
        
def Admi():
    try:
        NombreAdmin = input("ingrese usuario administrado.\n")
        NombreAdmin = NombreAdmin.strip()
        ContraseñaAdmi = int(input("ingrese clave del administrador.\n"))
        
        if (NombreAdmin in adminstrador) and (ContraseñaAdmi in adminstrador):
            print("1)eliminar producto")
            
            codigo = int(input("ingrese codigo:\t"))
            posicion = Buscar(codigo)
            factura.pop(posicion)             
        else:
            call("clear")
            print("El usuario ingresado o la contraseña son incorrectas")
            return Admi()
    except:
        call("clear")
        print("ingreso algun dato inadecuado, vuelva a intentar")
        return  Admi()
def GenerarPago(usuario):
    listaCodigo = list()
    listaNombre = list()
    listaIva = list()
    listaPrecio = list()
    listaCantidad = list()
    factu = {'Cliente':0,'Codigo' :0, 'Nombre' : 0,'Iva' : 0,'Precio' : 0,'Cantidad' : 0 }
    SumaTotal = 0
    cliente = usuario()
    SumaSubTotal = 0
    domicilio = 4000
    for producto in factura:
        codigo,nombre,iva,precio,cantidad = producto.values()
        listaCodigo.append(codigo)
        listaNombre.append(nombre)
        listaIva.append(iva)
        listaPrecio.append(precio)
        listaCantidad.append(cantidad)
        SumaTotal += (precio)*cantidad
        SumaSubTotal += precio*cantidad
    if SumaTotal >= 100000:
        SumaTotal -= domicilio
    if SumaTotal >= 70000:
        SumaTotal *=1.19
    cliente['PagoTotal'] = SumaTotal + domicilio
    cliente['PagoSub'] = SumaSubTotal
    factu['Codigo'] = listaCodigo
    factu['Nombre'] = listaNombre
    factu['Iva'] = listaIva
    factu['Precio'] = listaPrecio

    factu['Cantidad'] = listaCantidad
    factu['Cliente'] = cliente
    
    return factu
def visualizar(valor):
    axuliar = valor['Cliente']
    Codigo = valor['Codigo']
    Nombre = valor['Nombre']
    Iva = valor['Iva']
    Precio = valor['Precio']
    Cantidad = valor['Cantidad']
    indice = 0
    veces = len(Iva)
    
    if axuliar['PagoSub'] >= 70000:
        pagoIva = 0.19
    else:
        pagoIva = 0 
    print(veces)
    print(f"el cliente: {axuliar['Nombre']} de cedular: {axuliar['Cedula']}")
    print("Codigo\t\tPrecio\tCantidad\tValor Neto\t\tValor con iva\tNombre")
    while indice < veces:
        print(f"{Codigo[indice]}\t\t{Precio[indice]}\t{Cantidad[indice]}\t\t{Precio[indice]*Cantidad[indice]}\t\t{(1+pagoIva)*Precio[indice]*Cantidad[indice]}\t\t{Nombre[indice]}")
        indice += 1
    print(f"Subtotal:\t{axuliar['PagoSub']}\nPago Total:\t{axuliar['PagoTotal']}")
def Cajer():
    try:
        NombreCajero = input("ingrese usuario caja.\n")
        Nombrecajero = NombreCajero.strip()
        ContraseñaCajero = int(input("ingrese clave de caja.\n"))
        
        if (Nombrecajero in facturacion) and (ContraseñaCajero in facturacion):
            fact = GenerarPago(ListaClientes)
            visualizar(fact)
            

        else:
            call("clear")
            print("El usuario ingresado o la contraseña son incorrectas")
            return Cajer()
    except:
        call("clear")
        print("ingreso algun dato inadecuado, vuelva a intentar")
        return  Cajer()
  
