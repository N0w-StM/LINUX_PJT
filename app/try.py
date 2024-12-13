import tkinter as tk
import functools
import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import sqlite3
#conn = sqlite3.connect('Eplois.db')
#cursor = conn.cursor()
#cursor.execute('''CREATE TABLE IF NOT EXISTS Gen
#                  (fil TEXT,day TEXT, time TEXT, course TEXT, prof TEXT, salle TEXT)''')
#conn.commit()

class Course:
    def __init__(self, name, prof,salle,duree):
        self.name = name
        self.prof = prof
        self.salle = salle
        self.duree = duree
        self.assigned_slots = []

class Prof:
    def __init__(self, name):
        self.name = name
        self.available_slots = []

class Salle:
    def __init__(self, name):
        self.name = name
        self.available_slots = []

class TimeSlot:
    def __init__(self, day, time):
        self.day = day
        self.time = time
        self.is_occupied = False

def gen_emp(courses, professors, rooms, timeslots):
    timetable = {}

    for course in courses:
        available_slots_for_course = []

        for slot in timeslots:
            if not slot.is_occupied:
                prof = course.prof
                salle = course.salle

                if prof.name not in [c.prof.name for c, slots in timetable.items() for s in slots if s.day == slot.day and s.time == slot.time] and \
                   salle.name not in [c.salle.name for c, slots in timetable.items() for s in slots if s.day == slot.day and s.time == slot.time]:

                    available_slots_for_course.append(slot)

        if available_slots_for_course:
            slot_count = 0
            while slot_count < 2:
                chosen_slot = random.choice(available_slots_for_course)
                if not chosen_slot.is_occupied:
                    timetable.setdefault(course, []).append(chosen_slot)
                    chosen_slot.is_occupied = True
                    prof.available_slots.append(chosen_slot)
                    salle.available_slots.append(chosen_slot)
                    slot_count += 1
                    available_slots_for_course.remove(chosen_slot)
    return timetable
def Main_emp():
    root.title("Sim@Zinder_hs")
    new_btn = tk.Button(root,text="New Emp",command=Cr_new)
    new_btn.pack()
    rem_btn = tk.Button(root,text="Remove",command=Rem_db)
    rem_btn.pack()
def Cr_new():
    new_win = tk.Toplevel(root)
    new_win.title("Generate an EMP")

    course_label = tk.Label(new_win, text="Courses (separated by newline):")
    course_label.pack()
    course_entry = tk.Text(new_win, height=3, width=30)
    course_entry.pack()
    prof_label = tk.Label(new_win, text="Professors (separated by newline):")
    prof_label.pack()
    prof_entry = tk.Text(new_win, height=3, width=30)
    prof_entry.pack()
    salle_label = tk.Label(new_win, text="Rooms (separated by newline):")
    salle_label.pack()
    salle_entry = tk.Text(new_win, height=3, width=30)
    salle_entry.pack()
    cours = course_entry.get("1.0", tk.END).splitlines()
    prof = prof_entry.get("1.0", tk.END).splitlines()
    salle = salle_entry.get("1.0", tk.END).splitlines()
    make_btn = tk.Button(new_win, text="MAKE", command=lambda: Make_emp([course_entry.get("1.0", tk.END).splitlines(),prof_entry.get("1.0", tk.END).splitlines(),salle_entry.get("1.0", tk.END).splitlines()]))
    make_btn.pack()
def Make_emp(data):
    cr,pr,sl = data
    print(cr, pr, sl)
    timeslots = [
        TimeSlot("Monday", "8:30"),
        TimeSlot("Monday", "10:30"),
        TimeSlot("Monday", "14:00"),
        TimeSlot("Monday", "16:00"),
        TimeSlot("Tuesday", "8:30"),
        TimeSlot("Tuesday", "10:30"),
        TimeSlot("Tuesday", "14:00"),
        TimeSlot("Tuesday", "16:00"),
        TimeSlot("Wednesday", "8:30"),
        TimeSlot("Wednesday", "10:30"),
        TimeSlot("Wednesday", "14:00"),
        TimeSlot("Wednesday", "16:00"),
        TimeSlot("Thursday", "8:30"),
        TimeSlot("Thursday", "10:30"),
        TimeSlot("Thursday", "14:00"),
        TimeSlot("Thursday", "16:00"),
        TimeSlot("Friday", "8:30"),
        TimeSlot("Friday", "10:30"),
        TimeSlot("Friday", "14:00"),
        TimeSlot("Friday", "16:00"),
        TimeSlot("Saturday", "8:30"),
        TimeSlot("Saturday", "10:30")
            ]
    print(cr,pr,sl)
    salle = []
    prof = []
    cours = []
    for s in sl:
        salle.append(Salle(s))
    for p in pr:
        prof.append(Prof(p))
    for c in cr:
        cours.append(Course(c,random.choice(prof),random.choice(salle),4))
    Gen_EMP = gen_emp(cours, prof, salle, timeslots)
    gen_pdf(Gen_EMP)
def gen_pdf(timetable):
    pdf = SimpleDocTemplate("EST_EMP.pdf", pagesize=letter)

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Weekly Timetable", styles['h1']))
    story.append(Spacer(1, 12))

    table_data = [["Course", "Professor", "Room", "Day", "Time"]]
    for course, slots in timetable.items():
        for slot in slots:
            table_data.append([course.name, course.prof.name, course.salle.name, slot.day, slot.time])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    story.append(table)
    pdf.build(story)
def Rem_db():
    print("hello")
root = tk.Tk()
my_gui = Main_emp()
root.mainloop()