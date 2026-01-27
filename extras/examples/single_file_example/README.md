# Single File Example

This example demonstrates the use of zenplate to render a single template.
Using the various command line options, you can specify the template, variables, and output file.

## Overview

- `vars/vars.yml` - Contains the variables used by the template.
- `templates/readme_template.md.j2` - The template file that will be rendered.

## Usage

1. Ensure the zenplate package is installed, see the main README.md for more information.
2. Run the corresponding `run_example.sh` / `run_example.ps1` script to execute the example.
3. Try modifying the inline `--var` argument or the contents of `vars/vars.yml` to see how the output changes.
4. Inspect the files in the `output_dir` directory to see the results.
