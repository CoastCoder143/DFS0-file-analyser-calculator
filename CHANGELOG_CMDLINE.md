# Command-Line Output Enhancement - Summary

## Problem Statement
User wanted: "iwant the cmd output on the commandline, not in csv so i can keep trying different combination"

## Solution Implemented

### What Changed

1. **Summary Display by Default**
   - Instead of showing full tables with X/- markers, now shows concise summary statistics
   - Displays exceedance count and percentage for each receptor
   - Much easier to compare different scaling combinations

2. **Iterative Loop**
   - After viewing results, user can choose to try different scaling factors
   - Files stay loaded - only scaling factors change
   - No need to restart the program for each combination

3. **Optional Features**
   - Full tables: Only shown if user requests them
   - CSV export: Only saved if user requests it
   - Both are opt-in instead of automatic

### Example Workflow

**Before (Old Behavior):**
```
1. Run program
2. Enter files
3. Enter scaling factors
4. See full tables (many pages)
5. Forced to save CSV
6. Exit
7. Run program again to try different scaling
8. Re-enter files
9. Enter new scaling factors
10. See tables again...
```

**After (New Behavior):**
```
1. Run program
2. Enter files (once)
3. Enter scaling factors
4. See summary statistics (quick view)
5. Choose: Try different scaling? → Yes
6. Enter new scaling factors
7. See new summary statistics
8. Compare with previous (scroll up in terminal)
9. Repeat until satisfied
10. Optionally save to CSV if desired
11. Exit
```

### Output Format

**Summary View (Default):**
```
====================================================================================================
EXCEEDANCE TABLE: Threshold = 5.0 mg/l
====================================================================================================
Summary (Total timesteps: 1440):
Receptor                                 Exceedances     Percentage     
----------------------------------------------------------------------
File1_Receptor_1                         523               36.3%
File1_Receptor_2                         892               62.0%
File2_Receptor_1                         678               47.1%
File2_Receptor_2                         1104              76.7%
====================================================================================================
```

**Benefits:**
- ✅ Quick to read (fits on one screen)
- ✅ Easy to compare percentages
- ✅ No CSV files unless you want them
- ✅ Perfect for rapid experimentation
- ✅ Terminal scroll shows all previous tries

### Files Modified

1. **interactive_analyzer.py**
   - Enhanced `display_tables()` method with `show_full` parameter
   - Modified `run()` method to include iteration loop
   - Added summary statistics display
   - Made CSV export optional

2. **INTERACTIVE_GUIDE.md**
   - Updated features list
   - Added new workflow documentation
   - Added section on testing different combinations
   - Updated example output

3. **test_enhanced_interactive.py** (new)
   - Tests for summary display feature
   - Demonstrates the new workflow

### Testing

All tests pass:
- ✅ Original DFS0 analyzer tests
- ✅ Interactive analyzer tests  
- ✅ New enhanced display tests

### User Benefits

1. **Faster Iteration**: Try multiple scaling combinations in one session
2. **Command-Line Focus**: Results displayed immediately in terminal
3. **No Forced CSV**: Save only when you've found the optimal combination
4. **Easy Comparison**: Scroll terminal to see previous results
5. **Summary First**: See key statistics without information overload

### How to Use

```bash
python interactive_analyzer.py
```

1. Enter your DFS0 file paths
2. Enter scaling factors (e.g., "1: 1.4")
3. View summary results on screen
4. When asked "Try different scaling factors?", answer "y"
5. Enter new scaling factors
6. Compare results with previous (scroll up)
7. Repeat until satisfied
8. Optionally save to CSV when done

Perfect for finding the optimal scaling combination through experimentation!
