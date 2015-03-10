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
