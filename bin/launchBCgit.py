import sys
from PySide import QtCore, QtGui

parentPath = '/'.join( sys.path[0].replace('\\', '/').split('/')[:-2] )
sys.path.append( parentPath )

import BCgit

app = QtGui.QApplication(sys.argv)
widget = BCgit.ui.ClassLoader()
widget.app().show()
sys.exit( app.exec_() )
