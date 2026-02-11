#!/usr/bin/env python3
"""
Demo script for the interactive DFS0 analyzer.

This creates sample DFS0 files and demonstrates the interactive analyzer functionality.
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import mikeio


def create_sample_dfs0_file(filepath: str, num_timesteps: int = 100, num_items: int = 3):
    """
    Create a sample DFS0 file for testing.
    
    Args:
        filepath: Path where to save the DFS0 file
        num_timesteps: Number of timesteps
        num_items: Number of items (receptors)
    """
    # Create time series
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    timestamps = pd.date_range(start=start_time, periods=num_timesteps, freq='h')
    
    # Create data for each item (receptor)
    data_arrays_raw = []
    item_names = []
    
    for i in range(num_items):
        # Generate random SSC data with some values exceeding thresholds
        # Mean value increases with receptor number
        mean_value = 8 + i * 5  # Receptor 1: ~8, Receptor 2: ~13, Receptor 3: ~18
        std_value = 5.0
        
        data = np.random.normal(mean_value, std_value, num_timesteps)
        # Ensure non-negative values
        data = np.maximum(data, 0)
        
        data_arrays_raw.append(data)
        item_names.append(f'Receptor_{i+1}')
    
    # Create mikeio Dataset
    from mikeio import Dataset, DataArray, ItemInfo, EUMType, EUMUnit
    
    data_arrays = []
    for i, (data, name) in enumerate(zip(data_arrays_raw, item_names)):
        da = DataArray(
            data=data,
            time=timestamps,
            name=name,
            type=EUMType.Concentration,
            unit=EUMUnit.gram_per_meter_pow_3
        )
        data_arrays.append(da)
    
    ds = Dataset(data_arrays)
    
    # Save to DFS0
    ds.to_dfs(filepath)
    print(f"Created sample DFS0: {filepath}")
    print(f"  - {num_items} receptors")
    print(f"  - {num_timesteps} timesteps")
    print(f"  - Time range: {timestamps[0]} to {timestamps[-1]}")
    return filepath


def demo_interactive_analyzer_with_mock_data():
    """
    Demonstrate the interactive analyzer with mock DFS0 files.
    """
    print("="*70)
    print("DEMO: Interactive DFS0 Analyzer")
    print("="*70)
    
    # Create temporary directory for sample files
    temp_dir = "/tmp/dfs0_demo"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Create sample DFS0 files
    print("\nCreating sample DFS0 files...")
    print("-"*70)
    
    file1 = os.path.join(temp_dir, "location1.dfs0")
    file2 = os.path.join(temp_dir, "location2.dfs0")
    file3 = os.path.join(temp_dir, "location3.dfs0")
    
    create_sample_dfs0_file(file1, num_timesteps=50, num_items=2)
    create_sample_dfs0_file(file2, num_timesteps=50, num_items=3)
    create_sample_dfs0_file(file3, num_timesteps=50, num_items=2)
    
    print("\n" + "="*70)
    print("Sample files created in:", temp_dir)
    print("="*70)
    print("\nTo run the interactive analyzer with these files:")
    print(f"  python interactive_analyzer.py")
    print("\nThen enter these paths when prompted:")
    print(f"  {file1}")
    print(f"  {file2}")
    print(f"  {file3}")
    print("\nExample scaling factors:")
    print("  1: 1.0")
    print("  2: 1.5")
    print("  3: 0.8")
    print("\n" + "="*70)
    
    return [file1, file2, file3]


def test_interactive_analyzer_programmatically():
    """
    Test the interactive analyzer programmatically (non-interactive).
    """
    from interactive_analyzer import InteractiveDFS0Analyzer
    import sys
    
    print("\n" + "="*70)
    print("PROGRAMMATIC TEST: Interactive DFS0 Analyzer")
    print("="*70)
    
    # Create sample files
    temp_dir = "/tmp/dfs0_test"
    os.makedirs(temp_dir, exist_ok=True)
    
    file1 = os.path.join(temp_dir, "test_location1.dfs0")
    file2 = os.path.join(temp_dir, "test_location2.dfs0")
    
    print("\nCreating test DFS0 files...")
    create_sample_dfs0_file(file1, num_timesteps=30, num_items=2)
    create_sample_dfs0_file(file2, num_timesteps=30, num_items=2)
    
    # Test the analyzer programmatically
    print("\n" + "="*70)
    print("Testing analyzer...")
    print("-"*70)
    
    analyzer = InteractiveDFS0Analyzer()
    
    # Manually set up the analyzer
    file_paths = [file1, file2]
    scaling_factors = {1: 1.0, 2: 1.5}
    
    print("Loading files programmatically...")
    analyzer.load_files(file_paths, scaling_factors)
    
    if analyzer.analyzers:
        print(f"✓ Loaded {len(analyzer.analyzers)} file(s)")
        
        print("\nGenerating exceedance tables...")
        tables = analyzer.generate_exceedance_tables()
        
        print(f"✓ Generated {len(tables)} table(s)")
        
        # Display summary
        print("\n" + "="*70)
        print("SUMMARY OF RESULTS")
        print("-"*70)
        
        for threshold, df in tables.items():
            print(f"\nThreshold: {threshold} mg/l")
            print(f"  Table dimensions: {df.shape[0]} timesteps × {df.shape[1]} receptors")
            
            # Count exceedances per receptor
            exceedance_counts = (df == 'X').sum()
            print(f"  Exceedance counts per receptor:")
            for receptor, count in exceedance_counts.items():
                percentage = (count / len(df)) * 100
                print(f"    {receptor}: {count}/{len(df)} ({percentage:.1f}%)")
        
        # Save tables
        output_dir = temp_dir
        print(f"\nSaving tables to: {output_dir}")
        analyzer.save_tables_to_csv(tables, output_dir)
        
        print("\n" + "="*70)
        print("TEST PASSED!")
        print("="*70)
    else:
        print("✗ Failed to load files")
        sys.exit(1)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        # Run programmatic test
        test_interactive_analyzer_programmatically()
    else:
        # Create demo files
        demo_interactive_analyzer_with_mock_data()
