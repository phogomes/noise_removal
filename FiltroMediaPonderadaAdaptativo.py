'''
Esse eh o trabalho de uma disciplina, no qual o objetico eh implementar
o metodo proposto no seguinte artigo:
"A New Adaptive Weighted Mean Filter for Removing Salt-and-Pepper Noise"
autores: Peixuan Zhang and Fang Li
publicado em: IEEE SIGNAL PROCESSING LETTERS


Autor do codigo: Paulo Henrique de Oliveira Gomes
email: phdeoliveiragomes@gmail.com 
'''
import numpy as np
import cv2
import math
import copy

def principal():
    #variaveis auxiliares
    max_janela = 39.0
    
    teto = math.ceil(max_janela/2.0)
    piso = math.floor(max_janela/2.0)
    teto = int(teto)
    piso = int(piso)
    max_janela = int(max_janela)
    
    #realiza leitura da imagem ruidosa, seleciona apenas um canal 
    #replica as bordas da imagem ruidosa e copia para outra variavel
    img_entrada = cv2.imread("Lena_noise.png")
    img = img_entrada[:,:,0]
    img = cv2.copyMakeBorder(img,piso,piso,piso,piso,cv2.BORDER_REPLICATE)
    
    img_limpa = img.copy()
    
    height, width = img.shape[:2]
    
    for i in range(teto-1, height-piso):
        for j in range(teto-1, width-piso):
            janela = img[ (i-piso):(i+piso+1), (j-piso):(j+piso+1) ]
            pixel_centro = janela[teto-1,teto-1]

            [pixel_min, pixel_max, media] = percorre_janela(janela,max_janela,3)

            for s in range(5,max_janela-2,2):
                [prox_pixel_min, prox_pixel_max, prox_media] = percorre_janela(janela,max_janela,s)
                
                if (pixel_min == prox_pixel_min) & (pixel_max == prox_pixel_max) & (media != -1):
                    if (pixel_centro <= pixel_min) | (pixel_centro >= pixel_max):
                        img_limpa[i,j] = media
                    
                    break
                pixel_min = prox_pixel_min
                pixel_max = prox_pixel_max
                media = prox_media
      
    #retira as bordas para a imagem final ter as dimensoes da imagem de entrada
    img_final = img_limpa[piso:height-piso, piso:width-piso]

    cv2.imshow("ruidosa",img_entrada)
    cv2.imshow("saida",img_final)
    cv2.imwrite("Resultado.png",img_final)
    cv2.waitKey(0) & 0xFF
    

def percorre_janela(janela,max_j,s):
    baixo = int(math.ceil(max_j/2.0)-math.floor(s/2.0))
    alto = int(math.ceil(max_j/2.0)+math.floor(s/2.0))

    lista = []
    lista_prox = []
    for i in range(baixo-1,alto):
        for j in range(baixo-1,alto):
            lista.append(janela[i,j])

    lista.sort()

    minp = lista[0]
    maxp = lista[len(lista)-1]
    quantos_a = 0
    ponderada = 0
    for i in range(len(lista)):
        if(lista[i] > minp) & (lista[i] < maxp):
            a = 1
            quantos_a = quantos_a + 1
        else:
            a = 0
        ponderada = ponderada + lista[i] * a
        
    if(quantos_a != 0):
        ponderada = ponderada / quantos_a
    else:
        ponderada = -1
        
    return lista[0], lista[len(lista)-1], ponderada

if __name__ == '__main__':
    principal()
    print("\n FIM!!")
    
