'''
arboresence :


| --- BCworkspace
|			|
|			| --- _master
|			|		 |
|			|		 | --- Forge
|			|		 |
|			|		 | --- BCshading
|			|
|			|
|			| --- __commit
|					 |
|					 | --- commit1
|					 |		|
|					 |		| --- commitFile ## resume of the commit
|					 |		|
|					 |		| --- files in the commit
|					 |
|					 | --- commit2
|					 |		|
|					 |		| --- commitFile ## resume of the commit
|					 |		|
|					 |		| --- files in the commit
|
|
| --- user1 workspace
|			|
|			| --- devCurrent
|			|		 |
|			|		 | --- Forge
|			|		 |
|			|		 | --- BCshading
|			|
|			|
|			| --- _branch
|					 |
|					 | --- _master
|					 |		|
|					 |		| --- Forge
|					 |		|
|					 |		| --- BCshading
|					 |
|					 | --- _branch1
|					 |		|
|					 |		| --- Forge
|					 |		|
|					 |		| --- BCshading
|					 |
|					 | --- _branch2
|					 		|
|					 		| --- Forge
|					 		|
|					 		| --- BCshading
|			
| --- user2 workspace
|			|
|			| --- devCurrent
|			|		 |
|			|		 | --- Forge
|			|		 |
|			|		 | --- BCshading
|			|
|			|
|			| --- _branch
|					 |
|					 | --- _master
|					 |		|
|					 |		| --- Forge
|					 |		|
|					 |		| --- BCshading
|					 |
|					 | --- _branch1
|					 |		|
|					 |		| --- Forge
|					 |		|
|					 |		| --- BCshading
|					 |
|					 | --- _branch2
|					 		|
|					 		| --- Forge
|					 		|
|					 		| --- BCshading



def merge():
	Copy file of the "commit directory" to BCworkspace.
	return
def resolveConflit():
	Write a tmp file with diff betwin differents files.
	return

# def pullRequest():
# 	return

'''

#################################################################################
################################################################################# 
#################################################################################

import os
import shutil
import difflib
import filecmp
from getpass import getuser

