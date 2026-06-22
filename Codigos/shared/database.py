import os
import firebase_admin
from firebase_admin import credentials, firestore

# ==========================================
#       PADRÃO CRIACIONAL: SINGLETON
# ==========================================

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("⚙️ Inicializando conexão com o Firebase...")
            cls._instance = super(Database, cls).__new__(cls)
            
            diretorio = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(diretorio, "firebase-adminsdk.json")
            
            if not os.path.exists(path):
                raise FileNotFoundError(f"❌ CRÍTICO: Arquivo do Firebase não encontrado em: {path}")
                
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred)
            
            cls._instance.db = firestore.client()
            
        return cls._instance

    def get_db(self):
        return self.db