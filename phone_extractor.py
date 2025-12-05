"""
Module for extracting and normalizing phone numbers from CSV/Excel files
"""
import pandas as pd
from typing import List, Optional
import re


def normalize_phone_number(phone: str) -> Optional[str]:
    """
    Normalize phone number to format: +966xxxxxxxxx
    
    Handles:
    - 966xxxxxxxxx -> +966xxxxxxxxx
    - 05xxxxxxxx -> +9665xxxxxxxx
    - +966xxxxxxxxx -> +966xxxxxxxxx (already correct)
    - Removes spaces, dashes, parentheses
    
    Args:
        phone: Phone number string to normalize
        
    Returns:
        Normalized phone number or None if invalid
    """
    if not phone or pd.isna(phone):
        return None
    
    # Convert to string and remove whitespace
    phone_str = str(phone).strip()
    
    # Remove common separators: spaces, dashes, parentheses, dots, underscores
    phone_str = re.sub(r'[\s\-\(\)\.\_]', '', phone_str)
    
    # Remove any non-digit characters except + at the start
    # Keep only digits and + at the beginning
    if phone_str.startswith('+'):
        phone_str = '+' + re.sub(r'[^\d]', '', phone_str[1:])
    else:
        phone_str = re.sub(r'[^\d]', '', phone_str)
    
    # If empty after cleaning, return None
    if not phone_str:
        return None
    
    # Handle different formats
    # Case 1: Already starts with +966
    if phone_str.startswith('+966'):
        # Validate length (should be +966 followed by 9 digits)
        if len(phone_str) == 13 and phone_str[4:].isdigit():
            return phone_str
        return None
    
    # Case 2: Starts with 966 (without +)
    if phone_str.startswith('966'):
        # Validate length (should be 966 followed by 9 digits)
        if len(phone_str) == 12 and phone_str[3:].isdigit():
            return '+' + phone_str
        return None
    
    # Case 3: Starts with 05 (Saudi mobile format)
    if phone_str.startswith('05') and len(phone_str) == 10 and phone_str.isdigit():
        # Convert 05xxxxxxxx to +9665xxxxxxxx
        return '+966' + phone_str[1:]
    
    # Case 4: Starts with 5 (without leading 0)
    if phone_str.startswith('5') and len(phone_str) == 9 and phone_str.isdigit():
        # Convert 5xxxxxxxx to +9665xxxxxxxx
        return '+966' + phone_str
    
    # Case 5: Already has + but different country code - return as is if valid
    if phone_str.startswith('+') and len(phone_str) >= 10:
        # Basic validation: should have country code and number
        return phone_str
    
    return None


def find_phone_column(df: pd.DataFrame) -> Optional[str]:
    """
    Find the phone number column in a DataFrame.
    
    Looks for columns with names containing: phone, Phone, number, phone number, ext
    
    Args:
        df: DataFrame to search
        
    Returns:
        Column name if found, None otherwise
    """
    if df.empty:
        return None
    
    # List of keywords to search for
    keywords = ['phone', 'number', 'ext', 'mobile', 'tel', 'whatsapp']
    
    # Search in column names (case-insensitive)
    for col in df.columns:
        col_lower = str(col).lower()
        # Check if any keyword is in the column name
        if any(keyword in col_lower for keyword in keywords):
            return col
    
    # If no matching column found, return first column as fallback
    return df.columns[0] if len(df.columns) > 0 else None


def extract_phone_numbers(file_path: str, file_type: str = None) -> List[str]:
    """
    Extract and normalize phone numbers from CSV or Excel file.
    
    Args:
        file_path: Path to the file or file-like object
        file_type: 'csv', 'xlsx', 'xls', or None for auto-detect
        
    Returns:
        List of normalized phone numbers (format: +966xxxxxxxxx)
    """
    # Determine file type if not provided
    if file_type is None:
        if hasattr(file_path, 'name'):
            filename = file_path.name
        else:
            filename = str(file_path)
        
        if filename.endswith('.csv'):
            file_type = 'csv'
        elif filename.endswith('.xlsx'):
            file_type = 'xlsx'
        elif filename.endswith('.xls'):
            file_type = 'xls'
        else:
            raise ValueError(f"Unsupported file type: {filename}")
    
    # Read the file
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path)
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")
    
    if df.empty:
        return []
    
    # Find phone column
    phone_col = find_phone_column(df)
    if phone_col is None:
        return []
    
    # Extract phone numbers
    phone_numbers = df[phone_col].astype(str).tolist()
    
    # Normalize phone numbers
    normalized_numbers = []
    for phone in phone_numbers:
        normalized = normalize_phone_number(phone)
        if normalized:
            normalized_numbers.append(normalized)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_numbers = []
    for num in normalized_numbers:
        if num not in seen:
            seen.add(num)
            unique_numbers.append(num)
    
    return unique_numbers


