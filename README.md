# Estrazione Estratti Conto (modello Mistral via HuggingFace)

Questa app Streamlit consente di:
- Caricare PDF contenenti estratti conto
- Estrarre i dati (Premio Lordo, Provvigioni, Totale Estratto Conto)
- Generare un file Excel riepilogativo

## ⚙️ Come usarla su Streamlit Cloud

1. Crea un nuovo repository GitHub
2. Carica i file di questo ZIP
3. Vai su https://streamlit.io/cloud
4. Seleziona il file `estratti_conto_huggingface_webapp.py` come file di avvio
5. In `⋮ Manage App → Secrets`, aggiungi:

```
HUGGINGFACE_TOKEN = "la-tua-api-key"
```

## 📦 Requirements (incluso nel file)
- streamlit
- pymupdf
- pandas
- requests

## 🔐 Sicurezza
Non includere mai la tua API key nel codice. Usare sempre i secrets.
