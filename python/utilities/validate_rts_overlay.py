#!/usr/bin/env python3
"""
RTS Overlay Structure Validation

Validates that build order JSON files are correctly structured for the RTS Overlay tool.
This checks syntax and structure (JSON format, required fields, data types).
This does NOT check BONG notation rules - use test_bong.py for that.
"""

import json
import sys
from pathlib import Path


def validate_structure(data: dict) -> tuple[bool, list[str]]:
    """Validate basic structure of a build order JSON.
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    
    # Check required top-level fields
    required_fields = ['name', 'build_order']
    for field in required_fields:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")
    
    if 'build_order' in data:
        if not isinstance(data['build_order'], list):
            errors.append("'build_order' must be a list")
        elif len(data['build_order']) == 0:
            errors.append("'build_order' must contain at least one step")
        else:
            # Validate each step
            for idx, step in enumerate(data['build_order']):
                step_num = idx + 1
                
                if not isinstance(step, dict):
                    errors.append(f"Step {step_num}: Must be a dictionary")
                    continue
                
                # Check required step fields
                if 'age' not in step:
                    errors.append(f"Step {step_num}: Missing required field 'age'")
                elif not isinstance(step['age'], int):
                    errors.append(f"Step {step_num}: 'age' must be an integer")
                
                if 'villager_count' not in step:
                    errors.append(f"Step {step_num}: Missing required field 'villager_count'")
                elif not isinstance(step['villager_count'], int):
                    errors.append(f"Step {step_num}: 'villager_count' must be an integer")
                
                if 'resources' not in step:
                    errors.append(f"Step {step_num}: Missing required field 'resources'")
                elif not isinstance(step['resources'], dict):
                    errors.append(f"Step {step_num}: 'resources' must be a dictionary")
                else:
                    required_resources = ['wood', 'food', 'gold', 'stone']
                    for resource in required_resources:
                        if resource not in step['resources']:
                            errors.append(f"Step {step_num}: Missing resource '{resource}'")
                        elif not isinstance(step['resources'][resource], int):
                            errors.append(f"Step {step_num}: Resource '{resource}' must be an integer")
                
                if 'notes' not in step:
                    errors.append(f"Step {step_num}: Missing required field 'notes'")
                elif not isinstance(step['notes'], list):
                    errors.append(f"Step {step_num}: 'notes' must be a list")
                elif len(step['notes']) == 0:
                    errors.append(f"Step {step_num}: 'notes' must contain at least one note")
                else:
                    for note_idx, note in enumerate(step['notes']):
                        if not isinstance(note, str):
                            errors.append(f"Step {step_num}, note {note_idx + 1}: Must be a string")
    
    return len(errors) == 0, errors


def validate_file(file_path: str) -> tuple[bool, list[str]]:
    """Validate a single JSON build order file for RTS Overlay structure.
    
    Returns:
        (is_valid, errors)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return validate_structure(data)
    
    except json.JSONDecodeError as e:
        return False, [f"JSON parse error: {e}"]
    except FileNotFoundError:
        return False, [f"File not found: {file_path}"]
    except Exception as e:
        return False, [f"Error reading file: {e}"]


def main():
    """Main entry point for RTS Overlay structure validation."""
    if len(sys.argv) < 2:
        print("Usage: python validate_rts_overlay.py <build_order_file.json> [<file2.json> ...]")
        print("   or: python validate_rts_overlay.py --directory <directory>")
        print("\nNote: This validates JSON structure only, not BONG notation.")
        print("      Use test_bong.py to validate BONG notation rules.")
        sys.exit(1)
    
    files_to_test = []
    
    if sys.argv[1] == '--directory':
        if len(sys.argv) < 3:
            print("Error: --directory requires a directory path")
            sys.exit(1)
        directory = Path(sys.argv[2])
        files_to_test = list(directory.glob('*.json'))
    else:
        files_to_test = [Path(f) for f in sys.argv[1:]]
    
    if not files_to_test:
        print("No JSON files found to validate")
        sys.exit(1)
    
    all_valid = True
    for file_path in files_to_test:
        print(f"\n{'='*60}")
        print(f"Validating RTS Overlay structure: {file_path.name}")
        print('='*60)
        
        is_valid, errors = validate_file(str(file_path))
        
        if is_valid:
            print("[VALID] - JSON structure is correct for RTS Overlay")
        else:
            all_valid = False
            print(f"\n[ERRORS] ({len(errors)}):")
            for error in errors:
                print(f"  - {error}")
    
    print(f"\n{'='*60}")
    if all_valid:
        print("All files passed RTS Overlay structure validation!")
        sys.exit(0)
    else:
        print("Some files failed validation.")
        sys.exit(1)


if __name__ == '__main__':
    main()
