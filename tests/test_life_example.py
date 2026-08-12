import yaml
import json
from pathlib import Path

def test_life_simulation():
    repo_root = Path(__file__).parent.parent
    yaml_path = repo_root / "examples" / "LIFE_Impact_Simulation_V0.1.yaml"
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    entities = {e['id']: e for e in data['entities']}
    needs = {n['id']: n for n in data['needs']}
    offers = {o['id']: o for o in data['offers']}
    matches = {m['id']: m for m in data['matches']}
    events = {e['id']: e for e in data['impact_events']}
    
    # ✓ alle entity_id existieren in Needs und Offers
    for need in needs.values():
        assert need['owner_id'] in entities, f"Need {need['id']} verweist auf unbekannte Entity {need['owner_id']}"
        
    for offer in offers.values():
        assert offer['owner_id'] in entities, f"Offer {offer['id']} verweist auf unbekannte Entity {offer['owner_id']}"
        
    # ✓ alle need_id und offer_id existieren in Matches
    for match in matches.values():
        assert match['need_id'] in needs, f"Match {match['id']} verweist auf unbekannten Need {match['need_id']}"
        assert match['offer_id'] in offers, f"Match {match['id']} verweist auf unbekanntes Offer {match['offer_id']}"
        
        # ✓ Need und Offer sind kompatibel (gleiche Kategorie für diesen einfachen Test)
        need = needs[match['need_id']]
        offer = offers[match['offer_id']]
        assert need['category'] == offer['category'], f"Kategorie-Mismatch in Match {match['id']}: {need['category']} != {offer['category']}"
        
        # ✓ dieselbe Entity darf in diesem MVP nicht beide Seiten eines Matches sein
        assert need['owner_id'] != offer['owner_id'], f"Selbst-Match in {match['id']} durch {need['owner_id']}"

    # Ledger Mathematik prüfen
    calc_commons = 0
    calc_personal_direct = 0
    calc_dividends = 0.0
    
    for event in events.values():
        # ✓ alle match_id existieren in Events
        assert event['match_id'] in matches, f"Event {event['id']} verweist auf unbekannten Match {event['match_id']}"
        
        # ✓ Receiver-Credit == Giver-Credit
        assert event['receiver_credit'] == event['giver_credit'], f"Ungleiche Credits in Event {event['id']}"
        
        # ✓ Commons Impact == final_life
        assert event['commons_impact'] == event['final_life'], f"Commons Impact != final_life in Event {event['id']}"
        
        calc_commons += event['commons_impact']
        calc_personal_direct += event['receiver_credit'] + event['giver_credit']
        calc_dividends += event['community_dividend']

    # ✓ Dividendensumme und Ledger stimmen
    ledger = data['ledger']
    assert ledger['commons_impact'] == calc_commons, f"Commons Impact falsch: Soll {calc_commons}, Ist {ledger['commons_impact']}"
    assert ledger['personal_direct_credits'] == calc_personal_direct, f"Personal Direct falsch: Soll {calc_personal_direct}, Ist {ledger['personal_direct_credits']}"
    assert abs(ledger['total_dividend'] - calc_dividends) < 0.001, f"Dividende falsch: Soll {calc_dividends}, Ist {ledger['total_dividend']}"
    assert ledger['total_matches'] == len(matches)
    
    expected_personal_total = calc_personal_direct + calc_dividends
    assert abs(ledger['personal_ledger_total'] - expected_personal_total) < 0.001, f"Personal Total falsch: Soll {expected_personal_total}, Ist {ledger['personal_ledger_total']}"
    
    print("✅ Alle 10 Invarianten-Tests bestanden!")
    print(f"Commons Impact: {calc_commons}")
    print(f"Personal Direct: {calc_personal_direct}")
    print(f"Dividends: {calc_dividends:.1f}")
    print(f"Personal Total: {expected_personal_total:.1f}")

if __name__ == "__main__":
    test_life_simulation()