def extract_from_uploaded_file(uploaded_file) -> List[str]:
    """
    Extract phone numbers from a Streamlit uploaded file.
    Supports CSV, Excel (.xlsx, .xls), and Apple Numbers (.numbers) files.
    
    Args:
        uploaded_file: Streamlit UploadedFile object
        
    Returns:
        List of normalized phone numbers
    """
    # Determine file type from filename
    filename = uploaded_file.name.lower()
    if filename.endswith('.csv'):
        file_type = 'csv'
    elif filename.endswith('.xlsx'):
        file_type = 'xlsx'
    elif filename.endswith('.xls'):
        file_type = 'xls'
    elif filename.endswith('.numbers'):
        file_type = 'numbers'
    else:
        raise ValueError(f"Unsupported file type: {uploaded_file.name}. Supported: CSV, Excel (.xlsx, .xls), Apple Numbers (.numbers)")
    
    # Read file into pandas
    try:
        if file_type == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_type == 'numbers':
            # Apple Numbers files - try to read using numbers-parser
            try:
                import numbers_parser
                # Save uploaded file temporarily to read it
                import tempfile
                import os
                # Reset file pointer to beginning
                uploaded_file.seek(0)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.numbers') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_path = tmp_file.name
                # Reset file pointer again for potential reuse
                uploaded_file.seek(0)
                
                try:
                    # Read Numbers file
                    doc = numbers_parser.Document(tmp_path)
                    sheets = doc.sheets
                    if not sheets:
                        raise ValueError("No sheets found in Numbers file")
                    
                    # Get first sheet and convert to DataFrame
                    sheet = sheets[0]
                    if not sheet.tables:
                        raise ValueError("No tables found in the first sheet of Numbers file")
                    
                    # Extract data from the first table
                    table = sheet.tables[0]
                    data = []
                    headers = None
                    
                    # Get all rows from the table
                    for row_idx, row in enumerate(table.rows()):
                        row_data = []
                        for cell in row:
                            # Get cell value, handling different data types
                            cell_value = cell.value
                            if cell_value is None:
                                row_data.append('')
                            else:
                                # Convert to string for consistency
                                # Handle numeric values (Numbers might store phone numbers as numbers)
                                if isinstance(cell_value, (int, float)):
                                    # Convert number to string, preserving leading zeros if needed
                                    cell_value = str(int(cell_value)) if isinstance(cell_value, float) and cell_value.is_integer() else str(cell_value)
                                row_data.append(str(cell_value).strip())
                        
                        # Skip completely empty rows
                        if not any(row_data):
                            continue
                        
                        # First non-empty row might be headers
                        if row_idx == 0 and headers is None:
                            # Check if first row looks like headers (contains text like "phone", "number", etc.)
                            first_row_lower = [str(cell).lower() for cell in row_data]
                            if any(keyword in ' '.join(first_row_lower) for keyword in ['phone', 'number', 'mobile', 'tel', 'ext']):
                                headers = row_data
                                continue
                        
                        data.append(row_data)
                    
                    if not data:
                        raise ValueError("No data rows found in Numbers file")
                    
                    # Create DataFrame
                    if headers:
                        # Use first row as headers
                        df = pd.DataFrame(data, columns=headers[:len(data[0])] if data else headers)
                    else:
                        # No headers, use default column names
                        max_cols = max(len(row) for row in data) if data else 0
                        df = pd.DataFrame(data, columns=[f'Column_{i+1}' for i in range(max_cols)])
                    
                finally:
                    # Clean up temp file
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                        
            except ImportError:
                raise ValueError("numbers-parser library is required to read Apple Numbers files. Install it with: pip install numbers-parser")
            except Exception as e:
                raise ValueError(f"Error reading Numbers file: {str(e)}. Make sure the file is a valid Numbers spreadsheet.")
        else:
            # Excel files
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        if "Unsupported file type" in str(e) or "numbers-parser" in str(e):
            raise
        raise ValueError(f"Error reading file: {str(e)}")
    
    if df.empty:
        return []
    
    # Find phone column
    phone_col = find_phone_column(df)
    if phone_col is None:
        # Return empty list with helpful message
        available_cols = ', '.join(df.columns.tolist())
        raise ValueError(f"No phone number column found. Available columns: {available_cols}. Please ensure your file has a column named 'phone', 'Phone', 'number', 'phone number', or 'ext'.")
    
    # Extract and normalize phone numbers
    phone_numbers = df[phone_col].astype(str).tolist()
    normalized_numbers = []
    failed_numbers = []
    
    for phone in phone_numbers:
        # Skip NaN, None, or empty strings
        if pd.isna(phone) or phone == '' or phone == 'nan' or phone.lower() == 'none':
            continue
        
        normalized = normalize_phone_number(phone)
        if normalized:
            normalized_numbers.append(normalized)
        else:
            # Keep track of failed normalizations for debugging
            failed_numbers.append(phone)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_numbers = []
    for num in normalized_numbers:
        if num not in seen:
            seen.add(num)
            unique_numbers.append(num)
    
    # If no valid numbers found, provide helpful error message
    if not unique_numbers:
        sample_numbers = failed_numbers[:5] if failed_numbers else phone_numbers[:5]
        sample_str = ', '.join([str(n) for n in sample_numbers if n])
        raise ValueError(f"No valid phone numbers found in column '{phone_col}'. Sample values: {sample_str}. Please ensure numbers are in format: +966xxxxxxxxx, 966xxxxxxxxx, or 05xxxxxxxx")
    
    return unique_numbers

