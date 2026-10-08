import re
import math
from collections import Counter

def parse_dataset(text):
    """
    Parses numbers from a user input string separated by commas, spaces, 
    semicolons, or newlines.
    """
    if not text or not str(text).strip():
        raise ValueError("Please enter at least one number.")
    
    tokens = re.split(r'[,;\s]+', str(text).strip())
    data = []
    for token in tokens:
        if not token:
            continue
        try:
            val = float(token)
            data.append(val)
        except ValueError:
            raise ValueError(f"Invalid numeric value: '{token}'")
            
    if not data:
        raise ValueError("No valid numbers found in the input.")
    return data

def format_num(val, max_decimals=4):
    """Formats numeric values nicely: integers as whole numbers, floats rounded."""
    if val is None:
        return "N/A"
    if isinstance(val, (int, float)):
        if math.isnan(val):
            return "NaN"
        if math.isinf(val):
            return "Infinity" if val > 0 else "-Infinity"
        if math.isclose(val, round(val), abs_tol=1e-9):
            return str(int(round(val)))
        return f"{val:.{max_decimals}f}".rstrip('0').rstrip('.')
    return str(val)

def _calc_median_helper(sorted_list):
    """Returns (median_val, step_text) for a sorted list."""
    k = len(sorted_list)
    if k == 0:
        return None, ""
    if k % 2 == 1:
        idx = k // 2
        med = sorted_list[idx]
        step = f"Since n = {k} (odd), median is middle element at position {(k + 1) // 2} = {format_num(med)}"
        return med, step
    else:
        idx1 = k // 2 - 1
        idx2 = k // 2
        val1 = sorted_list[idx1]
        val2 = sorted_list[idx2]
        med = (val1 + val2) / 2.0
        step = (f"Since n = {k} (even), median is average of elements at positions "
                f"{k // 2} ({format_num(val1)}) and {k // 2 + 1} ({format_num(val2)}): "
                f"({format_num(val1)} + {format_num(val2)}) / 2 = {format_num(med)}")
        return med, step

