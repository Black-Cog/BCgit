#!/usr/bin/env python

"""PyQt4 port of the layouts/basiclayout example from Qt v4.x"""

from PySide import QtCore, QtGui
import sys
import Anvil.core
import BCgit.core

class ClassLoader():
	NumGridRows = 3
	NumButtons = 4

	def __init__(self):
		# tmp var 
		self.projectWS  = 'E:/140817_tools/_framework/BCworkspace/'
		self.userWS     = 'E:/140817_tools/_framework/cedricWorkspace/'
		self.getEnv()

		# ui var
		__windowSize = [640, 350]

		# defind class
		Awindow      = Anvil.core.Window()
		Abox         = Anvil.core.Box()
		Alayout      = Anvil.core.Layout()
		Atext        = Anvil.core.Text()
		Atextfield   = Anvil.core.Textfield()
		Aitemlist    = Anvil.core.Itemlist()
		Abutton      = Anvil.core.Button()
		BCgitActions = BCgit.core.BCgitActions()

		# window init
		self.window = Awindow.create( title='BCgit', size=[ __windowSize[0], __windowSize[1] ] )

		# boxs init
		box_general = Abox.create( parent=self.window, name='General', w=450, h=320, x=10, y=25 )
		box_branch  = Abox.create( parent=self.window, name='Branch',  w=160, h=320, x=470, y=25 )

		# layouts init
		layout_workspace = Alayout.create( parent=box_general )
		layout_branch    = Alayout.create( parent=box_branch )

		# texts init
		text_projectWS = Atext.create( text='Project workspace :' )
		text_userWS    = Atext.create( text='User workspace     :' )

		# textfields init
		self.textfield_projectWS = Atextfield.create( text=self.projectWS, enable=False )
		self.textfield_userWS    = Atextfield.create( text=self.userWS, enable=False )

		# itemlists init
		self.itemlist_stat   = Aitemlist.create( 
												dbclick=lambda x:self.add( file=self.itemlist_stat.currentItem().text() )
												)
		self.itemlist_branch = Aitemlist.create(
												dbclick=lambda x:self.checkout( branch=self.itemlist_branch.currentItem().text() )
												)

		# buttons init
		button_stat   = Abutton.create( name='stat',   cmd=self.stat )
		button_diff   = Abutton.create( name='diff',   cmd=self.diff )
		button_rebase = Abutton.create( name='rebase', cmd=self.rebase )
		button_commit = Abutton.create( name='commit', cmd=self.commit )
		button_new    = Abutton.create( name='new',    cmd=self.newBranch )
		button_delete = Abutton.create( name='delete', cmd=self.deleteBranch )

		# defind layouts content
		layout_workspace.addRow( text_projectWS, self.textfield_projectWS )
		layout_workspace.addRow( text_userWS, self.textfield_userWS )
		# layout_workspace.addRow( button_stat, self.itemlist_stat )
		layout_workspace.addWidget( self.itemlist_stat )
		layout_workspace.addWidget( button_stat )
		layout_workspace.addWidget( button_diff )
		layout_branch.addWidget( button_rebase )
		layout_branch.addWidget( button_commit )
		layout_branch.addWidget( button_new )
		layout_branch.addWidget( button_delete )
		layout_branch.addWidget( self.itemlist_branch )

		# update UI
		self.stat()
		self.branch()


	def app( self ):
		return self.window

	def getEnv( self ):
		envFile  = open( 'E:/140817_tools/_framework/BCworkspace/_master/BCgit/env/env.py', 'r' )
		envLines = envFile.readlines()
		envFile.close()
		for i in envLines :
			exec(i)
		self.projectWS = projectWS
		self.userWS = userWS












