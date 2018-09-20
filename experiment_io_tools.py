#!/usr/bin/env sage

""" Module to contain all I/O functions used by 
cone conjecture experiment.
"""



import sys
import time

def autocontinue_query_yes_no(question,expire=5,default=True):
	start_time = time.time()
	expires_in = expire # seconds
	user_input = None
	while (time.time() - start_time < expires_in):
		if user_input is not None:
			return user_input
		user_input = query_yes_no(question)
	return default

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

def ask_int(string="Please input an integer: "):
	""" returns a user inputted integer """
	acceptable_input = False
	user_input = None
	while not acceptable_input:
		try:
			user_input = input(string)
		except:
			print("\tNon-integer input detected, try again...")
		if isinstance(user_input, (int,long)):
			acceptable_input = True
	return user_input


def printseparator(): 
    print("\n----------------------------------------------------------------------\n")
 
def printmenu(choices_dict,
		menutitle = "Menu"):
	new_screen(menutitle)
	for choice in choices_dict:
		print("{} : {}".format(choice, choices_dict[choice]))
	printseparator()
	


def menu(choices_dict,
		menutitle = "Menu",
		prompt = "Please enter your choice: "):
	""" displays a menu and returns the choice listed
	Args:
		choices_dict (dictionary) : ( int : "choice text")
		menutitle (string) : optional text
	Returns:
		user_choice (int)
			"""
	printmenu(choices_dict,menutitle)
	
	keys = choices_dict.keys()
	valid_input = False
	while not valid_input:
		user_input = ask_int(prompt)
		if user_input in keys:
			valid_input = True
		else:
			printmenu(choices_dict,menutitle)
	new_screen()
	return user_input










if __name__ == "__main__":

	""" Some testing code here """
	choice = menu({1: "New Experiment", 
		  		   2: "Load Experiment"})
	print("You chose {}".format(choice))
