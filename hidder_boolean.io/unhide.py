# -*- coding: utf-8 -*-
#
# Boolean-Hider - https://github.com/cr0hn/bo
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import json
import time

import requests
import argparse

from bitstring import BitArray
from collections import OrderedDict


def main(info):

	results_text = []

	tmp_info = json.load(open(info.FILE, "r"))
	info = OrderedDict()

	# Order dict
	keylist = list([int(x) for x in tmp_info.keys()])
	keylist.sort()
	for key in keylist:
		info[key] = tmp_info[str(key)]

	print("[i] Starting ... ")
	bin_text = []
	for i, (pos, e_id) in enumerate(info.items(), 1):

		print("    |- Reading: '%s'" % e_id)

		response = requests.get("https://api.booleans.io/%s" % e_id).text

		val = json.loads(response)['val']

		# Update value
		if val is True:
			val = "1"
		else:
			val = "0"

		bin_text.append(val)

		if (i % 8) == 0:
			result_chr = chr(int(BitArray("0b%s" % "".join(bin_text)).hex, 16))

			results_text.append(result_chr)

			# Reset intermediate binary string
			bin_text = []

		# Wait for service limitation: 40 req/ 2 minutes
		if (i % 40) == 0:
			print("Waiting 2 minutes for service limitation...")
			time.sleep(120)

	print("\n[i] Hidden message: '%s'" % ''.join(results_text))

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Unhider from booleans.io')

	# Main options
	parser.add_argument('-f', '--file', dest="FILE", help="input file with hidden info", required=True)

	parsed_args = parser.parse_args()

	main(parsed_args)
