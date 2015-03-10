import subprocess

class gitManager:
	def __init__(self):
		print("Initializing Git Manager.")

	def pull(self, directory):
		try:
			subprocess.call(("git pull"), shell=True, cwd=directory)
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
			subprocess.call(("git commit -m \"Automated commit from mob-boss.\""), shell=True, cwd=directory)
		except Exception as e:
			print("Error occured in Git Manager commit: " + str(e))
			print("Halting execution.")
			exit(0)
		try:
			subprocess.call(("git push"), shell=True, cwd=directory)
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




