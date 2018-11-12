#!/usr/bin/env sage

import sage.all
import os
import string

if __name__ == '__main__':
	alphabet = [string.ascii_uppercase[char] for char in range(10)]
	for dim in [4,5]:
		for letter in alphabet:
			for b in range(dim -3):
				if dim == 4:
					bound = b +2
				else:
					bound = b+1
				for i in range(2):
					numgen = i + dim

					
					

					experiment_topdown = "{} generators {} bound {}".format(numgen, bound, letter)
					directory_topdown = "DATA/{}d/".format(dim)+experiment_topdown +"/"

					experiment_bottomup =  "{} generators {} bound {} bottomup".format(numgen, bound, letter)
					directory_bottomup = "DATA/{}d/".format(dim)+experiment_bottomup +"/"

					latex_directory = "Python Generated Latex Files/"

					topdown_summary_path = directory_topdown + "Data Summary.txt"
					bottomup_summary_path = directory_bottomup + "Data Summary.txt"

					topdown_summary_string = ""
					topdown_string = ""
					bottomup_summary_string = ""
					bottomup_string = ""

					with open(topdown_summary_path,'r') as fp:
						topdown_array = fp.readlines()
						fp.close()

					i = 0
					for line in topdown_array:
						if i < 4:
							topdown_summary_string += line
						else:
							topdown_string += line[1:]
						i +=1

					
					
					with open(bottomup_summary_path,'r') as fp:
						bottomup_array = fp.readlines()
						fp.close()
					
					i = 0
					for line in bottomup_array:
						if i < 4:
							bottomup_summary_string += line
						else:
							bottomup_string += line[1:]
						i +=1
					
					initial_conditions_string = ""
					if topdown_summary_string <> bottomup_summary_string:
						print("Check this experiment: {}".format(experiment_topdown))
						initial_conditions_string += "Topdown:\n"+topdown_summary_string + "\nBottomup:\n"+bottomup_summary_string
					else:
						initial_conditions_string = topdown_summary_string

					latex_preamble = 	"\\documentclass[10pt]{article}\n\\begin{document}\n"
					latex_init_condit = "\\textbf{Initial Conditions:}\n\\begin{SAGE}\n" + initial_conditions_string + "\n\\end{SAGE}\n"
					latex_tabular  = 	"\\begin{tabular}{c|c}\n\\textbf{Top Down} & \\textbf{Bottom Up} \\\\ \\hline  \n\\begin{SAGE}\n"
					latex_tabular += 	topdown_string + "\\end{SAGE} \n&\n\\begin{SAGE}\n"
					latex_tabular +=	bottomup_string + "\\end{SAGE} \n\\\\ \\hline\n\n"
					latex_tabular += 	'\\begin{minipage}{.4\\textwidth}\n\\includegraphics[width=\\textwidth]{"'+"DATA/{}d/".format(dim)+experiment_topdown+'/top_sequence SIZE"}\n'
					latex_tabular += 	"\\end{minipage} &\n"
					latex_tabular +=	'\\begin{minipage}{.4\\textwidth}\n\\includegraphics[width=\\textwidth]{"'+"DATA/{}d/".format(dim)+experiment_bottomup+'/bottom_sequence SIZE"}\n'
					latex_tabular += 	"\\end{minipage} \\\\ \\\\\n\\hline \\\\"
					latex_tabular += 	'\\begin{minipage}{.4\\textwidth}\n\\includegraphics[width=\\textwidth]{"'+"DATA/{}d/".format(dim)+experiment_topdown+'/top_sequence LENGTH"}\n'
					latex_tabular += 	"\\end{minipage} &\n"
					latex_tabular +=	'\\begin{minipage}{.4\\textwidth}\n\\includegraphics[width=\\textwidth]{"'+"DATA/{}d/".format(dim)+experiment_bottomup+'/bottom_sequence LENGTH"}\n'
					latex_tabular += 	"\\end{minipage}\n\\end{tabular}\n\\end{document}"
					
					latex_code = latex_preamble + latex_init_condit + latex_tabular

					with open(latex_directory + "{}d ".format(dim) + experiment_topdown + ".tex", 'w') as fp:
						fp.write(latex_code)
