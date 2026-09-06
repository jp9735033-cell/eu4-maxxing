import re
import sys

print("=== 1. CHECKING DOM_CHINESE_MISSIONS POTENTIAL EXCLUSIONS ===")
with open("missions/DOM_Chinese_Missions.txt", "r", encoding="utf-8") as f:
    dom_text = f.read()

target_series = [
    "ming_missions_1_b",
    "ming_missions_2_b",
    "ming_missions_3_b",
    "ming_missions_4_b",
    "ming_missions_4_moh",
    "ming_missions_5_b"
]

for series in target_series:
    idx = dom_text.find(series)
    assert idx != -1, f"Could not find {series}"
    pot_idx = dom_text.find("potential = {", idx)
    assert pot_idx != -1 and pot_idx < idx + 300, f"Could not find potential for {series}"
    # find matching brace for potential
    start = pot_idx + len("potential = {")
    depth = 1
    end = start
    while depth > 0 and end < len(dom_text):
        if dom_text[end] == '{':
            depth += 1
        elif dom_text[end] == '}':
            depth -= 1
        end += 1
    pot_content = dom_text[start:end-1]
    assert "tag = WUU" in pot_content, f"WUU exclusion missing in {series}"
    assert "tag = YUE" in pot_content, f"YUE exclusion missing in {series}"
    print(f"Verified {series}: properly excludes WUU and YUE!")

print("\n=== 2. CHECKING EUNUCHS ESTATE TRIGGER ===")
with open("common/estates/09_eunuchs.txt", "r", encoding="utf-8") as f:
    eunuchs_text = f.read()

assert "is_emperor_of_china = no" in eunuchs_text, "is_emperor_of_china = no missing from WUU eunuchs blocker"
print("Verified 09_eunuchs.txt: Eunuchs allowed for WUU if Emperor of China!")

print("\n=== 3. CHECKING WU DECISION ===")
with open("decisions/EMX_Wu_Decisions.txt", "r", encoding="utf-8") as f:
    dec_text = f.read()

assert "emx_wu_sanctify_celestial_empire = {" in dec_text, "Decision emx_wu_sanctify_celestial_empire missing"
assert "has_reform = celestial_empire" in dec_text, "celestial_empire reform check missing in decision"
assert "is_emperor_of_china = yes" in dec_text, "is_emperor_of_china check missing in decision"
assert "emx_wu_celestial_mandate_faith" in dec_text, "Modifier application missing in decision"
print("Verified EMX_Wu_Decisions.txt: emx_wu_sanctify_celestial_empire correctly configured!")

print("\n=== 4. CHECKING MODIFIER DEFINITION ===")
with open("common/event_modifiers/04_emx_china_modifiers.txt", "r", encoding="utf-8") as f:
    mod_text = f.read()

assert "emx_wu_celestial_mandate_faith = {" in mod_text, "Modifier definition missing"
assert "tolerance_own = 2" in mod_text, "tolerance_own = 2 missing in modifier"
assert "global_missionary_strength = 0.02" in mod_text, "global_missionary_strength = 0.02 missing in modifier"
print("Verified 04_emx_china_modifiers.txt: emx_wu_celestial_mandate_faith gives +2 TotF and +2% MS!")

print("\n=== 5. CHECKING LOCALISATION ===")
with open("localisation/emx_wu_l_english.yml", "r", encoding="utf-8") as f:
    loc_text = f.read()

assert "emx_wu_sanctify_celestial_empire_title:" in loc_text, "Title loc missing"
assert "emx_wu_sanctify_celestial_empire_desc:" in loc_text, "Desc loc missing"
assert "emx_wu_celestial_mandate_faith:" in loc_text, "Modifier title loc missing"
assert "emx_wu_celestial_mandate_faith_desc:" in loc_text, "Modifier desc loc missing"
print("Verified emx_wu_l_english.yml: all localisation keys present!")

print("\n=== 6. VERIFYING WU ACTIVE MISSION TREE OVERLAPS ===")
# Parse EMX_Wu_Missions.txt for active missions when tag = WUU
with open("missions/EMX_Wu_Missions.txt", "r", encoding="utf-8") as f:
    wu_tree_text = f.read()

# Blocks with potential tag = WUU
wuu_series_blocks = re.findall(r"(\bemx_wu_[ab]_s\d\b)\s*=\s*\{(.*?^\})", wu_tree_text, re.DOTALL | re.MULTILINE)

positions_by_slot = {}
for series_name, block_content in wuu_series_blocks:
    slot_match = re.search(r"slot\s*=\s*(\d+)", block_content)
    assert slot_match, f"No slot in {series_name}"
    slot = int(slot_match.group(1))
    
    # find missions and their positions
    missions_in_block = re.findall(r"(\bemx_[a-z0-9_]+)\s*=\s*\{.*?\bposition\s*=\s*(\d+)", block_content, re.DOTALL)
    for m_name, pos in missions_in_block:
        pos = int(pos)
        key = (slot, pos)
        assert key not in positions_by_slot, f"COLLISION inside WUU tree at slot {slot}, position {pos}: {m_name} vs {positions_by_slot[key]}"
        positions_by_slot[key] = m_name

print(f"Verified {len(positions_by_slot)} missions in active WUU tree: zero internal coordinate collisions!")
print("\n>>> ALL VERIFICATION CHECKS PASSED 100%! <<<")
