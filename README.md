# FileSize
Python script remade from my original PowerShell scripts
  
This code implements a program that adds or removes the folder size information from folder names in a directory  
The folder size information is added to the name of the folder either at the leading position or the trailing position  
The size information is calculated by summing up the sizes of all files in the folder  
The size information is displayed in the format of B, KB, MB, GB, or TB, depending on the size of the folder  
  
Dependencies:  
OS  
RE (Regular Expressions)  
ARGPARSE  
  
Arguments to be passed are:  
-a or -add for adding  
-d or -delete for deleting  
-t or -trailing for trailing  
-l or -leading for leading  
[path\to\dir] a directory needs to be passed, if none is passed, it will assume the directory from where the script was opened from  
The -a and -t values are assumed if no flags are provided  

It can be run from the command line:  
python FileSize.py path\to\dir  
python FileSize.py -a -l path\to\dir  
python FileSize.py -a -t path\to\dir  
python FileSize.py -d path\to\dir  
python FileSize.py -l path\to\dir (assumes add)  
python FileSize.py -t path\to\dir (assumes add)  
python FileSize.py (assumes current dir, add, trailing)  
  
It is possible to add to both leading and trailing but must be done via seperate calls  
