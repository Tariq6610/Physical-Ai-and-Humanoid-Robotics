#!/usr/bin/env python3
"""
Script to validate code examples in the documentation.
This script checks for basic syntax errors in Python code examples.
"""

import os
import re
import subprocess
import tempfile
from pathlib import Path


def find_markdown_files(docs_dir):
    """Find all markdown files in the docs directory."""
    md_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files


def extract_code_blocks(file_path, language='python'):
    """Extract code blocks of a specific language from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex pattern to match code blocks with specific language
    pattern = rf'```{language}\n(.*?)```'
    matches = re.findall(pattern, content, re.DOTALL)

    return matches


def validate_python_code(code_block):
    """Validate Python code syntax."""
    try:
        # Remove common leading whitespace (dedent) to handle markdown formatting
        import textwrap
        dedented_code = textwrap.dedent(code_block)

        # Attempt to compile the code to check for syntax errors
        compile(dedented_code, '<string>', 'exec')
        return True, None
    except SyntaxError as e:
        return False, str(e)


def main():
    """Main function to validate code examples."""
    docs_dir = "docs/docs"

    if not os.path.exists(docs_dir):
        print(f"Directory {docs_dir} does not exist.")
        return

    md_files = find_markdown_files(docs_dir)
    print(f"Found {len(md_files)} markdown files to check.")

    total_code_blocks = 0
    valid_code_blocks = 0
    invalid_code_blocks = []

    for md_file in md_files:
        print(f"\nChecking file: {md_file}")

        # Extract Python code blocks
        python_blocks = extract_code_blocks(md_file, 'python')
        js_blocks = extract_code_blocks(md_file, 'js')
        bash_blocks = extract_code_blocks(md_file, 'bash')

        all_blocks = python_blocks  # For now, just focus on Python

        for i, code_block in enumerate(all_blocks):
            total_code_blocks += 1
            print(f"  Validating code block {i+1}...")

            is_valid, error = validate_python_code(code_block)

            if is_valid:
                print(f"    ✓ Code block {i+1} is valid")
                valid_code_blocks += 1
            else:
                print(f"    ✗ Code block {i+1} has syntax error: {error}")
                invalid_code_blocks.append({
                    'file': md_file,
                    'block_index': i+1,
                    'code': code_block,
                    'error': error
                })

    print(f"\n--- Validation Summary ---")
    print(f"Total code blocks checked: {total_code_blocks}")
    print(f"Valid code blocks: {valid_code_blocks}")
    print(f"Invalid code blocks: {len(invalid_code_blocks)}")

    if invalid_code_blocks:
        print(f"\n--- Invalid Code Blocks ---")
        for block in invalid_code_blocks:
            print(f"File: {block['file']}")
            print(f"Block #{block['block_index']}: {block['error']}")
            print(f"Code:\n{block['code'][:200]}...")  # Show first 200 chars
            print("-" * 40)

    # Return success if all code blocks are valid
    success = len(invalid_code_blocks) == 0
    return success


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)