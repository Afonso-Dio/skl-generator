# BNC SKL Downloader e Mapeador de Sinais RINEX 3.05

Ferramenta em Python para baixar, padronizar e atualizar arquivos de estrutura de estações (`.skl`) da RBMC do IBGE, utilizados pelo BNC (BKG Ntrip Client).

## Visão geral

Este projeto automatiza a obtenção e a padronização dos arquivos `.skl` específicos das estações da Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS (RBMC). A ferramenta amplia as definições dos tipos de observação por meio de um catálogo predefinido com base na especificação RINEX 3.05.

O desenvolvimento do script foi motivado pela identificação de um possível problema de compatibilidade: arquivos RINEX gerados pelo BNC a partir de fluxos de dados da RBMC apresentavam cabeçalhos, mas não continham registros de observação. Após a atualização dos arquivos de estrutura locais, a coleta de dados de observação foi realizada com sucesso nos testes executados. Entretanto, a causa exata do problema original ainda não foi determinada de forma conclusiva.

## Funcionalidades

* Lê os pontos de conexão (*mountpoints*) das estações RBMC-IP a partir de uma tabela de fontes NTRIP armazenada localmente.
* Baixa os arquivos `.skl` específicos das estações a partir do repositório do IBGE.
* Padroniza os cabeçalhos RINEX e as definições dos tipos de observação.
* Adiciona códigos de sinais predefinidos para sete constelações GNSS:

  * GPS
  * GLONASS
  * Galileo
  * BeiDou
  * QZSS
  * SBAS
  * NavIC/IRNSS
* Preserva os códigos de observação existentes e adiciona os códigos ausentes presentes no catálogo de sinais.
* Gera um relatório consolidado do mapeamento de sinais.
* Trata arquivos ausentes, erros HTTP e exceções durante o processamento.

## Fontes de dados

* **Tabela de fontes NTRIP da RBMC:** http://gps-ntrip.ibge.gov.br:2101/
* **Repositório de arquivos SKL da RBMC/IBGE:** http://gps-ntrip.ibge.gov.br/skl/
* **Código-fonte do BNC, revisão 10979:** https://software.rtcm-ntrip.org/browser/ntrip/trunk/BNC/src/rinex/rnxobsfile.cpp?rev=10979

## Requisitos

* Python 3.
* Acesso à internet para consultar o repositório de arquivos SKL da RBMC/IBGE.
* Uma cópia local da tabela de fontes NTRIP da RBMC.
* BNC instalado e configurado para utilizar os arquivos de estrutura locais gerados pelo script.

O script utiliza apenas módulos da biblioteca padrão do Python, portanto não requer a instalação de pacotes de terceiros.

## Configuração

Edite as variáveis de configuração no início do script:

| Variável           | Descrição                                                                                                    |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| `SOURCE_TABLE`     | Caminho para o arquivo local da tabela de fontes NTRIP.                                                      |
| `SKL_FOLDER`       | Diretório onde os arquivos `.skl` baixados e processados serão armazenados.                                  |
| `SKL_BASE_URL`     | URL base do repositório de arquivos SKL da RBMC/IBGE.                                                        |
| `NAO_SOBRESCREVER` | Controla se os arquivos locais existentes serão reutilizados, evitando novos downloads dos arquivos remotos. |

**Importante:** defina `NAO_SOBRESCREVER = True` para processar novamente os arquivos locais existentes sem baixá-los outra vez. Defina `NAO_SOBRESCREVER = False` para baixar os arquivos remotos e processá-los.

Ajuste os caminhos conforme o sistema operacional e o local de instalação do BNC.

## Como utilizar

1. Baixe a tabela de fontes NTRIP da RBMC e salve-a localmente.

2. Configure os caminhos de entrada e saída no script.

3. Execute o script em um terminal:

   ```bash
   python bnc_skl_downloader.py
   ```

4. Verifique as mensagens exibidas no terminal para acompanhar os resultados dos downloads e do processamento.

5. Configure o BNC para utilizar os arquivos `.skl` locais gerados pelo script.

6. Verifique se os arquivos RINEX resultantes contêm registros de observação e cabeçalhos válidos.

## Arquivos gerados

O script gera os seguintes resultados:

* **Arquivos `.skl` das estações:** arquivos de estrutura locais padronizados para as estações processadas com sucesso.
* **`mapeamento_sinais.txt`:** relatório consolidado dos códigos de observação definidos para cada estação e constelação GNSS.
* **Resumo da execução:** contagem de arquivos baixados, arquivos locais reprocessados, arquivos de estações não encontrados e erros ocorridos.

## Observações técnicas

### Definições de sinais RINEX 3.05

O script utiliza um catálogo predefinido de códigos de observação associados a sete constelações GNSS. Os códigos já existentes em cada arquivo de estrutura são preservados, enquanto as definições ausentes no catálogo são adicionadas.

O catálogo define os tipos de observação potencialmente utilizados, mas não indica quais sinais estão efetivamente disponíveis em uma determinada estação ou presentes no fluxo RTCM recebido. As observações realmente disponíveis dependem das capacidades do receptor, dos satélites visíveis, dos sinais rastreados e dos dados fornecidos pelo *caster* NTRIP.

### Possível problema de compatibilidade com o BNC

O projeto surgiu durante a investigação de uma possível incompatibilidade entre os arquivos de estrutura da RBMC e a interpretação de seu conteúdo pelo BNC. O histórico do código-fonte do programa constitui uma referência para investigar alterações no tratamento de arquivos RINEX de observação:

https://software.rtcm-ntrip.org/browser/ntrip/trunk/BNC/src/rinex/rnxobsfile.cpp?rev=10979

A relação entre essas alterações e a ausência de registros de observação identificada nos testes permanece uma hipótese, e não uma causa-raiz confirmada.

### Validação

Antes da utilização operacional, recomenda-se validar os cabeçalhos gerados conforme a especificação RINEX aplicável e a versão do BNC utilizada. Também é importante verificar se os tipos de observação declarados são compatíveis com o receptor e com o fluxo de dados recebido.

## Limitações

* São processadas apenas as estações identificadas como `RBMC-IP` na tabela de fontes local.
* Alguns arquivos `.skl` de estações podem não estar disponíveis no repositório.
* A inclusão de códigos de sinais nos arquivos de estrutura não cria nem recupera observações GNSS ausentes.
* Os cabeçalhos padronizados e o catálogo de sinais devem ser validados antes de serem utilizados em processamento científico.

## Licença

Até o momento, nenhuma licença foi especificada para o projeto. Antes de distribuir ou permitir a reutilização pública do código, recomenda-se adicionar um arquivo `LICENSE` ao repositório, definindo os termos de uso, modificação e redistribuição.

## Agradecimentos

* **IBGE** — Instituto Brasileiro de Geografia e Estatística, pela infraestrutura da RBMC e pelos recursos relacionados às estações.
* **BKG** — Desenvolvedor do BNC (BKG Ntrip Client).
* **International GNSS Service (IGS)** — Pelos padrões, especificações e recursos relacionados aos sistemas GNSS.
