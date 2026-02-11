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
        
        # Define expected timesteps per day for each series type
        self.expected_timesteps = {
            'V': 73,   # V1-V4 series: 73 timesteps per day
            'IT': 144  # IT1-IT7 series: 144 timesteps per day
        }
        
        # Define column order for output
        self.column_order = ['Date', 'V1', 'V2', 'V3', 'V4', 
                            'IT1', 'IT2', 'IT3', 'IT4', 'IT5', 'IT6', 'IT7']
        
        # ANSI color codes for terminal highlighting
        self.ORANGE = '\033[33m'  # ANSI 33 for orange
        self.RED = '\033[31m'     # ANSI 31 for red
        self.RESET = '\033[0m'    # Reset color
        
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
    
    def generate_daily_exceedance_tables(self) -> Dict[float, pd.DataFrame]:
        """
        Generate daily exceedance percentage tables.
        
        Each table shows:
        - Rows: Calendar days (one row per date)
        - Columns: Date | V1 | V2 | V3 | V4 | IT1 | IT2 | IT3 | IT4 | IT5 | IT6 | IT7
        - Cells: Percentage of that day's timesteps where value exceeded threshold
        
        Returns:
            Dictionary mapping threshold to DataFrame with daily exceedance percentages
        """
        if not self.analyzers:
            raise ValueError("No files loaded")
        
        print("\n" + "="*70)
        print("Generating Daily Exceedance Tables...")
        print("-"*70)
        
        # Create results dictionary for each threshold
        results = {threshold: {} for threshold in self.thresholds}
        
        # Process each file
        for file_idx, (analyzer, (filepath, scale)) in enumerate(zip(self.analyzers, self.files_data), 1):
            filename = os.path.basename(filepath)
            print(f"Processing file {file_idx}: {filename}")
            
            # Get all item names (series) from this file
            item_names = analyzer.get_item_names()
            timestamps = analyzer.timesteps
            
            for item_name in item_names:
                # Get data for this series
                data = analyzer.get_item_data(item_name) * scale
                
                # Determine series type and expected timesteps per day
                series_prefix = item_name.split('_')[0] if '_' in item_name else item_name
                
                # Map to V or IT series
                # Assuming item names follow patterns like "V1", "V2", "IT1", "IT2", etc.
                # or with prefixes like "Receptor_1" -> map to V1, etc.
                series_name = item_name
                
                # Create a DataFrame with timestamps and data
                df_series = pd.DataFrame({
                    'timestamp': timestamps,
                    'value': data
                })
                
                # Extract date from timestamp
                df_series['date'] = pd.to_datetime(df_series['timestamp']).dt.date
                
                # For each threshold, calculate daily exceedance percentages
                for threshold in self.thresholds:
                    df_series['exceeds'] = df_series['value'] > threshold
                    
                    # Group by date and calculate percentage
                    daily_stats = df_series.groupby('date').agg({
                        'exceeds': ['sum', 'count']
                    })
                    
                    # Flatten column names
                    daily_stats.columns = ['_'.join(col).strip('_') for col in daily_stats.columns.values]
                    
                    # Calculate percentage
                    daily_stats['percentage'] = (daily_stats['exceeds_sum'] / daily_stats['exceeds_count'] * 100).round(0)
                    
                    # Store results with series name
                    if series_name not in results[threshold]:
                        results[threshold][series_name] = daily_stats['percentage']
        
        # Convert to DataFrames with proper structure
        tables = {}
        for threshold in self.thresholds:
            if results[threshold]:
                # Create DataFrame from results
                df = pd.DataFrame(results[threshold])
                
                # Reset index to make date a column
                df.reset_index(inplace=True)
                
                # The first column after reset_index should be the date
                # Rename it to 'Date'
                if 'index' in df.columns:
                    df.rename(columns={'index': 'Date'}, inplace=True)
                elif df.columns[0] != 'Date':
                    # First column is the date column
                    df.rename(columns={df.columns[0]: 'Date'}, inplace=True)
                
                # Format date column
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d/%m/%Y')
                
                # Reorder columns if they match expected pattern
                available_cols = [col for col in self.column_order if col in df.columns or col == 'Date']
                if len(available_cols) > 1:  # At least Date + one series
                    df = df[available_cols]
                
                # Convert percentages to integers
                for col in df.columns:
                    if col != 'Date':
                        df[col] = df[col].astype(int)
                
                tables[threshold] = df
        
        print("✓ Daily tables generated successfully")
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
    
    def _format_colored_table(self, df: pd.DataFrame) -> str:
        """
        Format a DataFrame with colored values for terminal display.
        
        Args:
            df: DataFrame with Date and percentage columns
            
        Returns:
            Formatted string with ANSI color codes
        """
        # Build the output line by line
        lines = []
        
        # Define column widths
        date_width = 12
        value_width = 10
        
        # Header row
        header_parts = []
        for col in df.columns:
            if col == 'Date':
                header_parts.append(f"{col:<{date_width}}")
            else:
                header_parts.append(f"{col:>{value_width}}")
        lines.append("  ".join(header_parts))
        
        # Data rows
        for _, row in df.iterrows():
            row_parts = []
            for col in df.columns:
                value = row[col]
                if col == 'Date':
                    # Date column - no color
                    row_parts.append(f"{value:<{date_width}}")
                else:
                    # Numeric column - apply color
                    int_value = int(value)
                    colored_str = self._apply_color_to_value(int_value, col)
                    
                    # Manually pad to account for ANSI codes
                    # ANSI codes add characters but no visual width
                    visible_len = len(f"{int_value:3d}")  # Visual length without ANSI codes
                    padding_needed = value_width - visible_len
                    padded_value = " " * padding_needed + colored_str
                    row_parts.append(padded_value)
            lines.append("  ".join(row_parts))
        
        return "\n".join(lines)
    
    def _apply_color_to_value(self, value: int, column_name: str) -> str:
        """
        Apply color to a numeric value based on column type and value.
        
        Args:
            value: Numeric value
            column_name: Column name to determine color rules
            
        Returns:
            String with ANSI color codes if applicable
        """
        # Format the value
        formatted = f"{value:3d}"
        
        # Determine if this is a V or IT column
        is_v_column = column_name.startswith('V') and column_name[1:].isdigit()
        is_it_column = column_name.startswith('IT') and column_name[2:].isdigit()
        
        # Apply coloring rules
        if is_v_column and value > 15:
            # V columns: >15 → ORANGE (including >20)
            return f"{self.ORANGE}{formatted}{self.RESET}"
        elif is_it_column and value > 15:
            # IT columns: >15 → RED
            return f"{self.RED}{formatted}{self.RESET}"
        
        # No color
        return formatted
    
    def display_daily_tables(self, tables: Dict[float, pd.DataFrame]):
        """
        Display daily exceedance percentage tables with color highlighting.
        
        Args:
            tables: Dictionary mapping threshold to DataFrame with daily percentages
        """
        for threshold, df in tables.items():
            print("\n" + "="*100)
            print(f"DAILY EXCEEDANCE TABLE: Threshold = {threshold} mg/l")
            print("="*100)
            print("Each cell shows the percentage of that day's timesteps exceeding the threshold")
            print("-"*100)
            
            # Display the full table
            if len(df) > 0:
                if len(df) > 20:
                    print("\nFirst 10 days:")
                    print(self._format_colored_table(df.head(10)))
                    print(f"\n... ({len(df) - 20} days omitted) ...\n")
                    print("Last 10 days:")
                    print(self._format_colored_table(df.tail(10)))
                else:
                    print(self._format_colored_table(df))
                
                # Show summary statistics
                print("\n" + "-"*100)
                print("Summary Statistics:")
                for col in df.columns:
                    if col != 'Date':
                        mean_pct = df[col].mean()
                        max_pct = df[col].max()
                        days_exceeded = (df[col] > 0).sum()
                        print(f"  {col}: Mean={mean_pct:.1f}%, Max={max_pct:.0f}%, Days with exceedance={days_exceeded}")
            else:
                print("No data available")
            
            print("\n" + "="*100)
    
    def save_tables_to_csv(self, tables: Dict[float, pd.DataFrame], output_dir: str = ".", daily_format: bool = False):
        """
        Save exceedance tables to CSV files.
        
        Args:
            tables: Dictionary mapping threshold to DataFrame
            output_dir: Directory to save CSV files
            daily_format: If True, saves in daily format (no index), else saves with index
        """
        print("\n" + "="*70)
        print("Saving Tables to CSV...")
        print("-"*70)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for threshold, df in tables.items():
            if daily_format:
                filename = f"daily_exceedance_table_{int(threshold)}mgl_{timestamp}.csv"
            else:
                filename = f"exceedance_table_{int(threshold)}mgl_{timestamp}.csv"
            filepath = os.path.join(output_dir, filename)
            
            # For daily format, don't save index (Date is already a column)
            # For timestep format, save with index (timestamps)
            df.to_csv(filepath, index=(not daily_format))
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
                
                # Step 5: Ask user which table format they want
                print("\n" + "="*70)
                print("TABLE FORMAT OPTIONS")
                print("="*70)
                print("1. Daily Exceedance Percentages (NEW)")
                print("   - One row per calendar day")
                print("   - Shows % of timesteps exceeding threshold each day")
                print("   - Columns: Date | V1 | V2 | V3 | V4 | IT1-IT7")
                print("\n2. Timestep Summary (Original)")
                print("   - Summary of exceedance counts across all timesteps")
                print("="*70)
                
                format_choice = input("\nChoose format (1 or 2, default=1): ").strip()
                if not format_choice:
                    format_choice = '1'
                
                if format_choice == '1':
                    # Generate and display daily tables
                    tables = self.generate_daily_exceedance_tables()
                    
                    print("\n" + "="*70)
                    print("RESULTS - Daily Exceedance Percentages")
                    print("="*70)
                    self.display_daily_tables(tables)
                    is_daily_format = True
                else:
                    # Generate tables (original format)
                    tables = self.generate_exceedance_tables()
                    is_daily_format = False
                    
                    # Display tables (summary by default)
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
                    
                    self.save_tables_to_csv(tables, output_dir, daily_format=is_daily_format)
                
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
