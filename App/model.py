"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """
    Inicializa el catálogo de obras. Crea una lista vacia para guardar
    todas las obras, adicionalmente, crea una lista vacia para los artistas.
     Retorna el catalogo inicializado.
    """
    catalog = {'obras': None,
               'artistas': None,
               'medio': None}

    catalog['obras'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['artistas'] = lt.newList(datastructure='ARRAY_LIST')
    catalog['medio'] = mp.newMap(30,
                                maptype='CHAINING',
                                loadfactor=2.0,
                                comparefunction=compareMapObrasMedios)
    catalog['nacionalidad'] = mp.newMap(30,
                                maptype='CHAINING',
                                loadfactor=2.0,
                                )
    catalog['id'] = mp.newMap(
                                maptype='CHAINING',
                                loadfactor=4.0,
                                )

    return catalog

# Funciones para agregar informacion al catalogo
def addObra(catalog, obra):
    lt.addLast(catalog['obras'], obra)
    try:
        lt.addLast(me.getValue(mp.get(catalog['medio'],obra['Medium'])),obra)
    except:
        mp.put(catalog['medio'],obra['Medium'],lt.newList(datastructure='ARRAY_LIST')) 
        lt.addLast(me.getValue(mp.get(catalog['medio'],obra['Medium'])),obra)
    
def nacionalidades(catalog):
    for obra in lt.iterator(catalog['obras']):
        idsobra = obra['ConstituentID']
        x = idsobra.replace('[','')
        y = x.replace(']','')
        z = y.replace(' ','')
        ids = z.split(',')
        nacionalidades = lt.newList(datastructure='ARRAY_LIST')
        for id in ids:
            if lt.isPresent(nacionalidades,me.getValue(mp.get(catalog['id'],id))['Nationality']) == False:
                #print(ids)
                lt.addLast(nacionalidades,me.getValue(mp.get(catalog['id'],id))['Nationality'])
                #print(nacionalidades)
        for paisartista in lt.iterator(nacionalidades):
            try:
                #print(paisartista)
                #print(mp.get(catalog['nacionalidad'],paisartista))
                lt.addLast(me.getValue(mp.get(catalog['nacionalidad'],paisartista)),obra)
            except:
                mp.put(catalog['nacionalidad'],paisartista,lt.newList(datastructure='ARRAY_LIST')) 
                lt.addLast(me.getValue(mp.get(catalog['nacionalidad'],paisartista)),obra)
            


def addArtista(catalog, artista):
    lt.addLast(catalog['artistas'], artista)
    mp.put(catalog['id'],artista['ConstituentID'],artista)



# Funciones para creacion de datos

# Funciones de consulta
def busquedaID(array, element, start, end):
    if start > end:
        return -1

    mid = (start + end) // 2

    if element == int(lt.getElement(array,mid)['ConstituentID']):
        return mid

    if element < int(lt.getElement(array,mid)['ConstituentID']):
        return busquedaID(array, element, start, mid-1)
    else:
        return busquedaID(array, element, mid+1, end)
    
def busquedaano(lista, ano, start, end, tipo,criterio):
    if (start != end) and (end - start) > 1:
        mid = (start + end) // 2
        if ano == (aentero(lt.getElement(lista,mid)[criterio])):
            if tipo == 'menor':
                mid -= 1
                while aentero(lt.getElement(lista,mid)[criterio]) == ano:
                    mid -= 1
                return mid + 1
            elif tipo == 'mayor':
                mid += 1
                while aentero(lt.getElement(lista,mid)[criterio]) == ano:
                    mid += 1
                return mid - 1

        if ano < aentero(lt.getElement(lista,mid)[criterio]):
            return busquedaano(lista, ano, start, mid-1,tipo,criterio)
        else:
            return busquedaano(lista, ano, mid+1, end,tipo,criterio)
    elif tipo == 'menor':
        if ano < (aentero(lt.getElement(lista,end)[criterio])):
            while (ano < aentero(lt.getElement(lista,end)[criterio])) and aentero(lt.getElement(lista,end)[criterio]) != 0:
                end -= 1
            return end + 1    
        elif ano > aentero(lt.getElement(lista,end)[criterio]):
            
            while (ano > aentero(lt.getElement(lista,end)[criterio])) and aentero(lt.getElement(lista,end)[criterio]) != 0:
                end += 1
            return end - 1      
        return end
    elif tipo == 'mayor':
        if ano < aentero(lt.getElement(lista,end)[criterio]):
            while ano < aentero(lt.getElement(lista,end)[criterio]):
                end -= 1
        return end
    #Requerimientos 1 y 2

def buscarid(id,artistas):
    x = id.replace('[','')
    y = x.replace(']','')
    ids = y.split(',')
    indices = lt.newList(datastructure='ARRAY_LIST')
    for i in ids:
        lt.addLast(indices,lt.getElement(artistas,(busquedaID(artistas,int(i),0,lt.size(artistas) - 1))))
    return indices

def aentero(str):
    if str == '':
        return 0    
    return int(str.replace('-',''))


def rangoobras(obras,fecha_inicial,fecha_final):
    """
    Crea y devuelve la sublista de catalog con las obras ordenadas desde un año
    de inicio hasta otro de final.
    """
    fecha_inicial = aentero(fecha_inicial)
    fecha_final = aentero(fecha_final)
    indiceinicial = busquedaano(obras,fecha_inicial,0,lt.size(obras) - 1,'menor','DateAcquired')
    if lt.getElement(obras,indiceinicial)['DateAcquired'] == '':
        return lt.newList(datastructure='ARRAY_LIST')
    indicefinal = busquedaano(obras,fecha_final,0,lt.size(obras) - 1,'mayor','DateAcquired')
    rango = lt.subList(obras,indiceinicial,(indicefinal-indiceinicial+1))
    return rango

def no_compradas(list):
    i = 1
    compradas = 0
    while i <= lt.size(list):
        if 'purchase' in ((lt.getElement(list,i))['CreditLine']).lower():
            compradas += 1
        i += 1
    return compradas

def rangoartistas(artistas,fecha_inicial,fecha_final):
    """
    Crea y devuelve la sublista de catalog con los artistas ordenados desde un año
    de inicio hasta otro de final.
    """
    fecha_inicial = aentero(fecha_inicial)
    fecha_final = aentero(fecha_final)
    indiceinicial = busquedaano(artistas,fecha_inicial,0,lt.size(artistas) - 1,'menor','BeginDate')
    if lt.getElement(artistas,indiceinicial)['BeginDate'] == '0':
        return lt.newList(datastructure='ARRAY_LIST')
    indicefinal = busquedaano(artistas,fecha_final,0,lt.size(artistas) - 1,'mayor','BeginDate')
    rango = lt.subList(artistas,indiceinicial,(indicefinal-indiceinicial+1))
    return rango



# Funciones de ordenamiento

def organizarobras(obras):
    """
    Organiza el catálogo por el método elegido
    """
    mergesort.sort(obras,cmpArtworkByDateAcquired)

def organizarfechas(obras):
    """
    Organiza las obras por su año de creación
    """
    mergesort.sort(obras,cmpArtworkByDate)

def organizarartistas(artistas,cmpf):
    """
    Organiza los artistas por el método elegido
    """
    if cmpf == 'ID':
        mergesort.sort(artistas,cmpArtistsByConstituentID)
    else:
        mergesort.sort(artistas,cmpArtistsByDate)

# Funciones de comparación
def compareMapObrasMedios(keyname, medio):
    """
    Compara dos medios. El primero es una cadena
    y el segundo un entry de un map
    """
    medioentry = me.getKey(medio)
    if (keyname == medioentry):
        return 0
    elif (keyname > medioentry):
        return 1
    else:
        return -1

# Funciones utilizadas para comparar elementos dentro de una lista

def compareartists(artistaname1, artista):
    if (artistaname1.lower() in artista['name'].lower()):
        return 0
    return -1

def cmpArtworkByDateAcquired(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'DateAcquired' de artwork1 es menores que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'DateAcquired'
    artwork2: informacion de la segunda obra que incluye su valor 'DateAcquired'
    """
    return artwork1['DateAcquired'] < artwork2['DateAcquired']

