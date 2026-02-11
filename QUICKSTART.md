# DFS0 File Analyzer - Quick Start Guide

## Overview
This tool analyzes DFS0 files (DHI MIKE format) for Suspended Sediment Concentration (SSC) analysis. It provides two modes:

1. **Interactive Mode**: Multi-receptor analysis with exceedance tables (NEW!)
2. **Command-Line Mode**: Single-file analysis with statistics

## Installation

```bash
pip install -r requirements.txt
```

## Interactive Mode (Multi-Receptor Analysis)

For analyzing multiple DFS0 files with exceedance tables:

```bash
python interactive_analyzer.py
```

**What it does:**
- Asks for multiple UNC file paths
- Lets you set scaling factors (e.g., "1: 1.4" for file 1 with scale 1.4)
- Generates tables showing dates vs receptors
- Creates separate tables for 5mg/l, 10mg/l, and 25mg/l thresholds
- Exports to CSV files

**Example Output Table:**
```
Date/Time            File1_Receptor_1  File1_Receptor_2  File2_Receptor_1
2024-01-01 00:00:00  X                 X                 -
2024-01-01 01:00:00  X                 X                 X
```
(X = exceeds threshold, - = below threshold)

👉 **See [INTERACTIVE_GUIDE.md](INTERACTIVE_GUIDE.md) for full details**

## Command-Line Mode (Single File Analysis)

### Quick Usage Examples

### Example 1: Analyze a single SSC item
```bash
python dfs0_analyzer.py yourfile.dfs0 --items SSC --threshold 100.0
```

### Example 2: Analyze first 1440 timesteps (e.g., 1440 1-second intervals)
```bash
python dfs0_analyzer.py yourfile.dfs0 \
    --items SSC \
    --threshold 100.0 \
    --start 0 \
    --num-timesteps 1440
```

### Example 3: Multiple items with scaling factors
```bash
python dfs0_analyzer.py yourfile.dfs0 \
    --items Source1_SSC Source2_SSC Source3_SSC \
    --scaling 1.0 0.8 0.5 \
    --threshold 150.0 \
    --num-timesteps 1440
```

### Example 4: List all items in a DFS0 file
```bash
python dfs0_analyzer.py yourfile.dfs0 --list-items
```

## Python API Usage

```python
from dfs0_analyzer import DFS0Analyzer

# Load and analyze
analyzer = DFS0Analyzer('yourfile.dfs0')
analyzer.load_file()

# Perform analysis
result = analyzer.analyze_ssc(
    ssc_items=['SSC1', 'SSC2'],
    scaling_factors=[1.0, 0.5],
    threshold=100.0,
    start_index=0,
    num_timesteps=1440
)

# Access results
print(f"Exceedance: {result['exceedance_stats']['percentage']:.2f}%")
print(f"Count: {result['exceedance_stats']['count_exceeded']}")
```

## What the Tool Does

1. **Reads DFS0 files**: Extracts SSC data from extraction points
2. **Sums multiple items**: Combines data from multiple sources
3. **Applies scaling**: Multiplies each item by a scaling factor before summing
4. **Calculates exceedance**: Determines percentage of time above threshold
5. **Flexible time ranges**: Analyze specific timestep ranges

## Key Features

✓ Command-line interface for quick analysis
✓ Python API for integration into workflows
✓ Multiple item summation with scaling
✓ Exceedance percentage calculation
✓ Flexible time range selection
✓ Comprehensive error handling
✓ Well-tested and documented

## Running Tests

```bash
# Run the test suite
python test_dfs0_analyzer.py

# Run example demonstrations
python example_usage.py
```

## Common Use Cases

**Use Case 1**: Analyze total SSC from multiple sources at an extraction point
- Sum SSC contributions from different sources
- Apply scaling factors if sources have different weights
- Find percentage exceeding regulatory threshold

**Use Case 2**: Analyze specific time period (e.g., first 24 minutes at 1-second intervals)
- Use `--start 0 --num-timesteps 1440`
- Calculate percentage exceeding concentration limit
- Compare different time periods

**Use Case 3**: Multiple threshold analysis
- Test different concentration thresholds
- Determine compliance levels
- Generate reports for stakeholders

## Output Format

The tool provides:
- **Percentage**: % of time exceeding threshold
- **Count**: Number of timesteps exceeding threshold
- **Total timesteps**: Number of timesteps analyzed
- **Statistics**: Min, Max, Mean, Std Dev of total SSC

## Requirements

- Python 3.7+
- mikeio (for reading DFS0 files)
- numpy (for numerical calculations)

## Getting Help

```bash
python dfs0_analyzer.py --help
```

See README.md for detailed documentation.
