import random
import string

def gerar_codigo_convite():
    """Gera um código de convite aleatório com 8 caracteres"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def salvar_codigos(codigos, arquivo='convites.txt'):
    """Salva os códigos gerados no arquivo de texto"""
    with open(arquivo, 'a') as f:
        for codigo in codigos:
            f.write(codigo + '\n')

# Gerar e salvar 10 códigos de convite
codigos = [gerar_codigo_convite() for _ in range(10)]
salvar_codigos(codigos)
