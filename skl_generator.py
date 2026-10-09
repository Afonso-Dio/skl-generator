# -*- coding: utf-8 -*-
"""
Download, Padronização RINEX 3.05 e Mapeamento
de todos os Sinais Suportados pelo Padrão RINEX 3.05 para o BNC (BKG Ntrip Client).
"""

import os
import urllib.request
import urllib.error

# CONFIGURAÇÃO
SOURCE_TABLE = r"C:\pasta\sourcetable"
SKL_FOLDER = r"C:\pasta\skl"
SKL_BASE_URL = "http://enderecoskl/caster/"

# Se True, reprocessa arquivos locais sem re-fazer o download
NAO_SOBRESCREVER = False

# Arquivo com o relatório consolidado dos sinais
ARQUIVO_MAPEAMENTO = os.path.join(SKL_FOLDER, "mapeamento_sinais.txt")


# CATÁLOGO COMPLETO DE SINAIS (ESPECIFICAÇÃO OFICIAL RINEX 3.05)
FULL_GNSS_SIGNALS = {
    'G': [ # GPS (Tabela 14 - RINEX 3.05)
        # L1 (1575.42 MHz)
        'C1C', 'L1C', 'D1C', 'S1C', 'C1S', 'L1S', 'D1S', 'S1S', 'C1L', 'L1L', 'D1L', 'S1L',
        'C1X', 'L1X', 'D1X', 'S1X', 'C1P', 'L1P', 'D1P', 'S1P', 'C1W', 'L1W', 'D1W', 'S1W',
        'C1Y', 'L1Y', 'D1Y', 'S1Y', 'C1M', 'L1M', 'D1M', 'S1M', 'L1N', 'D1N', 'S1N',
        # L2 (1227.60 MHz)
        'C2C', 'L2C', 'D2C', 'S2C', 'C2D', 'L2D', 'D2D', 'S2D', 'C2S', 'L2S', 'D2S', 'S2S',
        'C2L', 'L2L', 'D2L', 'S2L', 'C2X', 'L2X', 'D2X', 'S2X', 'C2P', 'L2P', 'D2P', 'S2P',
        'C2W', 'L2W', 'D2W', 'S2W', 'C2Y', 'L2Y', 'D2Y', 'S2Y', 'C2M', 'L2M', 'D2M', 'S2M',
        'L2N', 'D2N', 'S2N',
        # L5 (1176.45 MHz)
        'C5I', 'L5I', 'D5I', 'S5I', 'C5Q', 'L5Q', 'D5Q', 'S5Q', 'C5X', 'L5X', 'D5X', 'S5X'
    ],
    'R': [ # GLONASS (Tabela 15 - RINEX 3.05)
        # G1 & G1a
        'C1C', 'L1C', 'D1C', 'S1C', 'C1P', 'L1P', 'D1P', 'S1P',
        'C4A', 'L4A', 'D4A', 'S4A', 'C4B', 'L4B', 'D4B', 'S4B', 'C4X', 'L4X', 'D4X', 'S4X',
        # G2 & G2a
        'C2C', 'L2C', 'D2C', 'S2C', 'C2P', 'L2P', 'D2P', 'S2P',
        'C6A', 'L6A', 'D6A', 'S6A', 'C6B', 'L6B', 'D6B', 'S6B', 'C6X', 'L6X', 'D6X', 'S6X',
        # G3
        'C3I', 'L3I', 'D3I', 'S3I', 'C3Q', 'L3Q', 'D3Q', 'S3Q', 'C3X', 'L3X', 'D3X', 'S3X'
    ],
    'E': [ # Galileo (Tabela 16 - RINEX 3.05)
        # E1
        'C1A', 'L1A', 'D1A', 'S1A', 'C1B', 'L1B', 'D1B', 'S1B', 'C1C', 'L1C', 'D1C', 'S1C',
        'C1X', 'L1X', 'D1X', 'S1X', 'C1Z', 'L1Z', 'D1Z', 'S1Z',
        # E5a
        'C5I', 'L5I', 'D5I', 'S5I', 'C5Q', 'L5Q', 'D5Q', 'S5Q', 'C5X', 'L5X', 'D5X', 'S5X',
        # E5b
        'C7I', 'L7I', 'D7I', 'S7I', 'C7Q', 'L7Q', 'D7Q', 'S7Q', 'C7X', 'L7X', 'D7X', 'S7X',
        # E5 AltBOC
        'C8I', 'L8I', 'D8I', 'S8I', 'C8Q', 'L8Q', 'D8Q', 'S8Q', 'C8X', 'L8X', 'D8X', 'S8X',
        # E6
        'C6A', 'L6A', 'D6A', 'S6A', 'C6B', 'L6B', 'D6B', 'S6B', 'C6C', 'L6C', 'D6C', 'S6C',
        'C6X', 'L6X', 'D6X', 'S6X', 'C6Z', 'L6Z', 'D6Z', 'S6Z'
    ],
    'C': [ # BeiDou (Tabela 19 - RINEX 3.05)
        # B1I
        'C2I', 'L2I', 'D2I', 'S2I', 'C2Q', 'L2Q', 'D2Q', 'S2Q', 'C2X', 'L2X', 'D2X', 'S2X',
        # B1C
        'C1D', 'L1D', 'D1D', 'S1D', 'C1P', 'L1P', 'D1P', 'S1P', 'C1X', 'L1X', 'D1X', 'S1X',
        # B1A
        'C1S', 'L1S', 'D1S', 'S1S', 'C1L', 'L1L', 'D1L', 'S1L', 'C1Z', 'L1Z', 'D1Z', 'S1Z',
        # B2a
        'C5D', 'L5D', 'D5D', 'S5D', 'C5P', 'L5P', 'D5P', 'S5P', 'C5X', 'L5X', 'D5X', 'S5X',
        # B2I
        'C7I', 'L7I', 'D7I', 'S7I', 'C7Q', 'L7Q', 'D7Q', 'S7Q', 'C7X', 'L7X', 'D7X', 'S7X',
        # B2b
        'C7D', 'L7D', 'D7D', 'S7D', 'C7P', 'L7P', 'D7P', 'S7P', 'C7Z', 'L7Z', 'D7Z', 'S7Z',
        # B2a+b
        'C8D', 'L8D', 'D8D', 'S8D', 'C8P', 'L8P', 'D8P', 'S8P', 'C8X', 'L8X', 'D8X', 'S8X',
        # B3I
        'C6I', 'L6I', 'D6I', 'S6I', 'C6Q', 'L6Q', 'D6Q', 'S6Q', 'C6X', 'L6X', 'D6X', 'S6X',
        # B3A
        'C6D', 'L6D', 'D6D', 'S6D', 'C6P', 'L6P', 'D6P', 'S6P', 'C6Z', 'L6Z', 'D6Z', 'S6Z'
    ],
    'J': [ # QZSS (Tabela 18 - RINEX 3.05)
        # L1
        'C1C', 'L1C', 'D1C', 'S1C', 'C1S', 'L1S', 'D1S', 'S1S', 'C1L', 'L1L', 'D1L', 'S1L',
        'C1X', 'L1X', 'D1X', 'S1X', 'C1Z', 'L1Z', 'D1Z', 'S1Z', 'C1B', 'L1B', 'D1B', 'S1B',
        # L2
        'C2S', 'L2S', 'D2S', 'S2S', 'C2L', 'L2L', 'D2L', 'S2L', 'C2X', 'L2X', 'D2X', 'S2X',
        # L5
        'C5I', 'L5I', 'D5I', 'S5I', 'C5Q', 'L5Q', 'D5Q', 'S5Q', 'C5X', 'L5X', 'D5X', 'S5X',
        'C5D', 'L5D', 'D5D', 'S5D', 'C5P', 'L5P', 'D5P', 'S5P', 'C5Z', 'L5Z', 'D5Z', 'S5Z',
        # L6
        'C6S', 'L6S', 'D6S', 'S6S', 'C6L', 'L6L', 'D6L', 'S6L', 'C6X', 'L6X', 'D6X', 'S6X',
        'C6E', 'L6E', 'D6E', 'S6E', 'C6Z', 'L6Z', 'D6Z', 'S6Z'
    ],
    'S': [ # SBAS (Tabela 17 - RINEX 3.05)
        # L1
        'C1C', 'L1C', 'D1C', 'S1C',
        # L5
        'C5I', 'L5I', 'D5I', 'S5I', 'C5Q', 'L5Q', 'D5Q', 'S5Q', 'C5X', 'L5X', 'D5X', 'S5X'
    ],
    'I': [ # NavIC / IRNSS (Tabela 20 - RINEX 3.05)
        # L5
        'C5A', 'L5A', 'D5A', 'S5A', 'C5B', 'L5B', 'D5B', 'S5B', 'C5C', 'L5C', 'D5C', 'S5C',
        'C5X', 'L5X', 'D5X', 'S5X',
        # S (2492.028 MHz)
        'C9A', 'L9A', 'D9A', 'S9A', 'C9B', 'L9B', 'D9B', 'S9B', 'C9C', 'L9C', 'D9C', 'S9C',
        'C9X', 'L9X', 'D9X', 'S9X'
    ]
}

