#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sys
import os
import json

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

class PyPass(object):

    def __init__( self, options):
        self.options = options
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.dirname(
                os.path.realpath( __file__ )) + "/../ui/pyrevelation.ui")
        self.mainwindow = self.builder.get_object('mainwindow')
        
        self.set_button_toolbar()
        
        treeview = self.builder.get_object("treefolderview")
        cell0 = gtk.CellRendererText()
        col0 = gtk.TreeViewColumn("title", cell0,    
                            text=0)
        treeview.append_column(col0)
        
        if self.options.filename is not None:
            self.data = self.read_password_file(self.options.filename)
            if self.data is not None:
                self.load_password_tree(self.data)
        
        dic = {
            "on_buttonQuit_clicked" : self.quit,
            "on_windowMain_destroy" : self.quit,
            "gtk_main_quit" : self.quit,
            "show_about" : self.show_about,
            "cursor_changed": self.on_pass_selected,
        }
        self.builder.connect_signals( dic )
        
        stbar = self.builder.get_object('statusbar')
        stbar.push(1, "Welcome into pypass")

        self.mainwindow.show()
        gtk.main()
    
    def set_button_toolbar(self):
        butons = {
                    "b_open": gtk.STOCK_OPEN,
                    "b_save": gtk.STOCK_SAVE,
                    "b_add": gtk.STOCK_ADD,
                    "b_edit": gtk.STOCK_EDIT,
                    "b_del": gtk.STOCK_REMOVE,
                    "b_quit": gtk.STOCK_QUIT,
                    "b_about": gtk.STOCK_ABOUT,
                    }
        for buton in butons.keys():
            butonopen = self.builder.get_object(buton)
            img = gtk.image_new_from_stock(butons[buton], 
                                            gtk.ICON_SIZE_LARGE_TOOLBAR)
            butonopen.set_image(img)

    def errorWindow(self, message, er = None):
        """ Display an error window with the given message """
        dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR)
        dialog.set_markup("<b>" + "Error" + "</b>")
        if er is not None:
            message = message + "\n %s" %er
        dialog.format_secondary_markup(message)
        dialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_YES)
        return self._dialog(dialog)

    def generate_error(self, errortext, er = None):
        """ 
        Function called when a error needs to be raised
        The error is then either showns in the console or in a window
        """
        if self.options.cli:
            print  errortext
            print er
            sys.exit(1)
        else:
            self.errorWindow(errortext, er)

    def read_password_file(self, filename):
        """Read the given json file and return the content """
        try:
            data = FileIO().readJson(filename)
        except IOError, er:
            self.generate_error(
                "Something went wrong when trying to load the database:",
                er)
            return
        return data

    def load_password_tree(self, tree):
        treeview = self.builder.get_object("treefolderview")
        treestore = gtk.TreeStore(gobject.TYPE_STRING)
        for key in tree.keys():
            parent = treestore.append(None, [key ])
            for password in tree[key]:
                if isinstance(password, dict):
                    treestore.append(parent, [password['name']])
        treeview.set_model(treestore)
        treeview.set_reorderable(True)

    
    def _dialog(self, dialog, timeout = 0, center_on = None):
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
    
    def show_about(self, widget):
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

        if model[iter].parent is not None:
            parent = model[iter].parent[0]
        
        if parent in self.data.keys():
            for passw in self.data[parent]:
                if key in passw['name']:
                    content = ""
                    for key in ('name','user','pass'):
                        content += "<b>%s:</b> %s \n" %(key, passw[key])
                    keys = passw.keys()
                    keys.sort()
                    for key in keys:
                        if key not in ('name','user','pass'):
                            if key.lower() == 'url':
                                content += "<b>%s:</b> <a href='%s'> %s</a> \n" %(
                                        key, passw[key], passw[key])
                            else:
                                content += "<b>%s:</b> %s \n" %(
                                        key, passw[key])
                    txtpass = self.builder.get_object("labelpass")
                    txtpass.set_text(content)
                    txtpass.set_use_markup(True)
        else:
            passwd = self.builder.get_object("labelpass")
            passwd.set_text("")
        
class FileIO(object):
    """
    Class handling the File Input/Output
    Aka: 
    - decrypt using gpg
    - read the json file
    - encrypt using gpg
    - write the encrypted file
    """
    def readJson(self, filename):
        """
        Read the given json file and return the json object
        """
        # TODO: make it decrypt the file
        f = open(filename, "r")
        content = f.read()
        f.close()
        return json.loads(content)
