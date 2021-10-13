"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as mp
assert cf
import time

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Ver las n obras más antiguas para un medio específico")
    print("3- Ver el número total de obras de una nacionalidad")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        start_time = time.process_time()
        print("Cargando información de los archivos ....")
        catalog = controller.initCatalog()
        controller.loadData(catalog)
        print('Obras cargadas: ' + str(lt.size(catalog['obras'])))
        print('Artistas cargados: ' + str(lt.size(catalog['artistas'])))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('El programa se demoró '+ str(elapsed_time_mseg) + ' en cargar los datos')

    elif int(inputs[0]) == 2:
        n = input('Cuántas obras quiere ver: ')
        medio = input('De qué medio las quiere ver: ')
        lista = controller.antiguaspormedio(int(n),medio,catalog)
        iterador = lt.iterator(lista)
        print('Las ' + n + ' obras mas viejas hechas en ' + medio + ' son:')
        for obra in iterador:
            print(obra)
    
    elif int(inputs[0]) == 3:
        nacionalidad = input('De qué nacionalidad quieres ver el número de obras: ')
        try:
            tamano = lt.size(me.getValue(mp.get(catalog['nacionalidad'],nacionalidad)))
            print('Hay ' + str(tamano) + ' obras para la nacionalidad ' + nacionalidad)
        except:
            print('No hay obras para la nacionalidad indicada')

    else:
        sys.exit(0)
sys.exit(0)
