#!/usr/bin/env python3
"""
make.fun news-image-01 entry script.
Copies entry.jpg byte-for-byte to /output/entry.png (or MAKEFUN_OUTPUT_DIR).
Standard library only, deterministic, works from any CWD.
"""

import os
import sys
from pathlib import Path

def main():
    # All paths resolved relative to this script file
    script_dir = Path(__file__).resolve().parent
    src_path = script_dir / "entry.jpg"
    
    # Determine output directory
    output_dir_env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if output_dir_env:
        output_dir = Path(output_dir_env)
    else:
        output_dir = Path("/output")
        
    output_dir.mkdir(parents=True, exist_ok=True)
    dest_path = output_dir / "entry.png"
    
    if not src_path.exists():
        print(f"Error: Source image {src_path} does not exist.", file=sys.stderr)
        sys.exit(1)
        
    # Read source bytes deterministically
    data = src_path.read_bytes()
    
    # Validate JPEG header / magic bytes and EOF marker
    if not data.startswith(b'\xff\xd8\xff') or not data.endswith(b'\xff\xd9'):
        print(f"Error: Source image is not a valid, complete JPEG stream.", file=sys.stderr)
        sys.exit(1)
        
    # Validate size limit (1 MiB = 1048576 bytes)
    max_size = 1048576
    if len(data) > max_size:
        print(f"Error: Image size {len(data)} bytes exceeds limit of {max_size} bytes.", file=sys.stderr)
        sys.exit(1)
        
    # Write destination file byte-for-byte
    dest_path.write_bytes(data)
    
    # Verify write and determinism (re-read and compare)
    written_data = dest_path.read_bytes()
    if written_data != data:
        print("Error: Written file content does not match source.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Successfully copied entry ({len(data)} bytes) to {dest_path}")

if __name__ == "__main__":
    main()
