import random,hashlib,re,base64
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtGui import QFont, QPixmap, QColor
import os,platform,time,json
from PyQt5.QtGui import QPixmap, QIcon
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem,QStackedWidget,
    QPushButton, QLineEdit, QListWidget, QLabel, QMessageBox, QComboBox,QListWidgetItem
)
from cryptography.fernet import Fernet
from PyQt5.QtCore import Qt,QTimer
import sqlite3
from PyQt5.QtWidgets import QSizePolicy, QSpacerItem

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.cd_v ="ae84ad74cf546f0d7fede42db2a184055d9930a3c9d3257ecd12883a38aa2bdf"
        if self.dj_act():
            self.go_ad()
        else:
            self.go_act()
    def go_act(self):
        self.setFixedSize(400, 200)
        mLay = QVBoxLayout()
        sLay = QHBoxLayout()
        act = QVBoxLayout()
        actLab = QLabel("   CODE D'ACTIVITATION  ")
        self.actEnt = QLineEdit()
        self.actEnt.setMaxLength(19)
        actBtn = QPushButton("ACTIVATE")
        actBtn.clicked.connect(self.activate)
        
        act.addStretch(1)
        act.addWidget(actLab)
        act.addWidget(self.actEnt)
        act.addWidget(actBtn)
        act.addStretch(1)

        sLay.addStretch(1)
        sLay.addLayout(act)
        sLay.addStretch(1)
        mLay.addLayout(sLay)
        self.setLayout(mLay)
        self.apply_styles()
    def dj_act(self):
        if os.path.exists("info.reg"):
            try:
                with open('info.reg','rb') as dt:
                    enc = dt.read()
                sim = Fernet(base64.urlsafe_b64encode(hashlib.sha256((platform.node() + "ASIMANE3").encode()).digest()))
                dta = json.loads(sim.decrypt(enc).decode())
                if dta['info'] and time.time()<dta['exp'] :
                    return True
            except Exception as er:
                print("[!]activitation echoue",er)
        return False
    def sav_cd(self,exp=3600):
        exprt = time.time()+exp
        dt = {
                'info':True,
                'act':self.cd_v,
                'exp':exprt
                }
        sim = Fernet(base64.urlsafe_b64encode(hashlib.sha256((platform.node() + "ASIMANE3").encode()).digest()))
        enc = sim.encrypt(json.dumps(dt).encode())
        with open('info.reg', 'wb') as file:
            file.write(enc)
        file.close()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: white; font-family: Arial, sans-serif; font-size: 15px; color: #333; }
            QLabel { font-size: 16px; font-weight: bold; color: #2a4d69; padding-bottom: 10px; }
            QLineEdit { padding: 15px; border: 2px solid #a1c4d8; border-radius: 6px; background-color: #f1b223; font-size: 14px; }
            QLineEdit:focus { border-color: #5b9bd5; background-color: #eef8ff; }
            QPushButton { padding: 10px; border: 1px solid #5b9bd5; border-radius: 6px; background-color: blue; color: white; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background-color: #407ec9; border-color: #407ec9; }
            QPushButton:pressed { background-color: #305d93; border-color: #305d93; }
        """)

    def activate(self): 
        code = self.actEnt.text().strip()
        if self.is_valid_code(code):
            QMessageBox.information(self, "Success", "Activation successful!")
            self.sav_cd()
            QTimer.singleShot(3000, self.go_ad)
        else:
            QMessageBox.warning(self, "Code Incorrect", f"Le Code que Vous Avez Entre est incorrect")

    def is_valid_code(self, code):
        if len(code) !=19  or not re.match(r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$", code):
            return False
        st = code.replace("-","")
        hashd = hashlib.sha256(st.encode()).hexdigest() 
        if hashd == self.cd_v:
            return True
        return False
    def go_ad(self):
        self.admin = Admin()
        self.admin.show()
        self.close()
class Admin(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Page")
        self.setFixedSize(800, 500)

        main_layout = QHBoxLayout()

        illustration_layout = QVBoxLayout()
        illustration_widget = QWidget()
        illustration_widget.setStyleSheet("background-color: #007dff; border-top-left-radius: 20px; border-bottom-left-radius: 20px;")

        illustration_label = QLabel()
        illustration_label.setPixmap(QPixmap("est.png").scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        illustration_label.setAlignment(Qt.AlignCenter)

        welcome_text = QLabel("UNIEMP")
        welcome_text.setFont(QFont("serif", 20, QFont.Bold))
        welcome_text.setStyleSheet("color: white;")
        welcome_text.setAlignment(Qt.AlignCenter)

        illustration_layout.addWidget(illustration_label)
        illustration_layout.addWidget(welcome_text)
        illustration_widget.setLayout(illustration_layout)

        main_layout.addWidget(illustration_widget, stretch=1)

        form_widget = QWidget()
        form_widget.setStyleSheet("background-color: white; border-top-right-radius: 10px; border-bottom-right-radius: 10px;")
        form_layout = QVBoxLayout()

        login_header = QLabel("WELCOME")
        login_header.setFont(QFont("Arial", 20, QFont.Bold))
        login_header.setStyleSheet("color: #1A73E8;")
        login_header.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(login_header, alignment=Qt.AlignCenter)

        subtitle = QLabel("UNI-EMP Account")
        subtitle.setFont(QFont("Serif", 16))
        subtitle.setStyleSheet("color:black;font-family: serif;font-size: 25px; text-align:center;")
        subtitle.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        form_fields = QFormLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Nom d'utilisateur")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding:20px; background-color: #d1f4fb; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;
                border: cyan solid;
            }
            QLineEdit:focus {
                border: 3px solid #1A73E8;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Mot de passe")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding:20px; background-color: #d1f4fb; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;
                border: cyan solid;
            }
            QLineEdit:focus {
                border: 3px solid #1A73E8;
            }
        """)
        lab_us = QLabel("Utilisateur")
        lab_us.setStyleSheet("padding:20px; background-color: white; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;")
        form_fields.addRow(lab_us, self.username_input)
        lab_ps = QLabel("Mot de Passe")
        lab_ps.setStyleSheet("padding:20px; background-color: white; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;")
        form_fields.addRow(lab_ps, self.password_input)
        form_layout.addLayout(form_fields)

        login_button = QPushButton("Connect")
        login_button.clicked.connect(self.verify)
        login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7; color: white;font-size:15px;font-weight:bold; padding: 5px; border-radius: 7px; height: 30px;
            }
            QPushButton:hover {
                background-color: #1557A5;
            }
        """)
        form_layout.addWidget(login_button, alignment=Qt.AlignCenter)

        footer_text = QLabel("Powered by @AB_ABIB")
        footer_text.setFont(QFont("Arial", 8))
        footer_text.setStyleSheet("color: #888888;")
        footer_text.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(footer_text, alignment=Qt.AlignCenter)

        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget, stretch=2)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #F1F3F4;
            }
            QLabel {
                color: #2E4053;
            }
        """)
    def verify(self):
        user = self.username_input.text()
        pas = self.password_input.text()

        if user == "admin" and pas == "admin":
            QMessageBox.information(self, "Login Successful", "Welcome!")
            QTimer.singleShot(1000,self.go_gr)
        else:
            QMessageBox.warning(self, "Login Failed", "Votre Nom ou Pass est incorrect")
            self.username_input.clear()
            self.password_input.clear()
    def go_gr(self):
        self.gr = _GEN_gn()
        self.gr.show()
        self.close()
#db
def init_db():
    conn = sqlite3.connect("UNI.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS filliere (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS course (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filliere_id INTEGER,
            name TEXT NOT NULL,
            professor TEXT,
            FOREIGN KEY (filliere_id) REFERENCES filliere (id)
        )
    """)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS days (day TEXT NOT NULL)""")
    cursor.execute(""" CREATE TABLE IF NOT EXISTS rooms (f_id int not null ,room TEXT NOT NULL,FOREIGN KEY (f_id) REFERENCES filliere (id))""")
    try:
        cursor.execute("INSERT INTO filliere VALUES (?,?)",(1,"ALL"))
    except Exception:
        pass
    cursor.execute(""" CREATE TABLE IF NOT EXISTS time (start TEXT NOT NULL,end TEXT NOT NULL)""")
    conn.commit()
    conn.close()
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
class Gen_emp:
    def __init__(self):
        self.Gen = None
    def check_av(self,day, time,var,x):
        conn = sqlite3.connect('UNI.db')
        cursor = conn.cursor()
        if x==1:
            try:
                query = """
            SELECT timeslot FROM timetable
            WHERE day = ? AND prof_name = ?
            """
                cursor.execute(query, (day, var))
                full_time = cursor.fetchall()
            except Exception :
                pass
        else:
            try:
                query = """
                SELECT timeslot FROM timetable
                WHERE day = ? AND room = ?
                """
                cursor.execute(query, (day, var))
                full_time = cursor.fetchall()
            except Exception:
                pass
        cursor.close()
        conn.close()
        for (full_time,) in full_time:
            if time == full_time:
                return False

        return True
    def save_tm(self,f_id):
        conn = sqlite3.connect("UNI.db")
        cursor = conn.cursor()
        if not self.Gen:
            QMessageBox.warning(None, "Warning", "No timetable data to save.")
            return

        try:
            for course, slots in self.Gen.items():
                prof_name = course.prof.name
                room = course.salle.name
                for slot in slots:
                    day = slot.day
                    timeslot = slot.time
                    cursor.execute("INSERT INTO timetable (f_id,prof_name, day, timeslot, room) VALUES (?,?, ?, ?, ?)", (f_id,prof_name, day, timeslot, room))
                    conn.commit()
        except (Exception, TypeError) as e:
            conn.rollback()
            QMessageBox.critical(None, "Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()
    def gen_emp(self, courses, professors, rooms, timeslots):
        timetable = {}
        for course in courses:
            available_slots_for_course = []

            for slot in timeslots:
                if not slot.is_occupied:
                    prof = course.prof
                    salle = course.salle

                    in_memory_prof_check = prof.name not in [
                        c.prof.name for c, slots in timetable.items()
                        for s in slots if s.day == slot.day and s.time == slot.time
                    ]
                    in_memory_room_check = salle.name not in [
                        c.salle.name for c, slots in timetable.items()
                        for s in slots if s.day == slot.day and s.time == slot.time
                    ]

                    db_prof_available = self.check_av(slot.day, slot.time, prof.name, 1)
                    db_room_available = self.check_av(slot.day, slot.time, salle.name, 0)

                    if in_memory_prof_check and in_memory_room_check and db_prof_available and db_room_available:
                        available_slots_for_course.append(slot)

            if available_slots_for_course:
                slot_count = 0
                while slot_count < 2 and available_slots_for_course:
                    chosen_slot = random.choice(available_slots_for_course)
                    if not chosen_slot.is_occupied:
                        timetable.setdefault(course, []).append(chosen_slot)
                        chosen_slot.is_occupied = True
                        prof.available_slots.append(chosen_slot)
                        salle.available_slots.append(chosen_slot)
                        slot_count += 1
                        available_slots_for_course.remove(chosen_slot)

        return timetable
    def gen_pdf(self, timetable,fill_name):
        conn = sqlite3.connect("UNI.db")
        cursor = conn.cursor()
        pdf = SimpleDocTemplate("./EMP/"+fill_name+".pdf", pagesize=letter)
        tit = "Emploi du Temps :"+fill_name
        styles = getSampleStyleSheet()
        story = []
        title = Paragraph(tit, styles['Title'])
        story.append(title)
        story.append(Spacer(1, 20))
        times = []
        cursor.execute("SELECT start,end FROM time")
        tal = cursor.fetchall()
        tm_s = [row[0] for row in tal]
        tm_e = [row[1] for row in tal]
        for i in range(len(tm_s)):
            atx = tm_s[i]+" ➔ "+tm_e[i]
            times.append(atx)
        cursor.execute("SELECT day from days")
        days = [row[0] for row in cursor.fetchall()]
        table_data = [[""] + times] 
        grid = [[None for _ in times] for _ in days]
        for course, slots in timetable.items():
            for slot in slots:
                day_idx = days.index(slot.day)
                time_idx = None
                for tm in tm_s:
                    if slot.time == tm:
                        time_idx = tm_s.index(tm)
                        break
                if time_idx is not None and grid[day_idx][time_idx] is None:
                    cell_content = f"{course.name}\n{course.prof.name}\n{course.salle.name}"
                    grid[day_idx][time_idx] = cell_content
        for day_idx, day in enumerate(days):
            row = [day]
            for time_idx in range(len(times)):
                cell_content = grid[day_idx][time_idx] if grid[day_idx][time_idx] else ""
                row.append(cell_content)
            table_data.append(row)
        #Design d Table
        table = Table(table_data, colWidths=[90] + [120] * len(times))
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgreen), 
            ('BACKGROUND', (0, 1), (0, -1), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 6), 
            ('BACKGROUND', (1, 1), (-1, -1), colors.beige), 
        ]))
        conn.close()
        story.append(table)
        pdf.build(story)
    def check(self):
        try:
            conn = sqlite3.connect("UNI.db")
            cursor = conn.cursor()
            required_tables = {
                "rooms": "Please enregistre les salles",
                "course": "Please enregistre les  filliers",
                "days": "Please enregistre les jours",
                "time": "Please enregistre les times"}
            for table, message in required_tables.items():
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count == 0:
                    QMessageBox.critical(None, "Error", message)
                    return False
            return True
        finally:
            if conn:
                conn.close()

    def Make_emp(self):
        #3andak nenssa nakhod l f
        if not self.check():
            return 0
        else:
            conn = sqlite3.connect("UNI.db")
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS timetable (id INTEGER PRIMARY KEY AUTOINCREMENT,f_id INT NOT NULL,prof_name TEXT,day TEXT,timeslot TEXT,room TEXT,FOREIGN KEY (f_id) REFERENCES filliere (id))")
        try:
            timeslots =[]
            cursor.execute("SELECT id, name FROM filliere WHERE id !=1")
            rows = cursor.fetchall()
            fid = [row[0] for row in rows]
            fil = [row[1] for row in rows]
            cursor.execute("SELECT start from time")
            time = [row[0] for row in cursor.fetchall()]
            cursor.execute("SELECT day from days")
            days = [row[0] for row in cursor.fetchall()]
            for d in days:
                for t in time:
                    timeslots.append(TimeSlot(d,t))
            for fi,name in zip(fid,fil):
                try:
                    cursor.execute(f"DELETE FROM timetable WHERE f_id={fi}")
                except Exception:
                    pass
                cursor.execute(f"SELECT name,professor FROM course WHERE filliere_id ={fi}")
                rows = cursor.fetchall()
                crs = [row[0] for row in rows]
                prf = [row[1] for row in rows]
                prof = [Prof(p) for p in prf]
                cours=[]
                salle =[]
                try:
                    cursor.execute(f"SELECT room FROM rooms WHERE f_id ={fi}")
                    if cursor.fetchone()[0] != 0:
                        rooms = [row[0] for row in cursor.fetchall()]
                    else:
                        return Exception
                except Exception:
                    cursor.execute("SELECT room FROM rooms WHERE f_id =1")
                    rooms = [row[0] for row in cursor.fetchall()]
                for s in rooms:
                    salle.append(Salle(s))
                for i,c in enumerate(crs):
                    cours.append(Course(c,prof[i % len(prof)],salle[i % len(salle)],4))
                try:
                    if cours and prof and salle and timeslots:
                        self.Gen = self.gen_emp(cours, prof, salle, timeslots)
                except Exception as e:
                     print(f"Error emp: {e}")
                try:
                    self.gen_pdf(self.Gen,name)
                except Exception as e:
                    print(f"Error generating PDF: {e}")
                conn.close()
                self.save_tm(fi)
                conn = sqlite3.connect("UNI.db")
                cursor = conn.cursor()
                QMessageBox.information(None, "Success", "Les Emplois sont Enregistre")
        except Exception as er:
            print(er,"Please Contact Mr.Z")

        conn.close()
