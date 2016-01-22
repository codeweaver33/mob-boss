#!/usr/bin/python3
# 
# Suricata Rule Management
# Authors: Dillon Bogenreif, Luke Young
# Design Help: Brandon Lattin

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
