#!/usr/bin/python 
# -*- coding: utf-8 -*-

import sys
import os
import json
import random
import string

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
        
        ## source to put the icons in the TreeView:
        ## http://www.eurion.net/python-snippets/snippet/Tree%20View%20Column.html
        
        # retrieve the TreeView
        treeview = self.builder.get_object("treefolderview")
        # create the TreeViewColumns to display the data
        col0 = gtk.TreeViewColumn("")
        treeview.append_column(col0) 
        
        # create a CellRenderers to render the data
        cellpb = gtk.CellRendererPixbuf()
        cell = gtk.CellRendererText()
        
        # add the cells to the columns - 2 in the first
        col0.pack_start(cellpb, False)
        col0.pack_start(cell, True)
        
        # set the cell attributes to the appropriate liststore column
        col0.set_attributes(cellpb, stock_id=1)
        col0.set_attributes(cell, text=0)
        
        if self.options.filename is not None:
            self.fio = FileIO(self.options.filename)
            data = self.read_password_file(self.options.filename)
            if data is not None:
                self.load_password_tree(data)
        
        dic = {
            "on_buttonQuit_clicked" : self.quit,
            "on_windowMain_destroy" : self.quit,
            "gtk_main_quit" : self.quit,
            "show_about" : self.show_about,
            "cursor_changed": self.on_pass_selected,
            "add_entry": self.add_entry,
            "generate_password": self.generate_password,
            "save_database": self.save_database,
        }
        self.builder.connect_signals( dic )
        
        self.update_status_bar("Welcome into pypass")

        self.modifiedDb = False

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
                    "b_add_entry": gtk.STOCK_OK,
                    "b_cancel_entry": gtk.STOCK_CANCEL,
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
            data = self.fio.readJson()
        except IOError, er:
            self.generate_error(
                "Something went wrong when trying to load the database:",
                er)
            return
        return data

    def load_password_tree(self, tree):
        self.data = tree
        treeview = self.builder.get_object("treefolderview")
        treestore = gtk.TreeStore(str, str)
        #print tree
        for key in tree.keys():
            if key is not None:
                parent = treestore.append(None, [key, gtk.STOCK_DIRECTORY])
            else:
                parent = None
            for password in tree[key]:
                if isinstance(password, dict):
                    icon = gtk.STOCK_DIALOG_AUTHENTICATION
                    treestore.append(parent, [password['name'], icon])
        treeview.set_model(treestore)
        treeview.set_reorderable(True)
    
    def reset_entry_dialog(self):
        """ Reset the different entry field of the add_entry dialog """
        self.builder.get_object("entry_name").set_text("")
        self.builder.get_object("entry_user").set_text("")
        self.builder.get_object("entry_password").set_text("")
        self.builder.get_object("entry_url").set_text("")
    
    def make_pb(self, tvcolumn, cell, model, iter):
        stock = model.get_value(iter, 1)
        pb = self.treeview.render_icon(stock, gtk.ICON_SIZE_MENU, None)
        cell.set_property('pixbuf', pb)
        return
    
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
        if self.modifiedDb:
            dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING)
            dialog.set_markup("<b>" + "Erreur" + "</b>")
            dialog.format_secondary_markup(
                    "Voulez-vous sauvez la base avant de quitter ?")
            dialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_YES,
                                gtk.STOCK_CANCEL, gtk.RESPONSE_NO)
            result = self._dialog(dialog)
            if result == gtk.RESPONSE_YES:
                self.save_database()
        sys.exit(0)
    
    def save_database(self, widget = None):
        """ Save the current database """
        # TODO: reconstruct the json from the TreeView
        self.fio.save_json(self.data)
        self.update_status_bar("Database saved")
    
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
                    for key in ('name','user','password'):
                        content += "<b>%s:</b> %s \n" %(key, passw[key])
                    keys = passw.keys()
                    keys.sort()
                    for key in keys:
                        if key not in ('name','user','password'):
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
    
    def add_entry(self, widget):
        add = self.builder.get_object("dialogaddentry")
        if self._dialog(add):
            name = self.builder.get_object("entry_name").get_text()
            user = self.builder.get_object("entry_user").get_text()
            password = self.builder.get_object("entry_password").get_text()
            url = self.builder.get_object("entry_url").get_text()
            if "" in (name, user, password):
                self.generate_error("Could not enter the password. \nOne of the mandatory field had missing information")
                return
            else:
                passdict = {"name": name, "user": user, "password": password}
                if url is not "":
                    passdict['url'] = urll
                level = self.get_level()
                data = PassDatabase().add_password_to_database(
                                            self.data, level, passdict)
                self.load_password_tree(data)
                self.reset_entry_dialog()
                self.update_status_bar("Password added*")
                self.modifiedDb = True
                
    
    def update_status_bar(self, entry):
        """ Update the status bar with the given text """
        stbar = self.builder.get_object('statusbar')
        stbar.push(1, entry)
    
    def get_level(self):
        """ Retrieve the level selected """
        selection = self.builder.get_object("treefolderview").get_selection()
        (model, iter) = selection.get_selected()
        if iter is None: 
            return
        key = model[iter][0]
        return key
    
    def generate_password(self, widget):
        """ Generate a random password """
        length = random.randrange(5,15)
        random_string = ''.join(random.choice(string.ascii_letters + 
                            string.digits) for x in range(length))
        entry = self.builder.get_object("entry_password")
        entry.set_text(random_string)
        return

class PassDatabase(object):
    """
    Class to handle the addition and removal from the database
    """
    
    def add_password_to_database(self, database, level, passdict):
        """ Add the given hashdict to the given database at the given
        level"""
        #if level is None:
            #level = ""
        if level in database.keys():
            database[level].append(passdict)
        else:
            database[level] = [passdict]
        return database

class FileIO(object):
    """
    Class handling the File Input/Output
    Aka: 
    - decrypt using gpg
    - read the json file
    - encrypt using gpg
    - write the encrypted file
    """
    def __init__(self, filename = None):
        self.filename = filename
    
    def readJson(self, filename = None):
        """
        Read the set json file and return the json object
        If no filename is specify it will use the one given to the constructor
        and if both are None it will return None
        """
        readfile = self.filename
        if filename is not None:
            readfile = filename
        if readfile is None:
            return
        # TODO: make it decrypt the file
        f = open(readfile, "r")
        content = f.read()
        f.close()
        return json.loads(content)
    
    def save_json(self, json):
        """
        Save the given json into a file
        """
        print json, self.filename