RINEX_LABELS = [
    "RINEX VERSION / TYPE", "PGM / RUN BY / DATE", "COMMENT", "MARKER NAME",
    "MARKER NUMBER", "MARKER TYPE", "OBSERVER / AGENCY", "REC # / TYPE / VERS",
    "ANT # / TYPE", "APPROX POSITION XYZ", "ANTENNA: DELTA H/E/N",
    "SYS / # / OBS TYPES", "WAVELENGTH FACT L1/2", "# / TYPES OF OBSERV",
    "SIGNAL STRENGTH UNIT", "INTERVAL", "TIME OF FIRST OBS", "TIME OF LAST OBS",
    "RCV CLOCK OFFS APPL", "SYS / DCBS APPLIED", "SYS / PCVS APPLIED",
    "SYS / SCALE FACTOR", "SYS / PHASE SHIFT", "GLONASS SLOT / FRQ #",
    "GLONASS COD/PHS/BIS", "LEAP SECONDS", "# OF SATELLITES", "PRN / # OF OBS",
    "END OF HEADER"
]


# FUNÇÕES AUXILIARES
def extrair_estacoes(arquivo):
    """Lê o sourcetable e extrai as estações válidas da rede RBMC-IP."""
    estacoes = []
    if not os.path.isfile(arquivo):
        return estacoes

    with open(arquivo, "r", encoding="latin-1") as f:
        for linha in f:
            if not linha.startswith("STR;"):
                continue
            campos = linha.rstrip("\r\n").split(";")
            if len(campos) < 8 or "RBMC-IP" not in campos:
                continue

            mountpoint = campos[1]
            station = mountpoint[:-1] if mountpoint.endswith("0") else mountpoint
            station = station.strip().lower()

            if station and station not in estacoes:
                estacoes.append(station)

    return sorted(estacoes)


