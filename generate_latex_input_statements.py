#!/usr/bin/env sage

import sage.all
import os
import string

if __name__ == '__main__':
	alphabet = [string.ascii_uppercase[char] for char in range(10)]
	with open("include_statements.tex","w") as fp:
				
		for dim in [4,5]:
			for letter in alphabet:
				for i in range(2):
					numgen = i + dim
					bound = 2

					fp.write('\\subsubsection{' + letter+'}\n\\input{"' + '{}d {} generators 2 bound {}'.format(dim, numgen, letter)+'.tex"}\n\n')