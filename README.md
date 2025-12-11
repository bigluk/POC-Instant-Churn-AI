# POC-Instant-Churn-AI
The project's goal is to build an AI model to predict users investment propensity


# 📦 Clonare la repository

Clona il branch master del progetto tramite:

git clone https://github.com/bigluk/POC-Instant-Churn-AI.git

# 🛠 Backend
## 🔧 Creazione ambiente virtuale

Apri il terminale nella directory <i>/backend/poc-ai-model/</i> e digita i seguenti comandi:
```
python3 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## 🐘 Installazione Database Postgres + PgAdmin (Docker)

Apri il terminale in <i>/backend/poc-ai-model/poc-ai-digical-branch</i> e avvia i container tramite Docker Compose:

`docker compose up -d`

⚠️ Nota:
Se riscontri conflitti di porta modifica i valori delle porte direttamente nel file docker-compose.yml.

## 📊 Eseguire lo script SQL

Apri il browser e vai su: http://localhost:8080

Accedi a PgAdmin utilizzando le credenziali definite nel docker-compose.yml.

Esegui lo script SQL situato in <i>/backend/poc-ai-model/poc-ai-digical-branch/query.sql</i>

## ▶️ Avvio del server FastAPI

Sempre nella directory <i>/backend/poc-ai-model/poc-ai-digical-branch</i> digita il comando:

`uvicorn main:app --reload`

# 🎨 Frontend

Apri il terminale nella directory <i>/frontend/poc-ai-digical-branch</i> ed esegui:
```
npm install
npm run dev
```

### ✅ Il progetto è avviato sulle seguenti porte:

Backend: http://localhost:8000<br>
Frontend: http://localhost:5173