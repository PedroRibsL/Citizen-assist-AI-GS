class Orientacao:
    def __init__(self, id, categoria, titulo, palavras_chave, resposta, documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        print(f">>{self.titulo} [{self.categoria}]")
        print(self.resposta)
        print("Documentos necessários:")
        for documento in self.documentos:
            print(f" - {documento}")
        print(f"Onde: {self.onde}")
        print(f"Fonte: {self.fonte}")
        print(f"Verificado: {self.verificado_em}")
        print("Aviso: esse assistente NÃO é um canal oficial.")