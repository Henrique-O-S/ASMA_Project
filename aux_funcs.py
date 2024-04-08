def extract_numeric_value(value_str):
    """
    Extracts the numeric value from a string containing numeric value followed by units.
    Example: "20km/h" -> 20
    """
    numeric_part = ""
    for char in value_str:
        if char.isdigit() or char == ".":
            numeric_part += char
        else:
            break
    return float(numeric_part) if numeric_part else None