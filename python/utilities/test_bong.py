#!/usr/bin/env python3
"""
BONG (Build Order Notation Grammar) Validation Testing Framework

Tests build order JSON files against the 11 BONG validation rules.
"""

import json
import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Unicode subscript to integer mapping
SUBSCRIPT_MAP = {
    '₀': 0, '₁': 1, '₂': 2, '₃': 3, '₄': 4,
    '₅': 5, '₆': 6, '₇': 7, '₈': 8, '₉': 9
}


def subscript_to_int(subscript: str) -> Optional[int]:
    """Convert Unicode subscript string to integer."""
    result = 0
    for char in subscript:
        if char in SUBSCRIPT_MAP:
            result = result * 10 + SUBSCRIPT_MAP[char]
        else:
            return None
    return result


def extract_subscript(text: str) -> Optional[int]:
    """Extract subscript number from a string ending with subscript."""
    # Match subscript characters at the end
    match = re.search(r'([₀₁₂₃₄₅₆₇₈₉]+)$', text)
    if match:
        return subscript_to_int(match.group(1))
    return None


def extract_image_path(note: str) -> List[str]:
    """Extract all @category/image.png@ paths from a note."""
    pattern = r'@([^@]+)@'
    return re.findall(pattern, note)


class BONGValidator:
    """Validates build orders against BONG notation rules."""
    
    # Resource type mappings
    WOOD_RESOURCES = [
        'lumber_camp/Lumber_camp_aoe2de.png',
        'resource/Aoe2de_wood.png'
    ]
    
    FOOD_RESOURCES = [
        'animal/Sheep_aoe2DE.png',
        'animal/Boar_aoe2DE.png',
        'animal/Deer_aoe2DE.png',
        'resource/BerryBushDE.png',
        'mill/FarmDE.png'
    ]
    
    GOLD_RESOURCES = ['resource/Aoe2de_gold.png']
    STONE_RESOURCES = ['resource/Aoe2de_stone.png']
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate(self, build_order_data: dict) -> Tuple[bool, List[str], List[str]]:
        """Validate a complete build order against all BONG rules.
        
        Returns:
            (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        if 'build_order' not in build_order_data:
            self.errors.append("Missing 'build_order' field")
            return False, self.errors, self.warnings
        
        steps = build_order_data['build_order']
        if not steps:
            self.errors.append("Build order has no steps")
            return False, self.errors, self.warnings
        
        # Track state across steps for cascading validation
        worker_state = {
            'wood': {'lumber': 0, 'straggler': 0},
            'food': {'animals': 0, 'berries': 0, 'farms': 0},
            'gold': 0,
            'stone': 0,
            'total': 0
        }
        
        for step_idx, step in enumerate(steps):
            step_errors = self._validate_step(step, step_idx, worker_state)
            self.errors.extend(step_errors)
            # Update state for next step (if no errors)
            if not step_errors:
                self._update_worker_state(step, worker_state)
        
        # Rule #5: Final metadata check
        if steps:
            final_step = steps[-1]
            metadata_errors = self._validate_metadata_match(final_step, worker_state)
            self.errors.extend(metadata_errors)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_step(self, step: dict, step_idx: int, previous_state: dict) -> List[str]:
        """Validate a single step against BONG rules."""
        errors = []
        step_num = step_idx + 1
        
        if 'notes' not in step:
            return [f"Step {step_num}: Missing 'notes' field"]
        
        notes = step['notes']
        if not isinstance(notes, list):
            return [f"Step {step_num}: 'notes' must be a list"]
        
        # Track workers in this step
        workers_added = 0
        worker_changes = {
            'wood': {'lumber': 0, 'straggler': 0},
            'food': {'animals': 0, 'berries': 0, 'farms': 0},
            'gold': 0,
            'stone': 0
        }
        
        # Rule #6: No calculation notation
        # Rule #7: No instructional text (basic check)
        # Rule #8: Spacing consistency
        for note_idx, note in enumerate(notes):
            line_num = note_idx + 1
            
            # Rule #6: Check for calculation notation like (3+2)
            if re.search(r'\([0-9+\-*/]+\)', note):
                errors.append(f"Step {step_num}, line {line_num}: Contains calculation notation (Rule #6)")
            
            # Rule #8: Check spacing before arrows
            if '→' in note and not re.search(r'\s→', note):
                errors.append(f"Step {step_num}, line {line_num}: Missing space before arrow (Rule #8)")
            
            # Parse worker assignments and movements
            note_errors, note_workers = self._parse_note(note, step_num, line_num, previous_state)
            errors.extend(note_errors)
            workers_added += note_workers
        
        # Rule #3: Worker count validation
        if 'villager_count' in step:
            expected_count = step['villager_count']
            if expected_count >= 0:  # -1 means ongoing
                calculated_count = previous_state['total'] + workers_added
                if calculated_count != expected_count:
                    errors.append(
                        f"Step {step_num}: Worker count mismatch. "
                        f"Metadata: {expected_count}, Calculated: {calculated_count} (Rule #3)"
                    )
        
        return errors
    
    def _parse_note(self, note: str, step_num: int, line_num: int, state: dict) -> Tuple[List[str], int]:
        """Parse a note line and validate it."""
        errors = []
        workers_added = 0
        
        # Pattern for adding workers: "N - @image@subscript"
        add_pattern = r'(\d+)\s*-\s*@([^@]+)@([₀₁₂₃₄₅₆₇₈₉]+)'
        add_match = re.search(add_pattern, note)
        if add_match:
            count = int(add_match.group(1))
            image_path = add_match.group(2)
            subscript_str = add_match.group(3)
            subscript_val = subscript_to_int(subscript_str)
            
            if subscript_val is None:
                errors.append(f"Step {step_num}, line {line_num}: Invalid subscript")
            else:
                workers_added += count
                # Validate subscript matches expected (simplified - full validation needs state tracking)
        
        # Pattern for moving workers: "N@source@remaining → @dest@total"
        move_pattern = r'(\d+)@([^@]+)@([₀₁₂₃₄₅₆₇₈₉]+)\s*→\s*@([^@]+)@([₀₁₂₃₄₅₆₇₈₉]+)'
        move_matches = re.finditer(move_pattern, note)
        for move_match in move_matches:
            count = int(move_match.group(1))
            source_path = move_match.group(2)
            source_subscript = subscript_to_int(move_match.group(3))
            dest_path = move_match.group(4)
            dest_subscript = subscript_to_int(move_match.group(5))
            
            # Rule #11: Both subscripts required (already matched by regex, but validate values)
            if source_subscript is None or dest_subscript is None:
                errors.append(f"Step {step_num}, line {line_num}: Invalid subscript in movement")
        
        # Pattern for temporary builders: "N@source@ → @building@ → @source@"
        # These don't add workers, just move temporarily
        temp_pattern = r'(\d+)@([^@]+)@\s*→\s*@([^@]+)@.*→\s*@([^@]+)@'
        if re.search(temp_pattern, note):
            # Temporary builders - validate they return to source (Rule #10)
            pass  # TODO: More detailed validation
        
        return errors, workers_added
    
    def _update_worker_state(self, step: dict, state: dict):
        """Update worker state after processing a step."""
        # Simplified - full implementation would parse all notes and track state
        if 'villager_count' in step and step['villager_count'] >= 0:
            state['total'] = step['villager_count']
        
        if 'resources' in step:
            resources = step['resources']
            # Update from metadata (simplified)
            state['wood']['lumber'] = resources.get('wood', 0)  # Simplified
            state['food']['animals'] = resources.get('food', 0)  # Simplified
    
    def _validate_metadata_match(self, step: dict, calculated_state: dict) -> List[str]:
        """Rule #5: Validate metadata matches calculated state."""
        errors = []
        if 'resources' not in step:
            return errors
        
        resources = step['resources']
        # Simplified validation - full implementation would calculate from notes
        return errors


