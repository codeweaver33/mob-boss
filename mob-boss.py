#!/usr/bin/python3
# 
# Suricata Rule Management
# Authors: Dillon Bogenreif, Luke Young, Brandon Lattin

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
	parser.add_argument('--initial', action='store_true', help="Use for first time run.")

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

	# If initial run generate RuleState
	if args.initial:
		subprocess.call(("python3 generateRuleState.py " + cp.getSystemConfig()["git-dir"] + "/all.rules " + cp.getSystemConfig()["git-dir"] + "/rule_state.conf"), shell=True)
		gm.push(cp.getSystemConfig()["git-dir"], "rule_state.conf")
if __name__ == "__main__":
	main()