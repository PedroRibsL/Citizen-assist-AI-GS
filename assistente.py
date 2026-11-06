import csv
import json
import time
from datetime import datetime

CAMPOS = ["data", "origem", "pergunta", "id_orientacao",
          "encontrou", "ajudou", "tentativas", "tempo", "nota"]


def tem_dado_pessoal(texto):
    digitos = sum(1 for c in texto if c.isdigit())
    return digitos >= 8 or "@" in texto


class Assistente:
    def __init__(self, nome, base, caminho_historico="data/historico.json"):
        self.nome = nome
        self.base = base
        self.caminho_historico = caminho_historico
        self.historico = []
        self.carregar_historico()
        self.inicio_sessao = len(self.historico)

    def carregar_historico(self):
        try:
            with open(self.caminho_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            self.historico = dados if isinstance(dados, list) else []
        except FileNotFoundError:
            self.historico = []
        except json.JSONDecodeError:
            print("Histórico corrompido. Começando um novo.")
            self.historico = []

    def salvar_historico(self):
        with open(self.caminho_historico, "w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=2)

    def ler_sn(self, mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "n"):
                return resposta == "s"
            print("Resposta inválida. Digite s ou n.")

    def ler_opcao(self, mensagem, maximo):
        while True:
            resposta = input(mensagem).strip()
            if resposta.isdecimal() and 0 <= int(resposta) <= maximo:
                return int(resposta)
            print(f"Opção inválida. Digite um número de 0 a {maximo}.")

    def ler_nota(self):
        while True:
            resposta = input("De 1 a 5, quão fácil foi usar o assistente? ").strip()
            if resposta.isdecimal() and 1 <= int(resposta) <= 5:
                return int(resposta)
            print("Nota inválida. Digite um número de 1 a 5.")

    def registrar(self, origem, pergunta, id_orientacao, encontrou,
                  ajudou, tentativas, tempo, nao_encontradas=None):
        self.historico.append({
            "data": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo": tempo,
            "nota": None,
            "nao_encontradas": nao_encontradas or [],
        })
        self.salvar_historico()

    def perguntar(self):
        inicio = time.time()
        tentativas = 0
        ultima_pergunta = ""
        ultima_id = None
        encontrou = False
        ajudou = False
        nao_encontradas = []

        print('Dica: escreva sua dúvida com suas palavras. '
              'Ex.: "como pego remédio de graça?" ou "tenho direito a ônibus grátis?"')

        while True:
            texto = input("Digite sua dúvida (0 para voltar): ").strip()
            if texto == "0":
                break
            if texto == "":
                print("Você não digitou nada. Tente de novo.")
                continue
            if tem_dado_pessoal(texto):
                print("Atenção: não digite CPF, telefone ou e-mail. Reescreva.")
                continue

            tentativas += 1
            ultima_pergunta = texto
            resultados = self.base.buscar(texto)

            if not resultados or resultados[0][0] < 3:
                encontrou = False
                ajudou = False
                ultima_id = None
                nao_encontradas.append(texto)
                print("Não encontrei uma orientação para essa dúvida.")
                print("Tente outras palavras ou veja as categorias:",
                      ", ".join(self.base.categorias()))
                continue

            pontos, melhor = resultados[0]
            encontrou = True
            ultima_id = melhor.id
            confianca = "ALTA" if pontos >= 6 else "MÉDIA"
            print(f"Confiança da resposta: {confianca} ({pontos} pontos)")
            melhor.exibir()

            alternativas = [r for r in resultados[1:3] if r[0] >= 3]
            if alternativas:
                print("Veja também:")
                for _, alternativa in alternativas:
                    print(f"  - {alternativa.titulo}")

            ajudou = self.ler_sn("Essa orientação respondeu sua dúvida? (s/n): ")
            if ajudou:
                break

        if tentativas > 0:
            tempo = round(time.time() - inicio, 1)
            self.registrar("pergunta", ultima_pergunta, ultima_id,
                           encontrou, ajudou, tentativas, tempo,
                           nao_encontradas)

    def navegar(self):
        categorias = self.base.categorias()
        inicio = time.time()
        while True:
            print("\nCategorias:")
            for i, categoria in enumerate(categorias, start=1):
                print(f"  {i} - {categoria}")
            print("  0 - Voltar")
            escolha = self.ler_opcao("Escolha uma categoria: ", len(categorias))
            if escolha == 0:
                break
            categoria = categorias[escolha - 1]
            orientacoes = self.base.por_categoria(categoria)

            while True:
                print(f"\n{categoria}:")
                for i, o in enumerate(orientacoes, start=1):
                    print(f"  {i} - {o.titulo}")
                print("  0 - Voltar")
                escolha = self.ler_opcao("Escolha uma orientação: ", len(orientacoes))
                if escolha == 0:
                    break
                orientacao = orientacoes[escolha - 1]
                orientacao.exibir()
                ajudou = self.ler_sn("Essa orientação respondeu sua dúvida? (s/n): ")
                tempo = round(time.time() - inicio, 1)
                self.registrar("categoria", orientacao.titulo, orientacao.id,
                               True, ajudou, 1, tempo)
                inicio = time.time()

    def encerrar(self):
        if len(self.historico) > self.inicio_sessao:
            self.historico[-1]["nota"] = self.ler_nota()
            self.salvar_historico()

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("Ainda não há atendimentos registrados.")
            return None

        encontrados = [a for a in self.historico if a.get("encontrou")]
        ajudados = [a for a in self.historico if a.get("ajudou")]
        pct_encontrou = round(len(encontrados) / total * 100, 1)
        pct_ajudou = round(len(ajudados) / total * 100, 1)

        if encontrados:
            soma = sum(a.get("tempo", 0) for a in encontrados)
            tempo_medio = round(soma / len(encontrados), 1)
        else:
            tempo_medio = 0
        tentativas = round(sum(a.get("tentativas", 0) for a in self.historico) / total, 1)

        notas = [a["nota"] for a in self.historico if a.get("nota") is not None]
        facilidade = round(sum(notas) / len(notas), 1) if notas else None

        sem_solucao = []
        for a in self.historico:
            if not a.get("ajudou") and a["pergunta"] not in sem_solucao:
                sem_solucao.append(a["pergunta"])

        for a in self.historico:
            for pergunta in a.get("nao_encontradas", []):
                if pergunta not in sem_solucao:
                    sem_solucao.append(pergunta)

        print("\n--- Indicadores ---")
        print(f"Atendimentos: {total}")
        print(f"Resposta encontrada: {pct_encontrou}%")
        print(f"Taxa de acerto (ajudou): {pct_ajudou}%")
        print(f"Tempo médio para encontrar: {tempo_medio} s")
        print(f"Tentativas por atendimento: {tentativas}")
        print("Facilidade de uso (1 a 5):",
              facilidade if facilidade is not None else "sem nota ainda")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for pergunta in sem_solucao:
                print(f"  - {pergunta}")
        else:
            print("  nenhuma")

        return {
            "total": total,
            "encontrada_pct": pct_encontrou,
            "acerto_pct": pct_ajudou,
            "tempo_medio": tempo_medio,
            "tentativas_media": tentativas,
            "facilidade": facilidade,
            "sem_solucao": sem_solucao,
        }

    def exportar_csv(self, caminho="data/atendimentos.csv"):
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS,
                                      extrasaction="ignore")
            escritor.writeheader()
            escritor.writerows(self.historico)
        print(f"{len(self.historico)} atendimentos exportados para {caminho}")