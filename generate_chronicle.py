import os
import json
from glob import glob

SNAPSHOTS_DIR = 'public-snapshots'
CHRONICLE_FILE = os.path.join(SNAPSHOTS_DIR, 'chronicle.json')

def generate_chronicle():
    print("Starte Chronicle Generator...")
    
    if not os.path.exists(SNAPSHOTS_DIR):
        print(f"Ordner {SNAPSHOTS_DIR} existiert nicht. Abbruch.")
        return

    snapshot_files = [f for f in glob(os.path.join(SNAPSHOTS_DIR, '*.json')) if os.path.basename(f) != 'chronicle.json']
    
    chronicle = []
    
    for file_path in snapshot_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Extrahiere Metadaten aus dem ersten Item (oder aus den Metadaten des Snapshots)
            # Im neuen Schema (v0.1) haben wir summary, published_at, tags im Root.
            # Fallback auf item content, falls es alte Snapshots gibt.
            
            first_item = data.get('items', [{}])[0]
            
            entry_id = first_item.get('id', 'unknown')
            entry_type = first_item.get('type', 'unknown')
            entry_title = first_item.get('title', 'Ohne Titel')
            
            summary = data.get('summary') or first_item.get('description', '')
            published_at = data.get('published_at') or data.get('approved_at')
            tags = data.get('tags', [])
            status = data.get('status', 'published')
            
            if not published_at:
                print(f" [WARNUNG] {file_path} hat kein published_at. Setze an das Ende der Chronik.")
                published_at = '1970-01-01T00:00:00Z'
            
            date_str = published_at.split('T')[0]
            
            chronicle_entry = {
                "id": entry_id,
                "date": date_str,
                "published_at": published_at,
                "type": entry_type,
                "title": entry_title,
                "description": summary,
                "tags": tags,
                "status": status,
                "snapshot_hash": data.get('snapshot_hash', '')
            }
            
            if status == 'withdrawn':
                chronicle_entry['withdrawn_at'] = data.get('withdrawn_at')
                chronicle_entry['withdrawal_reason'] = data.get('withdrawal_reason')
            
            chronicle.append(chronicle_entry)
            print(f" [+] Gelesen: {os.path.basename(file_path)}")
            
        except json.JSONDecodeError:
            print(f" [!] ÜBERSPRUNGEN: {file_path} enthält ungültiges JSON.")
        except Exception as e:
            print(f" [!] Fehler beim Lesen von {file_path}: {e}")

    # Nach Veröffentlichungsdatum absteigend sortieren (neueste zuerst)
    chronicle.sort(key=lambda x: x['published_at'], reverse=True)
    
    with open(CHRONICLE_FILE, 'w', encoding='utf-8') as f:
        json.dump(chronicle, f, indent=2, ensure_ascii=False)
        
    print(f"Erfolgreich! {len(chronicle)} Einträge in {CHRONICLE_FILE} generiert.")

if __name__ == '__main__':
    generate_chronicle()
