import os, re, csv

print('=== 1. CHECKING PROVINCE IDS ===')
with open('missions/EMX_Wu_Missions.txt', 'r', encoding='utf-8') as f:
    tree_text = f.read()

prov_ids = re.findall(r'(?:province_id|owns_core_province)\s*=\s*(\d+)', tree_text)
number_scopes = re.findall(r'(\d+)\s*=\s*\{', tree_text)
all_provs = set(prov_ids + number_scopes)

valid_provs = set()
if os.path.exists('map/definition.csv'):
    with open('map/definition.csv', 'r', encoding='latin-1') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row and row[0].isdigit():
                valid_provs.add(int(row[0]))

print(f'Provinces used in Wu tree: {sorted([int(x) for x in all_provs])}')
for p in all_provs:
    p_int = int(p)
    assert p_int in valid_provs, f'Invalid province ID: {p_int}'
print('All province IDs exist in map/definition.csv!')

print('\n=== 2. CHECKING AREAS AND REGIONS ===')
with open('map/area.txt', 'r', encoding='utf-8', errors='ignore') as f:
    area_text = f.read()
valid_areas = set(re.findall(r'([a-zA-Z0-9_]+_area)\s*=\s*\{', area_text))

with open('map/region.txt', 'r', encoding='utf-8', errors='ignore') as f:
    region_text = f.read()
valid_regions = set(re.findall(r'([a-zA-Z0-9_]+_region)\s*=\s*\{', region_text))

valid_superregions = {'china_superregion', 'east_asia_superregion'}

areas_used = re.findall(r'([a-zA-Z0-9_]+_area)\s*=\s*\{', tree_text)
for a in areas_used:
    assert a in valid_areas, f'INVALID AREA NAME: {a}'
    print(f'Area valid: {a}')

superregions_used = re.findall(r'([a-zA-Z0-9_]+_superregion)\s*=\s*\{', tree_text)
for sr in superregions_used:
    assert sr in valid_superregions, f'INVALID SUPERREGION NAME: {sr}'
    print(f'Superregion valid: {sr}')

print('\n=== 3. CHECKING REQUIRED MISSIONS & SLOTS ===')
missions = re.findall(r'(\bemx_[a-z0-9_]+)\s*=\s*\{', tree_text)
missions = [m for m in missions if not re.search(r'_(?:s\d|silk_s\d|spice_s\d)$', m)]
missions = list(dict.fromkeys(missions))
print(f'Missions found ({len(missions)}): {missions}')

req_missions = re.findall(r'required_missions\s*=\s*\{([^}]*)\}', tree_text)
for req_block in req_missions:
    for req in req_block.split():
        assert req in missions, f'Unknown required mission: {req}'
print('All required_missions link to existing missions!')

print('\n=== 4. CHECKING MODIFIERS DEFINITIONS ===')
with open('common/event_modifiers/04_emx_china_modifiers.txt', 'r', encoding='utf-8') as f:
    mod_text = f.read()

mods_used = re.findall(r'name\s*=\s*([a-z0-9_]+)', tree_text)
for mod in set(mods_used):
    assert f'{mod} =' in mod_text or f'{mod}=' in mod_text, f'Missing modifier: {mod}'
    print(f'Modifier valid: {mod}')

print('\n=== 5. CHECKING LOCALISATION KEYS ===')
with open('localisation/emx_wu_l_english.yml', 'r', encoding='utf-8') as f:
    loc_text = f.read()
with open('localisation/emx_silk_spice_l_english.yml', 'r', encoding='utf-8') as f:
    loc_text += '\n' + f.read()
with open('localisation/emx_china_l_english.yml', 'r', encoding='utf-8') as f:
    loc_text += '\n' + f.read()

for m in missions:
    assert f'{m}_title:' in loc_text, f'Missing title loc: {m}_title'
    assert f'{m}_desc:' in loc_text, f'Missing desc loc: {m}_desc'
    print(f'Loc valid for mission: {m}')

for mod in set(mods_used):
    assert f'{mod}:' in loc_text, f'Missing mod loc: {mod}'
    print(f'Loc valid for modifier: {mod}')

print('\n=== 6. CHECKING TRIGGERED MODIFIERS ===')
with open('common/triggered_modifiers/03_emx_wu_triggered_modifiers.txt', 'r', encoding='utf-8') as f:
    trig_text = f.read()

totf_trigs = re.findall(r'emx_wu_totf_(\d+)', trig_text)
ms_trigs = re.findall(r'emx_wu_ms_(\d+)', trig_text)
assert len(set(totf_trigs)) == 15, f'Expected 15 totf triggers, got {len(set(totf_trigs))}'
assert len(set(ms_trigs)) == 15, f'Expected 15 ms triggers, got {len(set(ms_trigs))}'
print(f'Triggered modifiers: 15 ToTF tiers and 15 MS tiers verified!')

print('\n=== ALL TESTS PASSED 100% PERFECTLY! ===')
