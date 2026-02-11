# Interactive DFS0 Analyzer - User Guide

## Overview

The Interactive DFS0 Analyzer is a tool for analyzing multiple DFS0 files with different receptors (measurement locations) and generating exceedance tables showing when concentrations exceed specific thresholds.

## Features

- **Interactive File Input**: Asks for UNC file paths interactively
- **Custom Scaling Factors**: Apply individual scaling factors to each file
- **Multi-Receptor Analysis**: Each column in the DFS0 file is treated as a separate receptor
- **Threshold Exceedance Tables**: Generates separate tables for 5mg/l, 10mg/l, and 25mg/l
- **Command-Line Output**: Results displayed immediately in terminal (no CSV required)
- **Summary Statistics**: Quick overview of exceedance percentages per receptor
- **Try Multiple Combinations**: Test different scaling factors without restarting
- **Optional CSV Export**: Save results to CSV files if needed

## Installation

Ensure you have all required dependencies:

```bash
pip install -r requirements.txt
```

This will install:
- `mikeio` - For reading DFS0 files
- `numpy` - For numerical operations
- `pandas` - For table formatting and CSV export

## Usage

### Running the Interactive Analyzer

```bash
python interactive_analyzer.py
```

### Interactive Workflow

#### Step 1: Enter File Paths

The tool will ask for UNC file paths of all DFS0 locations:

```
Enter the UNC file paths for all DFS0 locations.
Enter one path per line. Press Enter on an empty line when done.

File 1 path (or press Enter to finish): \\server\path\location1.dfs0
✓ Added: \\server\path\location1.dfs0

File 2 path (or press Enter to finish): \\server\path\location2.dfs0
✓ Added: \\server\path\location2.dfs0

File 3 path (or press Enter to finish): 
```

#### Step 2: Review Files

The tool displays all files you've entered:

```
Files to Analyze:
----------------------------------------------------------------------
1: location1.dfs0
   Path: \\server\path\location1.dfs0
2: location2.dfs0
   Path: \\server\path\location2.dfs0
```

#### Step 3: Enter Scaling Factors

Enter scaling factors for each file using the format: `<file_number>: <scaling_factor>`

```
Scaling Factors Input
----------------------------------------------------------------------
Enter scaling factors for each file.
Format: <file_number>: <scaling_factor>
Example: 1: 1.4  (sets file 1 to scale factor 1.4)

Enter scaling (or 'done'/'list'): 1: 1.4
✓ File 1 (location1.dfs0): scale = 1.4

Enter scaling (or 'done'/'list'): 2: 1.0
✓ File 2 (location2.dfs0): scale = 1.0

Enter scaling (or 'done'/'list'): done
```

**Alternative input formats:**
- `1: 1.4` - with colon and space
- `1:1.4` - with colon, no space
- `1 1.4` - space-separated

**Shortcuts:**
- Type `list` to see the files again
- Type `done` when finished
- Press Enter without input to set all remaining files to 1.0

#### Step 4: View Results

The tool will:
1. Load all DFS0 files
2. Apply scaling factors
3. Generate exceedance tables for each threshold (5, 10, 25 mg/l)
4. **Display summary statistics on the command line** (NEW!)

**Summary Output Example:**

```
====================================================================================================
EXCEEDANCE TABLE: Threshold = 5.0 mg/l
====================================================================================================
Legend: X = Exceeds threshold, - = Below threshold
----------------------------------------------------------------------------------------------------

Summary (Total timesteps: 1440):
Receptor                                 Exceedances     Percentage     
----------------------------------------------------------------------
File1_Receptor_1                         523               36.3%
File1_Receptor_2                         892               62.0%
File2_Receptor_1                         678               47.1%
File2_Receptor_2                         1104              76.7%

====================================================================================================
```

This summary view is **perfect for quickly comparing different scaling factor combinations!**

#### Step 5: Optional Full Tables

You can optionally view the full tables with all timesteps:

```
Show full tables? (y/n): y
```

If you select 'y', you'll see the detailed table with X/- markers for each timestep.

#### Step 6: Optional CSV Export

