# DFS0 File Analyzer and Calculator

A Python tool for analyzing DFS0 files (DHI MIKE format) with a focus on Suspended Sediment Concentration (SSC) analysis. This tool provides timestep-to-timestep summation with optional scaling multipliers and calculates the percentage of time concentrations exceed specified thresholds.

## Features

- **DFS0 File Reading**: Load and parse DFS0 files using the mikeio library
- **Multi-item Summation**: Combine multiple data items from the DFS0 file
- **Scaling Multipliers**: Apply scaling factors to each item before summation
- **Exceedance Analysis**: Calculate the percentage of time total concentrations exceed a threshold
- **Flexible Time Range**: Analyze specific time ranges (e.g., first 1440 timesteps)
- **Command-Line Interface**: Easy-to-use CLI for quick analysis
- **Python API**: Programmatic access for integration into other workflows

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `mikeio` - Library for reading DHI MIKE files
- `numpy` - Numerical computing library

## Usage

### Command-Line Interface

#### List Items in a DFS0 File

```bash
python dfs0_analyzer.py yourfile.dfs0 --list-items
```

#### Basic Analysis

Analyze a single item with a threshold:

```bash
python dfs0_analyzer.py yourfile.dfs0 --items SSC1 --threshold 100.0
```

#### Multiple Items with Scaling

Analyze multiple items with scaling factors:

```bash
python dfs0_analyzer.py yourfile.dfs0 --items SSC1 SSC2 --scaling 1.0 0.5 --threshold 100.0
```

#### Analyze Specific Time Range

Analyze the first 1440 timesteps (e.g., 1-second timesteps for 24 minutes):

```bash
python dfs0_analyzer.py yourfile.dfs0 --items SSC1 --threshold 100.0 --start 0 --num-timesteps 1440
```

### Python API

```python
from dfs0_analyzer import DFS0Analyzer

# Create analyzer
analyzer = DFS0Analyzer('yourfile.dfs0')
analyzer.load_file()

# List available items
items = analyzer.get_item_names()
print(f"Available items: {items}")

# Perform complete analysis
result = analyzer.analyze_ssc(
    ssc_items=['SSC1', 'SSC2'],  # Items to analyze
    scaling_factors=[1.0, 0.5],   # Optional scaling factors
    threshold=100.0,               # Concentration threshold
    start_index=0,                 # Start at first timestep
    num_timesteps=1440            # Analyze first 1440 timesteps
)

# Access results
print(f"Exceedance percentage: {result['exceedance_stats']['percentage']:.2f}%")
print(f"Timesteps exceeded: {result['exceedance_stats']['count_exceeded']}")
print(f"Total timesteps: {result['exceedance_stats']['total_timesteps']}")

# Access total SSC values at each timestep
total_ssc = result['total_ssc']
```

## Example Use Case

**Scenario**: You have a DFS0 file with SSC data from multiple sources at an extraction point. You want to:
1. Sum the SSC contributions with different scaling factors
2. Find out what percentage of the first 1440 1-second timesteps exceed a concentration of 100 mg/L

**Solution**:

```bash
python dfs0_analyzer.py extraction_point.dfs0 \
    --items Source1_SSC Source2_SSC Source3_SSC \
    --scaling 1.0 0.8 0.6 \
    --threshold 100.0 \
    --start 0 \
    --num-timesteps 1440
```

**Output**:
```
=== DFS0 SSC Analysis Results ===
Items analyzed: Source1_SSC, Source2_SSC, Source3_SSC
Scaling factors: 1.0, 0.8, 0.6

Threshold: 100.0
Timesteps analyzed: 1440

Exceedance Statistics:
  Percentage of time exceeding threshold: 45.83%
  Count exceeded: 660
  Total timesteps: 1440

Total SSC Statistics:
  Min: 12.3456
  Max: 234.5678
  Mean: 98.7654
  Std Dev: 45.6789
```

## API Reference

### DFS0Analyzer Class

#### `__init__(filepath: str)`
Initialize the analyzer with a DFS0 file path.

#### `load_file()`
Load the DFS0 file and extract data.

#### `get_item_names() -> List[str]`
Get the names of all items (variables) in the DFS0 file.

#### `get_item_data(item_name: str) -> np.ndarray`
Get data for a specific item.

#### `calculate_sum_with_scaling(item_names, scaling_factors=None) -> np.ndarray`
Calculate the sum of specified items with optional scaling factors.

**Parameters:**
- `item_names`: Single item name or list of item names
- `scaling_factors`: Single scaling factor or list of scaling factors (default: 1.0)

**Returns:** Numpy array of summed values at each timestep

#### `calculate_exceedance_percentage(values, threshold, start_index=0, num_timesteps=None) -> Dict`
Calculate the percentage of time values exceed a threshold.

**Parameters:**
- `values`: Array of values to analyze
- `threshold`: Concentration threshold
- `start_index`: Starting timestep index (default: 0)
- `num_timesteps`: Number of timesteps to analyze (default: all)

**Returns:** Dictionary with percentage, count_exceeded, total_timesteps, threshold

#### `analyze_ssc(ssc_items, scaling_factors=None, threshold=0.0, start_index=0, num_timesteps=None) -> Dict`
Perform complete SSC analysis.

**Parameters:**
- `ssc_items`: SSC item name(s) to analyze
- `scaling_factors`: Optional scaling factor(s)
- `threshold`: Concentration threshold (default: 0.0)
- `start_index`: Starting timestep index (default: 0)
- `num_timesteps`: Number of timesteps to analyze (default: all)

**Returns:** Dictionary with total_ssc, exceedance_stats, timesteps_analyzed

## Testing

To verify the installation and basic functionality:

```python
# Create a simple test
from dfs0_analyzer import DFS0Analyzer
import numpy as np

# Test the calculation logic (without requiring a DFS0 file)
values = np.array([50, 100, 150, 200, 75, 125])
analyzer = DFS0Analyzer.__new__(DFS0Analyzer)
result = analyzer.calculate_exceedance_percentage(values, threshold=100.0)
print(f"Test result: {result['percentage']}% exceeded") # Should be 50%
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please create an issue in the GitHub repository.