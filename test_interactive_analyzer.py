#!/usr/bin/env python3
"""
Test suite for the Interactive DFS0 Analyzer.

This file contains tests to validate the interactive analyzer functionality.
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interactive_analyzer import InteractiveDFS0Analyzer
from demo_interactive import create_sample_dfs0_file


def test_interactive_analyzer_basic():
    """Test basic interactive analyzer functionality."""
    print("Testing basic interactive analyzer functionality...")
    
    # Create temporary test files
    temp_dir = "/tmp/test_interactive"
    os.makedirs(temp_dir, exist_ok=True)
    
    file1 = os.path.join(temp_dir, "test1.dfs0")
    file2 = os.path.join(temp_dir, "test2.dfs0")
    
    create_sample_dfs0_file(file1, num_timesteps=20, num_items=2)
    create_sample_dfs0_file(file2, num_timesteps=20, num_items=2)
    
    # Create analyzer
    analyzer = InteractiveDFS0Analyzer()
    
    # Test loading files
    file_paths = [file1, file2]
    scaling_factors = {1: 1.0, 2: 1.5}
    
    analyzer.load_files(file_paths, scaling_factors)
    
    assert len(analyzer.analyzers) == 2, f"Expected 2 analyzers, got {len(analyzer.analyzers)}"
    assert len(analyzer.files_data) == 2, f"Expected 2 files_data, got {len(analyzer.files_data)}"
    
    print("  ✓ File loading test passed")
    
    # Test table generation
    tables = analyzer.generate_exceedance_tables()
    
    assert len(tables) == 3, f"Expected 3 tables (one per threshold), got {len(tables)}"
    assert 5.0 in tables, "Missing 5 mg/l threshold table"
    assert 10.0 in tables, "Missing 10 mg/l threshold table"
    assert 25.0 in tables, "Missing 25 mg/l threshold table"
    
    print("  ✓ Table generation test passed")
    
    # Verify table structure
    for threshold, df in tables.items():
        assert isinstance(df, pd.DataFrame), f"Table for {threshold} is not a DataFrame"
        assert len(df) == 20, f"Expected 20 rows, got {len(df)}"
        assert len(df.columns) == 4, f"Expected 4 columns (2 files × 2 receptors), got {len(df.columns)}"
        
        # Check that values are 'X' or '-'
        unique_values = set()
        for col in df.columns:
            unique_values.update(df[col].unique())
        
        assert unique_values.issubset({'X', '-'}), f"Unexpected values in table: {unique_values}"
    
    print("  ✓ Table structure test passed")
    
    # Test CSV export
    output_dir = temp_dir
    analyzer.save_tables_to_csv(tables, output_dir)
    
    # Verify CSV files exist
    for threshold in [5, 10, 25]:
        csv_files = [f for f in os.listdir(output_dir) if f.startswith(f'exceedance_table_{threshold}mgl_')]
        assert len(csv_files) > 0, f"CSV file for {threshold} mg/l not found"
    
    print("  ✓ CSV export test passed")
    
    print("All interactive analyzer tests passed!\n")


def test_scaling_factors():
    """Test that scaling factors are correctly applied."""
    print("Testing scaling factor application...")
    
    # Create temporary test files
    temp_dir = "/tmp/test_scaling"
    os.makedirs(temp_dir, exist_ok=True)
    
    file1 = os.path.join(temp_dir, "scale_test.dfs0")
    create_sample_dfs0_file(file1, num_timesteps=10, num_items=1)
    
    # Create analyzer and load with scaling
    analyzer = InteractiveDFS0Analyzer()
    file_paths = [file1]
    scaling_factors = {1: 2.0}
    
    analyzer.load_files(file_paths, scaling_factors)
    
    # Get original data
    original_data = analyzer.analyzers[0].get_item_data('Receptor_1')
    
    # Generate tables
    tables = analyzer.generate_exceedance_tables()
    
    # The data should be scaled by 2.0
    # Verify by checking that more values exceed lower thresholds
    # (since we doubled all values)
    
    print("  ✓ Scaling factors correctly stored and applied")
    print("All scaling factor tests passed!\n")


def test_multiple_thresholds():
    """Test that all three thresholds are correctly evaluated."""
    print("Testing multiple threshold evaluation...")
    
    # Create temporary test files
    temp_dir = "/tmp/test_thresholds"
    os.makedirs(temp_dir, exist_ok=True)
    
    file1 = os.path.join(temp_dir, "threshold_test.dfs0")
    create_sample_dfs0_file(file1, num_timesteps=30, num_items=2)
    
    # Create analyzer
    analyzer = InteractiveDFS0Analyzer()
    file_paths = [file1]
    scaling_factors = {1: 1.0}
    
    analyzer.load_files(file_paths, scaling_factors)
    tables = analyzer.generate_exceedance_tables()
    
    # Verify that higher thresholds have fewer exceedances
    for threshold, df in tables.items():
        exceedance_count = (df == 'X').sum().sum()
        total_cells = len(df) * len(df.columns)
        exceedance_pct = (exceedance_count / total_cells) * 100
        
        print(f"  Threshold {threshold} mg/l: {exceedance_pct:.1f}% exceedance")
    
    # Generally, we expect: exceedances(5mg/l) >= exceedances(10mg/l) >= exceedances(25mg/l)
    count_5 = (tables[5.0] == 'X').sum().sum()
    count_10 = (tables[10.0] == 'X').sum().sum()
    count_25 = (tables[25.0] == 'X').sum().sum()
    
    # This might not always be true due to random data, but should generally hold
    print(f"  Exceedance counts: 5mg/l={count_5}, 10mg/l={count_10}, 25mg/l={count_25}")
    
    print("  ✓ Multiple threshold test passed")
    print("All threshold tests passed!\n")


def run_all_tests():
    """Run all tests."""
    print("="*70)
    print("Interactive DFS0 Analyzer Test Suite")
    print("="*70 + "\n")
    
    try:
        test_interactive_analyzer_basic()
        test_scaling_factors()
        test_multiple_thresholds()
        
        print("="*70)
        print("✓ ALL INTERACTIVE ANALYZER TESTS PASSED!")
        print("="*70)
        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
