# Interactive DFS0 Analyzer - Example Session

This document shows a complete example session using the interactive analyzer.

## Running the Interactive Analyzer

```bash
$ python interactive_analyzer.py
```

## Complete Example Session

```
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

File 1 path (or press Enter to finish): \\server\project\location1.dfs0
✓ Added: \\server\project\location1.dfs0

File 2 path (or press Enter to finish): \\server\project\location2.dfs0
✓ Added: \\server\project\location2.dfs0

File 3 path (or press Enter to finish): \\server\project\location3.dfs0
✓ Added: \\server\project\location3.dfs0

File 4 path (or press Enter to finish): 

======================================================================
Files to Analyze:
----------------------------------------------------------------------
1: location1.dfs0
   Path: \\server\project\location1.dfs0
2: location2.dfs0
   Path: \\server\project\location2.dfs0
3: location3.dfs0
   Path: \\server\project\location3.dfs0
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
✓ File 1 (location1.dfs0): scale = 1.4

Enter scaling (or 'done'/'list'): 2: 1.0
✓ File 2 (location2.dfs0): scale = 1.0

Enter scaling (or 'done'/'list'): 3: 0.8
✓ File 3 (location3.dfs0): scale = 0.8

Enter scaling (or 'done'/'list'): done

======================================================================
Loading DFS0 Files...
----------------------------------------------------------------------
Loading file 1: location1.dfs0... ✓ (scale: 1.4)
Loading file 2: location2.dfs0... ✓ (scale: 1.0)
Loading file 3: location3.dfs0... ✓ (scale: 0.8)
======================================================================
Successfully loaded 3 file(s)

======================================================================
Generating Exceedance Tables...
----------------------------------------------------------------------
Processing file 1: location1.dfs0
Processing file 2: location2.dfs0
Processing file 3: location3.dfs0
✓ Tables generated successfully

====================================================================================================
EXCEEDANCE TABLE: Threshold = 5.0 mg/l
====================================================================================================
Legend: X = Exceeds threshold, - = Below threshold
----------------------------------------------------------------------------------------------------

First 10 rows:
Date/Time            File1_Receptor_1  File1_Receptor_2  File2_Receptor_1  File2_Receptor_2  File3_Receptor_1
2024-01-01 00:00:00  X                 X                 X                 X                 X
2024-01-01 01:00:00  X                 X                 X                 X                 X
2024-01-01 02:00:00  X                 X                 -                 X                 X
2024-01-01 03:00:00  X                 X                 X                 X                 -
2024-01-01 04:00:00  -                 X                 X                 X                 X
2024-01-01 05:00:00  X                 X                 X                 X                 X
2024-01-01 06:00:00  X                 X                 X                 X                 X
2024-01-01 07:00:00  X                 -                 X                 X                 X
2024-01-01 08:00:00  X                 X                 X                 X                 -
2024-01-01 09:00:00  -                 X                 -                 X                 X

... (more rows omitted) ...

====================================================================================================

====================================================================================================
EXCEEDANCE TABLE: Threshold = 10.0 mg/l
====================================================================================================
Legend: X = Exceeds threshold, - = Below threshold
----------------------------------------------------------------------------------------------------

First 10 rows:
Date/Time            File1_Receptor_1  File1_Receptor_2  File2_Receptor_1  File2_Receptor_2  File3_Receptor_1
2024-01-01 00:00:00  X                 X                 -                 X                 X
2024-01-01 01:00:00  -                 X                 X                 X                 -
2024-01-01 02:00:00  X                 X                 -                 X                 X
2024-01-01 03:00:00  X                 -                 X                 X                 -
2024-01-01 04:00:00  -                 X                 -                 X                 X
2024-01-01 05:00:00  X                 X                 X                 -                 X
2024-01-01 06:00:00  -                 X                 X                 X                 -
2024-01-01 07:00:00  X                 -                 X                 X                 X
2024-01-01 08:00:00  X                 X                 -                 -                 -
2024-01-01 09:00:00  -                 X                 -                 X                 X

... (more rows omitted) ...

====================================================================================================

====================================================================================================
EXCEEDANCE TABLE: Threshold = 25.0 mg/l
====================================================================================================
Legend: X = Exceeds threshold, - = Below threshold
----------------------------------------------------------------------------------------------------

First 10 rows:
Date/Time            File1_Receptor_1  File1_Receptor_2  File2_Receptor_1  File2_Receptor_2  File3_Receptor_1
2024-01-01 00:00:00  -                 -                 -                 X                 -
2024-01-01 01:00:00  -                 X                 -                 -                 -
2024-01-01 02:00:00  -                 -                 -                 X                 -
2024-01-01 03:00:00  -                 -                 -                 -                 -
2024-01-01 04:00:00  -                 -                 -                 X                 -
2024-01-01 05:00:00  -                 X                 -                 -                 -
2024-01-01 06:00:00  -                 -                 -                 -                 -
2024-01-01 07:00:00  -                 -                 -                 X                 -
2024-01-01 08:00:00  -                 -                 -                 -                 -
2024-01-01 09:00:00  -                 -                 -                 -                 -

... (more rows omitted) ...

====================================================================================================

Save tables to CSV files? (y/n): y
Enter output directory (or press Enter for current directory): ./results

======================================================================
Saving Tables to CSV...
----------------------------------------------------------------------
✓ Saved: exceedance_table_5mgl_20240115_143022.csv
✓ Saved: exceedance_table_10mgl_20240115_143022.csv
✓ Saved: exceedance_table_25mgl_20240115_143022.csv
======================================================================

######################################################################
#                        Analysis Complete!                          #
######################################################################
```