def calculate_full_statistics(data):
    """
    Performs full statistical calculations and returns structured results
    with comprehensive step-by-step processes and deviation tables.
    """
    n = len(data)
    data_sorted = sorted(data)
    sum_x = sum(data)
    mean_val = sum_x / n
    sum_x_squared = sum(x**2 for x in data)
    
    # Deviation Table and Sum of Squares
    deviation_rows = []
    sum_dev = 0.0
    sum_abs_dev = 0.0
    sum_sq_dev = 0.0
    
    for idx, x in enumerate(data, start=1):
        dev = x - mean_val
        abs_dev = abs(dev)
        sq_dev = dev ** 2
        
        sum_dev += dev
        sum_abs_dev += abs_dev
        sum_sq_dev += sq_dev
        
        deviation_rows.append({
            'index': idx,
            'x': format_num(x),
            'dev': format_num(dev),
            'abs_dev': format_num(abs_dev),
            'sq_dev': format_num(sq_dev)
        })
        
    table_totals = {
        'sum_x': format_num(sum_x),
        'sum_dev': format_num(round(sum_dev, 8)), # essentially 0
        'sum_abs_dev': format_num(sum_abs_dev),
        'sum_sq_dev': format_num(sum_sq_dev)
    }

    # Minimum, Maximum, Range
    min_val = data_sorted[0]
    max_val = data_sorted[-1]
    range_val = max_val - min_val

    # Median
    median_val, median_explanation = _calc_median_helper(data_sorted)

    # Mode calculation
    freq_counter = Counter(data)
    max_freq = max(freq_counter.values()) if freq_counter else 0
    freq_table = [
        {'value': format_num(val), 'count': count} 
        for val, count in sorted(freq_counter.items(), key=lambda item: (-item[1], item[0]))
    ]
    
    if n > 1 and max_freq == 1:
        mode_text = "No unique mode (all values appear once)"
        modes = []
    else:
        modes = [val for val, count in freq_counter.items() if count == max_freq]
        modes_sorted = sorted(modes)
        modes_formatted = [format_num(m) for m in modes_sorted]
        if len(modes) == 1:
            mode_text = f"{modes_formatted[0]} (frequency: {max_freq})"
        elif len(modes) == 2:
            mode_text = f"Bimodal: {', '.join(modes_formatted)} (frequency: {max_freq})"
        else:
            mode_text = f"Multimodal: {', '.join(modes_formatted)} (frequency: {max_freq})"

    # Variance and Standard Deviation
    if n > 1:
        sample_var = sum_sq_dev / (n - 1)
        sample_sd = math.sqrt(sample_var)
        se_mean = sample_sd / math.sqrt(n)
    else:
        sample_var = None
        sample_sd = None
        se_mean = None

    pop_var = sum_sq_dev / n
    pop_sd = math.sqrt(pop_var)
    mad_val = sum_abs_dev / n

    # Quartiles (Tukey's method)
    if n >= 4:
        if n % 2 == 0:
            lower_half = data_sorted[:n // 2]
            upper_half = data_sorted[n // 2:]
        else:
            lower_half = data_sorted[:n // 2]
            upper_half = data_sorted[n // 2 + 1:]
        q1_val, q1_step = _calc_median_helper(lower_half)
        q3_val, q3_step = _calc_median_helper(upper_half)
        iqr_val = q3_val - q1_val if (q1_val is not None and q3_val is not None) else None
    else:
        q1_val, q3_val, iqr_val = None, None, None
        q1_step = "Requires at least 4 data points"
        q3_step = "Requires at least 4 data points"

    # Step-by-Step Explanations dictionary
    sum_terms = " + ".join(format_num(x) for x in data[:8])
    if n > 8:
        sum_terms += f" + ... ({n - 8} more)"

    steps = {
        'mean': {
            'title': "Arithmetic Mean (x̄)",
            'formula': "x̄ = (Σ xᵢ) / n",
            'step1': f"Calculate the sum of all data values: Σ x = {sum_terms} = {format_num(sum_x)}",
            'step2': f"Divide the sum by total sample size (n = {n}): {format_num(sum_x)} / {n}",
            'result': format_num(mean_val)
        },
        'median': {
            'title': "Median (Middle Value)",
            'formula': "Position = (n + 1) / 2 (for odd n), or average of n/2 and (n/2 + 1) (for even n)",
            'step1': f"Sort data in ascending order: [{', '.join(format_num(x) for x in data_sorted)}]",
            'step2': median_explanation,
            'result': format_num(median_val)
        },
        'mode': {
            'title': "Mode (Most Frequent Value)",
            'formula': "Value(s) with maximum frequency in the dataset",
            'step1': f"Count frequencies of each unique value (highest frequency = {max_freq}).",
            'step2': mode_text,
            'result': mode_text
        },
        'sample_variance': {
            'title': "Sample Variance (s²)",
            'formula': "s² = Σ(xᵢ - x̄)² / (n - 1)",
            'step1': f"Compute sum of squared deviations from mean (SS): SS = {format_num(sum_sq_dev)}",
            'step2': f"Divide by degrees of freedom (n - 1 = {n - 1}): {format_num(sum_sq_dev)} / {n - 1}" if n > 1 else "Sample variance requires at least n = 2 data points.",
            'result': format_num(sample_var) if sample_var is not None else "Undefined (n < 2)"
        },
        'sample_stdev': {
            'title': "Sample Standard Deviation (s)",
            'formula': "s = √(s²)",
            'step1': f"Take the positive square root of sample variance: √({format_num(sample_var)})" if sample_var is not None else "Requires at least n = 2 data points.",
            'step2': f"s = {format_num(sample_sd)}" if sample_sd is not None else "Undefined",
            'result': format_num(sample_sd) if sample_sd is not None else "Undefined (n < 2)"
        },
        'pop_variance': {
            'title': "Population Variance (σ²)",
            'formula': "σ² = Σ(xᵢ - μ)² / n",
            'step1': f"Compute sum of squared deviations: SS = {format_num(sum_sq_dev)}",
            'step2': f"Divide by total population count (N = {n}): {format_num(sum_sq_dev)} / {n}",
            'result': format_num(pop_var)
        },
        'pop_stdev': {
            'title': "Population Standard Deviation (σ)",
            'formula': "σ = √(σ²)",
            'step1': f"Take square root of population variance: √({format_num(pop_var)})",
            'step2': f"σ = {format_num(pop_sd)}",
            'result': format_num(pop_sd)
        },
        'mad': {
            'title': "Mean Absolute Deviation (MAD)",
            'formula': "MAD = Σ|xᵢ - x̄| / n",
            'step1': f"Compute sum of absolute deviations: Σ|xᵢ - x̄| = {format_num(sum_abs_dev)}",
            'step2': f"Divide by count n = {n}: {format_num(sum_abs_dev)} / {n}",
            'result': format_num(mad_val)
        },
        'range': {
            'title': "Range & Extremes",
            'formula': "Range = Maximum - Minimum",
            'step1': f"Identify Minimum = {format_num(min_val)} and Maximum = {format_num(max_val)}",
            'step2': f"Range = {format_num(max_val)} - {format_num(min_val)} = {format_num(range_val)}",
            'result': format_num(range_val)
        },
        'quartiles': {
            'title': "Quartiles & Interquartile Range (IQR)",
            'formula': "Q₁ = 25th percentile, Q₃ = 75th percentile, IQR = Q₃ - Q₁",
            'step1': f"Lower half median (Q₁): {q1_step}",
            'step2': f"Upper half median (Q₃): {q3_step}",
            'step3': f"IQR = Q₃ - Q₁ = {format_num(q3_val)} - {format_num(q1_val)} = {format_num(iqr_val)}" if iqr_val is not None else "Requires at least 4 data points.",
            'result': f"Q₁: {format_num(q1_val)}, Q₂ (Median): {format_num(median_val)}, Q₃: {format_num(q3_val)}, IQR: {format_num(iqr_val)}" if iqr_val is not None else "N/A"
        }
    }

    summary = {
        'n': n,
        'sum': format_num(sum_x),
        'sum_sq': format_num(sum_x_squared),
        'mean': format_num(mean_val),
        'median': format_num(median_val),
        'mode': mode_text,
        'min': format_num(min_val),
        'max': format_num(max_val),
        'range': format_num(range_val),
        'sample_variance': format_num(sample_var),
        'sample_stdev': format_num(sample_sd),
        'pop_variance': format_num(pop_var),
        'pop_stdev': format_num(pop_sd),
        'mad': format_num(mad_val),
        'se_mean': format_num(se_mean),
        'q1': format_num(q1_val),
        'q3': format_num(q3_val),
        'iqr': format_num(iqr_val),
        'ss_deviations': format_num(sum_sq_dev)
    }

    return {
        'data': [format_num(x) for x in data],
        'data_sorted': [format_num(x) for x in data_sorted],
        'summary': summary,
        'deviation_table': deviation_rows,
        'table_totals': table_totals,
        'frequency_table': freq_table,
        'steps': steps
    }

