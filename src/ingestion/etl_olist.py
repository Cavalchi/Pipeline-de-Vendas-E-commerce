import pandas as pd
import os
from sqlalchemy import create_engine
import glob

# Configurações do Banco de Dados
# O usuário padrão do PostgreSQL costuma ser 'postgres' e a senha configuramos como 'postgres'
DB_CONNECTION = 'postgresql://postgres:50251407@localhost:5433/postgres' 

def main():
    print("Iniciando processo de ETL...")
    engine = create_engine(DB_CONNECTION)
    
    # Caminho para os CSVs
    csv_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')
    
    # Encontrar todos os arquivos CSV na pasta
    csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
    
    if not csv_files:
        print(f"Nenhum arquivo CSV encontrado em: {csv_dir}")
        print("Por favor, garanta que os arquivos baixados do Kaggle estao la.")
        return
        
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        # Limpar o nome do arquivo para usar como nome da tabela
        # 'olist_orders_dataset.csv' -> 'orders'
        table_name = file_name.replace('olist_', '').replace('_dataset.csv', '').replace('.csv', '')
        
        print(f"Processando e carregando: {table_name}...")
        df = pd.read_csv(file_path)
        
        # Limpeza genérica: remover duplicatas completas se existirem
        df = df.drop_duplicates()
        
        # Carregando no banco de dados (replace sobrescreve a tabela se já existir)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Tabela {table_name} salva com sucesso. ({len(df)} linhas)")

    print("ETL concluído com sucesso!")

if __name__ == "__main__":
    main()
