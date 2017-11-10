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
import subprocess

class gitManager:
	def __init__(self):
		print("Initializing Git Manager.")

	def pull(self, directory):
		try:
			subprocess.call(("git pull --quiet"), shell=True, cwd=directory)
		except Exception as e:
			print("Error occured in Git Manager pull: " + str(e))
			print("Halting execution.")
			exit(0)
		
	#filesToAdd will be a list of files that need to be added
	def push(self, directory, filesToAdd):
		#git add
		for f in filesToAdd:
			try:
				subprocess.call(("git add " + f), shell=True, cwd=directory)
			except Exception as e:
				print("Error has occured in Git Manager add: " + str(e))
				print("Halting execution.")
				exit(0)
		try:
			subprocess.call(("git commit --quiet -m \"Automated commit from mob-boss.\""), shell=True, cwd=directory)
		except Exception as e:
			print("Error occured in Git Manager commit: " + str(e))
			print("Halting execution.")
			exit(0)
		try:
			subprocess.call(("git push --quiet"), shell=True, cwd=directory)
		except Exception as e:
			print("Exception occured in Git Manager push: " + str(e))
			print("Halting execution.")
			exit(0)

# Will delete; design decision not to handle the cloning process
"""
	def clone(self, directory, url):
		try:
			subprocess.call(("git -C " + directory + "/ clone " + url), shell=True)
		except Exception as e:
			print("Faied to clone " + url + " Error: " + e)
			print("Halting execution.")
			exit(0)
"""




