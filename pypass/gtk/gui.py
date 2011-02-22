""" GTK GUI module for pypass """
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

#FIXME: should be from pypass import, but does not work due to name confusion
from .. import __version__, __author__, __copyright__, __credits__, __url__

try:
    import pygtk
    pygtk.require("2.0")
except ImportError:
    pass
try:
    import gtk
except ImportError:
    print("GTK not available")
    sys.exit(1)

def file_browse(dialog_action, title, pathname, file_name="",
                types=None):
    """This function is used to browse for a pyWine file.
    It can be either a save or open dialog depending on
    what dialog_action is.
    The path to the file will be returned if the user
    selects one, however a blank string will be returned
    if they cancel or do not select one.
    dialog_action - The open or save mode for the dialog either
    gtk.FILE_CHOOSER_ACTION_OPEN, gtk.FILE_CHOOSER_ACTION_SAVE
        file_name - Default name when doing a save
    source:
    http://www.pygtk.org/articles/extending-our-pygtk-application \
    /extending-our-pygtk-application.htm
    """

    if (dialog_action==gtk.FILE_CHOOSER_ACTION_OPEN):
        dialog_buttons = (gtk.STOCK_CANCEL
                            , gtk.RESPONSE_CANCEL
                            , gtk.STOCK_OPEN
                            , gtk.RESPONSE_OK)
    else:
        dialog_buttons = (gtk.STOCK_CANCEL
                            , gtk.RESPONSE_CANCEL
                            , gtk.STOCK_SAVE
                            , gtk.RESPONSE_OK)

    file_dialog = gtk.FileChooserDialog(title=title,
                action=dialog_action,
                buttons=dialog_buttons)
    #set the filename if we are saving
    if (dialog_action==gtk.FILE_CHOOSER_ACTION_SAVE):
        file_dialog.set_current_name(file_name)
    file_dialog.set_current_folder(pathname)
    file_dialog.set_default_response(gtk.RESPONSE_OK)
    
    if types is not None and isinstance(types, dict):
        for typek in types.keys():
            filefilter = gtk.FileFilter()
            filefilter.set_name(typek)
            for element in types[typek]:
                filefilter.add_mime_type(element)
            dialog.add_filter(filefilter)
    #Create and add the 'all files' filter
    filefilter = gtk.FileFilter()
    filefilter.set_name("All files")
    filefilter.add_pattern("*")
    file_dialog.add_filter(filefilter)

    #Init the return value
    result = None
    if file_dialog.run() == gtk.RESPONSE_OK:
        result = file_dialog.get_filename()
    file_dialog.destroy()

    return result

def _dialog(dialog):
    """ Display a dialog window """
    dialog.set_position(gtk.WIN_POS_CENTER_ON_PARENT)
    dialog.set_modal(True)
    dialog.set_keep_above(True)
    dialog.show_all()
    result = dialog.run()
    dialog.hide()
    return result


def error_window(message, error=None):
    """ Display an error window with the given message """
    dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR)
    dialog.set_markup("<b>" + "Error" + "</b>")
    if error is not None:
        message = message + "\n %s" % error
    dialog.format_secondary_markup(message)
    dialog.add_buttons(gtk.STOCK_OK, gtk.RESPONSE_YES)
    return _dialog(dialog)


def generate_error(errortext, error=None):
    """
    Function called when a error needs to be raised
    The error will be displayed in a window
    """
    error_window(errortext, error)


