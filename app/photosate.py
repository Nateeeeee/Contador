from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os

# Escopos necessários para acessar o Google Photos
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def autenticar_google_photos():
    creds = None
    # Verifica se já existe um token de acesso salvo
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Se não houver credenciais válidas, solicita autenticação
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Salva as credenciais para uso futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return creds

def listar_albuns():
    creds = autenticar_google_photos()
    service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
    
    # Lista os álbuns
    resultados = service.albums().list(pageSize=50).execute()
    albuns = resultados.get('albums', [])
    
    # Exibe os álbuns e seus IDs
    for album in albuns:
        print(f"Título: {album['title']}")
        print(f"ID: {album['id']}")
        print("-" * 40)

if __name__ == '__main__':
    listar_albuns()