def expandir_e_obter_sinais(sinais_existentes):
    """
    Injeta o catálogo completo de todas as 7 constelações do RINEX 3.05
    junto a qualquer sinal já existente no arquivo original.
    """
    mapa_completo = {}
    sistemas_alvo = set(FULL_GNSS_SIGNALS.keys())

    for sys in sorted(sistemas_alvo):
        sinais_base = sinais_existentes.get(sys, [])
        mestre = FULL_GNSS_SIGNALS.get(sys, [])

        sinais_combinados = list(sinais_base)
        for sig in mestre:
            if sig not in sinais_combinados:
                sinais_combinados.append(sig)

        if sinais_combinados:
            mapa_completo[sys] = sinais_combinados

    return mapa_completo


def formatar_linhas_sys_obs(sys_code, lista_obs):
    """
    Gera linhas 'SYS / # / OBS TYPES' no padrão RINEX 3 estrito
    (Alinhadas na coluna 61, máximo de 13 códigos por linha).
    """
    linhas = []
    total = len(lista_obs)
    chunk_size = 13
    chunks = [lista_obs[i:i + chunk_size] for i in range(0, total, chunk_size)]

    for idx, chunk in enumerate(chunks):
        if idx == 0:
            prefixo = f"{sys_code:>1} {total:>4} "
        else:
            prefixo = "       "

        obs_str = " ".join(f"{obs:>3}" for obs in chunk)
        dados = f"{prefixo}{obs_str}"
        linha = f"{dados:<60}SYS / # / OBS TYPES"
        linhas.append(linha)

    return linhas


