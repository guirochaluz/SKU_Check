import os
import psycopg2
import requests

DB_URL = os.getenv("DB_URL")

TABELA = "sua_tabela"
COLUNA = "sua_coluna"

WEBHOOK_URL = "https://prod-30.brazilsouth.logic.azure.com:443/workflows/119c9204c236452cacf39b2c9458e5e9/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=_t--TtgwDHCz8sFJGJYQB0kpb1e44W_Dq_03g8R5dKY"

def check_nulls_and_trigger_webhook():
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM {TABELA} WHERE {COLUNA} IS NULL;"
        cursor.execute(query)
        null_count = cursor.fetchone()[0]

        if null_count > 0:
            print(f"[ALERTA] {null_count} valores nulos em {TABELA}.{COLUNA}. Disparando webhook...")
            response = requests.post(WEBHOOK_URL, json={"null_count": null_count})
            print(f"Webhook status: {response.status_code}")
        else:
            print(f"[OK] Nenhum valor nulo encontrado em {TABELA}.{COLUNA}.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[ERRO] {e}")

if __name__ == "__main__":
    check_nulls_and_trigger_webhook()
