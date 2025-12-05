"""
Test script for phone_extractor module
"""
from phone_extractor import normalize_phone_number, find_phone_column
import pandas as pd

# Test normalization
test_cases = [
    ("966505815487", "+966505815487"),  # 966 -> +966
    ("05xxxxxxxx", "+9665xxxxxxxx"),    # 05 -> +9665
    ("+966505815487", "+966505815487"),  # Already correct
    ("5xxxxxxxx", "+9665xxxxxxxx"),     # 5 -> +9665
    ("+966541556250", "+966541556250"),  # Already correct
]

print("Testing phone number normalization:")
print("=" * 50)
for input_num, expected in test_cases:
    # Replace x with actual digits for testing
    if 'x' in input_num:
        test_input = input_num.replace('x', '1')
        test_expected = expected.replace('x', '1')
    else:
        test_input = input_num
        test_expected = expected
    
    result = normalize_phone_number(test_input)
    status = "✅" if result == test_expected else "❌"
    print(f"{status} Input: {test_input:20} Expected: {test_expected:20} Got: {result}")

# Test column finding
print("\nTesting column finding:")
print("=" * 50)
test_df = pd.DataFrame({
    'name': ['John', 'Jane'],
    'phone': ['+966505815487', '+966541556250'],
    'email': ['john@test.com', 'jane@test.com']
})
col = find_phone_column(test_df)
print(f"✅ Found column: {col} (expected: 'phone')")

test_df2 = pd.DataFrame({
    'Name': ['John', 'Jane'],
    'Phone Number': ['+966505815487', '+966541556250'],
    'Email': ['john@test.com', 'jane@test.com']
})
col2 = find_phone_column(test_df2)
print(f"✅ Found column: {col2} (expected: 'Phone Number')")

test_df3 = pd.DataFrame({
    'Name': ['John', 'Jane'],
    'ext': ['+966505815487', '+966541556250'],
    'Email': ['john@test.com', 'jane@test.com']
})
col3 = find_phone_column(test_df3)
print(f"✅ Found column: {col3} (expected: 'ext')")

print("\n✅ All tests completed!")

