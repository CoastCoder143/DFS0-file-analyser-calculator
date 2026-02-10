#!/usr/bin/env python3
"""
DFS0 File Analyzer and Calculator

This module provides functionality to analyze DFS0 files, specifically for:
- Reading SSC (Suspended Sediment Concentration) data at each timestep
- Performing timestep-to-timestep addition with optional scaling multipliers
- Calculating the percentage of time concentrations exceed a threshold
"""

import numpy as np
from typing import List, Dict, Optional, Union
import mikeio


class DFS0Analyzer:
    """Analyzer for DFS0 files with SSC concentration analysis capabilities."""
    
    def __init__(self, filepath: Optional[str] = None):
        """
        Initialize the DFS0 Analyzer.
        
        Args:
            filepath: Path to the DFS0 file (optional for testing/mock data)
        """
        self.filepath = filepath
        self.dfs0 = None
        self.data = None
        self.timesteps = None
        
    def load_file(self):
        """Load the DFS0 file and extract data."""
        if self.filepath is None:
            raise ValueError("Cannot load file: filepath not provided")
        self.dfs0 = mikeio.read(self.filepath)
        self.data = self.dfs0
        self.timesteps = self.dfs0.time
        return self
    
    def get_item_names(self) -> List[str]:
        """
        Get the names of all items (variables) in the DFS0 file.
        
        Returns:
            List of item names
        """
        if self.data is None:
            self.load_file()
        return list(self.data.items.keys())
    
    def get_item_data(self, item_name: str) -> np.ndarray:
        """
        Get data for a specific item.
        
        Args:
            item_name: Name of the item to retrieve
            
        Returns:
            Numpy array of values for the specified item
        """
        if self.data is None:
            self.load_file()
        return self.data[item_name].to_numpy()
    
    def calculate_sum_with_scaling(
        self, 
        item_names: Union[str, List[str]], 
        scaling_factors: Optional[Union[float, List[float]]] = None
    ) -> np.ndarray:
        """
        Calculate the sum of specified items with optional scaling factors.
        
        Args:
            item_names: Single item name or list of item names to sum
            scaling_factors: Single scaling factor or list of scaling factors.
                           If None, uses 1.0 for all items.
        
        Returns:
            Numpy array of summed values at each timestep
        """
        if self.data is None:
            self.load_file()
        
        # Ensure item_names is a list
        if isinstance(item_names, str):
            item_names = [item_names]
        
        # Handle scaling factors
        if scaling_factors is None:
            scaling_factors = [1.0] * len(item_names)
        elif isinstance(scaling_factors, (int, float)):
            scaling_factors = [scaling_factors] * len(item_names)
        
        if len(item_names) != len(scaling_factors):
            raise ValueError("Number of item names must match number of scaling factors")
        
        # Calculate weighted sum
        result = np.zeros(len(self.timesteps))
        for item_name, scale in zip(item_names, scaling_factors):
            data = self.get_item_data(item_name)
            result += data * scale
        
        return result
    
    def calculate_exceedance_percentage(
        self, 
        values: np.ndarray, 
        threshold: float,
        start_index: int = 0,
        num_timesteps: Optional[int] = None
    ) -> Dict[str, Union[float, int]]:
        """
        Calculate the percentage of time values exceed a threshold.
        
        Args:
            values: Array of values to analyze
            threshold: Concentration threshold to check against
            start_index: Starting timestep index (default: 0)
            num_timesteps: Number of timesteps to analyze (default: all from start_index)
        
        Returns:
            Dictionary containing:
                - percentage: Percentage of time exceeding threshold
                - count_exceeded: Number of timesteps exceeding threshold
                - total_timesteps: Total number of timesteps analyzed
                - threshold: The threshold value used
        """
        if num_timesteps is None:
            num_timesteps = len(values) - start_index
        
        end_index = start_index + num_timesteps
        subset = values[start_index:end_index]
        
        count_exceeded = np.sum(subset > threshold)
        total_timesteps = len(subset)
        percentage = (count_exceeded / total_timesteps) * 100.0
        
        return {
            'percentage': percentage,
            'count_exceeded': int(count_exceeded),
            'total_timesteps': total_timesteps,
            'threshold': threshold
        }
    
    def analyze_ssc(
        self,
        ssc_items: Union[str, List[str]],
        scaling_factors: Optional[Union[float, List[float]]] = None,
        threshold: float = 0.0,
        start_index: int = 0,
        num_timesteps: Optional[int] = None
    ) -> Dict:
        """
        Perform complete SSC analysis: sum items with scaling and calculate exceedance.
        
        Args:
            ssc_items: SSC item name(s) to analyze
            scaling_factors: Optional scaling factor(s) for each item
            threshold: Concentration threshold for exceedance calculation
            start_index: Starting timestep index
            num_timesteps: Number of timesteps to analyze
        
        Returns:
            Dictionary containing:
                - total_ssc: Array of total SSC at each timestep
                - exceedance_stats: Statistics about threshold exceedance
                - timesteps_analyzed: Number of timesteps analyzed
        """
        if self.data is None:
            self.load_file()
        
        # Calculate total SSC with scaling
        total_ssc = self.calculate_sum_with_scaling(ssc_items, scaling_factors)
        
        # Calculate exceedance statistics
        exceedance_stats = self.calculate_exceedance_percentage(
            total_ssc, threshold, start_index, num_timesteps
        )
        
        return {
            'total_ssc': total_ssc,
            'exceedance_stats': exceedance_stats,
            'timesteps_analyzed': exceedance_stats['total_timesteps']
        }


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze DFS0 files for SSC concentration analysis'
    )
    parser.add_argument('filepath', help='Path to DFS0 file')
    parser.add_argument(
        '--items', 
        nargs='+', 
        help='Item name(s) to analyze (space-separated)'
    )
    parser.add_argument(
        '--scaling', 
        nargs='+', 
        type=float,
        help='Scaling factor(s) for each item (space-separated)'
    )
    parser.add_argument(
        '--threshold', 
        type=float, 
        default=0.0,
        help='Concentration threshold for exceedance calculation (default: 0.0)'
    )
    parser.add_argument(
        '--start', 
        type=int, 
        default=0,
        help='Starting timestep index (default: 0)'
    )
    parser.add_argument(
        '--num-timesteps', 
        type=int,
        help='Number of timesteps to analyze (default: all from start)'
    )
    parser.add_argument(
        '--list-items', 
        action='store_true',
        help='List all items in the DFS0 file and exit'
    )
    
    args = parser.parse_args()
    
    # Create analyzer
    analyzer = DFS0Analyzer(args.filepath)
    analyzer.load_file()
    
    # List items if requested
    if args.list_items:
        print("Items in DFS0 file:")
        for item_name in analyzer.get_item_names():
            print(f"  - {item_name}")
        return
    
    # Perform analysis
    if args.items:
        result = analyzer.analyze_ssc(
            ssc_items=args.items,
            scaling_factors=args.scaling,
            threshold=args.threshold,
            start_index=args.start,
            num_timesteps=args.num_timesteps
        )
        
        print("\n=== DFS0 SSC Analysis Results ===")
        print(f"Items analyzed: {', '.join(args.items)}")
        if args.scaling:
            print(f"Scaling factors: {', '.join(map(str, args.scaling))}")
        print(f"\nThreshold: {args.threshold}")
        print(f"Timesteps analyzed: {result['timesteps_analyzed']}")
        print(f"\nExceedance Statistics:")
        print(f"  Percentage of time exceeding threshold: {result['exceedance_stats']['percentage']:.2f}%")
        print(f"  Count exceeded: {result['exceedance_stats']['count_exceeded']}")
        print(f"  Total timesteps: {result['exceedance_stats']['total_timesteps']}")
        
        # Display some statistics about the total SSC
        total_ssc = result['total_ssc']
        print(f"\nTotal SSC Statistics:")
        print(f"  Min: {np.min(total_ssc):.4f}")
        print(f"  Max: {np.max(total_ssc):.4f}")
        print(f"  Mean: {np.mean(total_ssc):.4f}")
        print(f"  Std Dev: {np.std(total_ssc):.4f}")
    else:
        print("Please specify --items to analyze or use --list-items to see available items")


if __name__ == '__main__':
    main()
