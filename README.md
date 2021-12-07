Usage: './testEng.py'

*	Place the script in the project's dir.
	Make sure the config file 'ExampleInput.txt' exists.
	Make sure the directory 'tests/scenarios' exists.
	Each scenario should be a text file of commands, and expected output; scenario files should have the extension '.scene'.
	Last command in each scenario should be 'closeall'.


*	The script is going to mention which scenarios failed.
	For the failed scenarios, the differences between the expected output and the actual one will be dumped as *.html files in the 'tests/outputs' dir (to be viewed in-browser.)


*	Format of a *.scene file:

		<series of commands, ending with 'closeall'>
		<blank line>
		*****
		<blank line>
		<expected output>


* 	This script was written to run in a linux terminal (may or may not run on windows).
	To run the script you need python and valgrind (can be installed by running 'sudo apt install python3 valgrind -y' on ubuntu-based/debian-based systems.)

You can view this usage information by running './testEng.py -u' or './testEng.py --usage'.
