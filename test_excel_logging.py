#!/usr/bin/env python3
"""Test with real Excel file to debug logging"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

import os
print("="*70)
print("TESTING WITH REAL EXCEL FILE")
print("="*70)
print()

# Clean old logs
if os.path.exists('logs/app.log'):
    os.remove('logs/app.log')
    print("✅ Old log file deleted")
else:
    print("No old log file found")

from logger import CustomLogger
from exception import ValidationException
from src.piv.io.excel_reader import read_workbook_text

print()
print("="*70)
print("TEST 1: Read Excel file with logging")
print("="*70)

_logger = CustomLogger()
logger = _logger.get_logger('excel_test')

excel_path = r"C:\Users\mohammed.a\Desktop\doc_validation\external_data\intro_part_test.xlsx"

print(f"Excel path: {excel_path}")
print(f"File exists: {os.path.exists(excel_path)}")
print()

logger.info(f"Starting to read Excel file: {excel_path}")

try:
    text = read_workbook_text(excel_path)
    logger.info(f"Successfully read Excel file, content length: {len(text)} chars")
    print(f"✅ Read {len(text)} characters from Excel")
except ValidationException as e:
    logger.error(f"Failed to read Excel: {e.error_message}")
    print(f"❌ Error: {e.error_message}")
except Exception as e:
    logger.error(f"Unexpected error: {str(e)}")
    print(f"❌ Unexpected error: {str(e)}")

print()
print("="*70)
print("TEST 2: Check log file content")
print("="*70)

if os.path.exists('logs/app.log'):
    with open('logs/app.log', 'r', encoding='utf-8') as f:
        content = f.read()
    size = os.path.getsize('logs/app.log')
    print(f"✅ Log file exists: {size} bytes")
    print()
    print("Log content (first 1000 chars):")
    print("-"*70)
    print(content[:1000])
    print("-"*70)
else:
    print("❌ Log file NOT created!")

print()
print("="*70)
print("Tests completed")
print("="*70)
