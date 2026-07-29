import os
import glob
import pandas as pd
from datasus_dbc import decompress
from dbfread import DBF

# ==============================================================================
# 1. LISTA OFICIAL DE CAMPOS EXTRAÍDA DO SEU DICIONÁRIO DE DADOS (PDF)
# ==============================================================================
CAMPOS_DICIONARIO = [
    # Dados Gerais e Demográficos
    "SG_UF_NOT", "ID_MUNICIP", "ID_CPF", "CNES", "ID_ESTRANG", "ID_OCUPA_N", 
    "ANO_NASC", "NU_IDADE_N", "ID_PAIS", "CS_SEXO", "CS_RACA", "COMU_TRAD", 
    "CS_ESCOL_N", "SG_UF", "ID_MN_RESI", "SG_PAIS", "DT_NOTIFIC", "ANO_DIAG",
    
    # Suspeição e Diagnóstico
    "MO_SUSPEIT", "OUTRO_SUSP", "CS_GESTANT", "UF_NASC", "MUN_NASC", 
    "COUFINF", "COMUNINF", "EIE_IGG", "IFI_IGG", "HAI_IGG", "QUIMIO_IGG", 
    "PCR", "OUTRO_POSI", "OUTRO_QUAL",
    
    # Acompanhamento e Unidade
    "AC_NOT", "UF_UBS_AC", "MUN_UBS_AC", "HOSP_ESP", "UF_HOSPESP", "MUN_ESP",
    
    # Exames Complementares e Forma Clínica
    "ELETROCARD", "RX_TORAX", "RX_COLON", "RX_ESOFAGO", "ECOCARDIO", 
    "OUTRO_EXAM", "EXAME_DESC", "FORMA", "REATIVACAO", "HIST_BNZ",
    
    # Tratamentos e Reações Adversas
    "TRAT_BNZ", "BNZ_TOT_CP", "BNZ_DIAS", "TRAT_NFX", "NFX_TOT_CP", "NFX_DIAS", 
    "ADVERS_BNZ", "BNZ_OUTRAS", "ADVERS_NFX", "NFX_OUTRAS",
    
    # Histórico e Busca Ativa Familar
    "HIST_EPIDE", "BUSCAATIVA", "DIAG_FAMIL", "EXAM_FAMIL", "CONF_FAMIL",
    
    # Transferência e Mudanças de Unidade
    "TF_RESIDEN", "UF_RESI_TF", "MN_RESI_TF", "MUD_UBS_AC", "UF_NOV_AC", 
    "MUN_NOV_AC", "NOVO_ESPEC", "ANT_UF_ESP", "ANT_MUN",
    
    # Encerramento e Datas
    "ST_ENCERRA", "DT_OBITO", "DT_ENCERRA", "SITUACAO", "DT_DIGITACAO",
    
    # Comorbidades
    "COMORBID_", "HIV", "HIPERTEN", "HEPATITE", "DIABETES", "CARDIOPAT", 
    "NEOPLASIA", "LEISHMANIA", "OUT_COMORB", "ESP_COMORB",
    
    # Códigos IBGE Complementares
    "CD_MUNICIP", "CD_MN_RESI", "CD_MUN_NASC", "CD_COMUNIN", "CD_MUN_UBS", 
    "CD_MUN_ESP", "CD_ANT_MUN"
]

PASTA_DADOS = "./dados_chagas_esus"

# ==============================================================================
# 2. FUNÇÃO DE AUDITORIA (Adaptada para datasus-dbc)
# ==============================================================================
def ler_dbc_para_pandas(caminho_arquivo):
    """Descompacta o .dbc para .dbf e lê como DataFrame Pandas."""
    caminho_dbf = caminho_arquivo.replace('.dbc', '.dbf')
    
    # Descompacta o arquivo DATASUS
    decompress(caminho_arquivo, caminho_dbf)
    
    # Lê o arquivo DBF extraído
    dbf = DBF(caminho_dbf, encoding='iso-8859-1')
    df = pd.DataFrame(iter(dbf))
    
    # Limpa o arquivo .dbf temporário para economizar espaço
    if os.path.exists(caminho_dbf):
        os.remove(caminho_dbf)
        
    return df

def auditar_arquivos_dbc(pasta_origem):
    arquivos = glob.glob(os.path.join(pasta_origem, "*.dbc"))
    
    if not arquivos:
        print(f"❌ Nenhum arquivo .dbc encontrado no diretório: '{pasta_origem}'")
        return

    dicionario_set = set([c.upper() for c in CAMPOS_DICIONARIO])
    print(f"📋 Total de variáveis no Dicionário Oficial: {len(dicionario_set)}\n")

    for caminho_arquivo in arquivos:
        nome_arquivo = os.path.basename(caminho_arquivo)
        print("=" * 70)
        print(f"🔍 AUDITANDO ARQUIVO: {nome_arquivo}")
        print("=" * 70)

        try:
            # Usando a nova função customizada
            df = ler_dbc_para_pandas(caminho_arquivo)
            
            colunas_arquivo = [col.upper() for col in df.columns]
            arquivo_set = set(colunas_arquivo)

            presentes = dicionario_set.intersection(arquivo_set)
            ausentes = dicionario_set.difference(arquivo_set)
            extras = arquivo_set.difference(dicionario_set)

            print(f"📊 Registros no arquivo: {len(df):,}")
            print(f"📊 Total de Colunas no arquivo: {len(arquivo_set)}")
            print(f"✅ Colunas do Dicionário PRESENTES: {len(presentes)} / {len(dicionario_set)}")
            print(f"❌ Colunas do Dicionário AUSENTES: {len(ausentes)}")
            print(f"❓ Colunas no arquivo NÃO MAPEADAS no dicionário: {len(extras)}\n")

            # --- NOVO BLOCO ADICIONADO AQUI ---
            if presentes:
                print("✅  VARIÁVEIS DO DICIONÁRIO PRESENTES NESTE ARQUIVO:")
                print(sorted(list(presentes)))
                print()
            # ----------------------------------

            if ausentes:
                print("⚠️  VARIÁVEIS DO DICIONÁRIO QUE NÃO ESTÃO NESTE ARQUIVO:")
                print(sorted(list(ausentes)))
                print()

            if extras:
                print("ℹ️  VARIÁVEIS ENCONTRADAS NO ARQUIVO, MAS NÃO MENCIONADAS NO PDF:")
                print(sorted(list(extras)))
                print()

        except Exception as e:
            print(f"❌ Erro ao ler o arquivo {nome_arquivo}: {e}\n")

if __name__ == "__main__":
    auditar_arquivos_dbc(PASTA_DADOS)