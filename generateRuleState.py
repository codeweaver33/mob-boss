#!/usr/bin/python3
#    mob-boss is a suricata rule management program
#    Copyright (C) 2016  Dillon Bogenreif, Luke Young, Brandon Lattin
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Imports
import os
import re
import csv
import argparse

# Main function
def main():

	# Setup an argparse instance
	parser = argparse.ArgumentParser(
		description = "mob-boss rule_state.conf generator"
	)

	# Add the file args
	parser.add_argument('all.rules', help='The location of the all.rules file')
	parser.add_argument('rule_state.conf', help='The location to save the generated rule_state.conf')

	# Parse the args from the command line input
	args = parser.parse_args()

	# Open up the rule_state.conf file for writing
	ruleState = open(getattr(args, 'rule_state.conf'), 'w', newline='')
	ruleStateWriter = csv.writer(ruleState)

	# Write the header row
	ruleStateWriter.writerow(['sid', 'state', 'name'])

	# Loop each line in all.rules
	allRules = open(getattr(args, 'all.rules'), 'r');
	for line in allRules:
		# Ignore empty lines
		if not line:
			continue
		# Ignore whitespace lines
		if line.isspace():
			continue
		# Get the sid
		sid = re.search("sid:(\d+);", line)
		# If we found an sid
		if sid:
			# Write the row
			ruleStateWriter.writerow([sid.group(1), 0 if line.startswith('#') else 1, re.search("msg:\"([^\"]+)\";", line).group(1)])

	# Cleanup
	allRules.close()
	ruleState.close()

# Call main if needed
if __name__ == "__main__":
	main()
