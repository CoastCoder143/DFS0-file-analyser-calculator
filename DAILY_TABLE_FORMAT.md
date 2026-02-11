# Daily Exceedance Table Format - Documentation

## Overview

The daily exceedance table format provides a day-by-day view of exceedances, showing the percentage of each day's timesteps where concentrations exceeded specified thresholds.

## Table Structure

### Orientation
- **One table per threshold** (5 mg/l, 10 mg/l, 25 mg/l)
- **Rows**: Calendar days (one row per date)
- **Columns**: Fixed order - Date | V1 | V2 | V3 | V4 | IT1 | IT2 | IT3 | IT4 | IT5 | IT6 | IT7

### Column Definitions

#### Date Column
- **Type**: String (Date)
- **Format**: D/M/YYYY (e.g., "01/01/2024" or "1/1/2024")
- **Note**: Leading zeros may vary depending on display

#### V Series (V1-V4)
- **Type**: Numeric (integer percentage)
- **Expected timesteps per day**: 73
- **Meaning**: Each cell shows:
  ```
  % = 100 × (# timesteps where Vx > threshold) / (total timesteps that day)
  ```
- **Range**: 0-100
- **Rounding**: Rounded to nearest integer

#### IT Series (IT1-IT7)
- **Type**: Numeric (integer percentage)
- **Expected timesteps per day**: 144
- **Meaning**: Each cell shows:
  ```
  % = 100 × (# timesteps where ITx > threshold) / (total timesteps that day)
  ```
- **Range**: 0-100
- **Rounding**: Rounded to nearest integer

### Row Ordering
- Dates sorted in ascending order (earliest date first)
- Days with no data may appear with 0% or may be omitted

### Cell Values
- **Type**: Integer (0-100)
- **Meaning**: Percentage of that day's timesteps exceeding the threshold
- **Special cases**:
  - 0 = No exceedances that day
  - 100 = All timesteps exceeded threshold that day

## Example Table

```
Date        V1  V2  V3  V4  IT1 IT2 IT3 IT4 IT5 IT6 IT7
01/01/2024  45  67  23  12   34  56  78  90  45  23  12
02/01/2024  50  70  25  15   38  60  80  92  48  25  15
03/01/2024  42  65  20  10   30  55  75  88  42  20  10
```

## Usage

### In Interactive Mode

1. Run the analyzer:
   ```bash
   python interactive_analyzer.py
   ```

2. When prompted for table format, choose option 1:
   ```
   Choose format (1 or 2, default=1): 1
   ```

3. Results will be displayed on screen and can be saved to CSV.

### CSV Output

When saved, creates files like:
- `daily_exceedance_table_5mgl_TIMESTAMP.csv`
- `daily_exceedance_table_10mgl_TIMESTAMP.csv`
- `daily_exceedance_table_25mgl_TIMESTAMP.csv`

CSV format:
```csv
Date,V1,V2,V3,V4,IT1,IT2,IT3,IT4,IT5,IT6,IT7
01/01/2024,45,67,23,12,34,56,78,90,45,23,12
02/01/2024,50,70,25,15,38,60,80,92,48,25,15
```

## Summary Statistics

The display includes summary statistics for each series:
- **Mean %**: Average exceedance percentage across all days
- **Max %**: Highest single-day exceedance percentage
- **Days with exceedance**: Number of days where at least one timestep exceeded

## Comparison with Original Format

### Daily Format (NEW)
- **Granularity**: One row per day
- **Cell values**: Percentage (0-100)
- **Use case**: Day-by-day trends, regulatory compliance tracking
- **Output size**: Smaller (one row per day)

### Timestep Format (Original)
- **Granularity**: One row per timestep
- **Cell values**: X/- markers
- **Use case**: Detailed timestep analysis
- **Output size**: Larger (one row per timestep)

## Technical Notes

### Expected Timesteps
- The expected timesteps per day (73 for V, 144 for IT) are configurable
- If actual timesteps differ from expected, the percentage uses actual count as denominator
- This ensures percentages remain meaningful even with irregular data

### Date Handling
- Dates are extracted from timestamp data using calendar day boundaries
- All timesteps on the same calendar day are grouped together
- Timezone is preserved from original DFS0 files

### Missing Data
- If a day has no data, it may be:
  - Omitted from the table entirely, or
  - Shown with 0% (depending on implementation)
- This is handled automatically based on the data present

## Example Use Cases

1. **Regulatory Compliance**: Check which days exceeded regulatory limits
2. **Trend Analysis**: Identify patterns in daily exceedance rates
3. **Event Detection**: Spot specific days with high exceedance rates
4. **Reporting**: Generate daily summary reports for stakeholders
5. **Comparison**: Compare different monitoring locations across same time period
