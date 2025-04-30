import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import json
from io import BytesIO
import requests
import os

# Token da HuggingFace (inserito nei secrets)
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN") or "INSERISCI_LA_TUA_CHIAVE"

# Modello HuggingFace leggero (7B compatibile)
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {HUGGINGFACE_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    st.code(f"DEBUG status: {response.status_code}", language="text")
    try:
        result = response.json()
        st.code(result, language="json")
        return result[0]["generated_text"]
    except Exception as e:
        st.error(f"Errore nella risposta HuggingFace: {e}")
        return None

def estrai_testo_da_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])[:3000]

def estrai_dati_con_huggingface(testo):
    prompt = f"""
Estrai i seguenti dati dal testo di un estratto conto assicurativo e restituiscili in JSON:

- Broker
- Data documento (gg/mm/aaaa)
- Premio Lordo Totale
- Provvigioni
- Totale Estratto conto (Netto + Provvigioni)

Solo JSON valido, senza testo extra.

Testo:
\"\"\"
{testo}
\"\"\"
"""
    output = query({"inputs": prompt})
    try:
        return json.loads(output.split("```")[0].strip())
    except:
        return None

def main():
    st.set_page_config(page_title="Estrazione Estratti Conto (Zephyr)", layout="centered")
    st.title("📄 Estrazione Estratti Conto - modello Zephyr via HuggingFace")
    uploaded_files = st.file_uploader("Carica PDF", type="pdf", accept_multiple_files=True)

    if uploaded_files and st.button("Estrai dati"):
        risultati = []
        for file in uploaded_files:
            st.info(f"Elaboro: {file.name}")
            testo = estrai_testo_da_pdf(file)
            dati = estrai_dati_con_huggingface(testo)
            if dati:
                dati["File"] = file.name
                risultati.append(dati)
            else:
                st.warning("Nessun dato estratto.")

        if risultati:
            df = pd.DataFrame(risultati)
            excel_file = BytesIO()
            df.to_excel(excel_file, index=False)
            excel_file.seek(0)
            st.download_button("📥 Scarica Excel", data=excel_file, file_name="estratti_conto_zephyr.xlsx")
        else:
            st.warning("❌ Nessun risultato ottenuto.")

if __name__ == "__main__":
    main()
