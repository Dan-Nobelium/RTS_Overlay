# Build Order Workflow Guide

This document describes the workflow for creating and maintaining Age of Empires II build orders using BONG notation.

## Folder Structure

- **`/BuildOrders/Vanilla/`** - Archive folder containing original builds from buildorderguide.com or other sources, kept unchanged for reference
- **`/BuildOrders/Poly/`** - Active work folder containing builds converted to BONG notation and actively being improved

## Workflow Steps

### 1. Adding a New Build Order

1. **Create placeholder in Vanilla:**
   - Create a new JSON file in `/BuildOrders/Vanilla/` with basic structure
   - Example: `CastleRushUnique.json`

2. **Enter build order data:**
   - Fill in the JSON structure with the build order information
   - Use simple text notation initially (can be from buildorderguide.com format)

3. **View and validate locally:**
   - Open `docs/index.html` in a web browser (Chrome or Edge recommended)
   - This provides the visual editor with inline PNG image display
   - Copy/paste your JSON into the interface to see images rendered

### 2. Converting to BONG Notation

1. **Copy to Poly folder:**
   - Copy the JSON file from `/Vanilla/` to `/Poly/`
   - This becomes your working copy

2. **Convert notation:**
   - Replace text descriptions with image references: `@category/image.png@`
   - Add Unicode subscripts (₀₁₂₃₄₅₆₇₈₉) to track worker counts
   - Add arrow notation (`→`) for worker movements
   - Reference `BONG.md` for full notation rules

3. **Validate with testing framework:**
   ```bash
   cd python/utilities
   python test_bong.py ../BuildOrders/Poly/YourBuildOrder.json
   ```
   Or test all files in a directory:
   ```bash
   python test_bong.py --directory ../../BuildOrders/Poly
   ```

4. **Test in visual editor:**
   - Open `docs/index.html` in browser
   - Copy/paste the BONG-formatted JSON
   - Verify images load correctly and notation displays properly

### 3. Iterative Improvement

1. **Make changes to the build order** (in `/Poly/` folder)

2. **Run validation tests:**
   - Use `test_bong.py` to check against all 11 BONG rules
   - Fix any errors reported

3. **Test visually:**
   - Use `docs/index.html` to verify appearance
   - Ensure all images load (images must be in `/docs/assets/aoe2/`)

4. **Repeat** until build order is complete and validated

## Validation Rules (BONG)

All build orders in `/Poly/` must pass all 11 validation rules (see `BONG.md` for details):

1. **Subscript Arithmetic** - Movement math must validate
2. **Shared Pool Tracking** - Wood and food pools must sum correctly
3. **No Hallucinated Workers** - Total workers match metadata
4. **Cascading Updates** - Changes propagate to later steps
5. **Metadata Must Match Notes** - Resource counts match calculations
6. **No Calculation Notation** - Subscripts show final numbers only
7. **No Instructional Text** - Remove comments and instructions
8. **Spacing Consistency** - Space before arrows (` → `)
9. **Source Subscript = Zero** - Depleted resources show `@₀`
10. **Temporary Movements** - Builders who return need no final subscript
11. **Movement Subscript Validation** - Both source and dest subscripts required

## Image Assets

- All images must be in `/docs/assets/aoe2/` directory structure
- Images are organized by category (animal, barracks, lumber_camp, etc.)
- Image format: `@category/image.png@`
- Example: `@animal/Sheep_aoe2DE.png@`

## Local Viewing

**Recommended Method:**
1. Open `docs/index.html` in a web browser (Chrome or Edge work best)
2. Paste JSON into the "Design your own" section
3. Images will display inline in the visual editor

**Alternative:**
- Use the online version at https://rts-overlay.github.io/
- Copy/paste JSON to see visual representation
- Note: Online version is slower but works the same way

## Testing Commands

### Validate a single file:
```bash
cd python/utilities
python test_bong.py ../../BuildOrders/Poly/RiseofBalance4.json
```

### Validate all files in a directory:
```bash
python test_bong.py --directory ../../BuildOrders/Poly
```

### Validate all vanilla files:
```bash
python test_bong.py --directory ../../BuildOrders/Vanilla
```

## Example: RiseofBalance4.json

This is our best example of BONG notation implementation:
- Located in: `/BuildOrders/RiseofBalance4.json` (currently)
- Uses: Full PNG style with subscript notation
- Tracks: Worker movement step-by-step
- Reference: Use this as a template for new builds

## Next Steps

When working on a new build order:

1. ✅ Create placeholder in `/Vanilla/`
2. ✅ Enter build order data
3. ⏭️ Copy to `/Poly/` and convert to BONG
4. ⏭️ Run validation tests
5. ⏭️ Test in visual editor (`docs/index.html`)
6. ⏭️ Iterate and improve
7. ⏭️ Final validation and review

