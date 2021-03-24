'''
Videos de referencia: https://www.youtube.com/watch?v=8yOMflB0AZU
https://www.youtube.com/watch?v=k6Bg_kOZn2M

Referencia FFMPEG
https://trac.ffmpeg.org/wiki/Debug/MacroblocksAndMotionVectors
'''

import os
import glob
import subprocess
import sys

video = 'bola.mp4'

#Salva todos os frames do video em um arquivo
def divideFrames(video):
    os.system('ffmpeg -i Videos/'+video+' Frames/Todos/frame%03d-'+video+'.jpg')

#Divide o video em frames I, B e P
def divideFramesIBP(video):
    #Pegando os frames I
    os.system('ffmpeg -i Videos/'+video+' -vf "select=\'eq(pict_type\,I)" -vsync 0 -frame_pts 1 Frames/Keyframes/I-frame-%02d-'+video+'.jpg')
    #Pegando os frames B
    os.system('ffmpeg -i Videos/'+video+' -vf "select=\'eq(pict_type\,B)" -vsync 0 -frame_pts 1 Frames/Keyframes/B-frame-%02d-'+video+'.jpg')
    #Pegando os frames P
    os.system('ffmpeg -i Videos/'+video+' -vf "select=\'eq(pict_type\,P)" -vsync 0 -frame_pts 1 Frames/Keyframes/P-frame-%02d-'+video+'.jpg')

#Cria um video mostrando o vetor de movimento de cada frame
def vetorMovimento(video):
    currentDir = os.getcwd()
    os.chdir('ffmpeg-3.1.11')
    os.system('./ffmpeg -flags2 +export_mvs -i ../Videos/'+video+' -vf codecview=mv=pf+bf+bb ../Videos/'+video+'-vetorMovimento.mp4')
    os.chdir(currentDir)

#Cria um video mostrando os macroblocos de cada frame
def macroblocos(video):
    currentDir = os.getcwd()
    os.chdir('ffmpeg-3.1.11')
    os.system('./ffmpeg -debug vis_mb_type -i ../Videos/'+video+' ../Videos/'+video+'-macroblocos.mp4')
    os.chdir(currentDir)

#Imprimindo quantos frames foram criados de cada
'''
divideFrames(video)
divideFramesIBP(video)
total = len(glob.glob1('Frames/Todos',"frame*"))
totalI = len(glob.glob1('Frames/Keyframes',"I-*"))
totalB = len(glob.glob1('Frames/Keyframes',"B-*"))
totalP = len(glob.glob1('Frames/Keyframes',"P-*"))
print("Total de frames: ", str(total))
print("Total de frames I: ", str(totalI))
print("Total de frames B: ", str(totalB))
print("Total de frames P: ", str(totalP))
'''

#Ordem de execucao de frames
'''
lista = subprocess.check_output('ffprobe -select_streams v -show_frames -show_entries frame=pict_type -of csv Videos/'+video, shell=True).decode(sys.stdout.encoding)
lista = lista.replace(","," ")
execucao = []
c = 0
temp = ""
for char in lista:
    if(c < 7):
        temp += char
        c += 1
    else:
        execucao.append(temp)
        temp = ""
        c = 0
print (execucao)
'''

#Criando video mostrando os vetores de movimentos
vetorMovimento(video)

#Criando video mostrando os macroblocos
#macroblocos(video)