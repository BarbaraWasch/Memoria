from tkinter import Tk, Label, Frame, Button, NSEW, Scale, messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import tkinter as tk
import pygame
import random

# Definindo as cores
HotPink = "#FF69B4"  # Rosa choque
LightPink = "#FFB6C1"  # Rosa envelhecido 
Pink = "#FFC0CB"  # Rosa
Violet = "#EE82EE"  # Violeta
Black = "#000000"  # Preto
White = "#F5FFFA"  # Branco

# Definindo as configurações de jogo
NumLinhas = 4
NumColunas = 4
CartaoSizeW = 135
CartaoSizeH = 145
FontStyle = ('Arial', 12, 'bold')
TentativasMax = 25

# Criar a janela
janela = Tk()
janela.title("Mini game")
janela.geometry('700x700')
janela.configure(background=Pink)
janela.resizable(width=False, height=False)

# Criar frame inicial
frameInicial = Frame(janela, width=700, height=700, bg=Pink)  
frameInicial.grid(row=0, column=0, pady=0, padx=0, sticky=NSEW)

# Carregar e redimensionar a imagem de fundo
imgBackground = Image.open('background.png').resize((700, 700))
imgBackground = ImageTk.PhotoImage(imgBackground)

# Carregar e redimensionar a imagem de verso do card
imgCard = Image.open('cartaverso.png').resize((135, 145))
imgCard = ImageTk.PhotoImage(imgCard)

# Carregar e redimensionar a imagem do botão start
imgBotao = Image.open('botao.png').resize((150, 50))
imgBotao = ImageTk.PhotoImage(imgBotao)

# Criar um Label para a imagem de fundo e posicioná-lo
backgroundLabel = Label(frameInicial, image=imgBackground, bg=Pink)
backgroundLabel.place(x=0, y=0)  

# Criar um Label para o texto e posicioná-lo
lEstado = Label(frameInicial, text='Jogo da Memória', font=('Comic Sans MS', 25), fg=HotPink, bg=Pink)
lEstado.place(x=220, y=300)

# Manter a referência da imagem para evitar que seja coletada pelo garbage collector
backgroundLabel.image = imgBackground

# Estilizar o botão
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 16), padding=10)

# Criar o botão para iniciar o jogo
btnIniciar = tk.Button(janela, command=lambda: SegundaTela(frameInicial), image=imgBotao)
btnIniciar.place(x=272, y=440, width=150, height=40)

# Adicionar controle de volume
volume_label = tk.Label(janela, text="Volume", font=('Comic Sans MS', 15), fg=HotPink, bg=Pink)
volume_label.place(x=320, y=520)
volume_slider = tk.Scale(janela, from_=0, to=100, orient='horizontal', length=200, command=lambda volume: pygame.mixer.music.set_volume(float(volume) / 100))
volume_slider.set(50)  # Defina o valor inicial do volume para 50%
volume_slider.place(x=250, y=550)

# Carregar e redimensionar a imagem dos pokemons
imgCaterpie = Image.open('caterpie.png').resize((135, 145))
imgCaterpie = ImageTk.PhotoImage(imgCaterpie)

imgCharmander = Image.open('charmander.png').resize((135, 145))
imgCharmander = ImageTk.PhotoImage(imgCharmander)

imgMagikarp = Image.open('magikarp.png').resize((135, 145))
imgMagikarp = ImageTk.PhotoImage(imgMagikarp)

imgMew = Image.open('mew.png').resize((135, 145))
imgMew = ImageTk.PhotoImage(imgMew)

imgPikachu = Image.open('pikachu.png').resize((135, 145))
imgPikachu = ImageTk.PhotoImage(imgPikachu)

imgPsyduck = Image.open('psyduck.png').resize((135, 145))
imgPsyduck = ImageTk.PhotoImage(imgPsyduck)

imgSquirtle = Image.open('squirtle.png').resize((135, 145))
imgSquirtle = ImageTk.PhotoImage(imgSquirtle)

imgSrolax = Image.open('srolax.png').resize((135, 145))
imgSrolax = ImageTk.PhotoImage(imgSrolax)

PokemonCards = [imgCaterpie, imgCharmander, imgMagikarp, imgMew, imgPikachu, imgPsyduck, imgSquirtle, imgSrolax]

