import json
import pandas as pd

def parse_stix_and_logs(stix_file_path):
    """
    Ingests STIX 2.1 JSON files and extracts structured event records 
    containing timestamps, adversarial techniques, and observable indicators.
    """
    print(f"[*] Ingesting threat data from: {stix_file_path}")
    
    try:
        with open(stix_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"[!] Warning: {stix_file_path} not found. Initializing mock schema for validation.")
        data = {"objects": []}

    records = []
    for obj in data.get("objects", []):
        if obj.get("type") == "attack-pattern":
            technique_id = "UNKNOWN"
            for ref in obj.get("external_references", []):
                if ref.get("source_name") == "mitre-attack":
                    technique_id = ref.get("external_id")
            
            records.append({
                "id": obj.get("id"),
                "name": obj.get("name"),
                "technique_id": technique_id,
                "description": obj.get("description", "")
            })
            
    df = pd.DataFrame(records)
    print(f"[+] Successfully extracted {len(df)} threat records.")
    return df

if __name__ == "__main__":
    sample_df = parse_stix_and_logs("data/raw/stix_feed.json")
