#imports
import random
import sqlite3

#inicio do game
def jogo_de_advinhacao():
    numero_secreto = random.randint(1, 100)
    chances = 10
    chance_atual = 1
#inserir username
    jogador = (input('Bem-vindo ao nosso jogo, qual seu nome?   ')) 
#tela de boas vindas
    print("Ola", jogador, "Voce tem 10 chances para acertar um numero secreto de 1 a 100, boa sorte. ")
    while chance_atual <= chances:
        print("\nChance", chance_atual)
        tentativa = int(input("Qual seu palpite? "))
#tentativa correta
        if tentativa == numero_secreto:
            print("\nParabens", jogador ,'voce acertou na tentativa numero', chance_atual ,'o numero secreto e', numero_secreto)
            break
#tentativas_incorreta_menor
        elif tentativa < numero_secreto:
            print("Um pouco maior, tente novamente, restam", chances - chance_atual, 'tentativas.')
#tentativa_correta_maior
        else:
            print("Um pouco menor, tente novamente, restam", chances - chance_atual, 'tentativas.')
        chance_atual += 1
#fim das tentativas
    if chance_atual > chances:
        print("Suas tentativas infelizmente acabaram, o numero secreto e", numero_secreto)
jogo_de_advinhacao()