# BONG Notation Guide

**Build Order Notation Grammar** - A standardized notation system for Age of Empires II build orders.

## Table of Contents
1. [Overview](#overview)
2. [Basic Syntax](#basic-syntax)
3. [Subscript System](#subscript-system)
4. [Resource Types](#resource-types)
5. [Movement Notation](#movement-notation)
6. [Validation Rules](#validation-rules)
7. [Examples](#examples)
8. [Common Patterns](#common-patterns)

---

## Overview

BONG notation provides a precise, mathematical way to express Age of Empires II build orders. Each line represents villager assignments using images and subscripts to track exact worker counts.

### Key Principles
- **Subscripts track cumulative totals** at each resource
- **Images represent game entities** (units, buildings, resources)
- **Movement is explicit** using arrow notation (→)
- **Math must always validate** - subscripts must match metadata

---

## Basic Syntax

### Adding Workers
```
N - @category/image.png@subscript
```

**Example:**
```json
"6 - @animal/Sheep_aoe2DE.png@₆"
```
- `6` = number of workers added
- `@animal/Sheep_aoe2DE.png@` = resource image
- `₆` = cumulative total at this resource

### Moving Workers
```
N@source/image.png@source_subscript → @destination/image.png@dest_subscript
```

**Example:**
```json
"2@animal/Sheep_aoe2DE.png@₁₀ → @resource/BerryBushDE.png@₅"
```
- `2` = workers moved
- `@₁₀` = animals remaining after move
- `@₅` = berries total after move

### Research/Buildings Only
```
"@category/image.png@@category/image.png@"
```

**Example:**
```json
"@town_center/LoomDE.png@@age/FeudalAgeIconDE_alpha.png@"
```

---

## Subscript System

### Subscript Characters
Use Unicode subscript numerals: ₀₁₂₃₄₅₆₇₈₉

### Rules
1. **Subscripts show CUMULATIVE totals** (not deltas)
2. **Source subscripts show REMAINING** after workers leave
3. **Destination subscripts show TOTAL** after workers arrive
4. **Shared pools must use combined subscripts**

### Shared Resource Pools

Some resources share a subscript pool:

#### Wood Pool
```
Wood Total = Lumber Camp Workers + Straggler Tree Workers
```

**Example:**
```json
// Step 1: 4 lumber camp workers
"4 - @lumber_camp/Lumber_camp_aoe2de.png@₄"

// Step 2: Add 2 straggler workers
"2@animal/Sheep_aoe2DE.png@₈ → @resource/Aoe2de_wood.png@₆"
// Wood subscript = 4 (lumber) + 2 (straggler) = 6

// Later: Add 6 more to lumber camp
"6@animal/Sheep_aoe2DE.png@₀ → @lumber_camp/Lumber_camp_aoe2de.png@₁₂"
// Wood subscript = 10 (lumber) + 2 (straggler) = 12
```

#### Food Pool
```
Food Total = Animals + Berries + Farms + Fishing + Deer
```

---

## Resource Types

### Common Resources

| Category | Image Path | Type |
|----------|-----------|------|
| Sheep/Animals | `@animal/Sheep_aoe2DE.png@` | Food |
| Boar | `@animal/Boar_aoe2DE.png@` | Food |
| Deer | `@animal/Deer_aoe2DE.png@` | Food (no subscript) |
| Berries | `@resource/BerryBushDE.png@` | Food |
| Farms | `@mill/FarmDE.png@` | Food |
| Lumber Camp | `@lumber_camp/Lumber_camp_aoe2de.png@` | Wood |
| Straggler Trees | `@resource/Aoe2de_wood.png@` | Wood |
| Gold | `@resource/Aoe2de_gold.png@` | Gold |
| Stone | `@resource/Aoe2de_stone.png@` | Stone |

---

## Movement Notation

### Standard Movement
```
N@source@remaining → @destination@total
```

### Transitional Rally Points
When workers pass through intermediate locations:
```
N@source@remaining → @waypoint@ → @destination@total
```

**Example:**
```json
"6@animal/Sheep_aoe2DE.png@₀ → @animal/Deer_aoe2DE.png@ → @lumber_camp/Lumber_camp_aoe2de.png@₁₂"
```
- 6 workers from sheep
- Lure deer (transitional, no subscript)
- Go to lumber camp (subscript @₁₂)

### Temporary Builders
Workers who build then return to same resource:
```
N@source@ → @building1@@building2@ → @source@
```

**Example:**
```json
"2@resource/BerryBushDE.png@ → @blacksmith/Blacksmith_aoe2de.png@@archery_range/Archery_range_aoe2DE.png@ → @resource/BerryBushDE.png@"
```
- No subscripts needed (workers return to same place)

### Rally Point Symbol
Use `⛋` to indicate continuous production/rally:
```json
"@siege_workshop/Scorpion_aoe2DE.png@ → ⛋"
```

---

## Validation Rules

### Rule #1: Subscript Arithmetic
Every movement must validate mathematically:
```
source_before - workers_moved = source_after
dest_before + workers_moved = dest_after
```

### Rule #2: Shared Pool Tracking
Wood and food pools must track all sub-resources:
```
wood_subscript = lumber_workers + straggler_workers
food_subscript = animal_workers + berry_workers + farm_workers
```

### Rule #3: Never Hallucinate Workers
Total workers must match metadata exactly:
```
sum(all_workers_in_notes) = metadata.villager_count
```

### Rule #4: Cascading Updates
Changes ripple through subsequent steps:
```
If Step 2 changes → recalculate Step 3, Step 4, etc.
```

### Rule #5: Metadata Must Match Notes
```
metadata.resources.wood = lumber_workers + straggler_workers
metadata.resources.food = animals + berries + farms
metadata.resources.gold = gold_workers
metadata.resources.stone = stone_workers
```

### Rule #6: No Calculation Notation
Never show calculations in subscripts:
```
❌ "@resource/Aoe2de_wood.png@(3+2)"
✅ "@resource/Aoe2de_wood.png@₅"
```

### Rule #7: No Instructional Text
Remove all comments and instructions:
```
❌ "2@animal/Sheep@ → @wood@ (STRAGGLER TREE HERE)"
✅ "2@animal/Sheep@₈ → @resource/Aoe2de_wood.png@₆"
```

### Rule #8: Spacing Consistency
Always space before arrows:
```
❌ "@barracks@→ @gold@"
✅ "@barracks@ → @gold@"
```

### Rule #9: Source Subscript = Zero
When depleting a resource completely:
```
"6@animal/Sheep_aoe2DE.png@₀ → @lumber_camp/Lumber_camp_aoe2de.png@₁₂"
```

### Rule #10: Temporary Movements
Builders who return need no final subscript:
```
"2@berry@ → @blacksmith@ → @berry@"
```

### Rule #11: Movement Subscript Validation
Both source and destination subscripts required for movements:
```
❌ "2@animal@ → @berry@"
✅ "2@animal@₁₀ → @berry@₅"
```

---

## Examples

### Complete Dark Age Example
```json
{
    "age": 1,
    "villager_count": 19,
    "resources": {
        "wood": 4,
        "food": 14,
        "gold": 1,
        "stone": 0
    },
    "notes": [
        "6 - @animal/Sheep_aoe2DE.png@₆",
        "4 - @lumber_camp/Lumber_camp_aoe2de.png@₄",
        "1 - @animal/Boar_aoe2DE.png@₇",
        "3 - @other/House_aoe2DE.png@@mill/Mill_aoe2de.png@ @resource/BerryBushDE.png@₃",
        "1 - @animal/Sheep_aoe2DE.png@₈",
        "1 - @other/House_aoe2DE.png@@barracks/Barracks_aoe2DE.png@ → @resource/Aoe2de_gold.png@₁",
        "3 - @animal/Sheep_aoe2DE.png@₁₁",
        "@town_center/LoomDE.png@@age/FeudalAgeIconDE_alpha.png@",
        "@barracks/MilitiaDE.png@₃"
    ]
}
```

**Validation:**
- Workers: 6+4+1+3+1+1+3 = 19 ✓
- Food: 11 (animals) + 3 (berries) = 14 ✓
- Wood: 4 (lumber) = 4 ✓
- Gold: 1 ✓

### Feudal Transition Example
```json
{
    "age": 2,
    "villager_count": 19,
    "resources": {
        "wood": 12,
        "food": 5,
        "gold": 2,
        "stone": 0
    },
    "notes": [
        "2@animal/Sheep_aoe2DE.png@₉ → @resource/BerryBushDE.png@₅",
        "2@animal/Sheep_aoe2DE.png@₇ → @resource/Aoe2de_wood.png@₆",
        "1@animal/Sheep_aoe2DE.png@₆ → @resource/Aoe2de_gold.png@₂",
        "6@animal/Sheep_aoe2DE.png@₀ → @animal/Deer_aoe2DE.png@ → @lumber_camp/Lumber_camp_aoe2de.png@₁₂",
        "5@resource/BerryBushDE.png@₀ → @mill/FarmDE.png@₅"
    ]
}
```

**Validation:**
- Line 2: Wood subscript = 4 (existing lumber) + 2 (new straggler) = @₆ ✓
- Line 4: Wood subscript = 10 (lumber) + 2 (straggler) = @₁₂ ✓
- Total workers: 19 (no workers added) ✓

---

## Common Patterns

### Dark Age Opening
```json
"6 - @animal/Sheep_aoe2DE.png@₆",
"4 - @lumber_camp/Lumber_camp_aoe2de.png@₄",
"1 - @animal/Boar_aoe2DE.png@₇",
"3 - @mill/Mill_aoe2de.png@ @resource/BerryBushDE.png@₃"
```

### Feudal Age Transition
```json
"N@animal@X → @resource/BerryBushDE.png@Y",
"N@animal@X → @resource/Aoe2de_wood.png@Y",
"N@animal@₀ → @lumber_camp/Lumber_camp_aoe2de.png@Z"
```

### Building Construction
```json
"2@resource/BerryBushDE.png@ → @blacksmith/Blacksmith_aoe2de.png@ → @resource/BerryBushDE.png@"
```

### Military Production
```json
"@barracks/MilitiaDE.png@₃",
"@barracks/ManAtArmsUpgDE.png@"
```

---

## JSON Structure

### Complete Build Order Schema
```json
{
    "name": "BuildOrderName",
    "civilization": "Generic|CivName",
    "author": "AuthorName",
    "source": "Source description",
    "description": "Build order description",
    "build_order": [
        {
            "age": 1,
            "villager_count": 19,
            "resources": {
                "wood": 4,
                "food": 14,
                "gold": 1,
                "stone": 0
            },
            "notes": [
                "BONG notation lines..."
            ]
        }
    ]
}
```

### Metadata Fields
- **age**: 1 (Dark), 2 (Feudal), 3 (Castle), 4 (Imperial)
- **villager_count**: Total villagers at end of step (-1 for ongoing)
- **resources**: Current worker distribution
  - All values must match note calculations
  - Use -1 for ongoing/unknown counts
- **notes**: Array of BONG notation strings

---

## Best Practices

### 1. Always Validate Before Committing
Run through all 11 validation rules on every change.

### 2. Track Resource Pools Carefully
Wood and food have multiple sub-resources that share subscript pools.

### 3. Show Your Work
When debugging, create step-by-step resource tracking tables.

### 4. Update Cascading Steps
Any change to an early step requires recalculating all subsequent steps.

### 5. No Shortcuts
Never use calculation notation or instructional comments in final notation.

### 6. Double-Check Subscripts
The most common errors are in subscript arithmetic for shared pools.

### 7. Metadata Last
Calculate all subscripts from notes first, then derive metadata.

---

## Troubleshooting

### Common Errors

**Error: Subscript doesn't match**
- Check if resource is part of a shared pool
- Verify all previous movements in the pool
- Ensure cascading updates were applied

**Error: Worker count mismatch**
- Sum all "N -" additions
- Verify no workers were hallucinated
- Check that temporary builders return

**Error: Metadata doesn't validate**
- Recalculate from notes (notes are source of truth)
- Check for shared pool totals (wood, food)
- Verify all subscripts are current

### Validation Checklist

- [ ] All subscripts present and correct
- [ ] Shared pools properly summed
- [ ] No calculation notation (@₅, not @(3+2))
- [ ] No instructional text
- [ ] Spacing before arrows consistent
- [ ] Metadata matches note totals
- [ ] Worker count matches additions
- [ ] No hallucinated workers
- [ ] Cascading updates applied
- [ ] Temporary movements handled correctly

---

## Version History

- **v1.0** - Initial BONG specification
- **v1.1** - Added shared pool tracking rules
- **v1.2** - Clarified transitional rally points
- **v1.3** - Added temporary builder patterns
- **v1.4** - Standardized validation rules

---

## Contributing

When proposing changes to BONG notation:
1. Document the use case
2. Show before/after examples
3. Validate against all existing build orders
4. Update this specification
5. Add examples to demonstrate new pattern

---

## License

BONG Notation is open-source and free to use for Age of Empires II build order documentation.