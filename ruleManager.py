import os
import requests
import tarfile
import re
import glob
import csv
import shutil
import fileinput
import sys


class ruleManager:
	def __init__(self, fm, gm, cp, rp):
		print("Initializing Rule Manager.")
		self.fm = fm
		self.gm = gm
		self.cp = cp
		self.rp = rp

	def build(self):
		self.clearTmp()
		self.initTmp()
		self.gitPull()
		self.initReports()
		self.migrateOldRules()
		self.getNewRules()
		self.extract()
		self.mergeCategories()
		self.updateRuleState()
		self.moveRules()
		self.callReporter()
		self.gitPush()

	def clearTmp(self):
		print("Clearing Temp directories.")
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		self.fm.clearDir(tmpDir, True)


	def initTmp(self):
		print("Re-initializing Temp directories.")
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		self.fm.createDir((tmpDir + "/rules"))
		self.fm.createDir((tmpDir + "/rules-new"))
		self.fm.createDir((tmpDir + "/rules-old"))

	def gitPull(self):
		print("Performing git Pull.")
		sysConfig = self.cp.getSystemConfig()
		gitDir = sysConfig["git-dir"]
		self.gm.pull(gitDir)

	def initReports(self):
		print("Initializing reports directory.")
		sysConfig = self.cp.getSystemConfig()
		gitDir = sysConfig["git-dir"]
		
		if not os.path.isdir((gitDir + "/reports")):
			self.fm.createDir((gitDir + "/reports"))

	def migrateOldRules(self):
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		gitDir = sysConfig["git-dir"]
		print("Moving old rules to " + tmpDir + "/rules-old/all.rules.")
		if os.path.isfile((gitDir + "/all.rules")):
			self.fm.mvFile((gitDir + "/all.rules"),(tmpDir + "/rules-old/all.rules"))
		#if os.path.isfile((gitDir + "/local.rules")):
		#	self.fm.mvFile((gitDir + "/local.rules"),(tmpDir + "/rules-old/local.rules"))


	def getNewRules(self):
		print("Retrieving new rules.")
		ruleDownload = self.cp.getRuleUrl()
		ruleUrl = ruleDownload["rule-url"]
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		#gitDir = sysConfig["git-dir"]

		#Pull down tarball from rule download location
		try:
			r = requests.get(ruleUrl, stream=True)
			f = open((tmpDir + "/rules.tar.gz"), "wb")
			for chunk in r.iter_content(chunk_size=1024):
				if chunk: #filters out keep-alive new chunks
					f.write(chunk)
					f.flush()
			f.close()
		except Exception as e:
			print(e)
			sys.exit(0)

	def extract(self):
		print("Extracting rules from tarball.")
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		try:
			f = tarfile.open((tmpDir + "/rules.tar.gz"), "r:gz")
			f.extractall(path=tmpDir+"/rules/")
			f.close()
		except Exception as e:
			print("Error occured in extracting tarball. Ensure that downloaded file is in fact a valid rules.tar.gz file. Error output: " + str(e))
			sys.exit(0)


	def mergeCategories(self):
		print("Merging categories into a new all.rules file.")
		sysConfig = self.cp.getSystemConfig()
		categories = self.cp.getCategories()
		tmpDir = sysConfig["temp-dir"]
		


		f = open((tmpDir + "/rules-new/all.rules-new"), "w")

		for item in categories:
			if(os.path.isfile((tmpDir + "/rules/rules/" + item))):
				fTwo = open((tmpDir + "/rules/rules/" + item), "r")
				for line in fTwo:
					f.write(line)
				fTwo.close()
			else:
				print("ALERT: Category: " + item + " does not exist. Rules will not be added. Please check mob-boss.yaml and disable " + item + ".")
		print("Rule merge complete.")
		f.close()

	def updateRuleState(self):
		print("Updating rule_state.conf with new rules.")

		# Read in the system configuration from config
		sysConfig = self.cp.getSystemConfig()

		# Catch first-run
		try:

			# Open the old ruleState first
			with open(sysConfig["git-dir"] + "/rule_state.conf", 'r', newline='') as ruleStateFile:

				# Use the builtin csv class reader
				ruleStateReader = csv.DictReader(ruleStateFile)

				# Read state into memory as a dictionary by sid
				ruleState = dict((rule["sid"], rule["state"]) for rule in ruleStateReader)
		
		# Catch file not existing
		except FileNotFoundError:
			ruleState = {}

		# Open the rule_state and close it
		with open(sysConfig["git-dir"] + "/rule_state.conf", 'w', newline='') as ruleStateFile:

			# Use the builtin csv class writer to write to the file
			ruleStateWriter = csv.writer(ruleStateFile)

			# Write the headers
			ruleStateWriter.writerow(['sid', 'state', 'name'])

			# Loop each line in all.rules
			for line in fileinput.input(sysConfig["temp-dir"] + "/rules-new/all.rules-new", inplace=True):

				# Ignore empty and whitespace lines, no changes needed
				if not line or line.isspace():
					print(line, end='') # Write as-is
					continue
				# Get the sid
				sid = re.search("sid:(\d+);", line)
				# If we didn't find an sid
				if not sid:
					print(line, end='') # Write as-is
					continue
				# Extract the sid
				sid = sid.group(1)
				# Grab the state from ET
				state = '0' if line.startswith('#') else '1'
				# If we have an rule_state value to disable the sid
				if sid in ruleState and ruleState[sid] == '0' and state != '0':
					# Over-ride the ET value
					state = '0'
					# Write the rule as disabled
					print("#" + line, end='')
				# No over-ride
				else:
					print(line, end='') # Write as-is
				# Write the row
				ruleStateWriter.writerow([
					sid, 
					state,
					re.search("msg:\"([^\"]+)\";", line).group(1)
				])

	#May be added in later
	#def processFlowbits(self):
	#	pass

	def moveRules(self):
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		gitDir = sysConfig["git-dir"]

		os.rename((tmpDir + "/rules-new/all.rules-new"), (tmpDir + "/rules-new/all.rules"))
		self.fm.mvFile((gitDir + "/all.rules"), (tmpDir + "/rules-old/all.rules"))
		self.fm.cpFile((tmpDir + "/rules-new/all.rules"), (gitDir + "/all.rules"))

		for file in glob.glob(tmpDir + "/rules/rules/*.map"):
			shutil.copy(file, (gitDir + "/"))

		for file in glob.glob(tmpDir + "/rules/rules/*.config"):
			shutil.copy(file, (gitDir + "/"))

		
	def callReporter(self):
		self.rp.generateReport()

	def gitPush(self):
		sysConfig = self.cp.getSystemConfig()
		gitDir = sysConfig["git-dir"]
		if not os.path.isfile((gitDir) + "/local.rules"):
			f = open(gitDir+"/local.rules", "w")
			f.write("")
			f.close()
		self.gm.push(gitDir, ["all.rules", "rule_state.conf", "reports", "*.map", "*.config", "local.rules"])

