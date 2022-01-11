# notebooks_to_api
An easy to use framework for converting jupyter notebooks into REST APIs.

# Installation
Clone this repo to your project directory.

# Use
Jupyter notebooks are great for developing, prototyping and debugging ML projects, but they are not suitable for production since serving them as a REST API is a lot more complicated. This is where notebooks_to_api comes in, it converts your notebooks into REST APIs.

FLOW :  notebooks -> scripts -> api


# Usage

## For converting notebooks to scripts:

  `!python notebooks_to_api/nbs_to_script.py notebook2script notebook_name`

![Eg. image](../main/source/nbs2script.png)

(this converts the codes from cells marked with "#export" to scripts, for Eg. in the above picture it converts last 2 cells excluding the first one)

The converted scripts name is same as its notebook's name, they are all stored in a directory "exports" in unstructured manner. 



## For structuring the converted scripts:

  `!python notebooks_to_api/nbs_to_script.py structure`
                                                             
(this command takes the folder structure defined in "module_structure.json" and structures the converted scripts)

The structured scripts are stored in a directory "exp_api_modules".



## For creating a API:

  `!python notebooks_to_api/create_api.py choose_api`

(this command takes the inputs from "api_config.json" and configures the api on top of your converted scripts)

A file named "api_core.py" will be created in "exp_api_modules" directory which contains the REST API code.


## For updating a file:
  
  **If you want to update a script make changes in the corresponding notebook and run-**
  
  `!python notebooks_to_api/nbs_to_scripts.py update notebook_name`
    
  (this updates the cooresponding script in "exp_api_module" directory)
  
  **If you want to change the api modules structure or api configurations, update their corresponding config files and run-**
    
  `!python notebooks_to_api/nbs_to_scripts.py update`
    
  
## NOTE -
  * Before running it make sure the current terminal path is at your project folder.
  * The model flow file has to be named "api_flow.py", the flow function "main()", model loading function "load_model()" both the functions should be inside "api_flow.py".
  * This package uses FastAPI framework to create API.
  * If you are not a fan of python notebooks and use text editors/IDEs, you can use "create_api.py" to build API on top of your scripts.


## Credits:
 
 The notebooks to script code was taken from fast.AI's course notebooks
