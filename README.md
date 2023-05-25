


# Cookiecutter Tutorial
This is a cookiecutter repo for demonstrating what cookiecutter is, what it can do, how to use it, and much of its functionalities.

See https://cookiecutter.readthedocs.io/en/stable/installation.html for installation.

This repo is also contains a cookiecutter project which demonstrates much of Cookiecutter's functionality. Feel free to download and experiment with it. You can also generate a project directly from the repo (see [Running Cookiecutter](#if-youre-running-with-a-remote-cookiecutter-repo-from-github)) (make sure you're using a command line with Unix support!)

Much of this wiki's content is thanks to the help of Cookiecutter's official documentation, along with personal experimentation to see into Cookiecutter's workings. See https://cookiecutter.readthedocs.io/en/stable/advanced/index.html for the official documentation.

# Table of contents  
1. [Introduction](#introduction) 
    1. [What is Cookiecutter?](#what-is-cookiecutter)
    4. [Running Cookiecutter](#running-cookiecutter)
        1. [Command line](#running-via-command-line)
        2. [Command line arguments](#command-line-arguments)
        3. [Python](#running-from-python)
        4. [Python arguments](#python-arguments)
2. [Cookiecutter in-depth](#cookiecutter-in-depth)  
	1. [Runtime - Cookiecutter's project generation process](#runtime---cookiecutters-project-generation-process)
	2. [Templates and file structure](#templates-and-file-structure)
		1. [cookiecutter.json](#cookiecutterjson)
		2. [Processed directory](#processeddirectory)
		3. [Hooks](#hooks)

# Introduction
## What is Cookiecutter?
Cookiecutter is a utility which generates "projects" from templates with the assistance of Python and Jinja2. It can be executed through the command line, or by Python through the Cookiecutter API.

Cookiecutter takes a cookiecutter directory or cookiecutter repo as its main input. Typically, the template directory is the same as the root directory of the cookiecutter. While running Cookiecutter, you'll be prompted with several variables and their default values from *cookiecutter.json*. You can type your own value in place of the default, or simply press enter without typing anything to retain the default value. Upon answering all these prompts, Cookiecutter will proceed with generating the project.

The generated project directory is a modified copy of the original template. The modifications typically involve the removal and movement of files within the original template, along with a wide range of text formatting for the names of every file along with their contents. Depending on how the template is created and what answers are given to the prompts during generation, the resulting directory can be structured and formatted in a near-infinite range of different possibilities. Cookiecutter is especially powerful for applications such as generating project directories containing all the dependencies and structuring needed as a framework for new coding projects.

**Note that "Cookiecutter" can refer to the utility itself, or to the repo/directory which is given as input. For disambiguation, I'll try to refer to the utility in uppercase as in "Cookiecutter," and the input directory in lowercase as in "cookiecutter."**


## Running Cookiecutter
### Running via command-line

Note that your chosen command line must support Unix commands in order to work.

#### If you're running with a local cookiecutter:
~~~bash  
  cookiecutter <path>
~~~

Where `<path>` is the path to the zip or root directory of your chosen cookiecutter.  

---

#### If you're running with a remote cookiecutter repo from github:
~~~bash  
  cookiecutter https://github.com/Aleyssu/cookiecutter-tutorial
~~~
Or for short:
~~~bash  
  cookiecutter gh:Aleyssu/cookiecutter-tutorial
~~~
You can replace the url with that of any other cookiecutter repo.  

### Command-line Arguments

If you wish to see the full list of arguments available, simply type `cookiecutter` into your command line and press enter.

#### Output directory
By default, cookiecutter outputs to the current working directory. The `-o` argument can override this behavior.
~~~bash
cookiecutter -o <output-path> <path>
~~~

#### Template directory
By default, cookiecutter assumes that the main directory is the same as the template directory. If the template is located within a subdirectory, or there are multiple templates in the given cookiecutter, the `--directory` argument will be required.
~~~bash
cookiecutter --directory <template-path> <path>
~~~

#### Reusing inputs from past executions
When generating projects, cookiecutter saves your inputs to a json file in *~/.cookiecutter_replay/*. You can re-generate a project using those same inputs using the `--replay` argument, or `--replay-file` argument if you have a custom file which you wish to replay from.
~~~bash
cookiecutter --replay <path>
~~~
~~~bash
cookiecutter --replay-file <replay-file-path> <path>
~~~

#### Skip input prompts
If you wish to use only the default configurations for your project, you can use the `--no-input` argument.
~~~bash
cookiecutter --no-input <path>
~~~

#### Load from a pre-configured config file
If you have a .yaml config file available for your cookiecutter, you can load it using the `--config-file` argument. This works alongside the `--no-input` argument.
~~~bash
cookiecutter --config-file <config-file-path> <path>
~~~

### Running from Python
Cookiecutter projects can be generated from Python using the Cookiecutter API.

First, make sure you include the Cookiecutter library with `from cookiecutter.main import cookiecutter`. 

From there, you can run Cookiecutter using the `cookiecutter('<path>')` function.

Example script (assuming that *example-cookiecutter/* is within the same directory as the python script):
```python
from cookiecutter.main import cookiecutter

cookiecutter('example-cookiecutter')
```

### Python arguments
#### Overriding default configurations
The `extra_context` argument allows you to override the default configurations from *cookiecutter.json* and potentially inject custom-generated data from python. For example, you can inject a timestamp from python's `datetime` library:
```python
cookiecutter(
    'example-cookiecutter',
    extra_context={
        'project_name': 'Python Generated Project',
        '_timestamp': datetime.utcnow().isoformat()
    }
)
```
This function call assumes that *cookiecutter.json* contains the variables `project_name` and `_timestamp`

#### Template Directory
By default, Cookiecutter assumes that the main directory is the same as the template directory. If the template is located within a subdirectory, or there are multiple templates in the given cookiecutter, the `directory` argument will be required.
```python
cookiecutter('example-cookiecutter', directory='template1')
```
This function call assumes that there is a cookiecutter named *example-cookiecutter* in the same directory as the python script, and that there is a template directory located within the cookiecutter named *template1/*.

#### Skip input prompts
By default, a command line will open to prompt the user for input. To skip this and use only default values or values assigned in the `extra_context` argument, use the `no_input=True` argument.

#### Reusing inputs from past executions
When generating projects, Cookiecutter saves your inputs to a json file in *~/.cookiecutter_replay/*. You can re-generate a project using those same inputs using the `replay=true` argument.

# Cookiecutter in-depth

## Runtime - Cookiecutter's project generation process
When running Cookiecutter, the first thing that happens is that *cookiecutter.json* is scanned and the user prompted for input, assuming that the `--no-input` argument is not used.

Second, *pre_gen_project.py* is run. Note that the project directory has not been created yet. If the script exits with a non-zero status (through `sys.exit(1)`), Cookiecutter will cancel project generation. Typically, *pre_gen_project.py* is used for input validation, making sure that the user's input is valid before continuing.

Following the script's execution, the template is scanned for the first subdirectory with a Jinja variable in its name (the chosen directory is determined by lexicographical order), where that directory is then copied into the current working directory (or the directory assigned by the `-o` argument). During this process, the directory and all its subdirectories are traversed, with their names and contents scanned and rendered by Jinja. This is where Jinja code and variables such as `{{ cookiecutter.project_name }}` are converted into text such as "example_project," depending on the values of the variables or the execution results of the Jinja code.  
If at any point a Jinja variable is found which is not present in *cookiecutter.json*, Cookiecutter will throw an error and cancel project generation, removing the newly created project directory.

Finally, *post_gen_project.py* is run. Typically, it is used for removing and restructuring files and directories to trim down the final project into just the required files. Just like *pre_gen_project.py*, if *post_gen_project.py* exits with a non-zero status, Cookiecutter will cancel project generation and remove the newly generated project directory.

## Templates and file structure
In a typical cookiecutter where the template directory is the root directory, the file structure would look something like this:

```
Main Directory / Repo/  
├── {{ processed_directory }}/  
│   └── # Files here will processed
├── hooks/  
│   ├── pre_gen_project.py  
│   └── post_gen_project.py  
└── cookiecutter.json  
```
### <a name="cookiecutterjson"></a>cookiecutter.json
This is a vital component of all cookiecutters. Within this file contains all the Jinja variables which the user is prompted with during project generation, and these are the variables which are used when formatting the text in the names and contents of the project files.  
Here's an example file with all the different variable types present:
```json
{
    "standard_variable": "Test Project",
	"__private_rendered_variable": "{{ cookiecutter.standard_variable }}",
	"_private_unrendered_variable": "{{ cookiecutter.standard_variable }}",
	"_copy_without_render": [
		"*.html",
		"*unrendered"
	],
	"choice_variable": [
		"choice_1",
		"choice_2",
		"choice_3"
	],
	"dictionary_variable": {
        "png": {
            "name": "Portable Network Graphic",
            "library": "libpng",
            "apps": [
                "GIMP"
            ]
        },
        "bmp": {
            "name": "Bitmap",
            "library": "libbmp",
            "apps": [
                "Paint",
                "GIMP"
            ]
        }
    },
	"__jinja2_extension_variable": "{% now 'utc', '%Y' %}"
}
```
`"standard_variable": ""`  
These are the simplest Jinja2 variables, holding the value of a string or other variable (using the {{  }} syntax).

`"__private_rendered_variable": ""`  
Similar to standard variables, private rendered variables, indicated by the prepended `__`, can hold the value of a string or other variable. As a private variable, there will be no prompt for this variable during project generation.
In this example, this variable holds the value, "Test Project."

`"_private_unrendered_variable": ""`  
Private unrendered variables, indicated by the prepended `_`, will only display strings. As a private variable, there will be no prompt for this variable during project generation. 
In this example, this variable holds the value, "{{ cookiecutter.standard_variable }}."

`"_copy_without_render": []`  
This is a special variable which must be written exactly as shown. `_copy_without_render` contains a list of strings representative to [Unix wildcards](https://tldp.org/LDP/GNU-Linux-Tools-Summary/html/x11655.htm) which indicate the files and directories that should not be rendered by Jinja2. In this example, .html files and files/directories named "unrendered" will not be rendered.

`"choice_variable": []`  
Choice variables, indicated by the square brackets containing a list of strings, provide the user with a multiple-choice prompt on project generation where they are given the option to select one of the given strings. The first string in the list is the default value.

`"dictionary_variable": {}`  
Dictionary variables are as the name suggests, containing key-value pairs. Dictionaries can also contain lists and other dictionaries. They provide a way to define deep-structured information when rendering templates.

`"__jinja2_extension_variable": ""`  
This is just another rendered private variable put in place to demonstrate the ability to fill variable values with those from Jinja2 extensions. In this example, the built-in *jinja2_time.TimeExtension* extension is used to display the current year at the time of project generation.

### <a name="processeddirectory"></a>"{{ processed_directory }}"
Note the formatting of the first sub-directory's name. This is the syntax for Jinja variables, and it's necessary for there to be a directory named under a variable from `cookiecutter.json` in this syntax. When executing, Cookiecutter will pick the first directory / file it finds which contains a Jinja variable in its name (based on lexicographical order) to copy and process into a project. 

In this example, it is assumed that there's a variable named `processsed_directory` within `cookiecutter.json`. After running Cookiecutter, a new directory will be created with the name of whatever value `processed_directory` was assigned. If `processed_directory` was assigned with "apple," then the generated project directory would also be called "apple."

Note that outside of the double curly brackets you may include whatever text you wish, so if the sub-directory was instead named "pine{{ processed_directory }}," the outputted directory would be named "pineapple" (assuming that `processed_directory` was still assigned with "apple"). A more in-depth explanation of Jinja2 can be found [here](https://jinja.palletsprojects.com/en/3.1.x/).

### Hooks
Hooks are an optional component of cookiecutter templates. They can assist in input validation for the prompts, and custom generation behavior such as removing and restructuring directories in the final project directory.

The *pre_gen_project.py* hook runs right after all the input prompts have been answered, and right before the new project directory has been created. It is typically used to ensure that the input prompts are valid for the given template.

Example script (found in this repo's cookiecutter template):
```pre_gen_project.py```  
```python
import re
import sys
import os

MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9 ]+$'
project_name = '{{ cookiecutter.project_name }}'

if not re.match(MODULE_REGEX, project_name):
    print('ERROR: %s is not a valid project name!' % project_name)

    # exits with status 1 to indicate failure
    sys.exit(1)
```
This script checks the `project_name` variable and makes sure that it is at least 2 characters long, and doesn't contain any special characters. If this condition isn't met, it exits with a non-zero status (1 in this case) to indicate failure and tell Cookiecutter to abort project generation.

Meanwhile, the *post_gen_project.py* script runs after the project directory has been created and rendered by Jinja2. It's typically used for moving and removing directories/files, but you can realistically do anything that Python permits here.

Example script (found in this repo's cookiecutter template):
`post_gen_project.py`  
```python
import os
import shutil
from pathlib import Path

REMOVE_PATHS = []
MOVE_PATHS = []

keep_files = '{{ cookiecutter.keep_files }}'

if keep_files == "test1.txt":
    REMOVE_PATHS.append("test2.txt")
elif keep_files == "test2.txt":
    REMOVE_PATHS.append("test1.txt")
elif keep_files == "none":
    REMOVE_PATHS += ["test1.txt", "test2.txt"]
    
path_to_remove: str
for path_to_remove in REMOVE_PATHS:
    path_to_remove = path_to_remove.strip()
    if path_to_remove and os.path.exists(path_to_remove):
        if os.path.isdir(path_to_remove):
            shutil.rmtree(path_to_remove)
        else:
            os.unlink(path_to_remove)
```
This script, based on the user's selection for `keep_files`, removes a combination of the files *test1.txt* and *test2.txt*. `MOVE_PATHS` is unused here.

---
On the other hand, a cookiecutter where there are multiple templates or where the template directory is located within a sub-directory of the cookiecutter would look something like this: 
```
Main Directory / Repo/
├── Template Directory 1/
│   ├── {{ processed_directory }}/
│   │   └── # Files here will processed by cookiecutter
│   ├── hooks/
│   │   ├── pre_gen_project.py
│   │   └── post_gen_project.py
│   └── cookiecutter.json
|
└── Template Directory 2/
    ├── {{ processed_directory }}/
    │   └── # Files here will processed by cookiecutter
    ├── hooks/
    │   ├── pre_gen_project.py
    │   └── post_gen_project.py
    └── cookiecutter.json
```
Fundamentally, the templates themselves are structured the same as that of regular cookiecutters.

If you were to run Cookiecutter on a project like this, you would have to use the `--directory` argument like this:
```bash
cookiecutter --directory "Template Directory 1" <path to main directory>
```
Assuming that the first template is the one you're after.