# Iniciar a música
def iniciarMusica(volume):
    pygame.mixer.init()
    pygame.mixer.music.load("Song.mp3")
    pygame.mixer.music.set_volume(volume / 100)  # Convertendo para intervalo de 0 a 1
    pygame.mixer.music.play(-1)

# Inicializa o mixer do pygame
pygame.mixer.init()

def createCardGrid():
    cards = PokemonCards * 2
    random.shuffle(cards)
    grid = []

    for _ in range(NumLinhas):
        linha = []
        for _ in range(NumColunas):
            carta = cards.pop()
            linha.append(carta)
        grid.append(linha)
    return grid

# Criar grade de cartões
grid = createCardGrid()
cartoes = []
cartaoRevelado = []
cartaoCorrespondentes = []
numeroTentativas = 0

# Lidar com clique do jogador em cartão
def card_clicked(linha, coluna):
    cartao = cartoes[linha][coluna]
    cor = cartao['bg']
    if cor == PokemonCards:
        cartao['bg'] = grid[linha][coluna]
        cartaoRevelado.append(cartao)
        if len(cartaoRevelado) == 2:
            checkMatch()

# Verificar se os dois cartões revelados são iguais
def checkMatch():
    global cartaoRevelado
    cartao1, cartao2 = cartaoRevelado
    if cartao1['bg'] == cartao2['bg']:
        cartao1.after(1000, cartao1.destroy)
        cartao2.after(1000, cartao2.destroy)
        cartaoCorrespondentes.extend([cartao1, cartao2])
        checkWin()
    else:
        cartao1.after(1000, lambda: cartao1.configure(bg='black'))
        cartao2.after(1000, lambda: cartao2.configure(bg='black'))
    cartaoRevelado.clear()
    updateScore()

# Vou fazer uma tela de ganhador no lugar dessa
def checkWin():
    if len(cartaoCorrespondentes) == NumLinhas * NumColunas:
        messagebox.showinfo('Parabéns', 'Você ganhou o jogo!')
        janela.quit()

# Atualizar a pontuação e verificar se o jogador perdeu o jogo
def updateScore():
    global numeroTentativas
    numeroTentativas += 1
    labelTentativas.config(text='Tentativas: {}/{}'.format(numeroTentativas, TentativasMax))
    if numeroTentativas >= TentativasMax:
        messagebox.showinfo('Fim de jogo', 'Você perdeu o jogo!')
        janela.quit()

def SegundaTela(frame):
    frame.destroy()
    segundaTela = tk.Toplevel(janela)
    segundaTela.title("Segunda Tela")
    segundaTela.geometry("700x700")
    
    # Carregar e redimensionar a imagem de fundo
    imgBackground = Image.open('background.png').resize((700, 700))
    imgBackground = ImageTk.PhotoImage(imgBackground)
    
    # Criar um Label para a imagem de fundo e posicioná-lo
    backgroundLabel = tk.Label(segundaTela, image=imgBackground, bg="pink")
    backgroundLabel.place(x=0, y=0)  
    
    # Manter a referência da imagem 
    backgroundLabel.image = imgBackground
    
    # Criar a grade de cartões
    grid = createCardGrid()
    
    # Iterar sobre a grade e criar botões para cada carta
    global cartoes
    cartoes = []
    for linha in range(NumLinhas):
        linhaCartoes = []
        for coluna in range(NumColunas):
            carta = tk.Button(segundaTela, command=lambda r=linha, c=coluna: card_clicked(r, c), width=CartaoSizeW, height=CartaoSizeH, bg=Pink, relief=tk.RAISED, bd=3, image=imgCard)
            carta.grid(row=linha, column=coluna, padx=13, pady=12)
            linhaCartoes.append(carta)
        cartoes.append(linhaCartoes)

# Label para número de tentativas
labelTentativas = tk.Label(janela, text='Tentativas {}/{}'.format(9, TentativasMax), fg=Pink, bg=HotPink, font=FontStyle)
labelTentativas.grid(row=NumLinhas, columnspan=NumColunas, padx=10, pady=10)

# Iniciar o loop principal da janela
janela.mainloop()
