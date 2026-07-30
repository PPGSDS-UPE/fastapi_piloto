import os
import glob
import pandas as pd
import numpy as np
from datasus_dbc import decompress
from dbfread import DBF

# ==============================================================================
# 1. LISTA OFICIAL DE CAMPOS EXTRAÍDA DO SEU DICIONÁRIO DE DADOS (PDF)
# ==============================================================================
CAMPOS_DICIONARIO = [
    "SG_UF_NOT", "ID_MUNICIP", "ID_CPF", "CNES", "ID_ESTRANG", "ID_OCUPA_N", 
    "ANO_NASC", "NU_IDADE_N", "ID_PAIS", "CS_SEXO", "CS_RACA", "COMU_TRAD", 
    "CS_ESCOL_N", "SG_UF", "ID_MN_RESI", "SG_PAIS", "DT_NOTIFIC", "ANO_DIAG",
    "MO_SUSPEIT", "OUTRO_SUSP", "CS_GESTANT", "UF_NASC", "MUN_NASC", 
    "COUFINF", "COMUNINF", "EIE_IGG", "IFI_IGG", "HAI_IGG", "QUIMIO_IGG", 
    "PCR", "OUTRO_POSI", "OUTRO_QUAL", "AC_NOT", "UF_UBS_AC", "MUN_UBS_AC", 
    "HOSP_ESP", "UF_HOSPESP", "MUN_ESP", "ELETROCARD", "RX_TORAX", "RX_COLON", 
    "RX_ESOFAGO", "ECOCARDIO", "OUTRO_EXAM", "EXAME_DESC", "FORMA", "REATIVACAO", 
    "HIST_BNZ", "TRAT_BNZ", "BNZ_TOT_CP", "BNZ_DIAS", "TRAT_NFX", "NFX_TOT_CP", 
    "NFX_DIAS", "ADVERS_BNZ", "BNZ_OUTRAS", "ADVERS_NFX", "NFX_OUTRAS",
    "HIST_EPIDE", "BUSCAATIVA", "DIAG_FAMIL", "EXAM_FAMIL", "CONF_FAMIL",
    "TF_RESIDEN", "UF_RESI_TF", "MN_RESI_TF", "MUD_UBS_AC", "UF_NOV_AC", 
    "MUN_NOV_AC", "NOVO_ESPEC", "ANT_UF_ESP", "ANT_MUN", "ST_ENCERRA", 
    "DT_OBITO", "DT_ENCERRA", "SITUACAO", "DT_DIGITACAO", "COMORBID_", "HIV", 
    "HIPERTEN", "HEPATITE", "DIABETES", "CARDIOPAT", "NEOPLASIA", "LEISHMANIA", 
    "OUT_COMORB", "ESP_COMORB", "CD_MUNICIP", "CD_MN_RESI", "CD_MUN_NASC", 
    "CD_COMUNIN", "CD_MUN_UBS", "CD_MUN_ESP", "CD_ANT_MUN"
]

PASTA_DADOS = "./dados_chagas_esus"

# ==============================================================================
# 2. FUNÇÕES DE LEITURA E AUDITORIA
# ==============================================================================
def ler_dbc_para_pandas(caminho_arquivo):
    """Descompacta o .dbc para .dbf e lê como DataFrame Pandas."""
    caminho_dbf = caminho_arquivo.replace('.dbc', '.dbf')
    
    decompress(caminho_arquivo, caminho_dbf)
    
    dbf = DBF(caminho_dbf, encoding='iso-8859-1')
    df = pd.DataFrame(iter(dbf))
    
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
            df = ler_dbc_para_pandas(caminho_arquivo)
            
            # --- LIMPEZA DE DADOS VAZIOS ---
            # Arquivos DBF costumam preencher campos vazios com espaços (ex: "   ").
            # Precisamos transformar isso em valores nulos (NaN) para a contagem funcionar.
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = df[col].str.strip().replace('', np.nan)
            
            total_linhas = len(df)
            colunas_arquivo = [col.upper() for col in df.columns]
            # Renomear as colunas no DF para facilitar o acesso
            df.columns = colunas_arquivo 
            arquivo_set = set(colunas_arquivo)

            presentes = dicionario_set.intersection(arquivo_set)
            ausentes = dicionario_set.difference(arquivo_set)
            extras = arquivo_set.difference(dicionario_set)

            print(f"📊 Registros no arquivo: {total_linhas:,}")
            print(f"📊 Total de Colunas no arquivo: {len(arquivo_set)}")
            print(f"✅ Colunas do Dicionário PRESENTES: {len(presentes)} / {len(dicionario_set)}")
            print(f"❌ Colunas do Dicionário AUSENTES: {len(ausentes)}\n")

            # --- VERIFICAÇÃO DE PREENCHIMENTO ---
            if presentes:
                var_com_dados = []
                var_vazias = []
                
                for col in sorted(list(presentes)):
                    qtd_preenchida = df[col].notna().sum()
                    if qtd_preenchida > 0:
                        percentual = (qtd_preenchida / total_linhas) * 100
                        var_com_dados.append(f"  - {col}: {qtd_preenchida:,} registros ({percentual:.1f}%)")
                    else:
                        var_vazias.append(f"  - {col}")
                
                print("🟢 VARIÁVEIS DO DICIONÁRIO PRESENTES *E* COM DADOS:")
                if var_com_dados:
                    for linha in var_com_dados:
                        print(linha)
                else:
                    print("  - Nenhuma variável possui dados (todas estão 100% nulas).")
                print()
                
                if var_vazias:
                    print("🔴 VARIÁVEIS PRESENTES, MAS TOTALMENTE VAZIAS (0% preenchidas):")
                    for linha in var_vazias:
                        print(linha)
                    print()

            if ausentes:
                print("⚠️ VARIÁVEIS DO DICIONÁRIO QUE NÃO EXISTEM NESTE ARQUIVO (Não exportadas):")
                print(sorted(list(ausentes)))
                print()

            if extras:
                print("ℹ️ VARIÁVEIS ENCONTRADAS NO ARQUIVO, MAS NÃO MENCIONADAS NO PDF:")
                print(sorted(list(extras)))
                print()

        except Exception as e:
            print(f"❌ Erro ao ler o arquivo {nome_arquivo}: {e}\n")

if __name__ == "__main__":
    auditar_arquivos_dbc(PASTA_DADOS)