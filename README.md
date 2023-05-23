
# Cookiecutter Tutorial
This is a cookiecutter repo for demonstrating what cookiecutter is, what it can do, how to use it, and much of its functionalities.

See https://cookiecutter.readthedocs.io/en/stable/installation.html for installation.

# Table of contents  
1. [Introduction](#introduction) 
    1. [What is Cookiecutter?](#what-is-cookiecutter)
    2. [What does it do?](#what-does-it-do)
    3. [What's a template?](#whats-a-template)
    4. [How do I execute it?](#how-do-i-execute-it)
        1. [Command line](#running-via-command-line)
        2. [Command line arguments](#command-line-arguments)
        3. [Python](#running-from-python)
        4. [Python arguments](#python-arguments)
2. [Examples/Advanced usage](#examplesadvanced-usage)  

# Introduction
## What is Cookiecutter?

## What does it do?

## What's a template?

## How do I execute it?
### Running via command-line

Note that your chosen command line must support Unix commands in order to work.

#### If you're running on a local cookiecutter:
~~~bash  
  cookiecutter <path>
~~~

Where <path> is the path to the zip or root directory of your chosen cookiecutter.  

---

#### If you're running on a remote cookiecutter repo on github:
~~~bash  
  cookiecutter https://github.com/Aleyssu/cookiecutter-tutorial-example1
~~~
Or for short:
~~~bash  
  cookiecutter gh:Aleyssu/cookiecutter-tutorial-example1
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
When generating projects, cookiecutter saves your inputs to a json file in '~/.cookiecutter_replay/'. You can re-generate a project using those same inputs using the `--replay` argument, or `--replay-file` argument if you have a custom file which you wish to replay from.
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

From there, you can run cookiecutter using the `cookiecutter('<path>')` function.

Example script (assuming that there is a cookiecutter named 'example-cookiecutter' within the same directory as the python script):
```python
from cookiecutter.main import cookiecutter

cookiecutter('example-cookiecutter')
```

### Python arguments
#### Overriding default configurations
The `extra_context` argument allows you to override the default configurations from `cookiecutter.json` and potentially inject custom-generated data from python. For example, you can inject a timestamp from python's `datetime` library:
```python
cookiecutter(
    'example-cookiecutter',
    extra_context={
        'project_name': 'Python Generated Project',
        '_timestamp': datetime.utcnow().isoformat()
    }
)
```
This function call assumes that the `cookiecutter.json` contains the variables `project_name` and `_timestamp`

#### Template Directory
By default, cookiecutter assumes that the main directory is the same as the template directory. If the template is located within a subdirectory, or there are multiple templates in the given cookiecutter, the `directory` argument will be required.
```python
cookiecutter('example-cookiecutter', directory='template1')
```
This function call assumes that there is a cookiecutter named 'example-cookiecutter' in the same directory as the python script, and that there is a template directory located within the cookiecutter named 'template1.'

#### Skip input prompts
By default, a command line will open to prompt the user for input. To skip this and use only default values or values assigned in the `extra_context` argument, use the `no_input=True` argument.

#### Reusing inputs from past executions
When generating projects, cookiecutter saves your inputs to a json file in '~/.cookiecutter_replay/'. You can re-generate a project using those same inputs using the `replay=true` argument.

# Examples/Advanced Usage

