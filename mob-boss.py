#!/usr/bin/python3
#
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

import sys
import argparse
import subprocess
import fileManager
import gitManager
import configParser
import ruleManager
import reporter

def main():

	# If not Python 3, bail
	if sys.version_info <= (3, 0):
		sys.stderr.write("Sorry, mob-boss requires Python 3\n")
		sys.exit(1)

	# Setup an argparse instance
	parser = argparse.ArgumentParser(
		description = "Suricata Rule Management"
	)

	# The path to the configuration file
	parser.add_argument('-c', '--config', required=True)

	# Parse the args from the command line input
	args = parser.parse_args()
	
	# Create a config parser instance
	cp = configParser.configParser(args.config)

	# Initialize Objects
	fm = fileManager.fileManager()
	gm = gitManager.gitManager()
	rp = reporter.reporter(cp)
	rm = ruleManager.ruleManager(fm, gm, cp, rp)
	
	# Call Rule Manager for Build Process
	rm.build()

if __name__ == "__main__":
	main()
