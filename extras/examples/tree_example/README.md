# File Tree Example

This example demonstrates the use of zenplate to render a directory of templates, including file and directory names.
Using the various command line options, you can specify the template, variables, and output file.

> Note:  <br>
> The usage of templating Python source files such as `templates/{{ project_stub }}/main.py` is not recommended (and tbh kinda cursed).
> In this instance, zenplate is behaving almost like the C pre-processor. It's something that Python does not in any way need, but is cool nonetheless.

> Another note: <br>
> Not a lot of effort has been put into testing the templating of file and directory names. 
> Nothing is going to prevent you from using invalid characters in the template variables.

## Overview

- `vars/general_vars.yml` - Contains variables used by the template. Meant to be used as a global variable file.
- `vars/specific_vars.yml` - Contains variables used by the template. Meant to be used as a project-specific variable file.
- `templates/README.md` - A template that contains information about the fake project.
- `templates/{{ project_stub }}` - A directory containing the fake project source code.
- `templates/{{ project_stub }}/main.py` - A file that simply prints a welcome message and copyright.

## Usage

1. Ensure the zenplate package is installed, see the main README.md for more information.
2. Run the corresponding `run_example.sh` / `run_example.ps1` script to execute the example.
3. Try running the resulting `output_files/tree_example/main.py` file to see the output.
   `python output_dir/tree_example/main.py`
4. Inspect the files in the `output_dir` directory to see the results.