class _GEN_gn(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UNIEMP")
        self.setGeometry(100, 100, 800, 500)
        init_db()
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.unwtd = ['-',',','/','\n','\t','\r','\a','\\']
        header = QLabel("UNIEMP")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("background: rgb(14,0,240);color: white;padding: 20px; font-weight:bold;letter-spacing:5px; font-size: 35px;border-radius:15px; font-family:serif;")
        main_layout.addWidget(header)
        #n9essmo page
        content_layout = QHBoxLayout()
        left_sidebar = QVBoxLayout()
        left_sidebar.setSpacing(20)
        # Btn
        days_button = QPushButton("JOURS")
        timeslots_button = QPushButton("TIMESLOTS")
        filliere_button = QPushButton("FILLIERE")
        rooms_button = QPushButton("SALLE")
        for btn in (days_button, timeslots_button, filliere_button, rooms_button):
            btn.setFixedHeight(50)
            btn.setStyleSheet("background-color: #23ABEF;font-weight:bold;padding: 10px; border-radius: 15px; color: white;font-size:20px;font-family:serif;")
            left_sidebar.addWidget(btn)
        gen_btn = QPushButton("GENERATE")
        gen_btn.setFixedHeight(50)
        gen_btn.setStyleSheet("background: #190482;color: white;padding: 10px; font-weight:bold; font-size: 30px;border-radius:15px; font-family:serif;")
        left_sidebar.addWidget(gen_btn)
        right_content = QVBoxLayout()
        self.stack = QStackedWidget()
        #les pg
        self.day_pg = self.day_pg()
        self.time_pg = self.time_pg()
        self.room_pg = self.room_pg()
        self.filliere_page = self.create_filliere_page()
        self.stack.addWidget(self.day_pg)
        self.stack.addWidget(self.time_pg)
        self.stack.addWidget(self.room_pg)
        self.stack.addWidget(self.filliere_page)
        right_content.addWidget(self.stack)
        #bg d left side
        left_sidebar_widget = QWidget()
        left_sidebar_widget.setLayout(left_sidebar)
        left_sidebar_widget.setStyleSheet("background-color:#3672EF;border-top-left-radius:10px; border-bottom-left-radius:10px;")#
        content_layout.addWidget(left_sidebar_widget, 1)
        content_layout.addLayout(right_content, 2)
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
        #BTN
        gen_btn.clicked.connect(self.gen_btn_cl)
        days_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.day_pg))
        timeslots_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.time_pg))
        filliere_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.filliere_page))
        rooms_button.clicked.connect(lambda: self.stack.setCurrentWidget(self.room_pg))

    def gen_btn_cl(self):
        Gen = Gen_emp()
        Gen.Make_emp()
    def create_filliere_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.filliere_name_input = QLineEdit()
        self.filliere_name_input.setPlaceholderText("Fillier : salle,salle,...")
        self.filliere_name_input.setStyleSheet("padding:20px; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;background-color: #cce6ff;")
        self.course_name_input = QLineEdit()
        self.course_name_input.setPlaceholderText("Enter course name")
        self.professor_name_input = QLineEdit()
        self.professor_name_input.setPlaceholderText("Enter professor name")
        self.course_name_input.setStyleSheet("padding:20px; background-color: white; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;")
        self.professor_name_input.setStyleSheet("padding:20px; background-color: white; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;")
        self.course_list = QListWidget()
        self.course_list.setStyleSheet("background-color: #F1F6F9; padding: 20px; border: 5px solid #ddd;font-size: 30px;font-family:monospace;font-weight:medium; ")
        add_course_btn = QPushButton("ADD")
        add_course_btn.setStyleSheet("background-color: #0078d7; color: white;font-weight:bold;font-size:15px; padding: 5px; border-radius: 7px; height: 30px;")
        add_course_btn.clicked.connect(self.add_course)
        update_course_btn = QPushButton("UPDATE")
        update_course_btn.setStyleSheet("background-color: #ffae42; color: white;font-weight:bold; padding: 5px;font-size:20px; border-radius: 5px;height: 25px;font-family:serif;")
        update_course_btn.clicked.connect(self.update_cr)
        save_filliere_btn = QPushButton("SAVE FILLIERE")
        save_filliere_btn.setStyleSheet("background-color: #28a745;font-family:serif;font-weight:bold; color: white; padding: 10px; border-radius: 5px;font-size:20px")
        save_filliere_btn.clicked.connect(self.save_fill)
        self.fill = QLabel("Nom et Salles du Fillier")
        self.cr_pr= QLabel("Cour et Prof")
        self.cr_pr.setStyleSheet("color:black;font-family: serif; font-weight: 10px;font-size: 15px; text-align:center;")
        self.fill.setStyleSheet("color:black;font-family: serif;font-size: 25px; text-align:center;")
        layout.addWidget(self.fill)
        layout.addWidget(self.filliere_name_input)
        layout.addWidget(self.cr_pr)
        layout.addWidget(self.course_name_input)
        layout.addWidget(self.professor_name_input)
        layout.addWidget(add_course_btn)
        layout.addWidget(self.course_list)
        layout.addWidget(update_course_btn)
        layout.addWidget(save_filliere_btn)
        self.course_list.itemDoubleClicked.connect(lambda item:self.load_ed(item,3))
        page.setLayout(layout)
        return page

    def add_course(self):
        cours = self.course_name_input.text().strip()
        prof = self.professor_name_input.text().strip()
        if cours and prof:
            if "-" in cours:
                cours = cours.replace("-",".")
            if "." in prof:
                prof= prof.replace("-",".")
            item_text = f"{cours} - {prof}"
            self.course_list.addItem(item_text)
            self.course_name_input.clear()
            self.professor_name_input.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Both course name and professor name must be filled!")
    def add_time(self):
        time_st = self.time_st_inp.text().strip()
        time_en = self.time_en_inp.text().strip()
        if time_st and time_en:
            if "-" in time_st:
                time_st = time_st.replace('-','.')
            if "-" in time_en:
                time_en = time_en.replace('-','.')
            self.box_list.addItem(f"{time_st} - {time_en}")
            self.time_st_inp.clear()
            self.time_en_inp.clear()
        else:
            QMessageBox.warning(self,"Input Error", "Both Start Time and End Time must be filled!")
    def add_day(self):
        day_t = self.day_inp.text().strip()
        if day_t.split(","):
            for i in day_t.split(","):
                self.dbox_list.addItem(i)
            self.day_inp.clear()
        else:
            self.dbox_list.addItem(day_t)
            self.day_inp.clear()
    def add_rm(self):
        rm = self.rm_inp.text().strip()
        if rm.split(","):
            for i in rm.split(","):
                self.rbox_list.addItem(i)
            self.rm_inp.clear()
        else:
            self.rbox_list.addItem(rm)
            self.rm_inp.clear()
    def load_ed(self, item,pd):
        if pd == 3:
            cours, prof = item.text().split(" - ")
            self.course_name_input.setText(cours.strip())
            self.professor_name_input.setText(prof.strip())
            self.sel_tm = item
        elif pd == 2:
            st,ed = item.text().split(" - ")
            self.time_st_inp.setText(st.strip())
            self.time_en_inp.setText(ed.strip())
            self.sel_tm = item
        elif pd == 1:
           self.day_inp.setText(item.text().strip())
           self.sel_tm = item
        elif pd == 4:
            self.rm_inp.setText(item.text().strip())
            self.sel_tm =item

    def update_cr(self):
        if hasattr(self, 'sel_tm') and self.sel_tm:
            updated_course_name = self.course_name_input.text().strip()
            updated_professor_name = self.professor_name_input.text().strip()
            
            if updated_course_name and updated_professor_name:
                updated_text = f"{updated_course_name} - {updated_professor_name}"
                self.sel_tm.setText(updated_text)  # Update item text in the list
                self.course_name_input.clear()
                self.professor_name_input.clear()
                try:
                    del self.sel_tm
                except AttributeError as e:
                    QMessageBox.warning(self,"Error",e)
            else:
                parent_list = self.sel_tm.listWidget()
                if parent_list:
                    parent_list.takeItem(parent_list.row(self.sel_tm))
                #QMessageBox.warning(self, "Input Error", "Both course name and professor name must be filled!")
    def update_d(self):
        if hasattr(self, 'sel_tm') and self.sel_tm:
            up_day = self.day_inp.text().strip()
            if up_day :
                self.sel_tm.setText(up_day)
                self.day_inp.clear()
                try:
                    QMessageBox.warning(self,"Done","updated")
                except (AttributeError,Exception) as e:
                    QMessageBox.warning(self,"Error",e)
            else:
                parent_list = self.sel_tm.listWidget()
                if parent_list:
                    parent_list.takeItem(parent_list.row(self.sel_tm))
                                #QMessageBox.warning(self, "Input Error", "Both course name and professor name must be filled!")
    def update_t(self):
        if self.sel_tm and hasattr(self, 'sel_tm'):
            sta = self.time_st_inp.text().strip()
            end = self.time_en_inp.text().strip()

            if sta and end:
                up_time = f"{sta} - {end}"
                self.sel_tm.setText(up_time)
                self.time_st_inp.clear()
                self.time_en_inp.clear()
                try:
                    del self.sel_tm
                except AttributeError as e:
                    QMessageBox.warning(self,"Error",e)
            else:
                parent_list = self.sel_tm.listWidget()
                if parent_list:
                    parent_list.takeItem(parent_list.row(self.sel_tm))
                #QMessageBox.warning(self, "Input Error", "Both course name and professor name must be filled!")
    def update_r(self):
        if self.sel_tm and hasattr(self, 'sel_tm'):
            up_day = self.rm_inp.text().strip()
            if up_day :
                self.sel_tm.setText(up_day)
                self.rm_inp.clear()
                parent_list = self.sel_tm.listWidget()
                parent_list.takeItem(parent_list.row(self.sel_tm))
                self.sel_tm=None
                try:
                    del self.sel_tm
                except AttributeError as e:
                    QMessageBox.warning(self,"Error",e)
            else:
                parent_list = self.sel_tm.listWidget()
                if parent_list:
                    parent_list.takeItem(parent_list.row(self.sel_tm))
                #QMessageBox.warning(self, "Input Error", "Both course name and professor name must be filled!")
    def time_pg(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.time_st_inp = QLineEdit()
        self.time_st_inp.setPlaceholderText("Time Start")
        self.time_en_inp = QLineEdit()
        self.time_en_inp.setPlaceholderText("Time End")
        self.time_st_inp.setStyleSheet("padding:20px; background-color: white; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;")
        self.time_en_inp.setStyleSheet("padding:20px; background-color: white; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;")
        self.box_list = QListWidget()
        self.box_list.setStyleSheet("background-color: #F1F6F9; padding: 20px; border: 5px solid #ddd;font-size: 30px;font-family:monospace;font-weight:medium; ")
        add_time = QPushButton("ADD")
        add_time.setStyleSheet("background-color: #0078d7; color: white;font-weight:bold;font-size:15px; padding: 5px; border-radius: 7px; height: 30px;")
        add_time.clicked.connect(self.add_time)
        update_time = QPushButton("UPDATE")
        update_time.setStyleSheet("background-color: #ffae42; color: white;font-weight:bold; padding: 5px;font-size:20px; border-radius: 5px;height: 25px;font-family:serif; ")
        update_time.clicked.connect(self.update_t)
        save_time = QPushButton("SAVE TIMES")
        save_time.setStyleSheet("background-color: #28a745;font-family:serif;font-weight:bold; color: white; padding: 10px; border-radius: 5px;font-size:20px")
        save_time.clicked.connect(lambda:self.save_oth("time"))
        self.st_en= QLabel("TIME START/END")
        self.st_en.setStyleSheet("color:black;font-family: serif;font-size: 25px; text-align:center;")
        layout.addWidget(self.st_en)
        layout.addWidget(self.time_st_inp)
        layout.addWidget(self.time_en_inp)
        layout.addWidget(add_time)
        layout.addWidget(self.box_list)
        layout.addWidget(update_time)
        layout.addWidget(save_time)
        self.box_list.itemDoubleClicked.connect(lambda item: self.load_ed(item,2))
        page.setLayout(layout)
        return page
    def room_pg(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.rm_inp = QLineEdit()
        self.rm_inp.setPlaceholderText("Les Salles")
        self.rm_inp.setStyleSheet("padding:20px; background-color: white; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;")
        self.rbox_list = QListWidget()
        self.rbox_list.setStyleSheet("background-color: #F1F6F9; padding: 20px; border: 5px solid #ddd;font-size: 30px;font-family:monospace;font-weight:medium; ")
        add_rm = QPushButton("AJOUTER")
        add_rm.setStyleSheet("background-color: #0078d7; color: white;font-size:15px;font-weight:bold; padding: 5px; border-radius: 7px; height: 30px;")
        add_rm.clicked.connect(self.add_rm)
        update_rm = QPushButton("UPDATE")
        update_rm.setStyleSheet("background-color: #ffae42; color: white; padding: 5px;font-weight:bold;font-size:20px; border-radius: 5px;height: 25px;font-family:serif; ")
        update_rm.clicked.connect(self.update_r)
        save_rm = QPushButton("ENREGITRE")
        save_rm.setStyleSheet("background-color: #28a745;font-family:serif;font-weight:bold; color: white; padding: 10px; border-radius: 5px;font-size:20px")
        save_rm.clicked.connect(lambda:self.save_oth("room"))
        self.r_lab= QLabel("Saisis Les Salle Avaiable : ")
        self.r_lab.setStyleSheet("color:black;font-family: serif;font-size: 25px; text-align:center;")
        layout.addWidget(self.r_lab)
        layout.addWidget(self.rm_inp)
        layout.addWidget(add_rm)
        layout.addWidget(self.rbox_list)
        layout.addWidget(update_rm)
        layout.addWidget(save_rm)
        self.rbox_list.itemDoubleClicked.connect(lambda item:self.load_ed(item,4))
        page.setLayout(layout)
        return page
    def day_pg(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.day_inp = QLineEdit()
        self.day_inp.setPlaceholderText("Entrer les Jours :")
        self.day_inp.setStyleSheet("padding:20px; background-color: white; border-radius: 5px; height: 19px; font-size: 15px;font-family:monospace;")
        self.dbox_list = QListWidget()
        self.dbox_list.setStyleSheet("background-color: #F1F6F9; padding: 20px; border: 5px solid #ddd;font-size: 30px;font-family:monospace;font-weight:medium; ")
        add_day = QPushButton("ADD")
        add_day.setStyleSheet("background-color: #0078d7; color: white;font-size:15px; padding: 5px; border-radius: 7px; height: 30px;font-weight:bold;")
        add_day.clicked.connect(self.add_day)
        update_day = QPushButton("UPDATE")
        update_day.setStyleSheet("background-color: #ffae42; color: white; padding: 5px;font-size:20px; border-radius: 5px;height: 25px;font-family:serif;font-weight:bold; ")
        update_day.clicked.connect(self.update_d)
        save_day = QPushButton("SAVE DAYS")
        save_day.setStyleSheet("background-color: #28a745;font-family:serif; color: white; padding: 10px; border-radius: 5px;font-size:20px;font-weight:bold;")
        save_day.clicked.connect(lambda: self.save_oth("day"))
        self.d_lab= QLabel("Entre Les Jours")
        self.d_lab.setStyleSheet("color:black;font-family: serif;font-size: 25px; text-align:center;")
        layout.addWidget(self.d_lab)
        layout.addWidget(self.day_inp)
        layout.addWidget(add_day)
        layout.addWidget(self.dbox_list)
        layout.addWidget(update_day)
        layout.addWidget(save_day)
        self.dbox_list.itemDoubleClicked.connect(lambda item:self.load_ed(item,1))
        page.setLayout(layout)
        return page

    def save_fill(self):
        fill= self.filliere_name_input.text().strip()
        f_sl = None
        if not fill:
            QMessageBox.warning(self, "Input Error", "Filliere name cannot be empty!")
            return

        conn = sqlite3.connect("UNI.db")
        cursor = conn.cursor()
        try:
            fil = fill.split(":")
            f_nm = fil[0]
            f_sl = fil[1]
        except Exception:
            f_nm = fill
        cursor.execute("INSERT INTO filliere (name) VALUES (?)", (f_nm,))
        fi_id = cursor.lastrowid
        
        for i in range(self.course_list.count()):
            course_professor_text = self.course_list.item(i).text()
            course_name, professor_name = course_professor_text.split(" - ")
            cursor.execute("INSERT INTO course (filliere_id, name, professor) VALUES (?, ?,?)", 
                           (fi_id, course_name.strip(), professor_name.strip()))
        if f_sl !=None:
            for s in f_sl.split(","):
                cursor.execute("INSERT INTO rooms (f_id,room) VALUES (?,?)",(fi_id,s.strip()))
        
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Success", "Les Fillieres, cours et  professors sont enregistre successfully!")
        self.filliere_name_input.clear()
        self.course_list.clear()
    def save_oth(self,var):
        conn = sqlite3.connect("UNI.db")
        cursor = conn.cursor()
        if var =="time":
            cursor.execute("DELETE FROM time")
            for i in range(self.box_list.count()):
                time = self.box_list.item(i).text()
                st,en=time.split("-")
                cursor.execute("INSERT INTO time (start,end) VALUES (?,?)",(st.strip(),en.strip()))
            conn.commit()
            conn.close()
        elif var=="room":
            cursor.execute("SELECT room FROM rooms")
            exs_rm =[r[0]for r in  cursor.fetchall()]
            for i in range(self.rbox_list.count()):
                rms = self.rbox_list.item(i).text()
                if rms not in exs_rm:
                    cursor.execute("INSERT INTO rooms (f_id,room) VALUES (?,?)",(1,rms.strip()))
            conn.commit()
            conn.close()
        elif var == "day":
            cursor.execute("DELETE FROM days")
            for i in range(self.dbox_list.count()):
                day = self.dbox_list.item(i).text()
                cursor.execute("INSERT INTO days (day) VALUES (?)",(day.strip(),))
            conn.commit()
            conn.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    tr = Login()
    chd = tr.dj_act()
    if chd:
        win = Admin()
    else:
        win = Login()
        win.show()
    sys.exit(app.exec_())