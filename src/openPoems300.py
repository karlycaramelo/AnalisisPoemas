from urllib.request import urlopen
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt
import json
from minisom import MiniSom
from string import punctuation
import stop_words
from minisom import MiniSom

#Yellow
#2Blue
#3Red

#file_name_poet0="1608_1674-john-milton"
#file_name_poet1="1885_1972-ezra-pound"
#file_name_poet2="1819_1892-walt-whitman"

#file_name_poet0="1809_1849-edgar-allan-poe"
#file_name_poet1="1854_1900-oscar-wilde"
#file_name_poet2="1842_1913-ambrose-bierce"

#file_name_poet0="1564_1616-william-shakespeare"
#file_name_poet1="1770_1850-william-wordsworth"
#file_name_poet2="1757_1827-william-blake"

#file_name_poet0="1854_1900-oscar-wilde"
#file_name_poet1="1770_1850-william-wordsworth"
#file_name_poet2="1842_1913-ambrose-bierce"

#file_name_poet0="1608_1674-john-milton"
#file_name_poet1="1809_1849-edgar-allan-poe"
#file_name_poet2="1770_1850-william-wordsworth"


#file_name_poet0="1865_1936-rudyard-kipling"
#file_name_poet1="1840_1928-thomas-hardy"
#file_name_poet2="1932_1963-sylvia-plath"


#file_name_poet0="1564_1616-william-shakespeare"
#file_name_poet1="1865_1936-rudyard-kipling"
#file_name_poet2="1932_1963-sylvia-plath"

file_name_poet0="1809_1849-edgar-allan-poe"
file_name_poet1="1770_1850-william-wordsworth"
file_name_poet2="1757_1827-william-blake"

#Obtenemos todos los poemas de los 3 poetas en diccionar donde las llaves son
#Los titulos
filepoet0 = open(file_name_poet0+'.txt', 'r')
poems_poet0 = json.load(filepoet0)
filepoet0.close()

filepoet1 = open(file_name_poet1+'.txt', 'r')
poems_poet1 = json.load(filepoet1)
filepoet1.close()

filepoet2 = open(file_name_poet2+'.txt', 'r')
poems_poet2 = json.load(filepoet2)
filepoet2.close()


#Listado de las "palabras vacias" estop world en ingles que son las palabras que no 
#tiene significado como artículos, pronombres, preposiciones, etc.
stopwords = stop_words.get_stop_words('english')
#Metodo que remueve todos los signos de puntuacion, caracteres vacios y "palabras vacias" de los poemas
#Y nos regresa un arreglo de con la palabras restantes
def tokenize_poem(poem):
    poem = poem.lower().replace('\n', ' ')
    for sign in punctuation:
        poem = poem.replace(sign, '')
    tokens = poem.split()
    tokens = [t for t in tokens if t not in stopwords and t != '']
    return tokens

#Metodo para obetner los GLOval VEctors o (glove), como un diccionario donde la palabra es
#la key y el vector el value
def getGlove():
    return {w: x for w, x in gimme_glove()}

#Metodo de ayuda que obtiene los vectores del archivo glove.6b.50d.txt
def gimme_glove():
    with open('glove.6B.300d.txt') as glove_raw:
        for line in glove_raw.readlines():
            splitted = line.split(' ')
            yield splitted[0], np.array(splitted[1:], dtype=np.float)
            

#Guardamos todos los poemas en un arreglo
all_poems = [poems_poet0, poems_poet1, poems_poet2]
#Guardamos los titulso en un arreglo de cadenas (Lo usaremos para graficar)
titles = np.concatenate([list(title_list.keys()) for title_list in all_poems])
#Guardamos para cada uno de poemas a cual poeta la pertenecen 0,1,3 (Lo usaremos para graficar)
y = np.concatenate([[i]*len(p) for i, p in enumerate(all_poems)])
#Obtenemos el texto de los poemas y los guardamos todos en un arreglo
#Esta arreglo es el que procesaremos
all_poems = np.concatenate([list(p.values()) for p in all_poems])


#Para cada uno de los poemas nos quedamos unicamente con las palabras "relevantes" es decir le aplciamos
#el metodo tokenized_poems
tokenized_poems = [tokenize_poem(poem) for poem in all_poems]

#Obtenemos el diccionar de los GLOval VEctors para las palabras
glove = getGlove()

#Metodo que dado un arreglo de palabras, filtra unicamente las palabras unicas
#del arreglo y  obtiene los vectos Glove para cada una de las palabras
#de todos los vectores obtenidops calcular el promedio para quedanos con 
#un unico vector representativo del poema
def poem_to_vec(tokens):
    words = [w for w in np.unique(tokens) if w in glove]
    return np.array([glove[w] for w in words]).mean(axis=0)


#Convetirmos nuestro arreglo de pomeas tokenizados en un arreglo
#De poemas vectorizados
poemsVector = [poem_to_vec(tokenized) for tokenized in tokenized_poems]

#Convertimos el arreglo en un arreglo de numpy
poemsVector = np.array(poemsVector)


#Definmos el tama;o del grid al que mapeare minisom
map_dim = 16
#Definimos el tama;o de entrada de los vectores
tamEntrada = 300
#Definimos la funcion de minisom
som = MiniSom(map_dim, map_dim, tamEntrada, sigma=1.0, random_seed=1)
#som.random_weights_init(poemsVector)
#Entrenamos la red neuronal con W que es el el arreglo de los revectores que 
#representan los poemas
som.train_batch(poemsVector, num_iteration=len(poemsVector)*500, verbose=True)


#Por ultimo vamos a graficar el resultado del SOM
author_to_color = {0: 'yellow',
                   1: 'blue',
                   2: 'red'}
color = [author_to_color[yy] for yy in y]

plt.figure(figsize=(14, 14))
#Para cada uno de los peomas (represtancion en vectores) lo emetamos con su titulo y el color
#Que le toca por su respectivo author para poder graficarlos
for i, (t, c, vec) in enumerate(zip(titles, color, poemsVector)):

    #Para cada uno los vectores (representacion vectorial del peoma) obtenemos el nodo
    #Al que se le fue aginado con SOM
    winnin_position = som.winner(vec)
    #Genramos el texto y lo graficamos en la posicion y color correspondiente
    #El random es para moverlo un poco del nodo asignado ya que si no muchos se encimarian en la misma posicion
    #Es decir es para una mejorar visualizacion
    plt.text(winnin_position[0], 
             winnin_position[1]+np.random.rand()*.9, 
             t,
             color=c)

plt.xticks(range(map_dim))
plt.yticks(range(map_dim))
plt.grid()
plt.xlim([0, map_dim])
plt.ylim([0, map_dim])
plt.plot()
plt.show()


import pdb; pdb.set_trace()

