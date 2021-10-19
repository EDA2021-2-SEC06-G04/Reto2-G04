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
 """

import config as cf
import model
import csv
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos
def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    
    loadArtistas(catalog)
    loadObras(catalog)
    model.nacionalidades(catalog)


def loadObras(catalog):
    """
    Carga las obras del archivo.
    """
    file = cf.data_dir + 'Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for obra in input_file:
        model.addObra(catalog, obra)

def loadArtistas(catalog):
    """
    Carga las obras del archivo.  Por cada obra se toman sus artistas y por
    cada uno de ellos, se crea en la lista de artistas, a dicho artista y una
    referencia a la obra que se esta procesando.
    """
    file = cf.data_dir + 'Artists-utf8-small.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for artista in input_file:
        model.addArtista(catalog, artista)
    

# Funciones de ordenamiento

def organizarobras(catalog):
    """
    Organiza el catálogo por el método elegido
    """
    model.organizarobras(catalog['obras'])

def organizarartistas(catalog):
    """
    Organiza los artistas por el método elegido
    """
    model.organizarartistas(catalog['artistas'],'date')

# Funciones de consulta sobre el catálogo

    #Requerimientos 1 y 2
def rangoobras(catalog,fecha_inicial,fecha_final):
    """
    Crea y devuelve la sublista de catalog con las obras ordenadas desde una fecha
    de inicio hasta otra de final.
    """
    return model.rangoobras(catalog['obras'],fecha_inicial,fecha_final)

def no_compradas(lista):
    return str(model.no_compradas(lista))

def buscarid(id,catalog):
    model.organizarartistas(catalog['artistas'],'ID')
    elementos = model.buscarid(id,catalog['artistas'])
    str = (lt.getElement(elementos,0))['DisplayName']
    i = 1
    while i < lt.size(elementos):
        str += (', ' + (lt.getElement(elementos,i))['DisplayName'])
        i += 1
    return str

def rangoartistas(catalog,fecha_inicial,fecha_final):
    """
    Crea y devuelve la sublista de catalog con los artistas ordenados desde una fecha
    de inicio hasta otra de final.
    """
    return model.rangoartistas(catalog['artistas'],fecha_inicial,fecha_final)


def antiguaspormedio(n,medio,catalog):
    """
    Devuelve una sublista con las n obras más antiguas de una lista ordenada por fecha
    """
    model.organizarfechas(me.getValue(mp.get(catalog['medio'],medio)))
    print(medio)
    lista = model.antiguaspormedio(n,medio,catalog)
    return lista
