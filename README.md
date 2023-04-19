# Crawler STJ
Esse projeto implementa um web crawler para o site [Jurisprudência STJ Website](https://scon.stj.jus.br/SCON/).

Esse bot é uma variação do crawler original do STJ que  <b>NÃO COLETA ARQUIVOS DE INTEIRO TEOR</b>

Um exemplo de input para rodar o STJ:

```json
{"date":"2021-10-05"}
```

Um exemplo de output desse bot que é salva no banco de dados está a seguir:
## Acórdão
```json
  {
        "_id" : "d0347256bfa59249249f892fcbb1630f",
        "data" : {
            "numeroProcesso" : "202101665464",
            "nomeProcesso" : "AGRG NO HC 670295 / SP",
            "nomeExtenso" : "AGRAVO REGIMENTAL NO HABEAS CORPUS",
            "uf" : "SP",
            "relator" : "MINISTRO JESUÍNO RISSATO (DESEMBARGADOR CONVOCADO DO TJDFT) (8420)",
            "orgaoJulgador" : "T5 - QUINTA TURMA",
            "dataPublicacao" : "2021-10-05",
            "dataJulgamento" : "2021-09-28",
            "ementa" : "PENAL. PROCESSO PENAL. AGRAVO REGIMENTAL NO HABEAS CORPUS. AUSÊNCIADE NOVOS ARGUMENTOS HÁBEIS A DESCONSTITUIR A DECISÃO IMPUGNADA.TRÁFICO ILÍCITO DE ENTORPECENTES. ILICITUDE DAS PROVAS. VIOLAÇÃO DEDOMICÍLIO. INOCORRÊNCIA. CRIME PERMANENTE. ENTRADA AUTORIZADA.EXISTÊNCIA DE FUNDADAS RAZÕES. FLAGRANTE ILEGALIDADE. INEXISTÊNCIA.HABEAS CORPUS NÃO CONHECIDO. DECISÃO AGRAVADA MANTIDA. AGRAVOREGIMENTAL DESPROVIDO.I - É assente nesta Corte Superior de Justiça que o agravoregimental deve trazer novos argumentos capazes de alterar oentendimento anteriormente firmado, sob pena de ser mantida a r.decisão agravada por seus próprios fundamentos.II - O eg. Tribunal a quo afastou motivadamente a alegada nulidadeda busca domiciliar sob o fundamento de que a inviolabilidade dedomicílio encontra exceção em caso de flagrante delito. In casu, opaciente fora condenado pela prática do crime de tráfico ilícito deentorpecentes, o qual configura delito permanente, ou seja, omomento consumativo protrai-se no tempo, permitindo a conclusão deque o agente estará em flagrante delito enquanto não cessar apermanência. Precedentes.III - De acordo com o arcabouço probatório produzido nos autos deorigem, constata-se que existiram fundadas razões para o ingresso nodomicílio do ora agravante porquanto, como bem asseverado peloparecer ministerial de cúpula, \"não se verifica a alegada nulidadereferente ao ingresso no domicílio do paciente tendo em vista doisfatores determinantes para que a violação tenha ocorrido: a fuga dopaciente para evitar a abordagem e se encontrar em local conhecidocomo ponto de drogas. Esse binômio deve levar inevitavelmente àconclusão por parte dos policiais que o paciente se encontra emsituação de flagrante, não tendo sido outro o resultado dadiligência policial, a qual acabou por apreender em posse dopaciente 18,60g (dezoito gramas e sessenta centigramas) de cocaína,repartidos em 61 (sessenta e uma) porções, e 01 (uma) espingarda damarca Beretta, calibre 36, numeração 39805, desmuniciada, de usopermitido, no interior de uma mala. Dessa forma, estão configuradasas fundadas razões pelas quais os policiais adentraram no domicíliodo paciente conforme exige a moderna jurisprudência desta Corte.Certamente a residência do criminoso não pode ser abrigo que garantaa prática de crime sem que possa ser importunado, mesmo diante deevidências de que se encontre praticando crime permanente no local.Por certo, fazer da residência do criminoso um oásis da práticacriminosa não foi o objetivo do instituto da inviolabilidade dodomicílio previsto na Constituição Federal, devendo, portanto, queser afasta a tese de ilegalidade da prova pela suposta violação dedomicílio, principalmente porque de fato o réu estava praticando ocrime de tráfico e posse ilegal de arma de fogo no local\" (fl. 83).IV - Nesse compasso, compreende-se que não há nulidade nas provasobtidas, tendo sido demonstradas as fundadas razões para se concluirque havia flagrante delito em andamento, bem como a autorizar oingresso em domicílio sem autorização judicial.V - Por fim, importante esclarecer a impossibilidade de se percorrertodo o acervo fático-probatório nesta via estreita do writ, comoforma de desconstituir as conclusões das instâncias ordinárias,soberanas na análise dos fatos e provas, providência inviável de serrealizada dentro dos estreitos limites do habeas corpus, que nãoadmite dilação probatória e o aprofundado exame do acervoprocessual. Precedentes.VI - Desta forma, verifica-se que o v. acórdão combatido está emconsonância com a jurisprudência desta Corte Superior de Justiça,não restando configurada as ilegalidades apontadas.Agravo regimental desprovido.",
            "acordao" : "VISTOS E RELATADOS ESTES AUTOS EM QUE SÃO PARTES AS ACIMA INDICADAS,ACORDAM OS MINISTROS DA QUINTA TURMA DO SUPERIOR TRIBUNAL DEJUSTIÇA, POR UNANIMIDADE, NEGAR PROVIMENTO AO AGRAVO REGIMENTAL.OS SRS. MINISTROS JOÃO OTÁVIO DE NORONHA, REYNALDO SOARES DAFONSECA, RIBEIRO DANTAS E JOEL ILAN PACIORNIK VOTARAM COM O SR.MINISTRO RELATOR.",
            "inteiroTeorArquivo" : [ 
                {
                    "urlOriginal" : "https://scon.stj.jus.br/SCON/GetInteiroTeorDoAcordao?num_registro=202101912413&dt_publicacao=05/10/2021",
                    "extensao" : "pdf",
                    "nomeArquivo" : "STJ/2021-10-05/21ce17d58afc9568b858742c83802898.pdf",
                }
            ],
            "tipoDecisao" : "ACÓRDÃO",
            "tribunal" : "STJ"
        },
        "metadata" : {
            "processingDate" : "2021-01-01T03:00:00+00:00",
            "spiderName" : "crawler-juris-stj"
        }
    }
```
Esse é outro exemplo do que o bot entrega:



Na versão 1.0.0, estava coletando apenas os Acórdãos
Na versão 1.0.1 o crawler coleta tanto Acórdãos como Decisões Monocráticas
É necessário colocar headers nas requisições 
Os arquivos de Inteiro teor das Decisões Monocráticas tem urls diferentes 
Na versão 1.0.3, esta coletando somente acordãos. Decisoes monocraticas estão em outro crawler

## Informações de coleta
- API: Não
- Captcha: Não
- Página a página: Não, passa em todas paralelamente
- Stats: Sim
- Spidermon: Sim
- no_recrawl : Sim