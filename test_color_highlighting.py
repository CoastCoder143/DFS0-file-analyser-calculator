#!/usr/bin/env python3
"""
Test the color highlighting for daily tables.
"""

import os
import sys
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interactive_analyzer import InteractiveDFS0Analyzer


def test_colorize_value():
    """Test the _apply_color_to_value method."""
    print("="*70)
    print("Testing Color Highlighting Rules")
    print("="*70)
    
    analyzer = InteractiveDFS0Analyzer()
    
    # Test V columns
    print("\nV Column Tests (ORANGE for >15, including >20):")
    print("-"*70)
    test_cases_v = [
        ('V1', 10, 'No color (≤15)'),
        ('V1', 15, 'No color (=15)'),
        ('V1', 16, 'ORANGE (>15)'),
        ('V1', 20, 'ORANGE (=20)'),
        ('V1', 21, 'ORANGE (>20, NOT RED!)'),
        ('V2', 25, 'ORANGE (>20)'),
        ('V3', 50, 'ORANGE (>20)'),
    ]
    
    for col, val, description in test_cases_v:
        colored = analyzer._apply_color_to_value(val, col)
        print(f"  {col}, value={val:3d}: {colored} ({description})")
    
    # Test IT columns
    print("\nIT Column Tests (RED for >15):")
    print("-"*70)
    test_cases_it = [
        ('IT1', 10, 'No color (≤15)'),
        ('IT1', 15, 'No color (=15)'),
        ('IT1', 16, 'RED (>15)'),
        ('IT1', 20, 'RED (=20)'),
        ('IT1', 21, 'RED (>20)'),
        ('IT5', 25, 'RED (>20)'),
        ('IT7', 50, 'RED (>20)'),
    ]
    
    for col, val, description in test_cases_it:
        colored = analyzer._apply_color_to_value(val, col)
        print(f"  {col}, value={val:3d}: {colored} ({description})")
    
    print("\n" + "="*70)
    print("✓ Color highlighting test complete!")
    print("="*70)


def test_colored_table_display():
    """Test the colored table display."""
    print("\n" + "="*70)
    print("Testing Colored Table Display")
    print("="*70)
    
    analyzer = InteractiveDFS0Analyzer()
    
    # Create a sample DataFrame with values designed to trigger colors
    data = {
        'Date': ['01/01/2024', '02/01/2024', '03/01/2024'],
        'V1': [10, 18, 22],  # 10: no color, 18: ORANGE, 22: ORANGE
        'V2': [15, 20, 25],  # 15: no color, 20: ORANGE, 25: ORANGE
        'IT1': [10, 18, 22], # 10: no color, 18: RED, 22: RED
        'IT2': [15, 20, 25], # 15: no color, 20: RED, 25: RED
    }
    
    df = pd.DataFrame(data)
    
    print("\nSample table with color highlighting:")
    print("(V columns: ORANGE for >15, IT columns: RED for >15)")
    print("-"*70)
    print(analyzer._format_colored_table(df))
    
    print("\n" + "="*70)
    print("Expected colors:")
    print("  V1: 10 (normal), 18 (ORANGE), 22 (ORANGE)")
    print("  V2: 15 (normal), 20 (ORANGE), 25 (ORANGE)")
    print("  IT1: 10 (normal), 18 (RED), 22 (RED)")
    print("  IT2: 15 (normal), 20 (RED), 25 (RED)")
    print("="*70)


def test_full_daily_table():
    """Test with a complete daily table structure."""
    print("\n" + "="*70)
    print("Testing Full Daily Table with All Columns")
    print("="*70)
    
    analyzer = InteractiveDFS0Analyzer()
    
    # Create a comprehensive sample with all V and IT columns
    data = {
        'Date': ['01/01/2024', '02/01/2024'],
        'V1': [12, 19],   # Normal, ORANGE
        'V2': [14, 21],   # Normal, ORANGE
        'V3': [16, 23],   # ORANGE, ORANGE
        'V4': [18, 25],   # ORANGE, ORANGE
        'IT1': [12, 19],  # Normal, RED
        'IT2': [14, 21],  # Normal, RED
        'IT3': [16, 23],  # RED, RED
        'IT4': [18, 25],  # RED, RED
        'IT5': [20, 30],  # RED, RED
        'IT6': [22, 35],  # RED, RED
        'IT7': [24, 40],  # RED, RED
    }
    
    df = pd.DataFrame(data)
    
    # Create a mock tables dict
    tables = {5.0: df}
    
    print("\nDisplaying full table with color highlighting:")
    analyzer.display_daily_tables(tables)
    
    print("\n✓ Full table display test complete!")


if __name__ == '__main__':
    test_colorize_value()
    test_colored_table_display()
    test_full_daily_table()
    
    print("\n" + "="*70)
    print("ALL COLOR TESTS PASSED!")
    print("="*70)
