#!/usr/bin/env sage

import sage.all
import os
import string

if __name__ == '__main__':
	dim = 5
	experiments = os.listdir("DATA/{}d/".format(dim))
	experiments.sort()
	print "{}".format(experiments) + "\n\n"
	alternating = []
	for expr in experiments:
		if "alternating" in expr:
			alternating.append(expr)

	print alternating

	latex_directory = "Python Generated Latex Files/"


	for expr in alternating:
		directory = "DATA/{}d/".format(dim) + expr + "/"
		summary_path = directory + "Data Summary.txt"
		with open(summary_path, 'r') as fp:
			summary_text = fp.read()
			fp.close()

		#print summary_path + "\n" + summary_text
		latex_preamble =	"\\documentclass[10pt]{article}\n\\begin{document}\n"
		latex_summary =		"\\textbf{Initial Conditions:}\n\\begin{SAGE}\n" + summary_text + "\n\\end{SAGE}\n"
		latex_tabular =		"\\begin{tabular}{c|c}\n\\textbf{Top Sequence} & \\textbf{Bottom Sequence} \\\\ \\hline \n"
		latex_tabular += 	'\\begin{minipage}{.45\\textwidth}\n\\includegraphics[width=\\textwidth]{"'+"DATA/{}d/".format(dim)+expr+'/top_sequence SIZE"}\n'
		latex_tabular += 	"\\end{minipage} &\n"
		latex_tabular +=	'\\begin{minipage}{.45\\textwidth}\n\\includegraphics[width=\\textwidth]{"'+"DATA/{}d/".format(dim)+expr+'/bottom_sequence SIZE"}\n'
		latex_tabular += 	"\\end{minipage} \\\\ \\\\\n\\hline \\\\\n"
		latex_tabular += 	'\\begin{minipage}{.45\\textwidth}\n\\includegraphics[width=\\textwidth]{"'+"DATA/{}d/".format(dim)+expr+'/top_sequence LENGTH"}\n'
		latex_tabular += 	"\\end{minipage} &\n"
		latex_tabular +=	'\\begin{minipage}{.45\\textwidth}\n\\includegraphics[width=\\textwidth]{"'+"DATA/{}d/".format(dim)+expr+'/bottom_sequence LENGTH"}\n'
		latex_tabular += 	"\\end{minipage}\n\\end{tabular}\n\\end{document}"
		
		latex_code = latex_preamble + latex_summary + latex_tabular

		latex_path = latex_directory + "{}d ".format(dim) + expr +".tex"
		with open(latex_path, 'w') as fp:
			fp.write(latex_code)