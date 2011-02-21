#!/usr/bin/python 
# -*- coding: utf-8 -*-

# Copyright (c) 2011 Pierre-Yves Chibon <pingou AT pingoured DOT fr>
# Copyright (c) 2011 Johan Cwiklinski <johan AT x-tnd DOT be>
#
# This file is part of pypass.
#
# pypass is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pypass is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pypass.  If not, see <http://www.gnu.org/licenses/>.

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
    print("GTK not available")
    sys.exit(1)
try:
    import gobject
except:
    print("gobject not available")
    sys.exit(1)

class PyPassGui(object):

    def __init__( self, pypass, options):
        self.pypass = pypass
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(
                os.path.realpath( __file__ )), "ui", "pyrevelation.ui"))
        self.mainwindow = self.builder.get_object('mainwindow')
        
        self.set_button_toolbar()
        
        ## source to put the icons in the TreeView:
        ## http://www.eurion.net/python-snippets/snippet/Tree%20View%20Column.html
        
        ## Handles the tree view in the main window
        # retrieve the TreeView
        treeview = self.builder.get_object("treefolderview")
        # create the TreeViewColumns to display the data
        col0 = gtk.TreeViewColumn("")
        treeview.append_column(col0) 
        
        # create a CellRenderers to render the data
        cellpb = gtk.CellRendererPixbuf()
        cell = gtk.CellRendererText()
        
        # add the cells to the columns - 2 
        col0.pack_start(cellpb, False)
        col0.pack_start(cell, True)
        
        # set the cell attributes to the appropriate liststore column
        col0.set_attributes(cellpb, stock_id=1)
        col0.set_attributes(cell, text=0)
        
        #FIXME: send the pasword to decode!
        filename = None
        if options.filename is not None:
            filename = options.filename()
        self.pypass.load_data(filename = filename)
        if self.pypass.data is not None and self.pypass.data != "":
            self.load_password_tree(self.pypass.data_as_json())
        
        dic = {
            "on_buttonQuit_clicked" : self.quit,
            "on_windowMain_destroy" : self.quit,
            "gtk_main_quit" : self.quit,
            "show_about" : self.show_about,
            "cursor_changed": self.on_pass_selected,
            "add_entry": self.add_entry,
            "generate_password": self.generate_password,
            "save_database": self.save_database,
            "open_database": self.open_database,
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
                    }
        self.set_button_img(butons)
    
    def set_button_img(self, butons):
        """ For a given hash of button, set the image """
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
        The error will be displayed in a window
        """
        self.errorWindow(errortext, er)

    def load_password_tree(self, tree):
        """ Load a given tree into the treefolderview """
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
            dialog.add_buttons( gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_REMOVE, gtk.RESPONSE_NO,
                                gtk.STOCK_OK, gtk.RESPONSE_YES,)
            result = self._dialog(dialog)
            if result == gtk.RESPONSE_YES:
                self.save_database()
            elif result == gtk.RESPONSE_CANCEL:
                self.mainwindow.show()
                return
        sys.exit(0)
    
    def select_file(self, title, pathname, types = {}):
        """ Open a given file chosser dialog and return the selection if any """
        dialog = gtk.FileChooserDialog(title= title,
                                        action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                        buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,
                                                gtk.STOCK_OPEN,gtk.RESPONSE_OK)
                                        )
        dialog.set_current_folder(pathname)
        dialog.set_default_response(gtk.RESPONSE_OK)
        response = dialog.run()
        
        if len(types.keys()) > 0:
            for typek in types.keys():
                filter = gtk.FileFilter()
                filter.set_name(typek)
                for el in types[typek]:
                    filter.add_mime_type(el)
                dialog.add_filter(filter)
        
        if response == gtk.RESPONSE_OK:
            #print dialog.get_filename(), 'selected'
            selection = dialog.get_filename()
        else:
            #print 'Closed, no files selected'
            selection = None
            
        dialog.destroy()
        return selection
    
    def set_combox_type(self):
        """ Set the different options in the combobox of the new entry
        dialog """
        
        options = {
            "website":"",
            "server": gtk.STOCK_NETWORK,
            "ftp": "",
            "Email": "",
        }
        
        combo = self.builder.get_object("combo_type")
        store = gtk.ListStore(str, str)
        opts = options.keys()
        opts.sort()
        for opt in opts:
            store.append([opt, options[opt]])
        combo.set_model(store)

        cell = gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, 'text', 0)

        combo.set_active(0)
    
    def set_keys_list(self):
        """ Set all the keys retrieved from pypass into the list """
        keys = self.pypass.list_recipients()
        treeview = self.builder.get_object("treeviewkey")
        column_str = gtk.TreeViewColumn('Key ID') 
        treeview.append_column(column_str)
        cell = gtk.CellRendererText()
        column_str.pack_start(cell, True)
        column_str.add_attribute(cell, "text", 0)
        
        column_str = gtk.TreeViewColumn('') 
        treeview.append_column(column_str)
        cell1 = gtk.CellRendererText()
        column_str.pack_start(cell1, True)
        column_str.add_attribute(cell1, "text", 1)
        
        store = gtk.ListStore(str, str)
        treeview.set_model(store)
        for key in keys:
            store.append([key['keyid'], " ".join(key['uids'])])
    
    def open_database(self, widget = None):
        """ Open a selected database """
        # get database file
        filename = self.select_file("Open a database", os.path.expanduser('~'))
        if filename is not None:
            self.builder.add_from_file(os.path.join(os.path.dirname(
                os.path.realpath( __file__ )), "ui", "dialogkeychooser.ui"))
            # retrieve all keys and create the list
            self.set_keys_list()
            # ask to select a key and a password
            add = self.builder.get_object("dialogkeychooser")
            if self._dialog(add) != 1:
                print "not-ok"
                return
            else:
                selection = self.builder.get_object("treeviewkey").get_selection()
                (model, iter) = selection.get_selected()
                key = model[iter][0]
                entry = self.builder.get_object("entry_key_password")
                password = entry.get_text()
                print "key: %s - password: %s" %(key, password)
                #self.load_password_tree(self.pypass.decrypt())
            add.destroy()
            return
    
    def save_database(self, widget = None):
        """ Save the current database """
        # TODO: reconstruct the json from the TreeView
        self.pypass.data_from_json(self.data)
        self.pypass.crypt()

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
        """ Display the dialog to add an entry to the database """
        self.builder.add_from_file(os.path.join(os.path.dirname(
                os.path.realpath( __file__ )), "ui", "dialogaddentry.ui"))
        butons = {
                "b_add_entry": gtk.STOCK_OK,
                "b_cancel_entry": gtk.STOCK_CANCEL,
                }
        self.set_button_img(butons)
        self.set_combox_type()
        
        dic = { "generate_password": self.generate_password }
        self.builder.connect_signals( dic )
        
        add = self.builder.get_object("dialogaddentry")
        if self._dialog(add) == 1:
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
                data = self.pypass.add_password(
                                            self.data, level, passdict)
                self.load_password_tree(data)
                self.reset_entry_dialog()
                self.update_status_bar("Password added*")
                self.modifiedDb = True
        add.destroy()

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
        password = self.pypass.generate_password()
        entry = self.builder.get_object("entry_password")
        entry.set_text(password)
        return
