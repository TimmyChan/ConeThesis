""" Module to contain all I/O functions used by 
cone conjecture experimet.
"""



import sys

def query_yes_no(question, default="yes"):
	"""Ask a yes/no question via raw_input() and return their answer.

	"question" is a string that is presented to the user.
	"default" is the presumed answer if the user just hits <Enter>.
		It must be "yes" (the default), "no" or None (meaning
		an answer is required of the user).

	The "answer" return value is True for "yes" or False for "no".

	Source: http://code.activestate.com/recipes/577058/)
	"""
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	if default is None:
		prompt = " [y/n] "
	elif default == "yes":
		prompt = " [Y/n] "
	elif default == "no":
		prompt = " [y/N] "
	else:
		raise ValueError("invalid default answer: '%s'" % default)

	while True:
		sys.stdout.write(question + prompt)
		choice = raw_input().lower()
		if default is not None and choice == '':
			return valid[default]
		elif choice in valid:
			return valid[choice]
		else:
			sys.stdout.write("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")


def new_screen(header=None):
	""" Prints new screen in terminal regardless of OS """
	print("\033[H\033[J")
	if header is not None:
		boxprint(header)

def boxprint(string,symbol='#'):
	""" prints a box around a string using symbol """
	length = len(string)+4
	mainline = []
	mainline.append(symbol)
	mainline.append(' ')
	mainline.append(string)
	mainline.append(' ')
	mainline.append(symbol)
	mainlinestring = "".join(str(e) for e in mainline)

	horizontalboarder = [symbol for i in range(length)]
	horizontalboarderstring = "".join(str(e) for e in horizontalboarder)
	print(horizontalboarderstring)
	print(mainlinestring)
	print(horizontalboarderstring)

def pause(pausestring="Press Enter to continue..."):
	try:
		input("\n"+pausestring)
	except:
		None