# -*- coding: utf-8 -*-
from collections import defaultdict

from PyPDF2 import PdfFileReader
from PyPDF2.pdf import PageObject, ContentStream, TextStringObject, u_, i, b_


def is_continuation(content, item):
	if content.operations[item - 1][1] == b_("Tm"):

		# Search previous "Tm"
		for bef in range(-2, -15, -1):
			try:
				if content.operations[item - bef][1] == b_("Tm"):
					prev_val = content.operations[item - bef][0]

					break
			except IndexError:
				return False
		else:
			return False

		key_1_preve = '{0:.5f}'.format(prev_val[4]).split(".")[1]
		key_2_preve = '{0:.5f}'.format(prev_val[5]).split(".")[1]

		prev_curr = content.operations[item - 1][0]
		key_1_curr = '{0:.5f}'.format(prev_curr[4]).split(".")[1]
		key_2_curr = '{0:.5f}'.format(prev_curr[5]).split(".")[1]

		# if key_1_curr != key_1_preve or key_2_curr != key_2_preve:
		if key_1_curr == key_1_preve:
			return True

	return False


def is_header(content, item):
	if content.operations[item - 1][1] == b_("Td"):
		return True
	elif content.operations[item - 1][1] == b_("Tm") and \
			content.operations[item - 2][1] == b_("Tf"):

		if content.operations[item - 3][1] == b_("BT") or \
			content.operations[item - 3][1] == b_("scn"):
			return True
		else:
			return False
	else:
		return False


def extractText_with_separator(self, remove_headers=False):
	text = u_("")
	content = self["/Contents"].getObject()
	if not isinstance(content, ContentStream):
		content = ContentStream(content, self.pdf)
	# Note: we check all strings are TextStringObjects.  ByteStringObjects
	# are strings where the byte->string encoding was unknown, so adding
	# them to the text here would be gibberish.
	for item, (operands, operator) in enumerate(content.operations):
		if operator == b_("Tj"):

			# Skip headers?
			if is_header(content, item):
				continue

			if not is_continuation(content, item):
				text += "\n"

			_text = operands[0]
			if isinstance(_text, TextStringObject):
				text += _text

		elif operator == b_("T*"):
			text += "\n"
		elif operator == b_("'"):
			text += "\n"
			_text = operands[0]
			if isinstance(_text, TextStringObject):
				text += operands[0]
		elif operator == b_('"'):
			_text = operands[2]
			if isinstance(_text, TextStringObject):
				text += "\n"
				text += _text
		elif operator == b_("TJ"):

			# Skip headers?
			if is_header(content, item):
				continue

			if not is_continuation(content, item):
				text += "\n"

			for i in operands[0]:
				if isinstance(i, TextStringObject):
					text += i

			# text += "\n"
	return text

PageObject.extractText_with_separator = extractText_with_separator


KEYWORDS = ["procesos electorales"]


def find_in_pdf(pdf_path, keywords):
	"""
	Try to find a word list into pdf file.

	.. note:

		The line number is approximately, not exactly.

	:param pdf_path: path to pdf
	:type pdf_path: str

	:param keywords: list of keyword to search
	:type keywords: list(str)

	:return: a structure like this: { PAGE_NUM: { LINE_NUM: TEXT_OF_LINE}
	:rtype: dict(str: dict(int: str))
	"""

	pdf = PdfFileReader(open(pdf_path, 'rb'))

	matches = defaultdict(dict)

	for page_no, page in enumerate(pdf.pages, 1):
		text = page.extractText_with_separator()

		line_no = 1

		# search
		for keyword in keywords:
			for line in text.split("\n"):
				if not line:
					continue

				line_no += 1

				if keyword in line.lower():
					matches["page_%s" % page_no][line_no] = line

	return matches

if __name__ == '__main__':
	r = find_in_pdf("BOE.pdf", KEYWORDS)

	print(r)