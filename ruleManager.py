import os
import requests
import tarfile
import re
import glob
import shutil


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
		self.purgeOld()
		self.etDisables()
		self.updateRuleState()
		self.applyCustomDisables()
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
		r = requests.get(ruleUrl, stream=True)
		f = open((tmpDir + "/rules.tar.gz"), "wb")
		for chunk in r.iter_content(chunk_size=1024):
			if chunk: #filters out keep-alive new chunks
				f.write(chunk)
				f.flush()
		f.close()

	def extract(self):
		print("Extracting rules from tarball.")
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]

		f = tarfile.open((tmpDir + "/rules.tar.gz"), "r:gz")
		f.extractall(path=tmpDir+"/rules/")
		f.close()


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


	def purgeOld(self):
		print("Purging old rules from rule_state.conf. This may take a bit.")
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		gitDir = sysConfig["git-dir"]
		ruleStateOld = []
		rulesNew = []
		ruleStateNew = []

		if os.path.isfile(gitDir + "/rule_state.conf"):
			f = open((gitDir + "/rule_state.conf"), "r")
		else:
			f = open((gitDir + "/rule_state.conf"), "w")
			f.write("sid,state,name\n")
			f.close()
			f = open((gitDir + "/rule_state.conf"), "r")
		#put rule_state.conf in memory as a list
		for line in f:
			ruleStateOld.append(line)
		f.close()
		#split list into list of lists
		i = 0
		while i < len(ruleStateOld):
			ruleStateOld[i] = ruleStateOld[i].split(",")
			i = i + 1
		#read in the new all.rules file
		f = open((tmpDir + "/rules-new/all.rules-new"), "r")
		for line in f:
			rulesNew.append(line)
		f.close()
		sidLookupList = []
		x = ""
		#create a lookup list of sids in rulesNew for efficiency
		for line in rulesNew:
			if not line == "":
				x = re.search(r'; sid:[0-9]*', line)
				if not x == None:
					x = x.group(0).strip("; sid:")
					sidLookupList.append(x)
		

		#Add in headers
		ruleStateNew.append(ruleStateOld[0][0] + "," + ruleStateOld[0][1] + "," + ruleStateOld[0][2])

		#for each element in ruleStateOld
		for element in ruleStateOld:
			#check if it is header
			if not element[0] == "sid":
				#for each element check if the sid is in the sidLookupList
				if element[0] in sidLookupList:
					ruleStateNew.append(element[0] + "," + element[1] + "," + element[2])

		#write the new rulestate to file
		f = open((gitDir + "/rule_state.conf"), "w")
		for line in ruleStateNew:
			if not line[len(line)-1] == "\n":
				line = line + "\n"
			f.write(line)

		f.close()


	def etDisables(self):
		print("Processing disables.")
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		gitDir = sysConfig["git-dir"]
		ruleStateOld = []
		sidLookupList = []

		#continual read ins/write outs of the rule_state are to ensure that if the process breaks along the way the file will still be intact
		f = open((gitDir + "/rule_state.conf"), "r")

		#read in rule_state.conf as a list of lists
		for line in f:
			ruleStateOld.append(line.split(","))
		f.close()

		f = open((tmpDir + "/rules-new/all.rules-new"), "r")
		
		# create a new lookup list with sid disables
		for line in f:
			if line.find("#") == 0:
				x = re.search(r'; sid:[0-9]*', line)
				if not x == None:
					x = x.group(0).strip("; sid:")
					sidLookupList.append(x)
		
		#go through and apply diables to rule_state.conf
		for element in ruleStateOld:
			if element[0] in sidLookupList:
				element[1] = "0"

		f = open((gitDir + "/rule_state.conf"), "w")
		for element in ruleStateOld:
			f.write(element[0] + "," + element[1] + "," + element[2])

		f.close()



	def updateRuleState(self):
		print("Updating rule_state.conf with new rules.")
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		gitDir = sysConfig["git-dir"]
		ruleStateOld = []
		ruleStateOldLookupList = []
		sidLookupList = []
		newRules = []

		f = open((gitDir + "/rule_state.conf"), "r")
		#read in rule_state.conf into list of lists
		for line in f:
			ruleStateOld.append(line.split(","))
		f.close()

		x = ""
		f = open((tmpDir + "/rules-new/all.rules-new"), "r")
		#read in sids for lookup list of new sids
		for line in f:
			if not line.find("#") == 0 and not line == "":
				x = re.search(r'; sid:[0-9]*', line)
				if not x == None:
					x = x.group(0).strip("; sid:")
					sidLookupList.append(x)
		f.close()
		#making a new list with same lookuplist structure
		for element in ruleStateOld:
			ruleStateOldLookupList.append(element[0])

		#check to see which sids are not in the rule_state.conf
		for element in sidLookupList:
			if element not in ruleStateOldLookupList:
				newRules.append(element)

		f = open((tmpDir + "/rules-new/all.rules-new"), "r")
		x = ""
		y = ""
		#add new rule into rule_state.conf
		#for each element in the newRules sid list
		for element in newRules:
			#for each line in the all.rules-new file
			for line in f:
				#ensure it is not disabled or a comment
				if not line.find("#") == 0:
					#find the sid
					pattern = "; sid:" + element
					x = re.search(pattern, line)
					#If sid was found
					if not x == None:
						#search for the msg field which contains value for the last column of rule_state.conf
						pattern = "\(msg:\"[A-Za-z0-9 \.\-\_\(\\)\|\/\+\,\?\=]*\";"
						y = re.search(pattern, line)
						#if found add a new entry to the ruleStateOld list
						if not y == None:
							#strip leading and trailing characters
							y = y.group(0).lstrip("(msg:\"").rstrip("\";").replace(",", "").replace("\"", "")
							if "," in y:
								print(y)
							y = y + "\n"
							newEle = [element, "1", y]
							ruleStateOld.append(newEle)

		f.close()

		f = open((gitDir + "/rule_state.conf"), "w")

		for element in ruleStateOld:
			f.write(element[0] + "," + element[1] + "," + element[2])
		f.close()

		



	def applyCustomDisables(self):
		print("Applying Custom Disables.")
		sysConfig = self.cp.getSystemConfig()
		tmpDir = sysConfig["temp-dir"]
		gitDir = sysConfig["git-dir"]
		ruleState = []
		rulesNew = []
		rulesNewSids = []

		f = open((gitDir + "/rule_state.conf"), "r")
		#read in rule_state.conf into list of lists
		for line in f:
			ruleState.append(line.split(","))
		f.close()

		#read in all.rules-new file
		f = open((tmpDir + "/rules-new/all.rules-new"), "r")
		for line in f:
			rulesNew.append(line)
		f.close()

		
		x = ""
		#create sid reference list for all-rules.new
		for element in rulesNew:
			#filter out comments/already disabled
			if not element.find("#") == 0:
				#find the sid
				pattern = "; sid:[0-9]*;"
				x = re.search(pattern, element)
				#if an sid is found, add it into rulesNewSids with an enabled value
				if not x == None:
					rulesNewSids.append([x.group(0).lstrip("; sid:").rstrip(";"), "1"])
		#for every element in the ruleState list
		for element in ruleState:
			#if that sid is disabled
			if element[1] == "0":
				#for every item in rulesNewSids
				i = 0
				while i < len(rulesNewSids):
					#if the sid matches the disabled sid set that rule to disabled
					if rulesNewSids[i][0] == element[0]:
						rulesNewSids[i][1] = "0"
					i = i + 1
		
		x = ""
		# for every element in rulesNewSids
		for element in rulesNewSids:
			#if the element is set to disabled
			if element[1] == "0":
				#iterate through rulesNew for sids
				i = 0
				while i < len(rulesNew):
					#filter out those that are comments or already disabled
					if not rulesNew[i].find("#") == 0:
						#search for the sid
						pattern = "; sid:[0-9]*;"
						x = re.search(pattern, rulesNew[i])
						# if found break to just sid
						if not x == None:
							x = x.group(0).lstrip("; sid:").rstrip(";")
							if x == element[0]:
								rulesNew[i] = "#" + rulesNew[i]
					i = i + 1

		f = open((tmpDir + "/rules-new/all.rules-new"), "w")

		for line in rulesNew:
			f.write(line)

		f.close()

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

