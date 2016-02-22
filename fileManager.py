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
import os
import shutil

class fileManager:
	def __init__(self):
		print("Initializing File Manager.")

	def clearDir(self, directory, recurse):
		print("Clearing directory " + directory + ". Recursion is set to " + str(recurse))
		if recurse:
			shutil.rmtree(directory, True)
		else:
			subprocess.call(("rm " + directory + "/*"), shell=True)

	def createDir(self, directory):
		print("Creating directory " + directory + ".")
		if os.path.isdir(directory):
			return
		else:
			os.makedirs(directory)

	#src and dst must be absolute paths -D
	def mvFile(self, src, dst):
		if os.path.isfile(src):
			subprocess.call(("mv " + src + " " + dst), shell=True)
		else:
			return

	def cpFile(self, src, dst):
		if os.path.isfile(src):
			subprocess.call(("cp " + src + " " + dst), shell=True)
		else:
			return

	def delFile(self, directory, f):
		if os.path.isfile(f):
			subprocess.call(("rm directory/" + f), shell=True)
		else:
			return

	def delDir(self, directory):
		if os.path.isdir(directory):
				subprocess.call(("rmdir " + directory), shell=True)
		else:
			return