You can optionally save the tables to CSV files:

```
Save tables to CSV files? (y/n): n
```

**You can skip this if you're just testing different combinations!**

#### Step 7: Try Different Combinations (NEW!)

After viewing results, you can try different scaling factors:

```
Try different scaling factors? (y/n): y
```

This lets you:
- Keep the same files loaded
- Enter new scaling factors
- See new results immediately
- Compare results in your terminal history
- Find the optimal combination without restarting

## Output Format

### Summary Statistics (Default View)

By default, you'll see a summary table for each threshold showing:
- **Receptor name**: Format `File<N>_<ReceptorName>`
- **Exceedances**: Number of timesteps exceeding the threshold
- **Percentage**: Percentage of total timesteps exceeding the threshold

This format is perfect for:
- Quick comparison of different scaling factors
- Identifying which receptors are most affected
- Finding optimal scaling combinations

### Full Table (Optional)

Each full table shows:
- **Rows**: Date/Time stamps from the DFS0 files
- **Columns**: Receptors from all files (format: `File<N>_<ReceptorName>`)
- **Values**: 
  - `X` = Concentration exceeds threshold at this time
  - `-` = Concentration below threshold at this time

### Example Full Table (5mg/l threshold)

```
Date/Time            File1_Receptor_1  File1_Receptor_2  File2_Receptor_1
2024-01-01 00:00:00  X                 X                 -
2024-01-01 01:00:00  X                 X                 X
2024-01-01 02:00:00  -                 X                 X
```

### CSV Files (Optional)

If you choose to save, three CSV files are generated, one for each threshold:
- `exceedance_table_5mgl_<timestamp>.csv` - 5 mg/l threshold
- `exceedance_table_10mgl_<timestamp>.csv` - 10 mg/l threshold  
- `exceedance_table_25mgl_<timestamp>.csv` - 25 mg/l threshold

The CSV files can be opened in Excel, imported into databases, or used for further analysis.

## Testing Different Scaling Combinations (NEW!)

One of the most powerful features is the ability to quickly test different scaling factor combinations:

### Workflow for Finding Optimal Scaling

1. **Enter files once** - Load all your DFS0 files
2. **Try first combination** - Start with initial scaling factors (e.g., all 1.0)
3. **View summary results** - See exceedance percentages immediately
4. **Decide to adjust** - Notice which receptors need adjustment
5. **Try new combination** - Enter different scaling factors (e.g., 1: 1.4, 2: 0.8)
6. **Compare results** - See new percentages, compare mentally or scroll up in terminal
7. **Iterate** - Keep trying until you find optimal combination
8. **Save final result** - Only save CSV when you're satisfied

### Example Iteration Session

```
First try: All scaling = 1.0
  File1_Receptor_1: 523 exceedances (36.3%)
  File2_Receptor_1: 892 exceedances (62.0%)

Second try: File1 = 1.4, File2 = 1.0
  File1_Receptor_1: 678 exceedances (47.1%)  ← Increased as expected
  File2_Receptor_1: 892 exceedances (62.0%)  ← Unchanged

Third try: File1 = 1.4, File2 = 0.8
  File1_Receptor_1: 678 exceedances (47.1%)  ← Unchanged
  File2_Receptor_1: 734 exceedances (51.0%)  ← Decreased as expected

Found optimal combination!
```

### Tips for Quick Comparison

- **Use terminal scroll** - Scroll up to see previous results
- **Take notes** - Write down interesting combinations
- **Focus on summary** - The percentage column is your key metric
- **Skip full tables** - Only view full tables when you need details
- **Skip CSV save** - Save only when you've found the best combination

## Example Session

Here's a complete example:

