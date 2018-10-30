#!/usr/bin/env sage

import sage.all
import os
import string

if __name__ == '__main__':
	alphabet = [string.ascii_uppercase[char] for char in range(10)]
	latex_directory = "Python Generated Latex Files/"
	with open(latex_directory + "include_statements.tex","w") as fp:
				
		for dim in [4,5]:
			fp.write('\\section{"Data in dimension ' + str(dim) + '"}\n')
			for b in range(dim -3):
				if dim == 4:
					bound = b +2
				else:
					bound = b+1
				for i in range(2):
					numgen = i + dim
					fp.write('\\subsection{"' + str(numgen) + ' generators with the absolute value of coordinates bounded by {}\n'.format(bound) + '"}\n\n')
					for letter in alphabet:					
						fp.write('\\subsubsection{' + letter+'}\n\\input{"' + '{}d {} generators {} bound {}'.format(dim, numgen, bound,letter)+'.tex"}\n\\newpage\n')
				