# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE

f_out_path = "salida_consola.txt"


with open(f_out_path, "w") as fin, open(f_out_path, "r") as fout:

	p = Popen(['python3.4'], stdout=fin, stdin=PIPE, stderr=fin)

	# Escribir en la consola
	p.communicate(input=b"print('a')\nprint('b')")

	# Leer de consola
	response = fout.readlines()

	# Manejar la info
	print(response)

