#!/usr/bin/env python3
"""
Example demonstrating how to use the DFS0 Analyzer programmatically.

This example shows various use cases without requiring an actual DFS0 file.
"""

import numpy as np
from dfs0_analyzer import DFS0Analyzer


def example_basic_usage():
    """Example: Basic usage with mock data."""
    print("="*60)
    print("Example 1: Basic SSC Analysis")
    print("="*60)
    
    # Create mock analyzer with simulated data
    class MockItem:
        def __init__(self, data):
            self.data = data
        def to_numpy(self):
            return self.data
    
    class MockData:
        def __init__(self):
            # Simulate 1440 timesteps (24 minutes at 1-second intervals)
            n = 1440
            np.random.seed(42)  # For reproducibility
            self.items = {
                'Source1_SSC': MockItem(np.random.uniform(30, 120, n)),
                'Source2_SSC': MockItem(np.random.uniform(20, 80, n)),
            }
            self.time = np.arange(n)
        
        def __getitem__(self, key):
            return self.items[key]
    
    analyzer = DFS0Analyzer()
    analyzer.data = MockData()
    analyzer.timesteps = analyzer.data.time
    
    # Analyze with default scaling (1.0 for all)
    result = analyzer.analyze_ssc(
        ssc_items=['Source1_SSC', 'Source2_SSC'],
        threshold=100.0,
        num_timesteps=1440
    )
    
    print(f"\nAnalyzing {result['timesteps_analyzed']} timesteps")
    print(f"Threshold: 100.0")
    print(f"\nResults:")
    print(f"  Percentage exceeding threshold: {result['exceedance_stats']['percentage']:.2f}%")
    print(f"  Count exceeded: {result['exceedance_stats']['count_exceeded']}")
    print(f"\nTotal SSC Statistics:")
    print(f"  Min: {np.min(result['total_ssc']):.2f}")
    print(f"  Max: {np.max(result['total_ssc']):.2f}")
    print(f"  Mean: {np.mean(result['total_ssc']):.2f}")
    print(f"  Median: {np.median(result['total_ssc']):.2f}")
    print()


def example_with_scaling():
    """Example: Analysis with scaling factors."""
    print("="*60)
    print("Example 2: SSC Analysis with Scaling Factors")
    print("="*60)
    
    # Create mock analyzer
    class MockItem:
        def __init__(self, data):
            self.data = data
        def to_numpy(self):
            return self.data
    
    class MockData:
        def __init__(self):
            n = 1440
            np.random.seed(42)
            self.items = {
                'Primary_Source': MockItem(np.random.uniform(50, 150, n)),
                'Secondary_Source': MockItem(np.random.uniform(20, 60, n)),
                'Tertiary_Source': MockItem(np.random.uniform(10, 40, n)),
            }
            self.time = np.arange(n)
        
        def __getitem__(self, key):
            return self.items[key]
    
    analyzer = DFS0Analyzer()
    analyzer.data = MockData()
    analyzer.timesteps = analyzer.data.time
    
    # Different scaling factors for different sources
    result = analyzer.analyze_ssc(
        ssc_items=['Primary_Source', 'Secondary_Source', 'Tertiary_Source'],
        scaling_factors=[1.0, 0.7, 0.3],  # Weight sources differently
        threshold=150.0,
        num_timesteps=1440
    )
    
    print(f"\nUsing scaling factors: [1.0, 0.7, 0.3]")
    print(f"Analyzing {result['timesteps_analyzed']} timesteps")
    print(f"Threshold: 150.0")
    print(f"\nResults:")
    print(f"  Percentage exceeding threshold: {result['exceedance_stats']['percentage']:.2f}%")
    print(f"  Count exceeded: {result['exceedance_stats']['count_exceeded']}")
    print(f"\nTotal SSC Statistics:")
    print(f"  Min: {np.min(result['total_ssc']):.2f}")
    print(f"  Max: {np.max(result['total_ssc']):.2f}")
    print(f"  Mean: {np.mean(result['total_ssc']):.2f}")
    print()


def example_subset_analysis():
    """Example: Analyzing a subset of timesteps."""
    print("="*60)
    print("Example 3: Analyzing Specific Time Range")
    print("="*60)
    
    # Create mock analyzer
    class MockItem:
        def __init__(self, data):
            self.data = data
        def to_numpy(self):
            return self.data
    
    class MockData:
        def __init__(self):
            n = 3600  # 1 hour of data
            np.random.seed(42)
            self.items = {
                'SSC': MockItem(np.random.uniform(40, 180, n)),
            }
            self.time = np.arange(n)
        
        def __getitem__(self, key):
            return self.items[key]
    
    analyzer = DFS0Analyzer()
    analyzer.data = MockData()
    analyzer.timesteps = analyzer.data.time
    
    # Analyze first 10 minutes (600 seconds)
    result1 = analyzer.analyze_ssc(
        ssc_items='SSC',
        threshold=120.0,
        start_index=0,
        num_timesteps=600
    )
    
    # Analyze next 10 minutes (600 seconds)
    result2 = analyzer.analyze_ssc(
        ssc_items='SSC',
        threshold=120.0,
        start_index=600,
        num_timesteps=600
    )
    
    print(f"\nThreshold: 120.0")
    print(f"\nFirst 10 minutes (timesteps 0-599):")
    print(f"  Percentage exceeding: {result1['exceedance_stats']['percentage']:.2f}%")
    print(f"  Count exceeded: {result1['exceedance_stats']['count_exceeded']}")
    
    print(f"\nSecond 10 minutes (timesteps 600-1199):")
    print(f"  Percentage exceeding: {result2['exceedance_stats']['percentage']:.2f}%")
    print(f"  Count exceeded: {result2['exceedance_stats']['count_exceeded']}")
    print()


def example_multiple_thresholds():
    """Example: Testing multiple thresholds."""
    print("="*60)
    print("Example 4: Multiple Threshold Analysis")
    print("="*60)
    
    # Create mock analyzer
    class MockItem:
        def __init__(self, data):
            self.data = data
        def to_numpy(self):
            return self.data
    
    class MockData:
        def __init__(self):
            n = 1440
            np.random.seed(42)
            self.items = {
                'SSC': MockItem(np.random.uniform(30, 200, n)),
            }
            self.time = np.arange(n)
        
        def __getitem__(self, key):
            return self.items[key]
    
    analyzer = DFS0Analyzer()
    analyzer.data = MockData()
    analyzer.timesteps = analyzer.data.time
    
    # Get total SSC values once
    total_ssc = analyzer.calculate_sum_with_scaling('SSC')
    
    # Test multiple thresholds
    thresholds = [50, 100, 150, 200]
    
    print(f"\nAnalyzing 1440 timesteps with multiple thresholds:\n")
    print(f"{'Threshold':<12} {'% Exceeded':<15} {'Count':<10}")
    print("-" * 40)
    
    for threshold in thresholds:
        result = analyzer.calculate_exceedance_percentage(total_ssc, threshold)
        print(f"{threshold:<12} {result['percentage']:<15.2f} {result['count_exceeded']:<10}")
    print()


if __name__ == '__main__':
    example_basic_usage()
    example_with_scaling()
    example_subset_analysis()
    example_multiple_thresholds()
    
    print("="*60)
    print("All examples completed successfully!")
    print("="*60)
