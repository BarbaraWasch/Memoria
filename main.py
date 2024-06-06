import tkinter as tk
from tkinter import messagebox
import random

# Definindo as configuração de jogo
NumLinhas = 4
NumColunas = 4
CartaoSizeW = 10
CartaoSizeH = 5
CoresCartao = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']
CorFundo = "#FFC0CB"
CorLetra = '#ffffff'
FontStyle = ('Arial', 12, 'bold')
TentativasMax = 25

# Criando uma grade aleatória de cores para os cartões
def createCardGrid():
    cores = CoresCartao * 2
    random.shuffle(cores)
    grid = []

    for _ in range(NumLinhas):
        linha = []
        for _ in range(NumColunas):
            cor = cores.pop()
            linha.append(cor)
        grid.append(linha)
    return grid

# Lidar com clique do jogador em cartão
def card_clicked(linha, coluna):
    cartao = cartoes[linha][coluna]
    corCartao = cartao['bg']
    if corCartao == '#FF69B4':  # Verifica se a cor do botão é rosa choque
        cartao['bg'] = grid[linha][coluna]
        cartaoRevelado.append(cartao)
        if len(cartaoRevelado) == 2:
            checkMatch()

# Verificar se os dois cartões revelados são iguais
def checkMatch():
    cartao1, cartao2 = cartaoRevelado
    if cartao1['bg'] == cartao2['bg']:
        cartao1.after(1000, cartao1.destroy)
        cartao2.after(1000, cartao2.destroy)
        cartaoCorrespondentes.extend([cartao1, cartao2])
        checkWin()
    else:
        cartao1.after(1000, lambda: cartao1.configure(bg='#FF69B4'))  # Voltar a cor rosa choque
        cartao2.after(1000, lambda: cartao2.configure(bg='#FF69B4'))  # Voltar a cor rosa choque
    cartaoRevelado.clear()
    updateScore()

# Verificar se o jogador ganhou o jogo
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

# Criando a interface principal
janela = tk.Tk()
janela.title('Jogo de Memória')
janela.configure(bg=CorFundo)

# Criar grade de cartões
grid = createCardGrid()
cartoes = []
cartaoRevelado = []
cartaoCorrespondentes = []
numeroTentativas = 0

for linha in range(NumLinhas):
    linhaDeCartoes = []
    for col in range(NumColunas):
        cartao = tk.Button(janela, command=lambda r=linha, c=col: card_clicked(r, c), width=CartaoSizeW, height=CartaoSizeH, bg="#FF69B4", relief=tk.RAISED, bd=3)
        cartao.grid(row=linha, column=col, padx=5, pady=5)
        linhaDeCartoes.append(cartao)
    cartoes.append(linhaDeCartoes)

# Personalizando o botão
buttonStyle = {'activebackground': '#f8f9fa', 'font': FontStyle, 'fg': CorLetra}
janela.option_add('*Button', buttonStyle)

# Label para número de tentativas
labelTentativas = tk.Label(janela, text='Tentativas: {}/{}'.format(numeroTentativas, TentativasMax), fg="#FF69B4", bg=CorFundo, font=FontStyle)
labelTentativas.grid(row=NumLinhas, columnspan=NumColunas, padx=10, pady=10)

janela.mainloop()
