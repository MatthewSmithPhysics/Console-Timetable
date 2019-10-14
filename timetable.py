import numpy
import tabulate

class Console:
    def __init__(self):
        self.reset()
        self.COMM = {
            "exit": exit,
            "set": self.timetable.set,
            "multiset": self.timetable.multiset,
            "erase": self.timetable.erase,
            "multierase": self.timetable.multierase,
            "create": self.timetable.create,
            "show": self.timetable.show,
            "read": self.read,
            "save": self.save,
            "reset": self.reset,
            "export": self.timetable.export,
            "load": self.load,
            "html": self.timetable.html,
            "superHTML": self.timetable.superHTML,
            "trash": self.timetable.trash,
            "edit": self.timetable.edit,
            "conceive": self.timetable.conceive,
            "conceiveDir": self.timetable.conceiveDir,
            "note": self.timetable.note,
            "multinote": self.timetable.multinote
        }
        return
    def reset(self):
        self.timetable = Timetable()
        self.history = []
        return
    def start(self):
        while(True):
            line = input(">> ")
            self.parse(line)
        return
    def parse(self, line):
        if(line.replace(" ", "") == ""): return
        words = line.split(" ")
        for i in range(len(words)): words[i] = words[i].replace(" ", "")
        command = self.COMM[words[0]]
        #print("Command: {}".format(words[0]))
        #print("Arguments: {}".format(words[1:]))
        try:
            if(len(words) == 1): command()
            else: command(words[1:])
            self.history.append(line)
        except Exception as ex:
            print("There has been an error: {}".format(ex))
        return
    def read(self, args):
        filename = "{}.stt".format(args[0])
        source = open(filename, "r")
        for line in source:
            print(">> {}".format(line[:(len(line)-1)]))
            self.parse(line[:(len(line)-1)])
        source.close()
        return
    def load(self, args):
        filename = "{}.scls".format(args[0])
        data = numpy.loadtxt(filename, delimiter = ",", dtype = str)
        for cls in data:
            self.timetable.createDir(cls[0], cls[1], cls[2], cls[3], cls[4])
        return
    def save(self, args):
        filename = "{}.stt".format(args[0])
        output = open(filename, "w")
        for line in self.history:
            output.write("{}\n".format(line))
        output.close()
        return

