# Citizen Assist AI

Assistente de terminal feito em Python que responde dúvidas de pessoas idosas sobre saúde, transporte, aposentadoria e benefícios, e golpes. Ele só responde com o que está na base de conhecimento, que tem fonte oficial e data de verificação em cada orientação. Trabalho da Global Solution 2026.2 (Pensamento Computacional e Automação com Python), FIAP.

## Integrantes

| Nome | RM |
|------|----|
| Pedro Ribeiro Lopes | 570083|
| Luan de Araujo Carneiro | 573691 |
| Lana Namie Kano Ozeki | 569795 |

## Público e problema escolhidos

Escolhemos pessoas idosas. Muitas delas têm dificuldade para descobrir como tirar o Cartão SUS, se têm direito a ônibus de graça, o que fazer na prova de vida do INSS ou como denunciar um golpe. A informação existe, mas está espalhada em vários sites do governo, em linguagem difícil, e ainda tem muita página falsa que se passa por oficial.

A ideia do assistente é juntar o essencial em respostas curtas, dizer onde ir e o que levar, e mostrar de onde veio cada informação. Ele nunca pede nome, CPF, telefone nem e-mail.

## ODS relacionados

- **ODS 3 (Saúde e Bem-Estar):** orientações sobre Cartão SUS, vacinas e remédios gratuitos.
- **ODS 10 (Redução das Desigualdades):** direitos como transporte gratuito e BPC, que ajudam quem tem menos renda.
- **ODS 16 (Paz, Justiça e Instituições Eficazes):** como denunciar violência contra a pessoa idosa e se proteger de golpes.

## Como executar

Precisa de Python 3 instalado. Não usa nenhuma biblioteca externa.

```
python main.py
```

O programa abre um menu com as opções de fazer uma pergunta, navegar por categorias, ver os indicadores, exportar o CSV e sair. Em qualquer tela, o `0` volta.

## Estrutura do projeto

