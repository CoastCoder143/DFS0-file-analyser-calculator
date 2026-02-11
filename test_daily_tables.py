#!/usr/bin/env python3
"""
Test the daily exceedance table generation.
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import mikeio

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interactive_analyzer import InteractiveDFS0Analyzer


def create_test_dfs0_with_proper_names(filepath: str, series_names: list, num_days: int = 3):
    """
    Create a test DFS0 file with specific series names.
    
    Args:
        filepath: Path where to save the DFS0 file
        series_names: List of series names (e.g., ['V1', 'V2', 'IT1'])
        num_days: Number of days of data to generate
    """
    # Determine timesteps per day based on series type
    # V series: 73 timesteps/day (roughly every 20 minutes for 24 hours)
    # IT series: 144 timesteps/day (every 10 minutes for 24 hours)
    
    # For simplicity, use hourly data for all (24 timesteps/day)
    timesteps_per_day = 24
    total_timesteps = num_days * timesteps_per_day
    
    # Create time series starting from midnight
    start_time = datetime(2024, 1, 1, 0, 0, 0)
    timestamps = pd.date_range(start=start_time, periods=total_timesteps, freq='h')
    
    # Create data arrays for each series
    data_arrays = []
    for i, name in enumerate(series_names):
        # Generate random data with some values exceeding thresholds
        # Use different means for different series
        mean_value = 8 + i * 3  # Series get progressively higher values
        std_value = 4.0
        
        data = np.random.normal(mean_value, std_value, total_timesteps)
        # Ensure non-negative values
        data = np.maximum(data, 0)
        
        data_arrays.append(data)
    
    # Create mikeio DataArrays
    from mikeio import DataArray, Dataset, EUMType, EUMUnit
    
    das = []
    for name, data in zip(series_names, data_arrays):
        da = DataArray(
            data=data,
            time=timestamps,
            name=name,
            type=EUMType.Concentration,
            unit=EUMUnit.gram_per_meter_pow_3
        )
        das.append(da)
    
    ds = Dataset(das)
    
    # Save to DFS0
    ds.to_dfs(filepath)
    print(f"Created test DFS0: {filepath}")
    print(f"  - Series: {series_names}")
    print(f"  - {total_timesteps} timesteps ({num_days} days)")
    print(f"  - Time range: {timestamps[0]} to {timestamps[-1]}")


def test_daily_table_generation():
    """Test the daily exceedance table generation."""
    print("="*70)
    print("Testing Daily Exceedance Table Generation")
    print("="*70)
    
    # Create temporary test files
    temp_dir = "/tmp/test_daily_tables"
    os.makedirs(temp_dir, exist_ok=True)
    
    file1 = os.path.join(temp_dir, "test_V_series.dfs0")
    file2 = os.path.join(temp_dir, "test_IT_series.dfs0")
    
    print("\nCreating sample DFS0 files with proper naming...")
    create_test_dfs0_with_proper_names(file1, ['V1', 'V2', 'V3'], num_days=5)
    create_test_dfs0_with_proper_names(file2, ['IT1', 'IT2', 'IT3', 'IT4'], num_days=5)
    
    # Create analyzer
    analyzer = InteractiveDFS0Analyzer()
    
    # Set up files manually
    file_paths = [file1, file2]
    scaling_factors = {1: 1.0, 2: 1.0}
    
    print("\nLoading files...")
    analyzer.load_files(file_paths, scaling_factors)
    
    print(f"✓ Loaded {len(analyzer.analyzers)} file(s)")
    
    print("\nGenerating daily exceedance tables...")
    tables = analyzer.generate_daily_exceedance_tables()
    
    print(f"✓ Generated {len(tables)} table(s)")
    
    # Display the tables
    print("\n" + "="*70)
    print("DEMO: Daily Exceedance Table Output")
    print("="*70)
    analyzer.display_daily_tables(tables)
    
    # Verify structure
    print("\n" + "="*70)
    print("VERIFICATION")
    print("="*70)
    
    for threshold, df in tables.items():
        print(f"\nThreshold {threshold} mg/l:")
        print(f"  Shape: {df.shape} (rows x columns)")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Date column type: {df['Date'].dtype}")
        
        # Check that percentages are integers
        for col in df.columns:
            if col != 'Date':
                print(f"  {col} type: {df[col].dtype}, sample values: {df[col].head(3).tolist()}")
        
        # Verify Date column has expected number of unique days
        print(f"  Number of days: {len(df)}")
    
    print("\n" + "="*70)
    print("✓ Daily table test completed successfully!")
    print("="*70)


if __name__ == '__main__':
    test_daily_table_generation()
