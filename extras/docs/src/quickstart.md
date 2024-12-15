# Zenplate Quickstart

This will show you how to install, configure, and use Zenplate.

## Installation

Clone the repo
```shell
pushd ~
git clone https://github.com/camratchford/zenplate
```

Create a virtual environment and install the package
```shell
cd zenplate
python3 -m venv venv
source venv/bin/activate
pip install .
```

(Optional) Set up the recommended workspace layout
```shell
mkdir -p ~/zenplate/templates ~/zenplate/output ~/zenplate/vars
cd ~/zenplate
zenplate --export-config --config-file zenplate.yml
echo 'source ~/zenplate/venv/bin/activate' >> .zenplaterc
echo 'export ZENPLATE_CONFIG_FILE="'$PWD'/zenplate.yml"' >> .zenplaterc
source .zenplatetrc
```

(Alternative to the workspace layout) link the python script to your path
```shell
ln -s ~/zenplate/venv/bin/zenplate /usr/local/bin/zenplate
```

## Usage Examples

### Single File Templating

Make a new directory where your zenplate project files will reside (if you didn't already set up a workspace).

```shell
mkdir -p ~/zenplate_project/templates ~/zenplate_project/output ~/zenplate_project/vars
```

Create a new template file in the `templates` directory. For this example we will be making a simple README.md file.

<pre>
<code>
echo "# {{ project_name }}" > ~/zenplate_project/templates/README.md
echo "{{ project_description }}" >> ~/zenplate_project/templates/README.md
echo "## Installation" >> ~/zenplate_project/templates/README.md
echo "```shell" >> ~/zenplate_project/templates/README.md
echo "pip install {{ project_package_name }}" >> ~/zenplate_project/templates/README.md
echo "```" >> ~/zenplate_project/templates/README.md
</code>
</pre>

Create your variables file in the `vars` directory.

```shell
echo "project_name: My Project" > ~/zenplate_project/vars/vars.yml
echo "project_description: This is a project description" >> ~/zenplate_project/vars/vars.yml
echo "project_package_name: my-project" >> ~/zenplate_project/vars/vars.yml
```

Run the zenplate command to render the template.

```shell
zenplate  --var-file ~/zenplate_project/vars/vars.yml ~/zenplate_project/templates/README.md ~/zenplate_project/output/README.md
```


### Directory Templating

If you haven't already gone through the previous example, do so now as we will be reusing the template and variables, adding onto them.

Create a new directory in the `templates` directory.

```shell
mkdir -p ~/zenplate_project/templates/{{\ project_slug\ }}
```

Create a new template file in the new directory.

```shell
echo 'print("Welcome to {{ project_name }}!\n Copyright '{{ project_author }}' {{ project_copyright }}.")' > ~/zenplate_project/templates/{{\ project_slug\ }}/main.py
```

Add the variables we just used to the variables file.

```shell
echo "project_slub: my_project" >> ~/zenplate_project/vars/vars.yml
echo "project_author: Your Name" >> ~/zenplate_project/vars/vars.yml
echo "project_copyright: $(date +'%Y')" >> ~/zenplate_project/vars/vars.yml

```

Run the zenplate command to render the template.

```shell
zenplate --var-file ~/zenplate_project/vars/vars.yml ~/zenplate_project/templates ~/zenplate_project/output
```

## Next Steps

Check out the examples included in the [examples](https://github.com/camratchford/zenplate/tree/main/extras/examples) directory. 
These examples will show you how to use the plugin system to extend Zenplate's functionality.