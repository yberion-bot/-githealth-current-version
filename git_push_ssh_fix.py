# Git SSH Quick-Fix Script
# Ziel: Überprüfen, dass dein Git SSH Key korrekt erkannt wird und Push möglich ist

import subprocess
import sys

# 1. Teste SSH-Verbindung
def test_ssh():
    try:
        result = subprocess.run(['ssh', '-T', 'git@github.com'], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        if 'successfully authenticated' in result.stderr.lower():
            print('\u2705 SSH Key funktioniert korrekt.')
        else:
            print('\u26A0️ SSH Key wird nicht erkannt! Prüfe GitHub Settings.')
    except Exception as e:
        print(f'Fehler beim Testen der SSH-Verbindung: {e}')

# 2. Zeige aktuellen Remote

def show_remote():
    subprocess.run(['git', 'remote', '-v'])

# 3. Push Test
def test_push():
    try:
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
    except subprocess.CalledProcessError as e:
        print(f'Push fehlgeschlagen: {e}')

if __name__ == '__main__':
    print('=== SSH Test ===')
    test_ssh()
    print('\n=== Remote prüfen ===')
    show_remote()
    print('\n=== Push Test ===')
    test_push()
