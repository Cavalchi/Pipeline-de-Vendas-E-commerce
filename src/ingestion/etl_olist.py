import pandas as pd
import os
from sqlalchemy import create_engine
import glob
from dotenv import load_dotenv

# Carrega configurações isoladas do ambiente
load_dotenv()

DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASS', 'postgres')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')

DB_CONNECTION = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Garantia de integridade referencial: as tabelas devem ser ingeridas
# na ordem de dependência das Foreign Keys.
INGESTION_ORDER = [
    'customers',
    'geolocation',
    'sellers',
    'products',
    'product_category_name_translation',
    'orders',
    'order_items',
    'order_payments',
    'order_reviews'
]

def main():
    engine = create_engine(DB_CONNECTION)
    csv_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'raw')
    csv_files = glob.glob(os.path.join(csv_dir, '*.csv'))
    
    if not csv_files:
        print("Aviso: Nenhum arquivo CSV detectado em data/raw/. Por favor, insira os dados e tente novamente.")
        return

    table_to_file = {}
    for file_path in csv_files:
        file_name = os.path.basename(file_path)
        table_name = file_name.replace('olist_', '').replace('_dataset.csv', '').replace('.csv', '')
        table_to_file[table_name] = file_path

    for table_name in INGESTION_ORDER:
        if table_name not in table_to_file:
            print(f"[{table_name}] CSV não encontrado. Pulando etapa.")
            continue
            
        file_path = table_to_file[table_name]
        print(f"[{table_name}] Iniciando ingestão de dados...")
        
        try:
            # Importação particionada (chunks) para otimização em ambientes de recurso restrito
            chunksize = 10000
            chunks = pd.read_csv(file_path, chunksize=chunksize)
            
            for i, chunk in enumerate(chunks):
                chunk = chunk.drop_duplicates()
                chunk.to_sql(table_name, engine, if_exists='append', index=False)
                print(f"[{table_name}] -> Chunk {i} inserted ({len(chunk)} rows)")
                
            print(f"[{table_name}] Carga finalizada com sucesso.")
            
        except Exception as e:
            print(f"[{table_name}] Falha na inserção: {e}")

if __name__ == "__main__":
    main()
