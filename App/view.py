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
    print("2- Listar cronológicamente artistas")
    print("3- Listar cronológicamente adquisiciones")

def organizarartistas(catalog):
    """
    Organiza la lista de artistas del catálogo
    """
    controller.organizarartistas(catalog)

def organizarobras(catalog):
    """
    Organiza la lista obras del catálogo
    """
    controller.organizarobras(catalog)

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
        organizarartistas(catalog)
        organizarobras(catalog)
        print('Obras cargadas: ' + str(lt.size(catalog['obras'])))
        print('Artistas cargados: ' + str(lt.size(catalog['artistas'])))
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('El programa se demoró '+ str(elapsed_time_mseg) + ' en cargar los datos')


    elif int(inputs[0]) == 2:
        fecha_inicial = input('Escriba el año inicial del rango: ')
        fecha_final = input('Escriba el año final del rango: ')
        start_time = time.process_time()
        print('\nOrganizando los artistas ...')
        rangoartista = controller.rangoartistas(catalog,fecha_inicial,fecha_final)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('El programa se demoró '+ str(elapsed_time_mseg) + ' en ordenar los datos de muestra por medio de Merge sort.')
        i = 1
        print('\nHay ' + str(lt.size(rangoartista)) + ' artistas nacidos en el rango indicado.\n')
        print('Los primeros y últimos 3 artistas en el rango son:\n')
        while i <= 3:
            try:
                muerte = (lt.getElement(rangoartista,i))['EndDate']
                genero = (lt.getElement(rangoartista,i))['Gender']
                if muerte == '0':
                    muerte = 'Desconocido o sigue vivo'
                if genero == '':
                    genero = 'Desconocido o no aplica'
                print('Nombre: ' + (lt.getElement(rangoartista,i))['DisplayName'] + '    Año de nacimiento: ' + (lt.getElement(rangoartista,i))['BeginDate'] + '    Año de fallecimiento: ' + muerte + '     Nacionalidad: ' + (lt.getElement(rangoartista,i))['Nationality'] + '    Género: ' + genero + '\n\n')
                i += 1
            except:
                i += 1
        i = 2
        while i >= 0:
            try:
                muerte = (lt.getElement(rangoartista,i))['EndDate']
                if muerte == '0':
                    muerte = 'Desconocido o sigue vivo'
                print('Nombre: ' + (lt.getElement(rangoartista,lt.size(rangoartista) - i))['DisplayName'] + '    Año de nacimiento: ' + (lt.getElement(rangoartista,lt.size(rangoartista) - i))['BeginDate'] + '    Año de fallecimiento: ' + muerte + '     Nacionalidad: ' + (lt.getElement(rangoartista,lt.size(rangoartista) - i))['Nationality'] + '    Género: ' + genero + '\n\n')
                i -= 1
            except:
                i -= 1
    
    elif int(inputs[0]) == 3:
        fecha_inicial = input('Escriba la fecha inicial en formato YYYY-MM-DD: ')
        fecha_final = input('Escriba la fecha final en formato YYYY-MM-DD: ')
        start_time = time.process_time()
        print('\nOrganizando el catálogo ...')
        organizarobras(catalog)
        rangoobra = controller.rangoobras(catalog,fecha_inicial,fecha_final)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('El programa se demoró '+ str(elapsed_time_mseg) + ' en ordenar los datos de muestra por medio de Merge sort.')
        i = 1
        print('\nHay ' + str(lt.size(rangoobra)) + ' obras en el rango indicado.\n')
        print(controller.no_compradas(rangoobra) + ' de estas obras fueron adquiridas por compra.\n')
        print('Las 3 primeras y 3 últimas obras en el rango son:\n')
        while i <= 3:
            dimensiones = (lt.getElement(rangoobra,i))['Dimensions']
            if dimensiones == '':
                dimensiones = 'Desconocidas'
            print('Titulo: ' + (lt.getElement(rangoobra,i))['Title'] + '   Artista(s): ' + controller.buscarid((lt.getElement(rangoobra,i))['ConstituentID'],catalog) + '    Fecha: ' + (lt.getElement(rangoobra,i))['Date'] + '    Fecha de adquisición: ' + (lt.getElement(rangoobra,i))['DateAcquired'] + '\nMedio: ' + (lt.getElement(rangoobra,i))['Medium'] + '    Dimensiones: ' + dimensiones + '\n\n')
            i += 1
        i = 2
        while i >= 0:
            dimensiones = (lt.getElement(rangoobra,lt.size(rangoobra) - i))['Dimensions']
            if dimensiones == '':
                dimensiones = 'Desconocidas'
            print('Titulo: ' + (lt.getElement(rangoobra,lt.size(rangoobra) - i))['Title'] + '   Artista(s): ' + controller.buscarid((lt.getElement(rangoobra,lt.size(rangoobra) - i))['ConstituentID'],catalog) + '    Fecha: ' + (lt.getElement(rangoobra,lt.size(rangoobra) - i))['Date'] + '    Fecha de adquisición: ' + (lt.getElement(rangoobra,lt.size(rangoobra) - i))['DateAcquired'] + '\nMedio: ' + (lt.getElement(rangoobra,lt.size(rangoobra) - i))['Medium'] + '    Dimensiones: ' + dimensiones + '\n\n')
            i -= 1

    else:
        sys.exit(0)
sys.exit(0)
