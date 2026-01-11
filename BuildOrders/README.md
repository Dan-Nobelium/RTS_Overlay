# Build Orders Directory

This directory contains Age of Empires II build orders for the RTS Overlay tool.

## Directory Structure

- **`/Vanilla/`** - Archive folder containing original builds from buildorderguide.com or other sources
  - These files are kept unchanged for reference
  - May use simple text notation or older formats
  
- **`/Poly/`** - Active work folder containing builds converted to BONG notation
  - Builds are actively being improved and maintained
  - All builds here should use BONG (Build Order Notation Grammar) notation
  - Must pass all 11 BONG validation rules (see `BONG.md` in project root)

## Current Files

### Vanilla (Original/Reference)
- `CastleRushUnique.json` - Placeholder for castle rush unique unit build (to be filled)

### Poly (BONG Converted/Active)
- *(Currently empty - builds will be added here)*

### Root Level (To be organized)
The following files are currently in the root and should be organized:
- `RiseofBalance4.json` - Example BONG notation build (should move to `/Poly/`)
- `Archers.json` - Original build (should move to `/Vanilla/` or convert to `/Poly/`)
- Other `.json` files - To be organized

## Workflow

See `WORKFLOW.md` in this directory for detailed workflow instructions.

## Quick Start

1. **Create new build:**
   - Create JSON file in `/Vanilla/` with basic structure
   - Fill in build order data

2. **View locally:**
   - Open `docs/index.html` in browser
   - Paste JSON to see visual representation

3. **Convert to BONG:**
   - Copy file to `/Poly/`
   - Convert notation following `BONG.md` rules
   - Run validation: `python python/utilities/test_bong.py BuildOrders/Poly/YourFile.json`

4. **Iterate and improve:**
   - Make changes
   - Re-run validation
   - Test in visual editor

## Validation

Use the BONG validation tool to check your builds:

```bash
# Test a single file
python python/utilities/test_bong.py BuildOrders/Poly/RiseofBalance4.json

# Test all files in Poly directory
python python/utilities/test_bong.py --directory BuildOrders/Poly
```

## Resources

- **BONG Notation Guide:** See `BONG.md` in project root
- **Workflow Guide:** See `WORKFLOW.md` in this directory
- **Example Build:** `RiseofBalance4.json` (best example of BONG notation)
- **Visual Editor:** Open `docs/index.html` in browser
- **Online Editor:** https://rts-overlay.github.io/

