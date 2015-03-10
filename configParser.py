# Imports
import yaml

# Exported class
class configParser:
	def __init__(self, file):
		# Read in the file and parse as yaml
		self.config = yaml.load(open(file, "r"))
	# Retrieves the list of rules to use
	def getCategories(self):
		return self.config["category-config"]
	# Retrieves the system configuration
	def getSystemConfig(self):
		return self.config["system-config"]
	# Retrieves the suricata configuration
	def getSuricataConfig(self):
		return self.config["suricata-config"]
	# Retrieves the download URL
	def getRuleUrl(self):
		return self.config["rule-download"]