def converter_e_padronizar_header(texto):
    """
    Processa o texto do arquivo SKL:
    1. Re-alinha todos os labels do cabeçalho na coluna 61.
    2. Converte cabeçalhos para o padrão RINEX 3.05.
    3. Injeta a lista completa de sinais das 7 constelações GNSS.
    """
    linhas_originais = texto.splitlines()
    sinais_detectados = {}

    for linha in linhas_originais:
        if "SYS / # / OBS TYPES" in linha:
            sys_id = linha[0:1].strip()
            obs_list = linha[6:60].split()
            if sys_id:
                if sys_id not in sinais_detectados:
                    sinais_detectados[sys_id] = []
                for o in obs_list:
                    if o not in sinais_detectados[sys_id]:
                        sinais_detectados[sys_id].append(o)

    mapa_sinais_final = expandir_e_obter_sinais(sinais_detectados)

    novas_linhas = []

    # 1. Cabeçalho oficial RINEX 3.05
    novas_linhas.append(f"{'3.05':>9}           {'OBSERVATION DATA':<20}{'M':<20}RINEX VERSION / TYPE")
    novas_linhas.append(f"{'BNC-SKL-FIXER':<20}{'IBGE/RBMC':<20}{'20260909 120000':<20}PGM / RUN BY / DATE")

    # 2. Processa as demais linhas do cabeçalho
    for linha in linhas_originais:
        if any(lbl in linha for lbl in [
            "RINEX VERSION / TYPE",
            "PGM / RUN BY / DATE",
            "# / TYPES OF OBSERV",
            "SYS / # / OBS TYPES",
            "WAVELENGTH FACT L1/2"
        ]):
            continue

        if "END OF HEADER" in linha:
            for sys_code in sorted(mapa_sinais_final.keys()):
                linhas_sys = formatar_linhas_sys_obs(sys_code, mapa_sinais_final[sys_code])
                novas_linhas.extend(linhas_sys)

            novas_linhas.append(f"{'':<60}END OF HEADER")
            break

        label_encontrado = None
        for lbl in RINEX_LABELS:
            if lbl in linha:
                label_encontrado = lbl
                break

        if label_encontrado:
            idx = linha.find(label_encontrado)
            dado = linha[:idx].rstrip("\r\n")
            if len(dado) > 60:
                dado = dado[:60]
            novas_linhas.append(f"{dado:<60}{label_encontrado}")
        else:
            novas_linhas.append(linha)

    texto_final = "\r\n".join(novas_linhas) + "\r\n"
    return texto_final, mapa_sinais_final


