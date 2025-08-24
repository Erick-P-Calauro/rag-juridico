from controllers.setup import setup
from controllers.manage_input import manage_input

MENSAGEM = "[1] - PERGUNTAR\n[0] - Sair\nEscolha: "

model, vector_store = setup()

escolha_usuario = input(MENSAGEM)
while escolha_usuario != "0":
    entrada = input("Entrada : \n")

    saida = manage_input(model, vector_store, entrada)
    print("Resposta : \n" + saida)

    escolha_usuario = input(MENSAGEM)