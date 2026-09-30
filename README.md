# Martial Armory

A standalone RimWorld 1.6 mod adding classic D&D and historical non-magical melee weapons, physical shields, a mechanical **One-Handed vs. Two-Handed** equipment system, and active shield deflection/blocking.

---

## ⚔️ Weapons Included

| Weapon | Hands | Tech Level | Crafting Tier | Materials | Damage Profiles | Tactical Role |
|---|---|---|---|---|---|---|
| **Halberd** | **Two-Handed** | Medieval | `LongBlades` (Skill 5) | 90 Metallic / Woody | Cut (24 dmg), Stab (22 dmg, 45% AP), Poke (11 dmg) | Heavy polearm; devastating cleaves and armor-piercing reach |
| **Morningstar** | **One-Handed** | Medieval | `Smithing` (Skill 3) | 60 Metallic / Woody | Blunt (14.5 dmg, 25% AP), Stab (15 dmg, 30% AP), Poke (8.5 dmg) | Hybrid weapon dealing crushing impact and puncturing armor |
| **War Pick** | **One-Handed** | Medieval | `Smithing` (Skill 3) | 50 Metallic / Woody | Stab (17 dmg, 60% AP), Blunt (10 dmg), Poke (8 dmg) | Dedicated anti-armor beak to punch plate and mechanoids |
| **Scimitar** | **One-Handed** | Medieval | `Smithing` (Skill 3) | 50 Metallic / Woody | Cut (14.5 dmg, 1.7s cd), Stab (13 dmg), Blunt (8 dmg) | Fast curved sword with high bleed infliction |
| **Quarterstaff** | **Two-Handed** | Neolithic | Crafting Spot / Smithing (Skill 2) | 40 Woody / Metallic | Blunt (11 dmg, 1.5s cd), Poke (8 dmg, 1.5s cd) | Fast blunt staff for non-lethal subdue and early defense |

---

## 🛡️ Shields (One-Handed Only)

Equipped in the Belt/Shield apparel slot. Shields provide passive armor and active melee parry/missile block chances:

| Shield | Tech Level | Crafting | Materials | Base Melee Block | Base Ranged Block | Move Speed Offset | Coverage & Focus |
|---|---|---|---|---|---|---|---|
| **Buckler** | Neolithic | Crafting Spot / Smithing (Skill 2) | 30 Wood / Metal | 35% | 15% | 0.00 c/s | Lightweight forearm shield; high melee parry with no mobility loss |
| **Round Shield** | Neolithic | Crafting Spot / Smithing (Skill 3) | 45 Wood / Metal | 45% | 30% | -0.05 c/s | Balanced circular shield; solid melee & missile defense |
| **Kite Shield** | Medieval | `Smithing` (Skill 4) | 65 Metal / Wood | 50% | 45% | -0.10 c/s | Elongated teardrop knight shield guarding legs and torso |
| **Tower Shield** | Medieval | `Smithing` (Skill 5) | 100 Metal / Wood | 60% | 60% | -0.25 c/s | Heavy barrier for defensive walls; supreme arrow/strike deflection |

---

## ⚙️ Mechanics

1. **One-Handed vs. Two-Handed:**
   * Pawns cannot equip a shield while wielding a two-handed weapon (`MA_TwoHanded`), and cannot equip a two-handed weapon while holding a shield.
   * Switching between them safely drops or unequips the conflicting piece.
   * Vanilla two-handed weapons (Longsword, Spear, Warhammer, Greatbow, Pila) are automatically patched and integrated.
2. **Active Combat Blocking:**
   * Incoming melee and ranged attacks check against the pawn's shield block chance (scaled by Pawn Melee skill and Manipulation).
   * Successful blocks completely negate pawn damage, deflect attacks, and absorb wear damage into the shield's durability.

---

## Project Structure

```
MartialArmory/
├── About/
│   └── About.xml
├── Assemblies/
│   ├── 0Harmony.dll
│   └── MartialArmory.dll
├── Defs/
│   └── ThingDefs/
│       ├── Apparel_Shields.xml
│       └── Weapons_MartialArmory.xml
├── Languages/
│   └── English/
│       └── Keyed/
│           └── MartialArmory_Keys.xml
├── Patches/
│   └── Vanilla_TwoHandedWeapons.xml
├── Textures/
│   └── Things/
│       └── Item/
│           └── Equipment/
│               ├── Shield/
│               │   ├── Buckler.png
│               │   ├── KiteShield.png
│               │   ├── RoundShield.png
│               │   └── TowerShield.png
│               └── WeaponMelee/
│                   ├── Halberd.png
│                   ├── Morningstar.png
│                   ├── Quarterstaff.png
│                   ├── Scimitar.png
│                   └── WarPick.png
├── Source/
│   ├── MartialArmory/
│   │   ├── CompShield.cs
│   │   ├── HarmonyPatches/
│   │   │   ├── Patch_EquipmentUtility.cs
│   │   │   ├── Patch_Pawn_ApparelTracker.cs
│   │   │   ├── Patch_Pawn_EquipmentTracker.cs
│   │   │   └── Patch_Pawn_PreApplyDamage.cs
│   │   ├── MartialArmory.csproj
│   │   ├── MartialArmoryMod.cs
│   │   └── ShieldUtility.cs
│   └── MartialArmory.Tests/
│       ├── ContentValidationTests.cs
│       ├── MartialArmory.Tests.csproj
│       └── ShieldLogicTests.cs
├── tools/
│   └── generate_textures.py
└── test.sh
```

## Testing

Run all unit and validation tests:
```bash
./test.sh
```