################################################################################################
################################### EXTERNALIZE JFn ############################################
################################################################################################

	def stat( self ):
		'''Update the itemlist for stat UI.'''
		# defind class
		Aitemlist    = Anvil.core.Itemlist()
		BCgitActions = BCgit.core.BCgitActions()

		# defind listStat
		bcstat = BCgitActions.stat( workspace=self.textfield_userWS.text() )
		formatDic = {}
		track   = [0,.5,0]
		untrack = [.75,0,0]
		for i in range( len(bcstat['newfiles'][0]) ) :
			color = untrack
			if bcstat['newfiles'][1][i] == True : color = track
			formatDic[ len(formatDic) ] = [ bcstat['newfiles'][0][i], 'BCgit/icons/new.png', color ]
		for i in range( len(bcstat['deletedfiles'][0]) ) :
			color = untrack
			if bcstat['deletedfiles'][1][i] == True : color = track
			formatDic[ len(formatDic) ] = [ bcstat['deletedfiles'][0][i], 'BCgit/icons/deleted.png', color ]

		for i in range( len(bcstat['editfiles'][0]) ) :
			color = untrack
			if bcstat['editfiles'][1][i] == True : color = track
			formatDic[ len(formatDic) ] = [ bcstat['editfiles'][0][i], 'BCgit/icons/edit.png', color ]

		listStat = Aitemlist.itemConvert( dic=formatDic )

		# add list in the ui
		Aitemlist.add( itemList=self.itemlist_stat, items=listStat, append=False )
		self.branch()

	def branch( self ):
		'''Update the itemlist for branch UI.'''
		# defind class
		Aitemlist = Anvil.core.Itemlist()
		BCgitActions = BCgit.core.BCgitActions()

		# defind listBranch
		bcstat = BCgitActions.branch( workspace=self.textfield_userWS.text(), query=True )
		formatDic = {}
		for i in range( len(bcstat['master']) )   : formatDic[ len(formatDic) ] = [ bcstat['master'][0],   'BCgit/icons/master.png',  [0.0, 0.0, 0.7] ]
		for i in range( len(bcstat['checkout']) ) : formatDic[ len(formatDic) ] = [ bcstat['checkout'][0], 'BCgit/icons/check.png',   [0.5, 0.3, 0.0] ]
		for i in range( len(bcstat['branch']) )   : formatDic[ len(formatDic) ] = [ bcstat['branch'][i],   'BCgit/icons/uncheck.png', [0.3, 0.3, 0.3] ]
		listBranch = Aitemlist.itemConvert( dic=formatDic )

		# add list in the ui
		Aitemlist.add( itemList=self.itemlist_branch, items=listBranch, append=False )

	def newBranch( self ):
		'''Create new branch.'''
		# defind class
		BCgitActions = BCgit.core.BCgitActions()

		# defind listStat
		name = self.openInputDialog( title='New branch', text='Name : ' )
		if name : BCgitActions.branch( workspace=self.textfield_userWS.text(), branch=name )

		# update ui
		self.branch()

	def deleteBranch( self ):
		'''Delete branch.'''
		# defind class
		BCgitActions = BCgit.core.BCgitActions()

		# defind listStat
		selectedBranch = self.itemlist_branch.currentItem()

		if selectedBranch:
			selectedBranch = selectedBranch.text()
			if selectedBranch == '_master':
				self.onShowInformation( title='Information', text='Impossible to delete the master branch!' )

			elif selectedBranch == BCgitActions.getCheckoutBranch( workspace=self.textfield_userWS.text() ):
				self.onShowInformation( title='Information', text='Impossible to delete a checkout branch!' )

			else :
				def removeBranchFolder():
					BCgitActions.branch( workspace=self.textfield_userWS.text(), branch=selectedBranch, delete=True )

				self.onShowQuestion( 	
									title='Question',
									text='Are you sur to delete the branch : "%s"?' % ( selectedBranch ),
									cmd1= removeBranchFolder
									)
		
		# update ui
		self.branch()

	def rebase( self ):
		'''Launch rebase cmd.'''
		# defind class
		BCgitActions = BCgit.core.BCgitActions()

		#launch rebase
		BCgitActions.rebase( workspace=self.textfield_userWS.text(), workspaceParent=self.textfield_projectWS.text() )

		self.checkout( branch='_master' )

	def commit( self ): ## TODO finir pop up textfiel
		'''Launch commit cmd.'''
		# defind class
		BCgitActions = BCgit.core.BCgitActions()

		#launch rebase
		commit = self.openInputDialog( title='Commit', text='Comment : ' )
		if commit : BCgitActions.commit( workspace=self.textfield_userWS.text(), workspaceParent=self.textfield_projectWS.text(), comment=commit )

		# update ui
		self.stat()

	def checkout( self, branch=None ):
		'''Launch checkout cmd.'''
		# defind class
		BCgitActions = BCgit.core.BCgitActions()

		# if branch != BCgitActions.getCheckoutBranch( workspace=self.textfield_userWS.text() ):
		BCgitActions.checkout( workspace=self.textfield_userWS.text(), branch=branch )

		# update ui
		self.branch()
		self.stat()

	def add( self, file=None ):
		'''Launch add cmd.'''
		# defind class
		BCgitActions = BCgit.core.BCgitActions()
		workspace = self.textfield_userWS.text()

		# check is file is track
		branch     = BCgitActions.getCheckoutBranch( workspace=workspace )
		trackFiles = BCgitActions.getAddedFile( workspace=workspace, branch=branch )
		
		if file in trackFiles : BCgitActions.removeFromAdd(workspace=workspace, file=file )
		else : BCgitActions.add(workspace=workspace, file=file )

		# update ui
		self.stat()

	def diff( self, file=None ):
		'''Launch diff cmd.'''
		# defind class
		BCgitActions = BCgit.core.BCgitActions()
		Aitemlist    = Anvil.core.Itemlist()

		workspace = self.textfield_userWS.text()
		file      = Aitemlist.list( itemList=self.itemlist_stat, selected=True )[0].text()

		content = BCgitActions.diff( workspace=self.textfield_userWS.text(), file=file, full=False )

		formatDic = {}
		for i in range( len(content) ):
			if content[i].startswith('+'):   formatDic[i] = [ content[i], 'BCgit/icons/new.png',     [0.0, 0.5, 0.0] ]
			elif content[i].startswith('-'): formatDic[i] = [ content[i], 'BCgit/icons/deleted.png', [1.0, 0.0, 0.0] ]
			else :                           formatDic[i] = [ content[i], 'BCgit/icons/uncheck.png', [0.3, 0.3, 0.3] ]

		content = Aitemlist.itemConvert( dic=formatDic)

		# build window
		self.diffWin = TextWindow( workspace=self.textfield_userWS.text(), title=file, content=content)
		self.diffWin.app().show()
		




