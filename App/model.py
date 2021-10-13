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
                                loadfactor=4.0,
                                comparefunction=compareMapObrasMedios)
    catalog['nacionalidad'] = mp.newMap(30,
                                maptype='CHAINING',
                                loadfactor=4.0,
                                )
    catalog['id'] = mp.newMap(2000,
                                maptype='PROBING',
                                loadfactor=0.5,
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
def antiguaspormedio(n,medio,catalog):
    lista = lt.subList(me.getValue(mp.get(catalog['medio'],medio)),1,n)
    return lista

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
def organizarfechas(obras):
    """
    Organiza las obras por su año de creación
    """
    mergesort.sort(obras,cmpArtworkByDate)

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

        

def cmpArtworkByDate(artwork1, artwork2):
    """
    Devuelve verdadero (True) si el 'Date' de artwork1 es menores que el de artwork2
    Args:
    artwork1: informacion de la primera obra que incluye su valor 'Date'
    artwork2: informacion de la segunda obra que incluye su valor 'Date'
    """
    return artwork1['Date'] < artwork2['Date']
