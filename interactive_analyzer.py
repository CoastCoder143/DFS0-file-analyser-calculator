#!/usr/bin/env python3
"""
Interactive DFS0 File Analyzer

This module provides an interactive interface for analyzing multiple DFS0 files,
with support for:
- Multiple UNC file paths input
- Individual scaling factors for each file
- Table output showing dates vs receptors (columns from DFS0)
- Separate tables for different threshold concentrations (5mg/l, 10mg/l, 25mg/l)
"""

import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple
from dfs0_analyzer import DFS0Analyzer


class InteractiveDFS0Analyzer:
    """Interactive analyzer for multiple DFS0 files with tabular output."""
    
    def __init__(self):
        """Initialize the interactive analyzer."""
        self.files_data = []  # List of (filepath, scaling_factor) tuples
        self.analyzers = []   # List of DFS0Analyzer instances
        self.thresholds = [5.0, 10.0, 25.0]  # mg/l thresholds
        
    def get_file_paths(self) -> List[str]:
        """
        Interactively get UNC file paths from the user.
        
        Returns:
            List of file paths
        """
        print("\n" + "="*70)
        print("DFS0 INTERACTIVE ANALYZER - File Input")
        print("="*70)
        print("\nEnter the UNC file paths for all DFS0 locations.")
        print("Enter one path per line. Press Enter on an empty line when done.")
        print("-"*70)
        
        file_paths = []
        file_num = 1
        
        while True:
            path = input(f"\nFile {file_num} path (or press Enter to finish): ").strip()
            
            if not path:
                if len(file_paths) == 0:
                    print("Error: At least one file path is required!")
                    continue
                else:
                    break
            
            # Validate file exists
            if not os.path.exists(path):
                print(f"Warning: File not found: {path}")
                confirm = input("Add anyway? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            
            file_paths.append(path)
            print(f"✓ Added: {path}")
            file_num += 1
        
        return file_paths
    
    def display_files(self, file_paths: List[str]):
        """
        Display the list of files with indices.
        
        Args:
            file_paths: List of file paths
        """
        print("\n" + "="*70)
        print("Files to Analyze:")
        print("-"*70)
        for idx, path in enumerate(file_paths, 1):
            filename = os.path.basename(path)
            print(f"{idx}: {filename}")
            print(f"   Path: {path}")
        print("="*70)
    
    def get_scaling_factors(self, file_paths: List[str]) -> Dict[int, float]:
        """
        Interactively get scaling factors for each file.
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Dictionary mapping file index to scaling factor
        """
        print("\n" + "="*70)
        print("Scaling Factors Input")
        print("="*70)
        print("\nEnter scaling factors for each file.")
        print("Format: <file_number>: <scaling_factor>")
        print("Example: 1: 1.4  (sets file 1 to scale factor 1.4)")
        print("\nPress Enter without input to use default scaling factor of 1.0")
        print("Type 'done' when finished, or 'list' to see files again.")
        print("-"*70)
        
        scaling_factors = {}
        
        while True:
            user_input = input("\nEnter scaling (or 'done'/'list'): ").strip()
            
            if user_input.lower() == 'done':
                break
            
            if user_input.lower() == 'list':
                self.display_files(file_paths)
                continue
            
            if not user_input:
                # Set all remaining files to 1.0
                for idx in range(1, len(file_paths) + 1):
                    if idx not in scaling_factors:
                        scaling_factors[idx] = 1.0
                print("✓ Set all remaining files to scaling factor 1.0")
                break
            
            # Parse input (format: "1: 1.4" or "1 1.4" or "1:1.4")
            try:
                # Replace : with space and split
                parts = user_input.replace(':', ' ').split()
                if len(parts) != 2:
                    print("Error: Invalid format. Use: <file_number>: <scaling_factor>")
                    continue
                
                file_idx = int(parts[0])
                scale = float(parts[1])
                
                if file_idx < 1 or file_idx > len(file_paths):
                    print(f"Error: File number must be between 1 and {len(file_paths)}")
                    continue
                
                scaling_factors[file_idx] = scale
                filename = os.path.basename(file_paths[file_idx - 1])
                print(f"✓ File {file_idx} ({filename}): scale = {scale}")
                
            except ValueError as e:
                print(f"Error: Invalid input format. {e}")
                continue
        
        # Fill in any missing scaling factors with 1.0
        for idx in range(1, len(file_paths) + 1):
            if idx not in scaling_factors:
                scaling_factors[idx] = 1.0
                print(f"ℹ File {idx}: using default scale = 1.0")
        
        return scaling_factors
    
    def load_files(self, file_paths: List[str], scaling_factors: Dict[int, float]):
        """
        Load all DFS0 files and their scaling factors.
        
        Args:
            file_paths: List of file paths
            scaling_factors: Dictionary mapping file index to scaling factor
        """
        print("\n" + "="*70)
        print("Loading DFS0 Files...")
        print("-"*70)
        
        for idx, filepath in enumerate(file_paths, 1):
            try:
                print(f"Loading file {idx}: {os.path.basename(filepath)}...", end=" ")
                analyzer = DFS0Analyzer(filepath)
                analyzer.load_file()
                
                scale = scaling_factors.get(idx, 1.0)
                self.files_data.append((filepath, scale))
                self.analyzers.append(analyzer)
                
                print(f"✓ (scale: {scale})")
                
            except Exception as e:
                print(f"✗ Error: {e}")
                print(f"Skipping file {idx}")
        
        print("="*70)
        print(f"Successfully loaded {len(self.analyzers)} file(s)")
    
    def generate_exceedance_tables(self) -> Dict[float, pd.DataFrame]:
        """
        Generate exceedance tables for each threshold.
        
        Returns:
            Dictionary mapping threshold to DataFrame with dates vs receptors
        """
        if not self.analyzers:
            raise ValueError("No files loaded")
        
        print("\n" + "="*70)
        print("Generating Exceedance Tables...")
        print("-"*70)
        
        # Get all timestamps from the first file (assuming all have same timestamps)
        timestamps = self.analyzers[0].timesteps
        
        # Create results dictionary
        results = {threshold: {} for threshold in self.thresholds}
        
        # Process each file
        for file_idx, (analyzer, (filepath, scale)) in enumerate(zip(self.analyzers, self.files_data), 1):
            filename = os.path.basename(filepath)
            print(f"Processing file {file_idx}: {filename}")
            
            # Get all item names (receptors/columns) from this file
            item_names = analyzer.get_item_names()
            
            for item_name in item_names:
                # Get data for this receptor
                data = analyzer.get_item_data(item_name) * scale
                
                # Create column name (receptor)
                receptor_name = f"File{file_idx}_{item_name}"
                
                # For each threshold, determine which dates exceed it
                for threshold in self.thresholds:
                    exceeds = data > threshold
                    
                    # Store the exceedance data
                    if receptor_name not in results[threshold]:
                        results[threshold][receptor_name] = exceeds
        
        # Convert to DataFrames
        tables = {}
        for threshold in self.thresholds:
            df = pd.DataFrame(results[threshold], index=timestamps)
            df.index.name = 'Date/Time'
            
            # Convert boolean to "Yes"/"No" or "X"/"-" for better readability
            # Use map() instead of applymap() for newer pandas versions
            df = df.map(lambda x: 'X' if x else '-')
            
            tables[threshold] = df
        
        print("✓ Tables generated successfully")
        return tables
    
    def display_tables(self, tables: Dict[float, pd.DataFrame], show_full: bool = False):
        """
        Display the exceedance tables.
        
        Args:
            tables: Dictionary mapping threshold to DataFrame
            show_full: If True, show full tables. If False, show summary only.
        """
        for threshold, df in tables.items():
            print("\n" + "="*100)
            print(f"EXCEEDANCE TABLE: Threshold = {threshold} mg/l")
            print("="*100)
            print("Legend: X = Exceeds threshold, - = Below threshold")
            print("-"*100)
            
            # Calculate and display summary statistics
            exceedance_counts = (df == 'X').sum()
            total_timesteps = len(df)
            
            print(f"\nSummary (Total timesteps: {total_timesteps}):")
            print(f"{'Receptor':<40} {'Exceedances':<15} {'Percentage':<15}")
            print("-"*70)
            for receptor, count in exceedance_counts.items():
                percentage = (count / total_timesteps) * 100
                print(f"{receptor:<40} {count:<15} {percentage:>6.1f}%")
            
            if show_full:
                print("\n" + "-"*100)
                print("Full Table:")
                # Display the table
                # For large tables, show first and last few rows
                if len(df) > 20:
                    print("\nFirst 10 rows:")
                    print(df.head(10).to_string())
                    print(f"\n... ({len(df) - 20} rows omitted) ...\n")
                    print("Last 10 rows:")
                    print(df.tail(10).to_string())
                else:
                    print(df.to_string())
            
            print("\n" + "="*100)
    
    def save_tables_to_csv(self, tables: Dict[float, pd.DataFrame], output_dir: str = "."):
        """
        Save exceedance tables to CSV files.
        
        Args:
            tables: Dictionary mapping threshold to DataFrame
            output_dir: Directory to save CSV files
        """
        print("\n" + "="*70)
        print("Saving Tables to CSV...")
        print("-"*70)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for threshold, df in tables.items():
            filename = f"exceedance_table_{int(threshold)}mgl_{timestamp}.csv"
            filepath = os.path.join(output_dir, filename)
            
            df.to_csv(filepath)
            print(f"✓ Saved: {filename}")
        
        print("="*70)
    
    def run(self):
        """Run the interactive analyzer."""
        print("\n" + "#"*70)
        print("#" + " "*68 + "#")
        print("#" + "  INTERACTIVE DFS0 ANALYZER - Multi-Receptor Exceedance Analysis".center(68) + "#")
        print("#" + " "*68 + "#")
        print("#"*70)
        
        try:
            # Step 1: Get file paths
            file_paths = self.get_file_paths()
            
            # Step 2: Display files
            self.display_files(file_paths)
            
            # Main analysis loop - allows trying different scaling factors
            while True:
                # Step 3: Get scaling factors
                scaling_factors = self.get_scaling_factors(file_paths)
                
                # Step 4: Load files with new scaling factors
                self.load_files(file_paths, scaling_factors)
                
                if not self.analyzers:
                    print("\nError: No files were successfully loaded!")
                    retry = input("Try again? (y/n): ").strip().lower()
                    if retry != 'y':
                        break
                    continue
                
                # Step 5: Generate tables
                tables = self.generate_exceedance_tables()
                
                # Step 6: Display tables (summary by default)
                print("\n" + "="*70)
                print("RESULTS - Exceedance Summary")
                print("="*70)
                self.display_tables(tables, show_full=False)
                
                # Ask if user wants to see full tables
                show_full = input("\nShow full tables? (y/n): ").strip().lower()
                if show_full == 'y':
                    self.display_tables(tables, show_full=True)
                
                # Ask to save to CSV
                save_option = input("\nSave tables to CSV files? (y/n): ").strip().lower()
                if save_option == 'y':
                    output_dir = input("Enter output directory (or press Enter for current directory): ").strip()
                    if not output_dir:
                        output_dir = "."
                    
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    
                    self.save_tables_to_csv(tables, output_dir)
                
                # Ask if user wants to try different scaling factors
                print("\n" + "="*70)
                retry = input("Try different scaling factors? (y/n): ").strip().lower()
                if retry != 'y':
                    break
                
                # Clear previous data for next iteration
                self.files_data = []
                self.analyzers = []
                print("\n" + "="*70)
                print("Starting new analysis with same files...")
                print("="*70)
            
            print("\n" + "#"*70)
            print("#" + "  Analysis Complete!".center(68) + "#")
            print("#"*70 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nAnalysis interrupted by user.")
            sys.exit(0)
        except Exception as e:
            print(f"\n\nError during analysis: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


def main():
    """Main function for interactive mode."""
    analyzer = InteractiveDFS0Analyzer()
    analyzer.run()


if __name__ == '__main__':
    main()