class Timetable:
    def __init__(self):
        self.sched = []
        self.event = []
        self.dayName = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.complimentary = {
            "white": "black",
            "silver": "black",
            "gray": "black",
            "black": "white",
            "red": "white",
            "maroon": "white",
            "yellow": "black",
            "olive": "white",
            "lime": "black",
            "green": "white",
            "aqua": "black",
            "teal": "white",
            "blue": "white",
            "navy": "white",
            "fuchsia": "black",
            "purple": "white",
            "#ff7000": "black",
            "#703100": "white"
        }
        self.conv = {
            "orange": "#ff7000",
            "brown": "#703100"
        }
        self.form = {}
        self.form["free"] = Session("", "", "", "white")
        self.form["none"] = Event("")
        for i in range(52):
            s_table = []
            e_table = []
            for j in range(24):
                s_row = []
                e_row = []
                s_row.append("{}:00".format(j))
                for k in range(7): 
                    s_row.append(self.form["free"])
                    e_row.append(self.form["none"])
                s_table.append(s_row)
                e_table.append(e_row)
            self.sched.append(s_table)
            self.event.append(e_table)
        return
    def create(self, args):
        abrv = args[0]
        name = input("Name: ")
        lect = input("Lecturer: ")
        room = input("Room: ")
        col = input("Colour: ")
        newForm = Session(name, lect, room, col)
        self.form[abrv] = newForm
        return
    def conceive(self, args):
        abrv = args[0]
        name = input("Name: ")
        newEvent = Event(name)
        self.form[abrv] = newEvent
        return
    def note(self, args):
        session = args[0]
        week = int(args[1])
        day = self.dayName.index(args[2])
        time = int(args[3])
        self.event[week - 1][time][day] = self.form[session]
        return
    def multinote(self, args):
        ev = args[0]
        weekmin = int(args[1])
        weekmax = int(args[2])
        weekinc = int(args[3])
        for n in range(weekmin, weekmax + 1, weekinc): self.note([ev, n, day, time])
        return
    def trash(self, args):
        abrv = args[0]
        self.form.pop(abrv, None)
        return
    def edit(self, args):
        abrv = args[0]
        resp = input("Current Name: {}. Edit? (y/n): ".format(self.form[abrv].name))
        if(resp in ["y", "Y"]): self.form[abrv].name = input("New Name: ")
        resp = input("Current Lecturer: {}. Edit? (y/n): ".format(self.form[abrv].lect))
        if(resp in ["y", "Y"]): self.form[abrv].lect = input("New Lecturer: ")
        resp = input("Current Room: {}. Edit? (y/n)".format(self.form[abrv].room))
        if(resp in ["y", "Y"]): self.form[abrv].room = input("New Room: ")
        resp = input("Current Colour: {}. Edit? (y/n): ".format(self.form[abrv].lect))
        if(resp in ["y", "Y"]): self.form[abrv].col = input("New Colour: ")
        return
    def createDir(self, abrv, name, lect, room, col):
        newForm = Session(name, lect, room, col)
        print("[Creating {}]".format(abrv))
        self.form[abrv] = newForm
        return
    def conceiveDir(self, abrv, name):
        newForm = Event(name)
        print("[Creating {}]".format(abrv))
        self.form[abrv] = newForm
        return
    def set(self, args):
        session = args[0]
        week = int(args[1])
        day = self.dayName.index(args[2]) + 1
        time = int(args[3])
        if(self.sched[week - 1][time][day] != self.form["free"]):
            occ = self.sched[week - 1][time][day]
            resp = input("Overwrite '{}' for week {} on {} at {}:00?".format(occ.name, week, args[1], time))
            if(resp not in ["Y", "y"]): return
        self.sched[week - 1][time][day] = self.form[session]
        return
    def erase(self, args):
        week = int(args[0])
        day = self.dayName.index(args[1]) + 1
        time = int(args[2])
        self.sched[week - 1][time][day] = self.form["free"]
        return
    def multiset(self, args):
        session = args[0]
        wmin = int(args[1])
        wmax = int(args[2])
        winc = int(args[3])
        day = args[4]
        time = args[5]
        for n in range(wmin, wmax + 1, winc): self.set([session, n, day, time])
        return
    def multierase(self, args):
        wmin = int(args[0])
        wmax = int(args[1])
        day = args[2]
        time = args[3]
        for n in range(wmin, wmax + 1): self.erase([n, day, time])
        return
    def show(self, args):
        week = int(args[0])
        dmin = self.dayName.index(args[1]) + 1
        dmax = self.dayName.index(args[2]) + 1
        tmin = int(args[3])
        tmax = int(args[4])
        subtable = []
        for i in range(tmin, tmax):
            row = [self.sched[week - 1][i][0]]
            for j in range(dmin, dmax + 1):
                entry = self.sched[week - 1][i][j]
                ev = self.event[week - 1][i][j - 1]
                row.append("{}\n{}\t{}\n{}".format(entry.name, entry.lect, entry.room, ev.name))
            subtable.append(row)
        head = ["Time"]
        for day in range(dmin, dmax + 1):
            head.append(self.dayName[day - 1])
        display = tabulate.tabulate(subtable, headers = head, tablefmt="grid")
        print(display)
    def export(self, args):
        week = int(args[0])
        dmin = self.dayName.index(args[1]) + 1
        dmax = self.dayName.index(args[2]) + 1
        tmin = int(args[3])
        tmax = int(args[4])
        filename = "{}.txt".format(args[5])
        subtable = []
        for i in range(tmin, tmax):
            row = [self.sched[week - 1][i][0]]
            for j in range(dmin, dmax + 1):
                entry = self.sched[week - 1][i][j]
                ev = self.event[week - 1][i][j - 1]
                row.append("{}\n{}\t{}\n{}".format(entry.name, entry.lect, entry.room, ev.name))
            subtable.append(row)
        head = ["Time"]
        for day in range(dmin, dmax + 1):
            head.append(self.dayName[day - 1])
        display = tabulate.tabulate(subtable, headers = head, tablefmt="grid")
        output = open(filename, "w")
        output.write(display)
        output.close()
        return
    def html(self, args):
        week = int(args[0])
        dmin = self.dayName.index(args[1]) + 1
        dmax = self.dayName.index(args[2]) + 1
        tmin = int(args[3])
        tmax = int(args[4])
        filename = "{}.html".format(args[5])
        subtable = []
        colours = []
        for i in range(tmin, tmax):
            row = [self.sched[week - 1][i][0]]
            colrow = ["silver"]
            for j in range(dmin, dmax + 1):
                entry = self.sched[week - 1][i][j]
                ev = self.event[week - 1][i][j - 1]
                row.append(entry.name + "<br>" + entry.room + "&emsp;" + entry.lect + "<br><strong>" + ev.name + "</strong>")
                colrow.append(entry.col)
            subtable.append(row)
            colours.append(colrow)
        head = ["Time"]
        for day in range(dmin, dmax + 1):
            head.append(self.dayName[day - 1])
        output = open(filename, "w")
        output.write("<html>\n\t<h1>{}</h1>\n\t<table style='width:100%; border: 1px solid black'>\n\t\t<tr>".format(args[5]))
        for h in head:
            output.write("\n\t\t\t<th style='border: 1px solid black; background-color: silver'>{}</th>".format(h))
        output.write("\n\t\t</tr>")
        for row in subtable:
            output.write("\n\t\t<tr>")
            for entry in row:
                col = "white"
                if(colours[i][j] in self.conv):
                    col = self.conv[colours[i][j]]
                elif(colours[i][j] in self.complimentary): col = colours[i][j]
                comp = self.complimentary[col]
                output.write("\n\t\t\t<td style='border: 1px solid black; background-color: {}; color: '>{}</td>".format(col, comp, entry))
            output.write("\n\t\t</tr>")
        output.write("\n\t</table>\n</html>")
        output.close()
        return
    def superHTML(self, args):
        weekmin = int(args[0])
        weekmax = int(args[1])
        dmin = self.dayName.index(args[2]) + 1
        dmax = self.dayName.index(args[3]) + 1
        tmin = int(args[4])
        tmax = int(args[5])
        folder = args[6]
        fileroot = args[7]
        for week in range(weekmin, weekmax + 1):
            subtable = []
            colours = []
            for i in range(tmin, tmax):
                row = [self.sched[week - 1][i][0]]
                colrow = ["silver"]
                for j in range(dmin, dmax + 1):
                    entry = self.sched[week - 1][i][j]
                    ev = self.event[week - 1][i][j - 1]
                    row.append(entry.name + "<br>" + entry.room + "&emsp;" + entry.lect + "<br><strong>" + ev.name + "</strong>")
                    colrow.append(entry.col)
                subtable.append(row)
                colours.append(colrow)
            head = ["Time"]
            for day in range(dmin, dmax + 1):
                head.append(self.dayName[day - 1])
            output = open("{}/{}_{}.html".format(folder, fileroot, week), "w")
            output.write("<html>\n\t<h1>{}- Week {}</h1><table style='width:100%; border: 1px solid black'>\n\t\t<tr>".format(fileroot, week))
            for h in head:
                output.write("\n\t\t\t<th style='border: 1px solid black;  background-color: silver'>{}</th>".format(h))
            output.write("\n\t\t</tr>")
            i = 0
            for row in subtable:
                j = 0
                output.write("\n\t\t<tr>")
                for entry in row:
                    col = "white"
                    if(colours[i][j] in self.conv):
                        col = self.conv[colours[i][j]]
                    elif(colours[i][j] in self.complimentary): col = colours[i][j]
                    comp = self.complimentary[col]
                    output.write("\n\t\t\t<td style='border: 1px solid black; background-color: {}; color: {}'>{}</td>".format(col, comp, entry))
                    j = j + 1
                output.write("\n\t\t</tr>")
                i = i + 1
            output.write("\n\t</table>")
            if(week != 1):
                output.write("\n\t<button onclick=\"window.location.href={}\">Previous Week</button>".format("'{}_{}.html'".format(fileroot, week - 1)))
            if(week != 52):
                output.write("\n\t<button onclick=\"window.location.href={}\">Next Week</button>".format("'{}_{}.html'".format(fileroot, week + 1)))
            output.write("\n</html>")
            output.close()

class Session:
    def __init__(self, name, lect, room, col):
        self.name = name
        self.lect = lect
        self.room = room
        self.col = col
      
class Event:
    def __init__(self, name):
        self.name = name

if __name__ == "__main__":
  console = Console()
  console.start()