class PyPassGui(object):
    """ Class handling the gtk gui for pypass """

    def __init__(self, pypass, options):
        """ Instanciate the window and set the basic element """
        self.pypass = pypass
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "ui", "pyrevelation.ui"))
        self.mainwindow = self.builder.get_object('mainwindow')

        self.set_button_toolbar()

        ## source to put the icons in the TreeView:
        ## http://www.eurion.net/python-snippets/
        ## snippet/Tree%20View%20Column.html

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

        filename = None
        if options.filename is not None:
            filename = options.filename()
        self.pypass.load_data(filename=filename)
        if self.pypass.data is not None and self.pypass.data != "":
            self.load_password_tree(self.pypass.data_as_json())

        # Add the images on the button :-)
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.get_settings().set_long_property('gtk-button-images', 
                                                    True, '')

        self.data = {}
        dic = {
            "on_buttonQuit_clicked": self.quit,
            "on_windowMain_destroy": self.quit,
            "gtk_main_quit": self.quit,
            "show_about": self.show_about,
            "cursor_changed": self.on_pass_selected,
            "add_entry": self.add_entry,
            "generate_password": self.generate_password,
            "save_database": self.save_database,
            "save_as_database": self.save_as_database,
            "open_database": self.open_database,
        }
        self.builder.connect_signals(dic)

        self.update_status_bar("Welcome into pypass")

        self.modified_db = False

        self.mainwindow.show()
        gtk.main()

    def set_button_toolbar(self):
        """ Set the button toolbar with their logo """
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

    def load_password_tree(self, tree):
        """ Load a given tree into the treefolderview """
        self.data = tree
        treeview = self.builder.get_object("treefolderview")
        treestore = gtk.TreeStore(str, str)
        if not isinstance(tree, dict):
            text = self.builder.get_object("labelpass")
            text.set_text(tree)
            self.data = {}
            return
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
        #treeview.set_reorderable(True)

    def reset_entry_dialog(self):
        """ Reset the different entry field of the add_entry dialog """
        self.builder.get_object("entry_name").set_text("")
        self.builder.get_object("entry_user").set_text("")
        self.builder.get_object("entry_password").set_text("")
        self.builder.get_object("entry_url").set_text("")

    def show_about(self, widget):
        """ Show the about diaglog """
        about = self.builder.get_object("aboutdialog")
        about.set_name("PyPass")
        about.set_version(__version__)
        about.set_copyright(__copyright__)
        about.set_authors(__credits__)
        about.set_comments('\n'.join(__author__))
        _lpath = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), "..", "datas", "gplv3.txt")
        about.set_license(open(_lpath).read())
        about.set_website(__url__)
        #_logo_path = os.path.join(self.path, 'images/logo.png')
        #about.set_logo(gtk.gdk.pixbuf_new_from_file(_logo_path))

        _dialog(about)

    def quit(self, widget):
        """ Quit the application """
        print "quitting..."
        if self.modified_db:
            dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_WARNING)
            dialog.set_markup("<b>" + "Erreur" + "</b>")
            dialog.format_secondary_markup(
                    "Voulez-vous sauvez la base avant de quitter ?")
            dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                gtk.STOCK_REMOVE, gtk.RESPONSE_NO,
                                gtk.STOCK_OK, gtk.RESPONSE_YES,)
            result = _dialog(dialog)
            if result == gtk.RESPONSE_YES:
                self.save_database()
            elif result == gtk.RESPONSE_CANCEL:
                self.mainwindow.show()
                return
        sys.exit(0)

    def set_combox_type(self):
        """ Set the different options in the combobox of the new entry
        dialog """

        options = {
            "website": "",
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

    def set_keys_list(self, hide=True):
        """ Set all the keys retrieved from pypass into the list """
        keys = self.pypass.list_recipients()
        treeview = self.builder.get_object("treeviewkey")
        if hide:
            treeview.set_visible(False)
            treeview.destroy()
        else:
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

    def open_database(self, widget=None):
        """ Open a selected database """
        # get database file
        filename = file_browse(gtk.FILE_CHOOSER_ACTION_OPEN, "Open a database", 
                                os.path.expanduser('~'))
        if filename is not None:
            self.pypass.load_data(filename=filename)
            self.load_password_tree(self.pypass.data_as_json())
            return

    def save_database(self, widget=None):
        """ Save the current database """
        self.pypass.data_from_json(self.data)
        self.pypass.crypt()

        self.update_status_bar("Database saved")
        self.modified_db = False
    
    def save_as_database(self, widget=None):
        """ Save the current database in a selected file """
        filename = file_browse(gtk.FILE_CHOOSER_ACTION_SAVE, "Open a database", 
                                os.path.expanduser('~'))
        self.pypass.data_from_json(self.data)
        self.pypass.crypt(recipients = filename)

        self.update_status_bar("Database saved")
        self.modified_db = False

    def on_pass_selected(self, widget):
        """ Display the password in the window when selected on the tree """
        selection = self.builder.get_object("treefolderview").get_selection()
        (model, itera) = selection.get_selected()
        key = model[itera][0]
        parent = None

        if model[itera].parent is not None:
            parent = model[itera].parent[0]

        if parent in self.data.keys():
            for passw in self.data[parent]:
                if key in passw['name']:
                    content = ""
                    for key in ('name', 'password'):
                        content += "<b>%s:</b> %s \n" % (key, passw[key])
                    keys = passw.keys()
                    keys.sort()
                    for key in keys:
                        if key not in ('name', 'password'):
                            if key.lower() == 'url':
                                content += "<b>%s:</b> <a href='%s'>" \
                                    "%s</a> \n" % (key, passw[key], passw[key])
                            else:
                                content += "<b>%s:</b> %s \n" % (
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
                os.path.realpath(__file__)), "ui", "dialogaddentry.ui"))
        butons = {
                "b_add_entry": gtk.STOCK_OK,
                "b_cancel_entry": gtk.STOCK_CANCEL,
                }
        self.set_button_img(butons)
        self.set_combox_type()

        dic = {"generate_password": self.generate_password}
        self.builder.connect_signals(dic)

        add = self.builder.get_object("dialogaddentry")
        if _dialog(add) == 1:
            name = self.builder.get_object("entry_name").get_text()
            password = self.builder.get_object("entry_password").get_text()
            user = self.builder.get_object("entry_user").get_text()
            url = self.builder.get_object("entry_url").get_text()
            description = \
                self.builder.get_object("entry_description").get_text()
            combotype = self.builder.get_object("combo_type")
            passtype = combotype.get_active()
            print passtype
            if "" in (name, password):
                generate_error(errortext="Could not enter the password. \n" \
                    "Name or password had missing information")
                return
            else:
                passdict = {"name": name, "user": user, "password": password}
                if url is not "":
                    passdict['url'] = url
                if user is not "":
                    passdict['user'] = user
                if description is not "":
                    passdict['description'] = description
                level = self.get_level()
                data = self.pypass.add_password(
                                            self.data, level, passdict)
                self.load_password_tree(data)
                self.reset_entry_dialog()
                self.update_status_bar("Password added*")
                self.modified_db = True
        add.destroy()

    def update_status_bar(self, entry):
        """ Update the status bar with the given text """
        stbar = self.builder.get_object('statusbar')
        stbar.push(1, entry)

    def get_level(self):
        """ Retrieve the level selected """
        selection = self.builder.get_object("treefolderview").get_selection()
        (model, itera) = selection.get_selected()
        if itera is None:
            return
        key = model[itera][0]
        return key

    def generate_password(self, widget):
        """ Generate a random password """
        password = self.pypass.generate_password()
        entry = self.builder.get_object("entry_password")
        entry.set_text(password)
        return