class BCgitActions():
	"""docstring for BCgit"""
	def __init__(self):
		self._master = '_master'
		self.workspaceParent = 'E:/140817_tools/_framework/BCworkspace'
		self.workspace       = 'E:/140817_tools/_framework/cedricWorkspace'
		self.path 			 = 'E:/140817_tools/_framework/cedricWorkspace/devCurrent/BCgit/tmp/master/file.txt'
		self.path2 			 = 'E:/140817_tools/_framework/cedricWorkspace/devCurrent/BCgit/tmp/branch/file.txt'

	def rebase( self, workspace, workspaceParent ):
		'''Copy the selected project id does not exist or update from BCworkspace to user workspace.'''
		'@parameter string workspace Path of the user workspace.'
		'@parameter string workspaceParent Path of the workspace parent.'
		
		workspaceParent += '/%s' % (self._master)
		workspace       += '/branch/%s' % (self._master)

		if os.path.isdir( workspaceParent ):
			#cleanup workspace master folder
			if os.path.isdir( workspace ):
				shutil.rmtree( workspace )

			#rebase
			shutil.copytree( workspaceParent, workspace )

	def branch( self, workspace, branch=None, query=False, delete=False ):
		'''Create a copy of the master folder in user workspace.'''
		'@parameter string workspace Path of the user workspace.'
		'@parameter string branch Name of the new branch.'
		'@parameter bool query If True, return a list of branch.'

		if query == False:
			masterBranchPath = '%s/branch/%s' %( workspace, self._master )
			branchPath       = '%s/branch/%s' %( workspace, branch )

			# creat branch
			if delete == False:
				# check if branch exist
				if not os.path.isdir( branchPath ) and os.path.isdir( masterBranchPath ):
					shutil.copytree( masterBranchPath, branchPath )

			# delete branch
			else:
				if branch != self._master:
					if os.path.isdir( branchPath ) : shutil.rmtree( branchPath )

		else:
			branchlist   = { 'master':[], 'checkout':[], 'branch':[] }
			branchDir    = '%s/branch/' %(workspace)
			if os.path.isdir( branchDir ):
				for i in os.listdir( '%s/branch/' %(workspace) ):
					if not '.' in i :
						if i == self._master : branchlist['master'].append(i)
						elif i == self.getCheckoutBranch(workspace) : branchlist['checkout'].append(i)
						else : branchlist['branch'].append(i)

			return branchlist

	def checkout( self, workspace, branch ):
		'''Change the current branch in user workspace.'''
		'@parameter string workspace Path of the user workspace.'
		'@parameter string branch Name of the branch for checkout.'

		devCurrent       = '%s/devCurrent' %( workspace )
		branchPath       = '%s/branch/%s' %( workspace, branch )
		checkoutFilePath = '%s/branch/checkout.info' %( workspace )
		oldBranch = self.getCheckoutBranch( workspace )

		if oldBranch and os.path.isdir( branchPath ) and os.path.isdir( devCurrent ):
			if branch == oldBranch:
				return
			elif oldBranch != self._master:
				#save current branch
				oldBranchPath = '%s/branch/%s' %( workspace, oldBranch )
				if os.path.isdir( oldBranchPath ):
					shutil.rmtree( oldBranchPath )
				shutil.copytree( devCurrent, oldBranchPath )

		if os.path.isdir( branchPath ):
			#cleanup workspace master folder
			if os.path.isdir( devCurrent ):
				shutil.rmtree( devCurrent )

			#checkout
			shutil.copytree( branchPath, devCurrent )
			ckFile = open( checkoutFilePath, 'w' )
			ckFile.write( branch )
			ckFile.close()

	def add( self, workspace, file ):
		'''Forward files in the pull in wait for a commit.'''
		'@parameter string workspace Path of the user workspace.'
		'@parameter string file Path of the file at add in the pull for the commit.'

		addFilePath = '%s/branch/%s.info' %( workspace, self.getCheckoutBranch(workspace) )

		item = file
		# for item in file.split( ' ' ):
		# if os.path.isfile( item ):
		itemName = '.'.join( item.split( '/' )[-1].split( '.' )[:-1] )
		addFile = open( addFilePath, 'a' )
		addFile.write( '%s\n' %( item ) )
		addFile.close()

	def removeFromAdd( self, workspace, file ):
		'''Remove files of the pull.'''
		'@parameter string workspace Path of the user workspace.'
		'@parameter string file Path of the file at remove to the pull for the commit.'

		addFilePath = '%s/branch/%s.info' %( workspace, self.getCheckoutBranch(workspace) )
		addFile = open( addFilePath, 'r' )
		fileList = addFile.readlines()
		addFile.close()

		for item in file.split( ' ' ):
			item = '%s\n' %( item )
			if item in fileList:
				fileList.remove( item )

		newFileList = []
		for i in fileList :
			if i != '\n' : newFileList.append( i )

		if newFileList:
			addFile = open( addFilePath, 'w' )
			addFile.write( ''.join(newFileList) )
			addFile.close()
		else:
			os.remove( addFilePath )

	def commit( self, workspace, workspaceParent, comment ):
		'''Forward the pull of files in the "commit directory" of BCworkspace in wait for a merge.'''
		'@parameter string workspace Path of the user workspace.'
		'@parameter string workspaceParent Path of the workspace parent.'
		'@parameter string comment Comment of the commit.'

		addFilePath = ( '%s/branch/%s.info' %( workspace, self.getCheckoutBranch(workspace) ) ).replace( '//', '/')
		addFile     = open( addFilePath, 'r' )
		fileList    = addFile.readlines()
		addFile.close()

		sourceDir    = ( '%s/devCurrent' %(workspace) ).replace( '//', '/')
		sourceBranch = ( '%s/branch' %(workspace) ).replace( '//', '/')
		commitDir    = ( '%s/__commit/%s/%s' %( workspaceParent, self.formatStr(getuser()), self.getCheckoutBranch(workspace) ) ).replace( '//', '/')

		# create directory if does not exist
		if not os.path.isdir( commitDir ) : os.makedirs( commitDir )

		# copy files
		for file in fileList:
			file = (sourceDir + file).replace( '\n', '')
			newfile   = file.replace( sourceDir, commitDir )
			newfolder = '/'.join( newfile.split('/')[:-1] )

			if not os.path.isdir( newfolder ) : os.makedirs( newfolder )
			shutil.copyfile( file, newfile )

		shutil.copyfile( addFilePath, addFilePath.replace( sourceBranch, commitDir ) )
		os.remove( addFilePath )

		# add comment to the info file
		addFileCommit  = open( addFilePath.replace( sourceBranch, commitDir ), 'a' )
		fileList = addFileCommit.write( '\n<<<<\n%s\n>>>>' %(comment) )
		addFileCommit.close()

	def removeCommitDirectory( self, workspaceParent, user, branch ):
		'''Delete files in the "commit directory".'''
		'@parameter string workspaceParent Path of the workspace parent.'
		'@parameter string user Name of the user.'
		'@parameter string branch Name of branch for delete the commit relatif.'

		commitDir = '%s/__commit/%s/%s' %( workspaceParent, self.formatStr(user), branch )

		# delete directory if exist
		if os.path.isdir( commitDir ) : shutil.rmtree( commitDir )

	def stat( self, workspace ):
		'''Return if files are edit, deleted or added in user workspace.'''
		'@parameter string workspace Path of the user workspace.'

		devCurrent   = '%s/devCurrent' %(workspace)
		branchMaster = '%s/branch/_master' %(workspace)
		listfilesCur = []
		listfilesMst = []
		status       = {'newfiles' : [[], []], 'deletedfiles' : [[], []], 'editfiles' : [[], []] }

		# defind listfilesCur
		for root, dirs, files in os.walk( devCurrent ):
			for file in files:
				if '.' in file : listfilesCur.append( '%s/%s' %(root.replace('\\', '/').replace(devCurrent, ''), file) )

		# defind listfilesMst
		for root, dirs, files in os.walk( branchMaster ):
			for file in files:
				if '.' in file : listfilesMst.append( '%s/%s' %(root.replace('\\', '/').replace(branchMaster, ''), file) )

		# defind newfiles
		for i in listfilesCur : 
			if not i in listfilesMst : 
				status['newfiles'][0].append(i)
				# newfiles.append(i)

		# defind deletedfiles
		for i in listfilesMst : 
			if not i in listfilesCur : 
				status['deletedfiles'][0].append(i)
				# deletedfiles.append(i) 


		for i in listfilesMst :
			if i in listfilesCur:
				if not filecmp.cmp( devCurrent+i, branchMaster+i ) :
					status['editfiles'][0].append( i )


		# list track files
		fileList = self.getAddedFile( workspace=workspace, branch=self.getCheckoutBranch(workspace) )
		for i in status:
			if status[i][0]:
				for j in status[i][0]:
					if j in fileList :
						status[i][1].append( True )
					else : status[i][1].append( False )

		return status

	@staticmethod
	def diff( workspace, file, full=False ):
		'''Compare betwin files in user workspace and BCworkspace.'''
		'@parameter string master Path of the file in the master branch.'
		'@parameter string child Path of the file in the current branch.'
		'@parameter bool full If True, return all lines in the file with the difference.'

		masterPath = '%s/branch/_master%s' %(workspace, file)
		childPath  = '%s/devCurrent%s' %(workspace, file)

		if not os.path.isfile( masterPath ):
			return ['New File.']

		elif not os.path.isfile( childPath ):
			return ['Deleted File.']

		else :
			with open(masterPath, 'r') as f1, open(childPath, 'r') as f2:
				diff = difflib.ndiff( f1.readlines(),f2.readlines() )
				if diff:
					sourceOut = []
					for line in diff:
						line = line.replace('\n', '').replace('\r', '')
						if full == True:
							if not line.startswith('?') : sourceOut.append(line)
						else:
							if line.startswith('-') : sourceOut.append( '%s |endline' %(line) )
							elif line.startswith('+') : sourceOut.append( '%s |endline' %(line) )

					return sourceOut

				else : return None

	@staticmethod
	def getCheckoutBranch( workspace ):
		checkoutFilePath = '%s/branch/checkout.info' %( workspace )
		branch = None

		if os.path.isfile( checkoutFilePath ):
			ckFile = open( checkoutFilePath, 'r' )
			branch = ckFile.read()
			ckFile.close()

		return branch

	@staticmethod
	def getAddedFile( workspace, branch ):
		addFilePath = ( '%s/branch/%s.info' %( workspace, branch ) ).replace( '//', '/')
		fileList = []
		if os.path.isfile( addFilePath ):
			addFile     = open( addFilePath, 'r' )
			fileListTmp = addFile.readlines()
			addFile.close()
			for i in fileListTmp : fileList.append( i.replace('\n', '') )

		return fileList

	@staticmethod
	def formatStr(str):
		alpha = [ "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
		newstring = ''
		for i in str:
			if i.isdigit() : newstring += i

			elif i == '_' : newstring += i

			else:
				for j in alpha:
					if i == j or i == j.capitalize() : newstring += i

		return newstring

	@staticmethod
	def process():
		print 'helloWorld'
		# print self.stat( self.workspace )
		# print self.diff( self.path, self.path2 )
		# self.commit( self.workspace, self.workspaceParent, 'mon premier debug' )
		# self.removeFromAdd( self.workspace, 'E:/140817_tools/_framework/cedricWorkspace/devCurrent/BCshading/rsl/BCglass.sl' )
		# self.rebase( self.workspace, self.workspaceParent )


# test = BCgitActions()
# test.process()