#!/usr/bin/env python3
"""
Test suite for DFS0 Analyzer

This file contains tests to validate the DFS0 analyzer functionality.
Note: These tests use mock data since we don't have actual DFS0 files in the repo.
"""

import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dfs0_analyzer import DFS0Analyzer


def test_exceedance_percentage():
    """Test exceedance percentage calculation."""
    print("Testing exceedance percentage calculation...")
    
    # Create test data
    values = np.array([50, 100, 150, 200, 75, 125, 80, 110])
    
    # Create analyzer instance without filepath (for testing)
    analyzer = DFS0Analyzer()
    
    # Test 1: 50% should exceed 100
    result = analyzer.calculate_exceedance_percentage(values, threshold=100.0)
    expected_percentage = 50.0  # 4 out of 8 values exceed 100
    assert abs(result['percentage'] - expected_percentage) < 0.01, \
        f"Expected {expected_percentage}%, got {result['percentage']}%"
    assert result['count_exceeded'] == 4
    assert result['total_timesteps'] == 8
    print(f"  ✓ Test 1 passed: {result['percentage']}% exceeded threshold of 100")
    
    # Test 2: Test with different threshold
    result = analyzer.calculate_exceedance_percentage(values, threshold=120.0)
    expected_percentage = 37.5  # 3 out of 8 values exceed 120
    assert abs(result['percentage'] - expected_percentage) < 0.01, \
        f"Expected {expected_percentage}%, got {result['percentage']}%"
    assert result['count_exceeded'] == 3
    print(f"  ✓ Test 2 passed: {result['percentage']}% exceeded threshold of 120")
    
    # Test 3: Test with subset of data (first 4 timesteps)
    result = analyzer.calculate_exceedance_percentage(values, threshold=100.0, 
                                                     start_index=0, num_timesteps=4)
    expected_percentage = 50.0  # 2 out of 4 values (150, 200) exceed 100
    assert abs(result['percentage'] - expected_percentage) < 0.01, \
        f"Expected {expected_percentage}%, got {result['percentage']}%"
    assert result['count_exceeded'] == 2
    assert result['total_timesteps'] == 4
    print(f"  ✓ Test 3 passed: {result['percentage']}% exceeded (subset)")
    
    print("All exceedance tests passed!\n")


def test_scaling_calculation():
    """Test the scaling calculation logic."""
    print("Testing scaling calculation...")
    
    # Create mock data structure
    class MockItem:
        def __init__(self, data):
            self.data = data
        
        def to_numpy(self):
            return self.data
    
    class MockData:
        def __init__(self):
            self.items = {
                'SSC1': MockItem(np.array([10, 20, 30, 40])),
                'SSC2': MockItem(np.array([5, 10, 15, 20])),
                'SSC3': MockItem(np.array([2, 4, 6, 8]))
            }
            self.time = np.arange(4)
        
        def __getitem__(self, key):
            return self.items[key]
    
    # Create analyzer with mock data
    analyzer = DFS0Analyzer()
    analyzer.data = MockData()
    analyzer.timesteps = analyzer.data.time
    
    # Test 1: Single item, no scaling
    result = analyzer.calculate_sum_with_scaling('SSC1')
    expected = np.array([10, 20, 30, 40])
    assert np.allclose(result, expected), f"Expected {expected}, got {result}"
    print(f"  ✓ Test 1 passed: Single item, no scaling")
    
    # Test 2: Multiple items, no scaling (sum)
    result = analyzer.calculate_sum_with_scaling(['SSC1', 'SSC2'])
    expected = np.array([15, 30, 45, 60])
    assert np.allclose(result, expected), f"Expected {expected}, got {result}"
    print(f"  ✓ Test 2 passed: Multiple items, no scaling")
    
    # Test 3: Multiple items with scaling
    result = analyzer.calculate_sum_with_scaling(['SSC1', 'SSC2', 'SSC3'], 
                                                 scaling_factors=[1.0, 0.5, 2.0])
    # SSC1*1.0 + SSC2*0.5 + SSC3*2.0
    # [10*1.0 + 5*0.5 + 2*2.0, 20*1.0 + 10*0.5 + 4*2.0, ...]
    expected = np.array([10 + 2.5 + 4, 20 + 5 + 8, 30 + 7.5 + 12, 40 + 10 + 16])
    expected = np.array([16.5, 33, 49.5, 66])
    assert np.allclose(result, expected), f"Expected {expected}, got {result}"
    print(f"  ✓ Test 3 passed: Multiple items with scaling")
    
    # Test 4: Single scaling factor applied to all
    result = analyzer.calculate_sum_with_scaling(['SSC1', 'SSC2'], scaling_factors=2.0)
    expected = np.array([30, 60, 90, 120])  # (SSC1 + SSC2) * 2
    assert np.allclose(result, expected), f"Expected {expected}, got {result}"
    print(f"  ✓ Test 4 passed: Single scaling factor for all items")
    
    print("All scaling tests passed!\n")


