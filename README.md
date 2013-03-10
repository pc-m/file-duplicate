fdup duplicate file finder
==========================


About
-----

Simple script I used to write everytime I import my photos or music to a computer.
Search a directory recursively and display a list of python list containing files with the same md5sum


Usage
-----

	# To delete all duplicate files in the current directory tree
	fdup.py | tr '\n' '\0' | xargs -0 rm