## CSV Output Example

The generated CSV files can be opened in Excel or any spreadsheet software:

**exceedance_table_10mgl_20240115_143022.csv:**

```csv
Date/Time,File1_Receptor_1,File1_Receptor_2,File2_Receptor_1,File2_Receptor_2,File3_Receptor_1
2024-01-01 00:00:00,X,X,-,X,X
2024-01-01 01:00:00,-,X,X,X,-
2024-01-01 02:00:00,X,X,-,X,X
2024-01-01 03:00:00,X,-,X,X,-
2024-01-01 04:00:00,-,X,-,X,X
2024-01-01 05:00:00,X,X,X,-,X
```

## Interpreting the Results

### What the Tables Show

- **Each row** represents a specific date/time from your DFS0 files
- **Each column** represents a receptor (measurement location) from each file
  - Format: `File<N>_<ReceptorName>`
  - Example: `File1_Receptor_1` means the first receptor from file 1
- **'X'** indicates the concentration exceeded the threshold at that time
- **'-'** indicates the concentration was below the threshold at that time

### How Scaling Works

In the example above:
- **File 1** has scaling factor 1.4 → all values multiplied by 1.4
- **File 2** has scaling factor 1.0 → values unchanged
- **File 3** has scaling factor 0.8 → all values multiplied by 0.8

This allows you to weight different sources or convert between units.

### Understanding the Three Thresholds

The tool generates three separate tables:

1. **5 mg/l threshold** - Often the most stringent regulatory limit
2. **10 mg/l threshold** - Moderate concern level
3. **25 mg/l threshold** - Higher concern level

You can see patterns across thresholds:
- More 'X' marks in the 5 mg/l table (lower threshold, more exceedances)
- Fewer 'X' marks in the 25 mg/l table (higher threshold, fewer exceedances)

### Use Cases

**Regulatory Compliance:**
- Quickly identify when and where concentrations exceed regulatory limits
- Generate reports showing compliance/non-compliance dates

**Trend Analysis:**
- Compare different receptors to find hotspots
- Identify temporal patterns (time of day, seasonal variations)

**What-If Scenarios:**
- Test different scaling factors to see impact on exceedances
- Evaluate mitigation strategies by adjusting source contributions

## Tips for Large Datasets

For DFS0 files with many timesteps:
- The table display will show first and last 10 rows
- Full data is always saved to CSV
- Open CSV in Excel to filter and analyze specific dates/receptors

## Next Steps

After generating your tables, you can:
1. Open CSV files in Excel for detailed analysis
2. Create pivot tables to summarize exceedances
3. Generate charts showing temporal trends
4. Compare results across different scenarios (by varying scaling factors)
