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
import binascii

from bitstring import BitArray


def main(info):

	info_to_db = {}

	with open(info.FILE, "r") as f:

		pos = 0

		for x in f.read():

			# Encode: x -> hex(x) -> bin
			c = BitArray("0x%s" % binascii.hexlify(x.encode(errors="ignore")).decode())

			print("[i] Storing char: '%s'" % x)

			# Call to get ID for each letter
			for i, l in enumerate(c.bin, 1):

				# Update value
				if l == "1":
					val = "true"
				else:
					val = "false"

				print("    |- Storing bit '%s'" % l)
				response = requests.post("https://api.booleans.io", data=dict(val=val))

				if response.status_code == 429:
					print("Waiting 2 minutes for service limitation...")

					time.sleep(120)

					response = requests.post("https://api.booleans.io", data=dict(val=val))

				res = json.loads(response.text)

				# Add to db
				info_to_db[pos] = res['id']

				# Wait for service limitation: 40 req/ 2 minutes
				if (i % 40) == 0:
					print("Waiting 2 minutes for service limitation...")
					time.sleep(120)

				pos += 1

	# Dump to file
	json.dump(info_to_db, open(info.OUT, "w"))


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Hider to booleans.io')

	# Main options
	parser.add_argument('-f', '--file', dest="FILE", help="input file with info to hide", required=True)
	parser.add_argument('-o', '--output', dest="OUT", help="output file with hidden info. Default: hidden.db", default="hidden.db")

	parsed_args = parser.parse_args()

	main(parsed_args)
