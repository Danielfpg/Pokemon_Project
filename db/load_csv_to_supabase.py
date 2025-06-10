import pandas as pd
import os
from db.supabase_client import get_supabase
def upload_csvs_to_supabase(csv_folder=".", supabase=None):
    if supabase is None:
        supabase = get_supabase()

    for filename in os.listdir(csv_folder):
        if filename.endswith(".csv"):
            table_name = filename.replace(".csv", "")
            file_path = os.path.join(csv_folder, filename)

            print(f"Procesando archivo: {filename}")
            try:
                df = pd.read_csv(file_path)
                data = df.to_dict(orient="records")
                print(f"Subiendo {filename} a la tabla '{table_name}'...")
                for row in data:
                    supabase.table(table_name).insert(row).execute()
                print(f"✅ {filename} subido correctamente.")
            except Exception as e:
                print(f"❌ Error al procesar {filename}: {e}")
# Llamar a la función automáticamente
if __name__ == "__main__":
    upload_csvs_to_supabase(csv_folder="./csv")