```
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

- `orientacao.py`: classe `Orientacao`, que guarda os dados de uma orientação e mostra ela na tela com `exibir()`.
- `base_conhecimento.py`: classe `BaseConhecimento`, que lê o JSON, lista as categorias e faz a busca com pontuação. A função `normalizar()` também fica aqui.
- `assistente.py`: classe `Assistente`, que faz o atendimento, guarda o histórico, calcula os indicadores e exporta o CSV.
- `main.py`: monta tudo e mostra o menu.

O `Assistente` tem uma `BaseConhecimento`, e ela tem uma lista de objetos `Orientacao` (composição).

## Regra de pontuação

A pergunta, as palavras-chave e o título são normalizados antes de comparar: tudo em minúsculas, sem acento e sem pontuação (`? ! . , ; : ( ) / -`).

| Regra | Pontos |
|-------|--------|
| Palavra-chave da orientação que aparece na pergunta | +3 |
| Palavra da pergunta (4 letras ou mais) que aparece no título | +1 |

A confiança depende da melhor pontuação:

- 6 pontos ou mais: confiança **ALTA**
- de 3 a 5 pontos: confiança **MÉDIA**
- menos de 3 pontos: "Não encontrei", com sugestão de usar outras palavras ou ver as categorias

O método `buscar()` devolve uma lista de tuplas `(pontos, orientacao)` da maior para a menor pontuação. O assistente mostra a melhor e até duas alternativas.

Exemplo: em "Como faço o cartão do SUS?", a orientação do Cartão SUS recebe +3 por "cartao do sus", +3 por "sus" e +1 porque "cartao" está no título, total de 7 pontos (ALTA).

Mudamos só um detalhe do que o enunciado sugeria: acrescentamos `/` e `-` na lista de sinais removidos, para "BPC/LOAS" e "maus-tratos" virarem palavras separadas.

## Fontes consultadas

A base tem 10 orientações em 4 categorias (Saúde, Transporte, Previdência e benefícios, Proteção e segurança). Todas foram conferidas por nós em 2026-11-05. As fontes de cada uma estão no campo `fonte` do arquivo `data/base_conhecimento.json`:

| Orientação | Fonte |
|------------|-------|
| 1. Cartão SUS | https://www.serasa.com.br/blog/cartao-sus-como-conseguir/ |
| 2. Vacinas para quem tem 60 anos ou mais | https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/s/saude-da-pessoa-idosa/vacinacao-da-pessoa-idosa |
| 3. Farmácia Popular | https://www.gov.br/saude/pt-br/composicao/sectics/farmacia-popular |
| 4. Ônibus urbano gratuito | https://www.planalto.gov.br/ccivil_03/leis/2003/l10.741.htm |
| 5. Carteira da Pessoa Idosa (viagem interestadual) | https://www.gov.br/pt-br/servicos/adquirir-carteira-do-idoso ou CRAS da sua cidade |
| 6. Aposentadoria por idade | https://www.gov.br/pt-br/servicos/solicitar-aposentadoria-por-idade-trabalhador-urbano |
| 7. Prova de vida do INSS | https://www.gov.br/governodigital/pt-br/identidade/prova-de-vida |
| 8. BPC/LOAS | https://www.gov.br/pt-br/servicos/solicitar-beneficio-assistencial-ao-idoso |
| 9. Disque 100 | https://sp156.prefeitura.sp.gov.br/portal/servicos/informacao?servico=787 |
| 10. Golpes contra aposentados | https://www.gov.br/inss/pt-br/assuntos/noticias/inss-alerta-aposentados-sao-vitimas-de-golpe-envolvendo-falsa-prova-de-vida |

## Resultado do teste com usuários

Testamos o assistente com 3 pessoas de fora da equipe, somando 10 atendimentos. Não registramos nomes nem dados pessoais de ninguém. Os números abaixo vêm do próprio programa (opção 3 do menu).

| Indicador | Resultado |
|-----------|-----------|
| Atendimentos | 14 |
| Resposta encontrada | 92,9% |
| Taxa de acerto (ajudou) | 92,9% |
| Tempo médio para encontrar | 34,1 s |
| Tentativas por atendimento | 1,0 |
| Facilidade de uso (1 a 5) | 5,0 |

**Dúvida sem solução:** "tem como fazer exames gratuitos?". A base não tem nenhuma orientação sobre exames.

**O que observamos:** durante o teste, uma pessoa digitou a dúvida direto no menu principal, em vez de escolher a opção 1, e só viu "Opção inválida". Ela não sabia que a dúvida era digitada em outra tela.

**Melhoria feita a partir do teste:** colocamos uma dica com dois exemplos de pergunta na tela de dúvida ("como pego remédio de graça?" e "tenho direito a ônibus grátis?"), para quem não sabe o que escrever. Isso ajuda, mas não resolve por completo o caso de quem digita no menu.

## Limitações

- A busca compara palavras exatas. Ela não entende sinônimos nem erros de digitação, então "carteirinha" não é a mesma coisa que "carteira" para o programa.
- Palavras comuns como "para" têm 4 letras e podem dar +1 ponto no título sem ter relação com o assunto.
- A base tem só 10 orientações. Dúvidas fora dela, como exames gratuitos, não são respondidas.
- As informações foram conferidas em 2026-11-05 e podem mudar. Para decidir qualquer coisa importante, a pessoa deve confirmar no site ou no telefone oficial.
- Algumas regras variam de cidade para cidade, como o ônibus gratuito a partir dos 60 anos. O assistente só avisa que isso pode acontecer.
- O menu só aceita números. Quem digita uma dúvida no menu recebe "Opção inválida".
- O bloqueio de dados pessoais recusa perguntas com 8 ou mais dígitos ou com `@`. Ele não identifica nomes escritos no texto.
- O teste foi pequeno (10 atendimentos). Os tempos incluem o tempo de leitura de quem estava usando, então não representam bem uma pessoa idosa de verdade.
- O assistente não é um canal oficial. Isso aparece em toda resposta.

## Vídeo técnico

[PREENCHER: link do YouTube, não listado]
