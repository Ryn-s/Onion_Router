"""
MODULE PROTOCOLE
Gère le formatage des messages réseaux sans utiliser JSON (interdit).
Format : HEADER|||DATA1|||DATA2...
"""

SEP = "|||"

def format_message(header, *args):
    """Crée une trame réseau standardisée"""
    payload = f"{header}"
    for arg in args:
        payload += f"{SEP}{str(arg)}"
    return payload

def parse_message(raw_data):
    """
    Découpe la trame reçue.
    Retourne (header, [liste_args])
    """
    try:
        if isinstance(raw_data, bytes):
            raw_data = raw_data.decode('utf-8')
            
        parts = raw_data.split(SEP)
        header = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        return header, args
    except Exception as e:
        print(f"[Proto] Erreur de parsing : {e}")
        return None, []