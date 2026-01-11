# Setup Complete - Build Order Workflow

All setup tasks have been completed. Here's what was created:

## ✅ Completed Tasks

### 1. Folder Structure Created
- **`/BuildOrders/Vanilla/`** - Archive folder for original builds (unchanged reference)
- **`/BuildOrders/Poly/`** - Active work folder for BONG-converted builds

### 2. Placeholder File Created
- **`/BuildOrders/Vanilla/CastleRushUnique.json`** - Ready for you to fill in the build order data

### 3. BONG Validation Testing Framework Created
- **`/python/utilities/test_bong.py`** - Automated testing tool that validates build orders against all 11 BONG rules
- Can test single files or entire directories
- Fixed Windows Unicode encoding issues

### 4. Documentation Created
- **`/BuildOrders/WORKFLOW.md`** - Complete workflow guide
- **`/BuildOrders/README.md`** - Directory overview and quick reference

## 📋 Next Steps

### Step 1: Fill in CastleRushUnique.json
1. Open `/BuildOrders/Vanilla/CastleRushUnique.json`
2. Enter your build order data (can use simple text notation initially)
3. Fill in name, civilization, author, source, description
4. Add build order steps with notes

### Step 2: View Your Build Locally
1. Open `docs/index.html` in your web browser (Chrome or Edge recommended)
2. Copy/paste the JSON content into the "Design your own" section
3. See images rendered inline (images must be in `/docs/assets/aoe2/`)

### Step 3: Convert to BONG Notation
1. Copy `/BuildOrders/Vanilla/CastleRushUnique.json` to `/BuildOrders/Poly/CastleRushUnique.json`
2. Convert notation following BONG.md rules:
   - Replace text with image references: `@category/image.png@`
   - Add Unicode subscripts (₀₁₂₃₄₅₆₇₈₉) to track worker counts
   - Use arrow notation (`→`) for worker movements
   - Reference `/BONG.md` for detailed rules

### Step 4: Validate with Testing Framework
```bash
# From project root
python python/utilities/test_bong.py BuildOrders/Poly/CastleRushUnique.json

# Or test all files in Poly
python python/utilities/test_bong.py --directory BuildOrders/Poly
```

### Step 5: Iterate and Improve
1. Fix any validation errors
2. Test in visual editor (`docs/index.html`)
3. Make improvements to the build order
4. Re-run validation
5. Repeat until complete

## 🎯 Local Viewing Option

**You can run the visual editor locally!**

Simply open `docs/index.html` in your web browser:
- Chrome or Edge work best
- No server needed - just open the file
- Images display inline as you type
- Much faster than using the online version

## 📚 Resources

- **BONG Notation Guide:** `/BONG.md` (project root)
- **Workflow Guide:** `/BuildOrders/WORKFLOW.md`
- **Example Build:** `/BuildOrders/RiseofBalance4.json` (best BONG example)
- **Visual Editor:** Open `/docs/index.html` in browser
- **Online Editor:** https://rts-overlay.github.io/ (slower, but works)

## 🔧 Testing Commands

```bash
# Test single file
python python/utilities/test_bong.py BuildOrders/Poly/YourFile.json

# Test all files in Poly directory
python python/utilities/test_bong.py --directory BuildOrders/Poly

# Test all files in Vanilla directory
python python/utilities/test_bong.py --directory BuildOrders/Vanilla
```

## 📝 Current Status

- ✅ Folder structure created
- ✅ Placeholder file ready
- ✅ Testing framework ready
- ✅ Documentation complete
- ⏭️ **Waiting for you to fill in CastleRushUnique.json**

Once you've entered the build order data, we'll proceed with:
1. Testing the build order
2. Converting to BONG notation
3. Testing again
4. Making improvements

## 💡 Tips

1. **Start simple:** Begin with basic text notation, then convert to BONG
2. **Use the visual editor:** Open `docs/index.html` to see images inline
3. **Reference the example:** Look at `RiseofBalance4.json` for BONG notation patterns
4. **Run tests often:** Validate frequently as you work
5. **Follow BONG.md:** All 11 rules must be satisfied

Ready to begin! Fill in CastleRushUnique.json and we'll proceed step by step.

