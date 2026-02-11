# Terminal Color Highlighting

## Overview

The daily exceedance tables now include terminal color highlighting to make it easier to identify values exceeding specific thresholds.

## Color Rules

### V Columns (V1-V4)

Values in V columns are highlighted in **ORANGE** when they exceed 15:

- Value ≤ 15: Normal (no color)
- Value > 15: **ORANGE** (ANSI 33)
- Value > 20: **ORANGE** (special rule - NOT red!)

### IT Columns (IT1-IT7)

Values in IT columns are highlighted in **RED** when they exceed 15:

- Value ≤ 15: Normal (no color)
- Value > 15: **RED** (ANSI 31)
- Value > 20: **RED**

## Visual Example

```
Date                  V1          V2          V3         IT1         IT2         IT3
01/01/2024            14          15          12          14          15          12
02/01/2024            16          20          18          16          20          18
03/01/2024            22          25          30          22          25          30
```

In the table above:
- Row 1: All values ≤15, shown in normal text
- Row 2: Values 16, 20, 18 are colored (ORANGE for V columns, RED for IT columns)
- Row 3: Values 22, 25, 30 are colored (ORANGE for V columns, RED for IT columns)

## Technical Implementation

### ANSI Escape Codes

The highlighting uses standard ANSI escape codes:

- **ORANGE**: `\033[33m` (ANSI 33)
- **RED**: `\033[31m` (ANSI 31)
- **RESET**: `\033[0m` (reset to default)

### Column Detection

The system automatically detects column types:

- **V columns**: Column name starts with 'V' followed by digit(s) (V1, V2, V3, V4)
- **IT columns**: Column name starts with 'IT' followed by digit(s) (IT1-IT7)
- **Other columns**: No color highlighting applied

### Alignment

The color codes are properly handled to maintain table alignment:
- ANSI codes add characters but take no visual space
- Padding is calculated based on visible character count
- Column widths remain consistent regardless of coloring

## Benefits

1. **Quick Identification**: Instantly spot values exceeding thresholds
2. **Visual Differentiation**: Different colors for V vs IT series
3. **Regulatory Focus**: Helps identify compliance issues at a glance
4. **Trend Spotting**: Easily see patterns of high values across days

## Compatibility

- Works in any terminal that supports ANSI color codes
- Most modern terminals (Linux, macOS, Windows Terminal, WSL)
- Colors are automatically stripped when output is redirected to files
- CSV exports remain unaffected (no color codes in files)

## Disabling Colors

If you need to disable colors (e.g., for automated scripts), you can:

1. Redirect output to a file (colors are automatically stripped):
   ```bash
   python interactive_analyzer.py > output.txt
   ```

2. Use environment variables (if implemented):
   ```bash
   NO_COLOR=1 python interactive_analyzer.py
   ```

## Example Output

When running the interactive analyzer with format option 1 (Daily Exceedance Percentages), you'll see:

```
====================================================================================================
DAILY EXCEEDANCE TABLE: Threshold = 5.0 mg/l
====================================================================================================
Each cell shows the percentage of that day's timesteps exceeding the threshold
----------------------------------------------------------------------------------------------------
Date                  V1          V2          V3          V4         IT1         IT2         IT3
01/01/2024            12          14          16          18          12          14          16
02/01/2024            19          21          23          25          19          21          23
03/01/2024            22          24          26          28          22          24          26
```

In this example:
- V1=12, V2=14, IT1=12, IT2=14: Normal text (≤15)
- V3=16, V4=18, IT3=16: Colored (ORANGE for V3/V4, RED for IT3)
- All row 2 and 3 values: Colored (ORANGE for V columns, RED for IT columns)

## Implementation Details

For developers, the color highlighting is implemented in `interactive_analyzer.py`:

- `_apply_color_to_value()`: Applies colors based on column and value
- `_format_colored_table()`: Formats entire DataFrame with colors
- `display_daily_tables()`: Uses colored formatting for display

The implementation is efficient and doesn't affect CSV export or data processing, only the terminal display.