def baixar_e_processar_skl(station):
    """Gerencia download, leitura e salvamento do arquivo SKL corrigido."""
    nome_arquivo = station + ".skl"
    destino = os.path.join(SKL_FOLDER, nome_arquivo)
    url = SKL_BASE_URL + nome_arquivo

    if NAO_SOBRESCREVER and os.path.isfile(destino):
        try:
            with open(destino, "r", encoding="latin-1") as f:
                texto = f.read()
            texto_corrigido, sinais = converter_e_padronizar_header(texto)
            with open(destino, "w", encoding="latin-1", newline="\r\n") as f:
                f.write(texto_corrigido)
            return "existente", sinais
        except Exception as e:
            print(f"[ERRO LOCAL] {nome_arquivo}: {e}")
            return "erro", {}

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BNC-SKL-Downloader/3.0"})
        with urllib.request.urlopen(req, timeout=20) as resposta:
            dados = resposta.read()
            texto = dados.decode("latin-1", errors="ignore")

            if "END OF HEADER" not in texto:
                print(f"[ERRO INVALIDO] {nome_arquivo}: Resposta não é um SKL válido.")
                return "erro", {}

            texto_corrigido, sinais = converter_e_padronizar_header(texto)

            with open(destino, "w", encoding="latin-1", newline="\r\n") as f:
                f.write(texto_corrigido)

        print(f"[OK] {nome_arquivo} atualizado para RINEX 3.05 (7 Constelações).")
        return "baixado", sinais

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"[NÃO ENCONTRADO] {nome_arquivo}")
            return "nao_existe", {}
        print(f"[HTTP {e.code}] {nome_arquivo}: {e.reason}")
        return "erro", {}
    except Exception as e:
        print(f"[ERRO] {nome_arquivo}: {e}")
        return "erro", {}


# MAIN
def main():
    print("=" * 60)
    print("DOWNLOAD E MAPEAMENTO RINEX 3.05 COMPLETO (ALL SIGNALS & SYSTEMS)")
    print("=" * 60)

    os.makedirs(SKL_FOLDER, exist_ok=True)

    if not os.path.isfile(SOURCE_TABLE):
        print(f"\nERRO: Sourcetable não encontrado no caminho: {SOURCE_TABLE}")
        return

    print("\nLendo sourcetable...")
    estacoes = extrair_estacoes(SOURCE_TABLE)
    print(f"Estações identificadas no Sourcetable: {len(estacoes)}\n")

    if not estacoes:
        print("Nenhuma estação RBMC-IP encontrada.")
        return

    contadores = {"baixado": 0, "existente": 0, "nao_existe": 0, "erro": 0}
    mapa_geral = {}

    for st in estacoes:
        status, sinais = baixar_e_processar_skl(st)
        contadores[status] += 1
        if sinais:
            mapa_geral[st.upper()] = sinais

    print("\n" + "=" * 60)
    print("SALVANDO RELATÓRIO COMPLETO DE SINAIS")
    print("=" * 60)

    with open(ARQUIVO_MAPEAMENTO, "w", encoding="utf-8") as fm:
        fm.write("RELATÓRIO DE SINAIS RINEX 3.05 MAPEADOS E INJETADOS NOS SKLS\n")
        fm.write("=" * 60 + "\n\n")
        for estacao, dicionario_sinais in mapa_geral.items():
            fm.write(f"ESTAÇÃO: {estacao}\n")
            for sys_code, list_obs in dicionario_sinais.items():
                fm.write(f"  [{sys_code}] ({len(list_obs)} sinais): {' '.join(list_obs)}\n")
            fm.write("\n")

    print(f"Relatório de sinais salvo em:\n{ARQUIVO_MAPEAMENTO}\n")

    print("=" * 60)
    print("RESUMO DA EXECUÇÃO")
    print("=" * 60)
    print(f"Arquivos baixados/processados: {contadores['baixado']}")
    print(f"Arquivos locais atualizados:    {contadores['existente']}")
    print(f"Estações não encontradas (404): {contadores['nao_existe']}")
    print(f"Erros de download/processamento:{contadores['erro']}")
    print(f"\nPasta de destino dos SKLs:\n{SKL_FOLDER}\n")


if __name__ == "__main__":
    main()