################################################################################################
################################## EXTERNALIZE ANVIL ###########################################
################################################################################################

	def onShowInformation( self, title=None, text=None ):
		"""
		Show the information message
		"""
		QtGui.QMessageBox.information(None, title, text)

	@staticmethod
	def onShowQuestion( title=None, text=None, cmd1=None, cmd2=None ):
		"""
		Show the question message
		"""
		flags = QtGui.QMessageBox.StandardButton.Yes 
		flags |= QtGui.QMessageBox.StandardButton.No
		response = QtGui.QMessageBox.question(None, title, text, flags)
		if response == QtGui.QMessageBox.Yes:
			cmd1()
		elif QtGui.QMessageBox.No:
			cmd2
		else:
			cmd2

	@staticmethod
	def openInputDialog( title=None, text=None, cmd1=None, cmd2=None ):
		"""
		Opens the text version of the input dialog
		"""
		text, result = QtGui.QInputDialog.getText(None, title, text)
		if result :
			if cmd1 : cmd1()
			else : return text
		
		elif cmd2 : cmd2()


class TextWindow():
	def __init__(self, workspace=None, title='None', content=None):
		"""Constructor"""
		# QtGui.QWidget.__init__(self)
		self.workspace = workspace
		self.fullMode = False

		Awindow      = Anvil.core.Window()
		Alayout      = Anvil.core.Layout()
		Aitemlist    = Anvil.core.Itemlist()
		Abutton      = Anvil.core.Button()
		Abox         = Anvil.core.Box()


		self.window = Awindow.create( title=title, size=[ 1000, 500 ] )
		box_diff  = Abox.create( parent=self.window, name='Difference',  w=1000, h=500, x=10, y=25 )
		layout_sourceCode = Alayout.create( parent=box_diff )
		self.sourceCode = Aitemlist.create()
		self.button_fullCode = Abutton.create( name='Compact code', cmd=self.fullCode )

		Aitemlist.add( itemList=self.sourceCode, items=content, append=False, sort=False )
		layout_sourceCode.addWidget( self.sourceCode )
		layout_sourceCode.addWidget( self.button_fullCode )

	def fullCode( self ):
		if self.fullMode == True :
			self.button_fullCode.setText('Compact code')
			self.fullMode = False
		else :
			self.button_fullCode.setText('Full code')
			self.fullMode = True

		BCgitActions = BCgit.core.BCgitActions()
		Aitemlist    = Anvil.core.Itemlist()

		content = BCgitActions.diff( workspace=self.workspace, file=self.window.windowTitle().title(), full=self.fullMode )

		formatDic = {}
		for i in range( len(content) ):
			if content[i].startswith('+'):   formatDic[i] = [ content[i], 'BCgit/icons/new.png',     [0.0, 0.5, 0.0] ]
			elif content[i].startswith('-'): formatDic[i] = [ content[i], 'BCgit/icons/deleted.png', [1.0, 0.0, 0.0] ]
			else :                           formatDic[i] = [ content[i], 'BCgit/icons/uncheck.png', [0.3, 0.3, 0.3] ]

		content = Aitemlist.itemConvert( dic=formatDic)

		Aitemlist.add( itemList=self.sourceCode, items=content, append=False, sort=False )


	def app( self ):
		return self.window