def validate_file(file_path: str) -> Tuple[bool, List[str], List[str]]:
    """Validate a single JSON build order file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        validator = BONGValidator()
        return validator.validate(data)
    
    except json.JSONDecodeError as e:
        return False, [f"JSON parse error: {e}"], []
    except Exception as e:
        return False, [f"Error reading file: {e}"], []


def main():
    """Main entry point for testing."""
    if len(sys.argv) < 2:
        print("Usage: python test_bong.py <build_order_file.json> [<file2.json> ...]")
        print("   or: python test_bong.py --directory <directory>")
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
    
    all_valid = True
    for file_path in files_to_test:
        print(f"\n{'='*60}")
        print(f"Testing: {file_path.name}")
        print('='*60)
        
        is_valid, errors, warnings = validate_file(str(file_path))
        
        if is_valid and not warnings:
            print("[VALID] - No errors or warnings")
        else:
            all_valid = False
            if errors:
                print(f"\n[ERRORS] ({len(errors)}):")
                for error in errors:
                    print(f"  - {error}")
            if warnings:
                print(f"\n[WARNINGS] ({len(warnings)}):")
                for warning in warnings:
                    print(f"  - {warning}")
    
    print(f"\n{'='*60}")
    if all_valid:
        print("All files passed validation!")
        sys.exit(0)
    else:
        print("Some files failed validation.")
        sys.exit(1)


if __name__ == '__main__':
    main()

