import Reto4.funcion as fun

def menu():
    fun.ListaMercancia()
    print("1)ingresando a caja para cancelar\n2)salir\n")
    opcion = 0
    salida = True
    while salida:
        try:
            opcion = int(input(""))
            if opcion == 1:
                fun.Cajer()        
            elif opcion == 2:
                salida = False
        except:
            print("algo salio mal")
            return menu()

if __name__ =="__main__":
    menu()


