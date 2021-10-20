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
    print("4- Clasificar las obras de un artista por técnica")
    #print("5- Clasificar obras por la nacionalidad de los artistas")
    print("6- Transportar las obras de un departamento")

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

def catalogarobras(obrasartista):
    """
    Cataloga las obras de un artista por técnica de creación
    """
    return controller.catalogarobras(obrasartista)

def agregarprecios(obras):
    """
    Agrega un precio de transporte a cada obra en la lista
    """
    return controller.agregarprecios(obras)

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

    elif int(inputs[0]) == 4:
        nombre_artista = input('Ingrese el nombre del artista a clasificar: ')
        start_time = time.process_time()
        print('\nClasificando las obras ...')
        idartista = me.getValue(mp.get(catalog['nombres'],nombre_artista))['ConstituentID']
        obrasartista = me.getValue(mp.get(catalog['id'],idartista))
        catalogarobra = catalogarobras(obrasartista)
        tecnicamayor = controller.tecnicamayor(catalogarobra) 
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('\nEl programa se demoró '+ str(elapsed_time_mseg) + ' en ordenar los datos de muestra por medio de Merge sort.')
        print('\nEl total de obras cargadas de ' + nombre_artista + ' es de ' + str(lt.size(obrasartista)))
        print('\nEl total de técnicas utilizadas por el artista es de ' + str(mp.size(catalogarobra)))
        print('\nLa técnica más usada por el artista fue ' + lt.getElement(tecnicamayor,1)['Medium'] + ' y sus elementos son:\n')
        i = 1
        while i <= lt.size(tecnicamayor):
            dimensiones = lt.getElement(tecnicamayor,i)['Dimensions']
            if dimensiones == '':
                dimensiones = 'Desconocidas'
            print('Titulo: ' + (lt.getElement(tecnicamayor,i))['Title'] + '    Fecha: ' + (lt.getElement(tecnicamayor,i))['Date'] + '   Medio: ' + (lt.getElement(tecnicamayor,i))['Medium'] + '    Dimensiones: ' + dimensiones + '\n\n')
            i += 1

    elif int(inputs[0]) == 6:
        dpto = input('Ingrese el departamento del museo que quiere trasportar: ')
        start_time = time.process_time()
        obrasdpto = me.getValue(mp.get(catalog['departamento'],dpto))
        costos = (agregarprecios(obrasdpto))[0]
        costototal = (agregarprecios(obrasdpto))[1]
        peso = (agregarprecios(obrasdpto))[2]
        controller.organizarcostos(costos)
        #print(costos)
        print('\nCalculando costos de transporte...')
        print('\nEl total de obras a transportar es de es de ' + str(lt.size(obrasdpto)))
        print('\nEl servicio costará un total estimado de ' + str(round(costototal,3)) + 'USD')
        print('\nEl peso estimado de la carga es de ' + str(round(peso,3)) + 'kg') 
        print('\nLas 5 obras más costosas de transportar son:\n')
        i = 1
        while i <= 5:
            dimensiones = lt.firstElement(lt.getElement(costos,i))['Dimensions']
            if dimensiones == '':
                dimensiones = 'Desconocidas'
            print('Titulo: ' + lt.firstElement(lt.getElement(costos,i))['Title'] + '   Artista(s): ' + controller.buscarid(lt.firstElement(lt.getElement(costos,i))['ConstituentID'],catalog) + '    Fecha: ' + lt.firstElement(lt.getElement(costos,i))['Date'] + '    Clasificación: ' + lt.firstElement(lt.getElement(costos,i))['Classification'] + '\nMedio: ' + lt.firstElement(lt.getElement(costos,i))['Medium'] + '    Dimensiones: ' + dimensiones + '    Costo de transporte: ' + str(round(lt.lastElement(lt.getElement(costos,i)),3)) + '\n\n')
            i += 1
        controller.organizarfechas(costos)
        print('\nLas 5 obras más antiguas a transportar son:\n')
        aux = 0
        i = 1
        while aux < 5:
            if lt.firstElement(lt.getElement(costos,i))['Date'] != '':
                dimensiones = lt.firstElement(lt.getElement(costos,i))['Dimensions']
                if dimensiones == '':
                    dimensiones = 'Desconocidas'
                print('Titulo: ' + lt.firstElement(lt.getElement(costos,i))['Title'] + '   Artista(s): ' + controller.buscarid(lt.firstElement(lt.getElement(costos,i))['ConstituentID'],catalog) + '    Fecha: ' + lt.firstElement(lt.getElement(costos,i))['Date'] + '    Clasificación: ' + lt.firstElement(lt.getElement(costos,i))['Classification'] + '\nMedio: ' + lt.firstElement(lt.getElement(costos,i))['Medium'] + '    Dimensiones: ' + dimensiones + '    Costo de transporte: ' + str(round(lt.lastElement(lt.getElement(costos,i)),3)) + '\n\n')
                aux += 1 
            i += 1
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print('\nEl programa se demoró '+ str(elapsed_time_mseg) + ' en ordenar los datos de muestra por medio de Merge sort.')

    elif int(inputs[0]) == 0:
        catalog = None

    else:
        sys.exit(0)
sys.exit(0)
