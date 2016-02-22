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