```bash
$ python interactive_analyzer.py

######################################################################
#                                                                    #
#    INTERACTIVE DFS0 ANALYZER - Multi-Receptor Exceedance Analysis #
#                                                                    #
######################################################################

======================================================================
DFS0 INTERACTIVE ANALYZER - File Input
======================================================================

Enter the UNC file paths for all DFS0 locations.
Enter one path per line. Press Enter on an empty line when done.
----------------------------------------------------------------------

File 1 path: \\data\site1\receptor_data.dfs0
✓ Added: \\data\site1\receptor_data.dfs0

File 2 path: \\data\site2\receptor_data.dfs0
✓ Added: \\data\site2\receptor_data.dfs0

File 3 path: 

======================================================================
Files to Analyze:
----------------------------------------------------------------------
1: receptor_data.dfs0
   Path: \\data\site1\receptor_data.dfs0
2: receptor_data.dfs0
   Path: \\data\site2\receptor_data.dfs0
======================================================================

======================================================================
Scaling Factors Input
======================================================================

Enter scaling factors for each file.
Format: <file_number>: <scaling_factor>
Example: 1: 1.4  (sets file 1 to scale factor 1.4)

Press Enter without input to use default scaling factor of 1.0
Type 'done' when finished, or 'list' to see files again.
----------------------------------------------------------------------

Enter scaling (or 'done'/'list'): 1: 1.4
✓ File 1 (receptor_data.dfs0): scale = 1.4

Enter scaling (or 'done'/'list'): 2: 1.0
✓ File 2 (receptor_data.dfs0): scale = 1.0

Enter scaling (or 'done'/'list'): done

======================================================================
Loading DFS0 Files...
----------------------------------------------------------------------
Loading file 1: receptor_data.dfs0... ✓ (scale: 1.4)
Loading file 2: receptor_data.dfs0... ✓ (scale: 1.0)
======================================================================
Successfully loaded 2 file(s)

======================================================================
Generating Exceedance Tables...
----------------------------------------------------------------------
Processing file 1: receptor_data.dfs0
Processing file 2: receptor_data.dfs0
✓ Tables generated successfully

[Tables displayed...]

Save tables to CSV files? (y/n): y
Enter output directory (or press Enter for current directory): ./output

======================================================================
Saving Tables to CSV...
----------------------------------------------------------------------
✓ Saved: exceedance_table_5mgl_20240101_153045.csv
✓ Saved: exceedance_table_10mgl_20240101_153045.csv
✓ Saved: exceedance_table_25mgl_20240101_153045.csv
======================================================================

######################################################################
#                        Analysis Complete!                          #
######################################################################
```

## Testing with Demo Files

To test the interactive analyzer with sample data:

```bash
# Create demo DFS0 files
python demo_interactive.py

# This will create sample files and show you the paths to use
# Then run the interactive analyzer and enter those paths
```

Or run an automated test:

```bash
python demo_interactive.py --test
```

## Tips

1. **File Paths**: Use full UNC paths (e.g., `\\server\share\file.dfs0`) or absolute paths
2. **Scaling Factors**: Use scaling factors to weight different sources or convert units
3. **Default Scaling**: Press Enter on empty input to use 1.0 for all remaining files
4. **Review Files**: Type `list` during scaling input to review the file list
5. **CSV Output**: Save to a dedicated output directory for better organization

## Troubleshooting

### File Not Found
If you get a file not found error, check:
- The UNC path is correct and accessible
- You have read permissions for the file
- The network path is reachable

### No Data Generated
If tables are empty:
- Check that DFS0 files contain data
- Verify the scaling factors are appropriate
- Ensure timestamps align across files

### Memory Issues
For very large DFS0 files:
- Process files in smaller batches
- Consider time range filtering (future feature)

## Advanced Usage

### Programmatic Usage

You can also use the analyzer programmatically:

```python
from interactive_analyzer import InteractiveDFS0Analyzer

# Create analyzer
analyzer = InteractiveDFS0Analyzer()

# Set up files manually
file_paths = [
    '\\\\server\\path\\location1.dfs0',
    '\\\\server\\path\\location2.dfs0'
]
scaling_factors = {1: 1.4, 2: 1.0}

# Load and analyze
analyzer.load_files(file_paths, scaling_factors)
tables = analyzer.generate_exceedance_tables()

# Save results
analyzer.save_tables_to_csv(tables, './output')
```

## Support

For issues or questions, please refer to the main README.md or create an issue in the repository.
