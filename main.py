import json
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class EntryBox(Gtk.Box):
    def __init__(self, mode, amount, date):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        if(mode == True):
            amount_label = Gtk.Label()
            amount_label.set_markup('<span foreground="#00ff00"> ' + str(amount) + '</span>')
            self.pack_start(amount_label, False, False, 3)
        else:
            amount_label = Gtk.Label()
            amount_label.set_markup('<span foreground="#ff0000"> ' + str(amount) + '</span>')
            self.pack_start(amount_label, False, False, 3)

        date_label = Gtk.Label()
        date_label.set_markup('<span foreground="#777777">' + date + '</span>')
        self.pack_end(date_label, False, False, 3)


class GoalStats(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)
        progbar = Gtk.ProgressBar()
        progbar.set_fraction(0.4)
        progbar.set_show_text(False)
        self.pack_start(progbar, False, False , 3)
        goal_label = Gtk.Label("40% of your monthly goal spent.")
        self.pack_end(goal_label, False, False, 3)


class GeneralStats(Gtk.Box):
    def __init__(self, entry_list):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.entry_list = entry_list
        self.set_size_request(200, 300)
        monthly_label = Gtk.Label("Overview for November:")
        self.pack_start(monthly_label, False, False, 4)
        incoming = entry_list.get_incoming()
        outgoing = entry_list.get_outgoing()
        self.in_label = Gtk.Label("In:\t\t" + str(incoming) + "€")
        self.out_label = Gtk.Label("Out:\t\t" + str(outgoing) + "€")
        calc_sep = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.comb_label = Gtk.Label("Combined:\t" + str(incoming - outgoing) + "€")
        self.pack_end(self.comb_label, False, False, 4)
        self.pack_end(calc_sep, False, False, 4)
        self.pack_end(self.out_label, False, False, 4)
        self.pack_end(self.in_label, False, False, 4)


    def update(self):
        incoming = self.entry_list.get_incoming()
        outgoing = self.entry_list.get_outgoing()
        self.out_label.set_text("In:\t\t" + str(outgoing) + "€")
        self.in_label.set_text("Out:\t\t" + str(incoming) + "€")
        self.comb_label.set_text("Combined:\t" + str(incoming-outgoing) + "€")


class SpendingsList(Gtk.TreeView):
    def __init__(self, entry_list):
        self.entry_list = entry_list
        # convert data to ListStore
        entry_list_store = Gtk.ListStore(float, str)
        for e in entry_list.get_entry_list():
            entry_list_store.append(e.to_list())

        Gtk.TreeView.__init__(entry_list_store)

        for i, col_title in enumerate(["amount", "date"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer)
            self.append_column(column)



class MainWindow(Gtk.Window):

    def __init__(self, entry_list):
        Gtk.Window.__init__(self, title="Bilanz")
        self.set_default_size(400, 600)
        self.connect("destroy", Gtk.main_quit)
        grid = Gtk.Grid()
        grid.set_row_spacing(4)
        grid.set_column_spacing(5)
        self.add(grid)
        self.entry_list = entry_list

        entry_list_store = Gtk.ListStore(float, str)
        for e in entry_list.get_entry_list():
            entry_list_store.append(e.to_list())
        self.entries = Gtk.TreeView(entry_list_store)

        for i, col_title in enumerate(["amount", "date"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            self.entries.append_column(column)

        self.top_label = GoalStats()
        self.general_stats_label = GeneralStats(entry_list)

        #entry_add pane
        self.add_grid = Gtk.Grid()
        self.add_grid.set_row_spacing(3)
        self.add_grid.set_column_spacing(3)
        self.input_label = Gtk.Label("Type: ")
        self.amount_label = Gtk.Label("Amount: ")
        self.date_label = Gtk.Label("Date: ")
        self.comment_label = Gtk.Label("Comment: ")
        self.input_type = Gtk.Switch()
        self.amount_entry = Gtk.Entry()
        self.date_entry = Gtk.Entry()
        self.comment_entry = Gtk.Entry()
        self.button = Gtk.Button(label="Add Entry")
        self.button.connect("clicked", self.on_button_clicked)
        self.add_grid.attach(self.input_label, 0, 0, 1, 1)
        self.add_grid.attach(self.amount_label, 0, 1, 1, 1)
        self.add_grid.attach(self.date_label, 0, 2, 1, 1)

        self.add_grid.attach(self.input_type, 1, 0, 1, 1)
        self.add_grid.attach(self.amount_entry, 1, 1, 1, 1)
        self.add_grid.attach(self.date_entry, 1, 2, 1, 1)

        self.add_grid.attach(self.comment_label, 2, 0, 2, 1)
        self.add_grid.attach(self.comment_entry, 2, 1, 2, 2)

        self.add_grid.attach(self.button, 4, 2, 1, 1)

        grid.attach(self.top_label, 0, 0, 3, 1)
        sep1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(sep1, 0, 1, 3, 1)
        grid.attach(self.general_stats_label, 0, 2, 1, 2)
        grid.attach(self.entries, 1, 2, 2, 2)
        sep2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        grid.attach(sep2, 0, 4, 3, 1)
        grid.attach(self.add_grid, 0, 5, 3, 1)

    def on_button_clicked(self, widget):
        new_amount = float(self.amount_entry.get_text())
        new_date = self.date_entry.get_text()
        new_comment = self.comment_entry.get_text()
        new_entry = Entry(self.input_type.get_active(), new_amount, new_date, new_comment)
        self.entry_list.add_entry(new_entry)
        self.entries = SpendingsList(self.entry_list)
        print("Added " + str(new_amount) + " to list")
        self.amount_entry.set_text("")
        self.date_entry.set_text("")
        self.comment_entry.set_text("")
        self.general_stats_label.update()
        self.entry_list.store_in_json()


class Entry:
    def __init__(self, dire, amount, date_string, comment_string):
        self.dire = dire
        self.amount = amount
        self.date_string = date_string
        self.comment_string = comment_string

    def to_list(self):
        out = []
        out.append(self.amount)
        out.append(self.date_string)
        return out


class EntryList:
    def __init__(self):
        self.entrylist = []
        self.goal = 0
        self.init_from_json()

    def init_from_json(self):
        try:
            f = open("ser.json", 'r')
            in_dict = json.load(f)
            f.close()
            self.goal = in_dict['goal']
            entries = in_dict['entrylist']
            for e in entries:
                new_dire = e['type']
                new_amount = e['amount']
                new_date = e['date_string']
                new_comment = e['comment_string']
                self.entrylist.append(Entry(new_dire, new_amount, new_date, new_comment))
        except:
            pass

    def store_in_json(self):
        serialized_list = []
        for e in self.entrylist:
            sobj = {}
            sobj['type'] = e.dire
            sobj['amount'] = e.amount
            sobj['date_string'] = e.date_string
            sobj['comment_string'] = e.comment_string
            serialized_list.append(sobj)

        obj = {'goal': self.goal, 'entrylist': serialized_list}
        f = open("ser.json", 'w')
        json.dump(obj, f)
        f.close()


    def get_incoming(self):
        result = 0
        for e in self.entrylist:
            if(e.dire):
                result += e.amount
        return result

    def get_outgoing(self):
        result = 0
        for e in self.entrylist:
            if(not e.dire):
                result += e.amount
        return result

    def add_entry(self, entry):
        self.entrylist.append(entry)

    def get_entry_list(self):
        return self.entrylist

    def get_entry_boxes(self):
        result = []
        for e in self.entrylist:
            result.append(EntryBox(e.dire, e.amount, e.date_string))
        return result


entries = EntryList()

win = MainWindow(entries)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