def cmpArtistsByConstituentID(artist1, artist2):
    """
    Devuelve verdadero (True) si el 'ConstituentID' de artist1 es menor que el de artist2
    Args:
    artist1: informacion del primer artista que incluye su valor 'ConstituentID'
    artist2: informacion del segundo artista que incluye su valor 'ConstituentID'
    """
    return int(artist1['ConstituentID']) < int(artist2['ConstituentID'])

def cmpArtistsByDate(artist1, artist2):
    """
    Devuelve verdadero (True) si el 'BeginDate' de artist1 es menor que el de artist2
    Args:
    artist1: informacion del primer artista que incluye su valor 'BeginDate'
    artist2: informacion del segundo artista que incluye su valor 'BeginDate'
    """
    return int(artist1['BeginDate']) < int(artist2['BeginDate'])

def cmpArtworkByCost(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el costo de transporte de artwork1 es menores que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su costo de transporte
    artwork2: informacion de la segunda obra que incluye su costo de transporte
    """
    return lt.lastElement(artwork1) > lt.lastElement(artwork2)

def cmpArtworkByDate(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'Date' de artwork1 es menores que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'Date'
    artwork2: informacion de la segunda obra que incluye su valor 'Date'
    """
    return (lt.firstElement(artwork1)['Date'] < lt.firstElement(artwork2)['Date'])





