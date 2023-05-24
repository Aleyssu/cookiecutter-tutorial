

# Cookiecutter Tutorial (WIP)
This is a cookiecutter repo for demonstrating what cookiecutter is, what it can do, how to use it, and much of its functionalities.

See https://cookiecutter.readthedocs.io/en/stable/installation.html for installation.

This repo is also contains a cookiecutter project which demonstrates much of Cookiecutter's functionality. Feel free to download and experiment with it. You can also generate a project directly from the repo (see [Running Cookiecutter](#if-youre-running-on-a-remote-cookiecutter-repo-on-github)) (make sure you're using a command line with Unix support!)

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

# Introduction
## What is Cookiecutter?
Cookiecutter is a utility which generates "projects" from templates with the assistance of Python and Jinja2. It can be executed through the command line, or by Python through the Cookiecutter API.

Cookiecutter takes a cookiecutter directory or cookiecutter repo as its main input. Typically, the template directory is the same as the root directory of the cookiecutter. While running Cookiecutter, you'll be prompted with several variables and their default values from *cookiecutter.json*. You can type your own value in place of the default, or simply press enter without typing anything to retain the default value. Upon answering all these prompts, Cookiecutter will proceed with generating the project.

The generated project directory is a modified copy of the original template. The modifications typically involve the removal and movement of files within the original template, along with a wide range of text formatting for the names of every file along with their contents. Depending on how the template is created and what answers are given to the prompts during generation, the resulting directory can be structured and formatted in a near-infinite range of different possibilities. Cookiecutter is especially powerful for applications such as generating project directories containing all the dependencies and structuring needed as a framework for new coding projects.

**Note that "Cookiecutter" can refer to the utility itself, or to the repo/directory which is given as input. For disambiguation, I'll try to refer to the utility in uppercase as in "Cookiecutter," and the input directory in lowercase as in "cookiecutter."**


## Running Cookiecutter
### Running via command-line

Note that your chosen command line must support Unix commands in order to work.

#### If you're running on a local cookiecutter:
~~~bash  
  cookiecutter <path>
~~~

Where `<path>` is the path to the zip or root directory of your chosen cookiecutter.  

---

#### If you're running on a remote cookiecutter repo on github:
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
### cookiecutter.json
This is a vital component of all cookiecutters. Within this file contains all the Jinja variables which the user is prompted with during project generation, and these are the variables which are used when formatting the text in the names and contents of the project files.  
Here's an example file with all the different variable types present:
**(to be extended)**
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

### "{{ processed_directory }}"
Note the formatting of the first sub-directory's name. This is the syntax for Jinja variables, and it's necessary for there to be a directory named under a variable from `cookiecutter.json` in this syntax. When executing, Cookiecutter will pick the first directory / file it finds which contains a Jinja variable in its name (based on lexicographical order) to copy and process into a project. 

In this example, it is assumed that there's a variable named `processsed_directory` within `cookiecutter.json`. After running Cookiecutter, a new directory will be created with the name of whatever value `processed_directory` was assigned. If `processed_directory` was assigned with "apple," then the generated project directory would also be called "apple."

Note that outside of the double curly brackets you may include whatever text you wish, so if the sub-directory was instead named "pine{{ processed_directory }}," the outputted directory would be named "pineapple" (assuming that `processed_directory` was still assigned with "apple"). A more in-depth explanation of Jinja2 can be found **(to be added)**

### Hooks
**(to be added)**

---
On the other hand, a cookiecutter where there are multiple templates or where the template directory is located within a sub-directory of the cookiecutter would look something like this: **(to be added)**

