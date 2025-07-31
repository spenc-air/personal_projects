import random

def crear_dicionario(contenido): # crea un dicionario para saber palabras siguientes 
    dicionario = {} # aqui es donde lo crea
    anterior = ""
    for palabra in contenido: # paso por todas las palabras en el archivo con un bucle
        if not anterior in dicionario:
            dicionario[anterior] = [palabra]
        else:
            dicionario[anterior].append(palabra)
        anterior = palabra
    return dicionario

def escribir(texto): # pone el texto en otro archivo
    with open("resultados.txt", 'w') as archivo:
        archivo.write(texto)

def generar_texto(archivo_para_abrir, primera_palabra, num_de_palabras):
    with open(archivo_para_abrir, 'r') as archivo: # abrir archivo
        contenido = archivo.read()
    # print(contenido) # imprime en el terminal
    dicionario = crear_dicionario(contenido.split())
    # print(dicionario)
    palabra = primera_palabra
    lista_de_texto = [primera_palabra] # vamos a agregar el texto generado a esta lista
    for _ in range(num_de_palabras): # este bucle dice cuantas veces debes hacer la acción
        # palabra = dicionario[palabra][0] # escegemos la primera cosa en la lista
        palabra = random.choice(dicionario[palabra]) # escogemos una cosa random de la lista
        lista_de_texto.append(palabra)
    texto = " ".join(lista_de_texto)
    # print(texto)
    escribir(texto)

def funcion_principal():
    generar_texto("1_Nefi_1.txt", "Yo,", 30)
    # generar_texto("cultura_de_ecuador.txt", "La", 30)
    # generar_texto("Abraham_Lincoln.txt", "Abraham", 30)

if __name__ == '__main__':
    funcion_principal()