# Imports
import os
import re
import time

# Parse a all.rules file
def parseRules(file):
	# Dict to hold the actual rules by sid
	rules = {}
	# Loop each line
	for line in file:
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
			# Add to rules dict (mark if it's a comment then remove that comment)
			rules[sid.group(1)] = (line.startswith('#'), line.lstrip('#'))
	# Return the dict
	return rules

# Exported class
class reporter:
	def __init__(self, cp):
		# Save the config parser instance
		self.cp = cp
	# Generates a report
	def generateReport(self):
		# Prep
		sysConfig = self.cp.getSystemConfig()
		categories = self.cp.getCategories()
		tmpDir = sysConfig["temp-dir"]
		gitDir = sysConfig["git-dir"]

		# Open the report file
		report = open(gitDir + '/reports/rules.md', 'w')

		# Write the current date and time as the header
		report.write("#Rules Report (" + time.strftime("%c") + ")\n");

		# Loop each category
		report.write("__Enabled Categories:__\n")
		for category in categories:
			# Print the name of the category
			report.write("* " + os.path.splitext(category)[0] + "\n")
		report.write("\n\n")

		# Parse the old rules and the new rules
		oldRules = os.path.join(tmpDir, "rules-old", "all.rules")
		if os.path.isfile(oldRules):
			oldRulesDict = parseRules(open(oldRules))
		else:
			oldRulesDict = {}
		newRules = os.path.join(gitDir, "all.rules")
		newRulesDict = parseRules(open(newRules))

		# Convert the sid lists to sets for set comprehensions
		oldRulesSet = set(oldRulesDict.keys())
		newRulesSet = set(newRulesDict.keys())
		
		# Perform all the comprehensions once
		addedSet = (newRulesSet - oldRulesSet)
		removedSet = (oldRulesSet - newRulesSet)
		intersectSet = (oldRulesSet & newRulesSet)

		# Write each of the categories
		report.write("__Added:__\n")
		for sid in addedSet:
			report.write("* [" + sid + "] " + re.search("msg:\"([^\"]+)\";", newRulesDict[sid][1]).group(1) + "\n")
		report.write("\n\n")
		report.write("__Removed:__\n")
		for sid in removedSet:
			report.write("* [" + sid + "] " + re.search("msg:\"([^\"]+)\";", oldRulesDict[sid][1]).group(1) + "\n")
		report.write("\n\n")
		report.write("__Disabled:__\n")
		for sid in intersectSet:
			if oldRulesDict[sid][0] == False and newRulesDict[sid][0] == True:
				report.write("* [" + sid + "] " + re.search("msg:\"([^\"]+)\";", newRulesDict[sid][1]).group(1) + "\n")
		report.write("\n\n")
		report.write("__Enabled:__\n")
		for sid in intersectSet:
			if oldRulesDict[sid][0] == True and newRulesDict[sid][0] == False:
				report.write("* [" + sid + "] " + re.search("msg:\"([^\"]+)\";", newRulesDict[sid][1]).group(1) + "\n")
		report.write("\n\n")
		report.write("__Modified:__\n")
		for sid in (oldRulesSet & newRulesSet):
			if oldRulesDict[sid][1] != newRulesDict[sid][1]:
				report.write("* [" + sid + "] " + re.search("msg:\"([^\"]+)\";", newRulesDict[sid][1]).group(1) + ":\n\n")
				report.write("       > " + oldRulesDict[sid][1] + "\n")
				report.write("       > " + newRulesDict[sid][1] + "\n")
		report.write("\n\n")

		# Count the enabled rules
		i = 0
		for sid in newRulesSet:
			if newRulesDict[sid][0] == False:
				i += 1
		report.write("**Total Enabled Rules:** " + str(i) + "\n")

		# Cleanup
		report.close()
		
		print("There are " + str(i) + " enabled rules.")