def test_integrated_analysis():
    """Test the integrated analysis workflow."""
    print("Testing integrated analysis...")
    
    # Create mock data
    class MockItem:
        def __init__(self, data):
            self.data = data
        
        def to_numpy(self):
            return self.data
    
    class MockData:
        def __init__(self):
            # Simulate 1440 timesteps (e.g., 1 second intervals for 24 minutes)
            n = 1440
            self.items = {
                'SSC1': MockItem(np.random.uniform(20, 150, n)),
                'SSC2': MockItem(np.random.uniform(10, 80, n))
            }
            self.time = np.arange(n)
        
        def __getitem__(self, key):
            return self.items[key]
    
    # Create analyzer with mock data
    analyzer = DFS0Analyzer()
    analyzer.data = MockData()
    analyzer.timesteps = analyzer.data.time
    
    # Perform integrated analysis
    result = analyzer.analyze_ssc(
        ssc_items=['SSC1', 'SSC2'],
        scaling_factors=[1.0, 0.5],
        threshold=100.0,
        start_index=0,
        num_timesteps=1440
    )
    
    # Verify result structure
    assert 'total_ssc' in result
    assert 'exceedance_stats' in result
    assert 'timesteps_analyzed' in result
    assert result['timesteps_analyzed'] == 1440
    assert len(result['total_ssc']) == 1440
    
    # Verify exceedance stats structure
    stats = result['exceedance_stats']
    assert 'percentage' in stats
    assert 'count_exceeded' in stats
    assert 'total_timesteps' in stats
    assert 'threshold' in stats
    assert stats['total_timesteps'] == 1440
    assert stats['threshold'] == 100.0
    assert 0 <= stats['percentage'] <= 100
    
    print(f"  ✓ Integrated analysis completed successfully")
    print(f"    Analyzed {result['timesteps_analyzed']} timesteps")
    print(f"    Exceedance: {stats['percentage']:.2f}%")
    print(f"    Count exceeded: {stats['count_exceeded']}")
    
    print("Integrated analysis test passed!\n")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")
    
    analyzer = DFS0Analyzer()
    
    # Test 1: All values below threshold (0% exceedance)
    values = np.array([10, 20, 30, 40, 50])
    result = analyzer.calculate_exceedance_percentage(values, threshold=100.0)
    assert result['percentage'] == 0.0
    assert result['count_exceeded'] == 0
    print(f"  ✓ Test 1 passed: 0% exceedance")
    
    # Test 2: All values above threshold (100% exceedance)
    values = np.array([110, 120, 130, 140, 150])
    result = analyzer.calculate_exceedance_percentage(values, threshold=100.0)
    assert result['percentage'] == 100.0
    assert result['count_exceeded'] == 5
    print(f"  ✓ Test 2 passed: 100% exceedance")
    
    # Test 3: Single value
    values = np.array([150])
    result = analyzer.calculate_exceedance_percentage(values, threshold=100.0)
    assert result['percentage'] == 100.0
    assert result['count_exceeded'] == 1
    assert result['total_timesteps'] == 1
    print(f"  ✓ Test 3 passed: Single value")
    
    print("Edge case tests passed!\n")


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("DFS0 Analyzer Test Suite")
    print("="*60 + "\n")
    
    try:
        test_exceedance_percentage()
        test_scaling_calculation()
        test_integrated_analysis()
        test_edge_cases()
        
        print("="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        return True
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
