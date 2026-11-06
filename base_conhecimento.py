import json

import orientacao
from orientacao import Orientacao

ACENTOS = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e",
           "í": "i", "ó": "o", "õ": "o", "ô": "o", "ú": "u", "ç": "c"}

def normalizar(texto):
    texto = texto.lower().strip()
    for letra, troca in ACENTOS.items():
        texto = texto.replace(letra, troca)
    for sinal, in "?!.,;:()/-":
        texto = texto.replace(sinal, "")
    return " " + " ".join(texto.split()) + " "

class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.orientacoes = [Orientacao(**item) for item in dados]
            return True
        except FileNotFoundError:
            print("Base de conhecimento não encontrada.")
        except (json.JSONDecodeError, TypeError):
            print("Base de conhecimento corrompida ou com campos faltando.")
        self.orientacoes = []
        return False

    def categorias(self):
        lista = []
        for o in self.orientacoes:
            if o.categoria not in lista:
                lista.append(o.categoria)
        return lista

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, orientacao, pergunta):
        pontos = 0
        for palavra_chave in orientacao.palavras_chave:
            if normalizar(palavra_chave) in pergunta:
                pontos += 3
        titulo = normalizar(orientacao.titulo)
        for palavra in set(pergunta.split()):
            if len(palavra) >= 4 and f" {palavra} " in titulo:
                pontos += 1
        return pontos

    def buscar(self, texto):
        pergunta = normalizar(texto)
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(orientacao, pergunta)
            if pontos:
                resultados.append((pontos, orientacao))
        resultados.sort(key=lambda t: t[0], reverse=True)
        return resultados