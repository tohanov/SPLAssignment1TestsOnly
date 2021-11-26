#!/usr/bin/python3
import subprocess
import os
import sys
import difflib
import shutil

scenariosPath = 'tests/scenarios'
outputsPath = 'tests/outputs'
sceneFileExtension = '.scene'
sceneSeparatorPrefix = '\n'
sceneSeparator = '*'*5+'\n'
sceneSeparatorSuffix = '\n'
# passedOutputExtension = ".pass"
failedOutputExtension = ".FAIL.html"
configFilePath = 'ExampleInput.txt'
binFilePath = 'bin/studio'
studioCommand = [binFilePath, configFilePath]
valgrindCommand = ['valgrind', '-v', '--leak-check=full', '--show-reachable=yes'] + studioCommand
scriptName = os.path.basename(__file__)

usageSeparator = "-"*20
usage = usageSeparator + "\n\033[1;32mUsage: './" + scriptName + "'\n\n[*]\033[0m\tPlace the script in the project's dir.\n"\
"\tMake sure the config file '" + configFilePath + "' exists.\n"\
"\tMake sure the directory '" + scenariosPath + "' exists.\n"\
"\tEach scenario should be a text file of commands, and expected output; scenario files should have the extension '"\
+ sceneFileExtension +\
"'.\n"\
"\tLast command in each scenario should be 'closeall'.\n"\
"\n\n"\
"\033[1;32m[*]\033[0m\tThe script is going to mention which scenarios failed.\n"\
"\tFor the failed scenarios, the differences between the expected output and the actual one will be dumped as *.html files in the '" + outputsPath + "' dir (to be viewed in-browser.)\n"\
"\n\n"\
"\033[1;32m[*]\033[0m\tFormat of a *" + sceneFileExtension + " file:\n"\
"\n"\
"\t\t<series of commands, ending with 'closeall'>\n"\
"\t\t<blank line>\n"\
"\t\t" + sceneSeparator +\
"\t\t<blank line>\n"\
"\t\t<expected output>\n"\
"\n\n\033[1;32m[*]\033[0m \tThis script was written to run in a linux terminal (may or may not run on windows).\n"\
"\tTo run the script you need python and valgrind (can be installed by running 'sudo apt install python3 valgrind -y' on ubuntu-based/debian-based systems.)\n\n"\
"You can view this usage information later by running './" + scriptName + " -u' or './" + scriptName + " --usage'.\n"+usageSeparator


if "-u" in sys.argv or\
	"--usage" in sys.argv:
	
	print(usage)
	exit()

if not os.path.isdir(scenariosPath):
	print()
	print("\033[1;31m[!]", scenariosPath, "dir wasn't found.\033[0m")

	print(usage)
	exit()

if not os.path.isfile(binFilePath):
	print()
	print("\033[1;31m[!]", binFilePath, "file wasn't found.\033[0m")

	print(usage)
	exit()

if not os.path.isfile(configFilePath):
	print()
	print("\033[1;31m[!]", configFilePath, "file wasn't found.\033[0m")

	print(usage)
	exit()

if os.path.isdir(outputsPath):
	shutil.rmtree(outputsPath)
os.mkdir(outputsPath)


for file in os.listdir(scenariosPath):
		if file.endswith(sceneFileExtension):
			print("\n[*] running", file)
			
			with open(scenariosPath + "/" + file) as f:
				scenario = f.read()
			
			userCommands,expectedOutput = scenario.split(sceneSeparatorPrefix + sceneSeparator + sceneSeparatorSuffix, 1)
			
			with subprocess.Popen(valgrindCommand, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,bufsize=1, universal_newlines=True) as p:
				valgrindOutput,stderr = p.communicate(userCommands)
				
				p.wait() # so the returncode will be set
				containedErrors = "ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)" not in valgrindOutput or\
									"All heap blocks were freed -- no leaks are possible" not in valgrindOutput

				if 	p.returncode is not 0 or\
					containedErrors:

					print("\033[1;31m[!]\033[0m valgrind check for {file} \033[1;31mFAILED\033[0m (exitcode: {returnCode}; {errorSummary})"\
						.format(file=file, returnCode=p.returncode, errorSummary=valgrindOutput.rsplit("==")[-1].rstrip("\n").lstrip(' ')))
				else:
					print("[+] valgrind check for", file, "passed")


			with subprocess.Popen(studioCommand, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE,bufsize=1, universal_newlines=True) as p:
				occuredOutput,stderr = p.communicate(userCommands)
			
			if expectedOutput != occuredOutput:
				outputFile = outputsPath + "/" + file.replace(sceneFileExtension, failedOutputExtension)
				print("\033[1;31m[!]\033[0m output check for {file} \033[1;31mFAILED\033[0m (see: {outputFile})"\
					.format(file=file, outputFile=outputFile))
				
				with open(outputFile, "w") as f:
					f.write(difflib.HtmlDiff().make_file(expectedOutput.split("\n"), occuredOutput.split("\n"), 'EXPECTED', 'OCCURED'))
			else:
				print("[+] output check for", file, "passed")

print()

