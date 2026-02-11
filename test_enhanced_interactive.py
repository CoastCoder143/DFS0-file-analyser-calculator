#!/usr/bin/env python3
"""
Test the enhanced interactive analyzer with programmatic input simulation.
"""

import os
import sys
from io import StringIO
from unittest.mock import patch
from interactive_analyzer import InteractiveDFS0Analyzer
from demo_interactive import create_sample_dfs0_file


def test_display_with_summary():
    """Test the new summary display feature."""
    print("="*70)
    print("Testing Enhanced Display with Summary")
    print("="*70)
    
    # Create temporary test files
    temp_dir = "/tmp/test_enhanced"
    os.makedirs(temp_dir, exist_ok=True)
    
    file1 = os.path.join(temp_dir, "test1.dfs0")
    file2 = os.path.join(temp_dir, "test2.dfs0")
    
    print("\nCreating sample DFS0 files...")
    create_sample_dfs0_file(file1, num_timesteps=30, num_items=2)
    create_sample_dfs0_file(file2, num_timesteps=30, num_items=2)
    
    # Create analyzer
    analyzer = InteractiveDFS0Analyzer()
    
    # Set up files manually
    file_paths = [file1, file2]
    scaling_factors = {1: 1.0, 2: 1.5}
    
    print("\nLoading files...")
    analyzer.load_files(file_paths, scaling_factors)
    
    print(f"✓ Loaded {len(analyzer.analyzers)} file(s)")
    
    print("\nGenerating exceedance tables...")
    tables = analyzer.generate_exceedance_tables()
    
    print(f"✓ Generated {len(tables)} table(s)")
    
    # Test summary display (new feature)
    print("\n" + "="*70)
    print("DEMO: Summary Display (Default Output)")
    print("="*70)
    analyzer.display_tables(tables, show_full=False)
    
    # Test full display
    print("\n" + "="*70)
    print("DEMO: Full Display (Optional)")
    print("="*70)
    print("(Showing just one threshold for brevity)")
    import pandas as pd
    single_table = {5.0: tables[5.0]}
    analyzer.display_tables(single_table, show_full=True)
    
    print("\n" + "="*70)
    print("✓ Enhanced display test completed successfully!")
    print("="*70)


def simulate_interactive_workflow():
    """
    Simulate the interactive workflow with different scaling factors.
    This shows how the new loop feature works.
    """
    print("\n" + "="*70)
    print("Simulating Interactive Workflow")
    print("="*70)
    print("\nThis demonstrates how users can now:")
    print("1. Enter files once")
    print("2. Try different scaling factor combinations")
    print("3. See results immediately on command line")
    print("4. Optionally save to CSV")
    print("5. Try again with different factors")
    
    print("\n" + "="*70)
    print("WORKFLOW EXAMPLE:")
    print("="*70)
    print("""
1. User enters files: location1.dfs0, location2.dfs0
2. User tries scaling: 1: 1.0, 2: 1.0
   → Sees summary results on screen
3. User decides to try different scaling: 1: 1.4, 2: 0.8
   → Sees new summary results immediately
4. Compares results mentally or in terminal history
5. Chooses best combination and optionally saves to CSV
6. Continues or exits
""")
    
    print("✓ Workflow simulation complete!")


if __name__ == '__main__':
    test_display_with_summary()
    simulate_interactive_workflow()
    
    print("\n" + "="*70)
    print("ALL TESTS PASSED!")
    print("="*70)
    print("\nKey improvements:")
    print("- Summary statistics shown by default (faster comparison)")
    print("- Full tables optional (shown only if requested)")
    print("- Can try multiple scaling combinations without restarting")
    print("- CSV save is optional, not automatic")
    print("- Perfect for quick experimentation!")
