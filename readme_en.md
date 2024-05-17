# downwards analysis

## How to

1. put the .pas file from the project into the same folder as the info.txt and main.py files
2. put the name of the main file with the .pas extension in the first line of the info.txt file
3. put the list of module to ignore in the 2nd line of the info.txt file
   modules to ignore are externals libraries and files containing classes 
4. (optional) run graphviz setup, check the option "add graphviz to the system path for current user" and restart your computer once the installation is finished to get the image version of the analysis
5. launch main.py if it fail try installing python, if it still fail try installing python in the current directory
## Restricitions

1. this program doesn't work with classes
2. this program doesn't differentiate between same name functions
3. this program doesn't differentiate between functions and variables if they have the same name 

    this could pose a problem with function but recursivity is not taken into account