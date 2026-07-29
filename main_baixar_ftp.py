import ftplib
import os

def baixar_arquivos_esusnotifica(
    pasta_destino="./dados_chagas_esus",
    filtro_prefixo="DCCR"  # 'DCCR' baixa apenas Doença de Chagas Crônica. Deixe "" para baixar TUDO da pasta.
):
    host = "ftp.datasus.gov.br"
    caminho_ftp = "/dissemin/publicos/ESUSNOTIFICA/DADOS/PRELIM"
    
    # 1. Cria a pasta local para salvar os dados caso ela não exista
    os.makedirs(pasta_destino, exist_ok=True)
    
    print(f"Conectando ao FTP público do DATASUS ({host})...")
    
    try:
        # 2. Conexão e login anônimo
        ftp = ftplib.FTP(host)
        ftp.login()
        
        # 3. Acessa o diretório específico encontrado
        ftp.cwd(caminho_ftp)
        print(f"✓ Pasta acessada: {caminho_ftp}\n")
        
        # 4. Lista todos os arquivos presentes no diretório
        todos_arquivos = ftp.nlst()
        
        # Aplica o filtro (por padrão, busca arquivos de Chagas Crônica 'DCCR')
        if filtro_prefixo:
            arquivos_para_baixar = [f for f in todos_arquivos if f.upper().startswith(filtro_prefixo.upper())]
        else:
            arquivos_para_baixar = todos_arquivos

        total = len(arquivos_para_baixar)
        print(f"Foram encontrados {total} arquivo(s) para download.\n" + "-"*45)
        
        # 5. Loop para baixar cada arquivo
        for index, nome_arquivo in enumerate(arquivos_para_baixar, start=1):
            caminho_local = os.path.join(pasta_destino, nome_arquivo)
            
            # Verificação para não baixar novamente se já existir
            if os.path.exists(caminho_local):
                print(f"[{index}/{total}] ⏭️  {nome_arquivo} já existe localmente. Pulando...")
                continue
                
            print(f"[{index}/{total}] ⬇️  Baixando: {nome_arquivo}...")
            
            # Escreve o arquivo no disco em modo binário ('wb')
            with open(caminho_local, "wb") as arquivo_local:
                ftp.retrbinary(f"RETR {nome_arquivo}", arquivo_local.write)
                
            print(f"       ✓ Concluído com sucesso!")

        ftp.quit()
        print("-" * 45)
        print("🎉 Todos os downloads foram finalizados!")
        print(f"📁 Os arquivos estão salvos em: {os.path.abspath(pasta_destino)}")

    except Exception as e:
        print(f"\n❌ Ocorreu um erro durante o processo FTP: {e}")

# Executa a função
if __name__ == "__main__":
    baixar_arquivos_esusnotifica()