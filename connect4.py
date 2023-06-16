import numpy as np
import math
import random


NUMERO_COLUNAS = 7
NUMERO_LINHAS = 6


JOGADOR = 0
IA = 1

VAZIO = 0
PECA_JOGADOR = 1
PECA_IA = 2

TAMANHO_JANELA = 4


def cria_board():
    board = np.zeros((NUMERO_LINHAS, NUMERO_COLUNAS))
    return board


def eh_valido(board, coluna):
    return board[NUMERO_LINHAS-1][coluna] == 0

def solta_peca(board, linha, coluna, peca):
    board[linha][coluna] = peca

def imprime_board(board):
    print(np.flip(board, 0))

def proxima_linha(board, coluna):
    for l in range(NUMERO_LINHAS):
        if board[l][coluna] == 0:
            return l

def verifica_vitoria(board, peca):

    for c in range(NUMERO_COLUNAS):
        for l in range(NUMERO_LINHAS-3):
            if board[l][c] == peca and board[l+1][c] == peca and board[l+2][c] == peca and board[l+3][c] == peca:
                return True
 
    for c in range(NUMERO_COLUNAS-3):
        for l in range(NUMERO_LINHAS):
            if board[l][c] == peca and board[l][c+1] == peca and board[l][c+2] == peca and board[l][c+3] == peca:
                return True


    for c in range(NUMERO_COLUNAS-3):
        for l in range(NUMERO_LINHAS-3):
            if board[l][c] == peca and board[l+1][c+1] == peca and board[l+2][c+2] == peca and board[l+3][c+3] == peca:
                return True


    for c in range(NUMERO_COLUNAS-3):
        for l in range(3, NUMERO_LINHAS):
            if board[l][c] == peca and board[l-1][c+1] == peca and board[l-2][c+2] == peca and board[l-3][c+3] == peca:
                return True


def avalia_janela(janela, peca):
    score = 0
    oponente = PECA_JOGADOR
    if peca == PECA_JOGADOR:
        oponente = PECA_IA

    if janela.count(peca) == 4:
        score += 200
    elif janela.count(peca) == 3 and janela.count(VAZIO) == 1:
        score += 10
    elif janela.count(peca) == 2 and janela.count(VAZIO) == 2:
        score += 5

    if janela.count(oponente) == 3 and janela.count(VAZIO) == 1:
        score -= 8

    return score


def posicao(board, peca):
    score = 0

    centro = [int(i) for i in list(board[:, NUMERO_COLUNAS //2])]
    conta_centro = centro.count(peca)
    score += conta_centro * 3


    for l in range(NUMERO_LINHAS):
        array_linha = [int(i) for i in list(board[l, :])]
        for c in range(NUMERO_COLUNAS-3):
            janela = array_linha[c:c+TAMANHO_JANELA]
            score += avalia_janela(janela, peca)


    for c in range(NUMERO_COLUNAS):
        array_coluna = [int(i) for i in list(board[:, c])]
        for l in range(NUMERO_LINHAS-3):
            janela = array_coluna[l:l+TAMANHO_JANELA]
            score += avalia_janela(janela, peca)


    for l in range(NUMERO_LINHAS-3):
        for c in range(NUMERO_COLUNAS-3):
            janela = [board[l+i][c+i] for i in range(TAMANHO_JANELA)]
            score += avalia_janela(janela, peca)

    for l in range(NUMERO_LINHAS-3):
        for c in range(NUMERO_COLUNAS-3):
            janela = [board[l+3-i][c+i] for i in range(TAMANHO_JANELA)]
            score += avalia_janela(janela, peca)

    return score


def fim_jogo(board):
    return verifica_vitoria(board, PECA_JOGADOR) or verifica_vitoria(board, PECA_IA) or len(pega_jogadas_validas(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    jogadas_validas = pega_jogadas_validas(board)
    final = fim_jogo(board)
    if depth == 0 or final:
        if final:
            if verifica_vitoria(board, PECA_IA):
                return (None, 1000)
            elif verifica_vitoria(board, PECA_JOGADOR):
                return (None, -1000)
            else: 
                return (None, 0)
        else:  
            return (None, posicao(board, PECA_IA))
    if maximizingPlayer:
        valor = -math.inf
        col = random.choice(jogadas_validas)
        for coluna in jogadas_validas:
            linha = proxima_linha(board, coluna)
            b_copy = board.copy()
            solta_peca(b_copy, linha, coluna, PECA_IA)
            novo_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if novo_score > valor:
                valor = novo_score
                col = coluna
            alpha = max(alpha, valor)
            if alpha >= beta:
                break
        return col, valor

    else:  
        valor = math.inf
        col = random.choice(jogadas_validas)
        for coluna in jogadas_validas:
            linha = proxima_linha(board, coluna)
            b_copy = board.copy()
            solta_peca(b_copy, linha, coluna, PECA_JOGADOR)
            novo_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if novo_score < valor:
                valor = novo_score
                col = coluna
            beta = min(beta, valor)
            if alpha >= beta:
                break
        return col, valor


def pega_jogadas_validas(board):
    jogadas_validas = []
    for coluna in range(NUMERO_COLUNAS):
        if eh_valido(board, coluna):
            jogadas_validas.append(coluna)
    return jogadas_validas


def pega_melhor_jogada(board, peca):

    jogadas_validas = pega_jogadas_validas(board)
    best_score = -10
    best_col = random.choice(jogadas_validas)
    for coluna in jogadas_validas:
        linha = proxima_linha(board, coluna)
        temp_board = board.copy()
        solta_peca(temp_board, linha, coluna, peca)
        score = posicao(temp_board, peca)
        if score > best_score:
            best_score = score
            best_col = coluna

    return best_col


board = cria_board()
imprime_board(board)
game_over = False

print("-----------------")


turno = JOGADOR

while not game_over:

    if (turno == JOGADOR):
        coluna = int(input("digite a coluna:"))
        if eh_valido(board, coluna):
            linha = proxima_linha(board, coluna)
            solta_peca(board, linha, coluna, PECA_JOGADOR)

            if verifica_vitoria(board, PECA_JOGADOR):
                print("Jogador 1 Ganhou!!")
                game_over = True

            turno += 1
            turno = turno % 2

            imprime_board(board)
            print("-----------------")
    if (turno == IA):				

        coluna, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if eh_valido(board, coluna):
            linha = proxima_linha(board, coluna)
            solta_peca(board, linha, coluna, PECA_IA)
            if verifica_vitoria(board, PECA_IA):
                print("Jogador 2 Ganhou!!")
                game_over = True

            imprime_board(board)
            print("-----------------")

            turno += 1
            turno = turno % 2