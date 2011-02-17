#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sys
import os
import ConfigParser
from PyPassjson import JsonClass

try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
except:
    print("GTK Not Availible")
    sys.exit(1)
try:
    import gobject
except:
    print("gobject Not Availible")
    sys.exit(1)


#config = ConfigParser.RawConfigParser()
#config.read('test.cfg')
data = JsonClass().generatePasswordList()

class PyPass(object):

    def __init__( self, filename = None ):
        
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.dirname(
                os.path.realpath( __file__ )) + "/pyrevelation.ui")
        self.mainwindow = self.builder.get_object('mainwindow')
        
        treeview = self.builder.get_object("treefolderview")
        cell0 = gtk.CellRendererText()
        col0 = gtk.TreeViewColumn("title", cell0,    
                            text=0)
        treeview.append_column(col0)
        
        treestore = gtk.TreeStore(gobject.TYPE_STRING)
        
        for key in data.keys():
            parent = treestore.append(None, [key ])
            for option in data[key ]:
                if isinstance(option, dict):
                    treestore.append(parent, [option['name']])
        treeview.set_model(treestore)
        treeview.set_reorderable(True)
        
        dic = {
            "on_buttonQuit_clicked" : self.quit,
            "on_windowMain_destroy" : self.quit,
            "gtk_main_quit" : self.quit,
            "show_about" : self.showAbout,
            "cursor_changed": self.on_pass_selected,
        }
        self.builder.connect_signals( dic )
        
        stbar = self.builder.get_object('statusbar')
        stbar.push(1, "Welcome into pypass")

        self.mainwindow.show()
    
    def _dialog(self, dialog, timeout=0, center_on=None):
        """ Display a dialog window """
        dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
        dialog.set_modal(True)
        dialog.set_keep_above(True)
        dialog.show_all()
        if timeout> 0:
            # hide after timeout seconds
            timer = gobject.timeout_add(timeout*1000, self._hide_dialog, dialog)
        result = dialog.run()
        dialog.hide()
        return result
    
    def showAbout(self, widget):
        """ Show the about diaglog """
        about = self.builder.get_object("aboutdialog")
        self._dialog(about)
    
    def quit(self, widget):
        """ Quit the application """
        print "quitting..."
        sys.exit(0)
    
    def on_pass_selected(self, widget):
        selection = self.builder.get_object("treefolderview").get_selection()
        (model, iter) = selection.get_selected()
        key = model[iter][0]
        parent = None
        print key
        if model[iter].parent is not None:
            parent = model[iter].parent[0]
        
        if parent in data.keys():
            for passw in data[parent]:
                if key in passw['name']:
                    passwd = self.builder.get_object("labelpass")
                    passwd.set_text(passw['pass'])
        else:
            passwd = self.builder.get_object("labelpass")
            passwd.set_text("")
        
    

if __name__ == "__main__":
   pypass = PyPass()
   gtk.main()
