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
            "edit": self.timetable.edit
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
            self.timetable.createDir(cls[0], cls[1], cls[2], cls[3])
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
        self.dayName = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.form = {}
        self.form["Free"] = Form("", "", "")
        for i in range(52):
            table = []
            for j in range(24):
                row = []
                row.append("{}:00".format(j))
                for k in range(7): row.append(self.form["Free"])
                table.append(row)
            self.sched.append(table)
        return
    def create(self, args):
        abrv = args[0]
        name = input("Name: ")
        lect = input("Lecturer: ")
        room = input("Room: ")
        newForm = Form(name, lect, room)
        self.form[abrv] = newForm
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
        return
    def createDir(self, abrv, name, lect, room):
        newForm = Form(name, lect, room)
        print("[Creating {}]".format(abrv))
        self.form[abrv] = newForm
        return
    def set(self, args):
        session = args[0]
        week = int(args[1])
        day = self.dayName.index(args[2]) + 1
        time = int(args[3])
        self.sched[week - 1][time][day] = self.form[session]
        return
    def erase(self, args):
        week = int(args[0])
        day = self.dayName.index(args[1]) + 1
        time = int(args[2])
        self.sched[week - 1][time][day] = self.form["Free"]
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
                row.append("{}\n{}\t{}".format(entry.name, entry.lect, entry.room))
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
                row.append(entry.name + "\n" + entry.room + "\t" + entry.lect)
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
        for i in range(tmin, tmax):
            row = [self.sched[week - 1][i][0]]
            for j in range(dmin, dmax + 1):
                entry = self.sched[week - 1][i][j]
                row.append(entry.name + "<br>" + entry.room + "&emsp;" + entry.lect)
            subtable.append(row)
        head = ["Time"]
        for day in range(dmin, dmax + 1):
            head.append(self.dayName[day - 1])
        output = open(filename, "w")
        output.write("<html>\n\t<h1>{}</h1>\n\t<table style='width:100%; border: 1px solid black'>\n\t\t<tr>".format(args[5]))
        for h in head:
            output.write("\n\t\t\t<th style='border: 1px solid black'>{}</th>".format(h))
        output.write("\n\t\t</tr>")
        for row in subtable:
            output.write("\n\t\t<tr>")
            for entry in row:
                output.write("\n\t\t\t<td style='border: 1px solid black'>{}</td>".format(entry))
            output.write("\n\t\t</tr>")
        output.write("\n\t</table>\n</html>")
        output.close()
        return
    def superHTML(self, args):
        dmin = self.dayName.index(args[0]) + 1
        dmax = self.dayName.index(args[1]) + 1
        tmin = int(args[2])
        tmax = int(args[3])
        fileroot = args[4]
        for week in range(1, 53):
            subtable = []
            for i in range(tmin, tmax):
                row = [self.sched[week - 1][i][0]]
                for j in range(dmin, dmax + 1):
                    entry = self.sched[week - 1][i][j]
                    row.append(entry.name + "<br>" + entry.room + "&emsp;" + entry.lect)
                subtable.append(row)
            head = ["Time"]
            for day in range(dmin, dmax + 1):
                head.append(self.dayName[day - 1])
            output = open("{}_{}.html".format(fileroot, week), "w")
            output.write("<html>\n\t<h1>{}- Week {}</h1><table style='width:100%; border: 1px solid black'>\n\t\t<tr>".format(fileroot, week))
            for h in head:
                output.write("\n\t\t\t<th style='border: 1px solid black'>{}</th>".format(h))
            output.write("\n\t\t</tr>")
            for row in subtable:
                output.write("\n\t\t<tr>")
                for entry in row:
                    output.write("\n\t\t\t<td style='border: 1px solid black'>{}</td>".format(entry))
                output.write("\n\t\t</tr>")
            output.write("\n\t</table>")
            if(week != 1):
                output.write("\n\t<button onclick=\"window.location.href={}\">Previous Week</button>".format("'{}_{}.html'".format(fileroot, week - 1)))
            if(week != 52):
                output.write("\n\t<button onclick=\"window.location.href={}\">Next Week</button>".format("'{}_{}.html'".format(fileroot, week + 1)))
            output.write("\n</html>")
            output.close()

class Form:
    def __init__(self, name, lect, room):
        self.name = name
        self.lect = lect
        self.room = room

if __name__ == "__main__":
  console = Console()
  console.start()
