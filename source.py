import tkinter as tk
import sys
from tkinter import StringVar, messagebox, simpledialog, ttk
from ttkthemes import ThemedTk
from mysqldbms import SQLDBConnector

dbname = 'bloodbank'
localhost = 'LAPTOP-E4QKL3K4\SQLEXPRESS'
sqlDB = SQLDBConnector(db=dbname, server=localhost)

class GUI:
    def __init__(self):
        print(f'log: app started')
        self.PLOpened = False
        self.title = "Blood Donor Database Management System"
        self.mainFont = 'Arial 20'
        self.subFont = 'Arial 10'
        self.main = ThemedTk(theme='yaru')
        self.menubar = tk.Menu(self.main)
        #self.main.geometry("852x480")
        self.main.resizable(0,0)
        self.main.title(self.title)
        print(f'log: main window drawn')
        self.createMainWindow()

    def createMainWindow(self):
        #set grid
        self.main.rowconfigure(8, weight = 0)
        self.main.rowconfigure(9, weight = 0)
        self.main.columnconfigure(0, weight = 1)
        self.main.columnconfigure(1, weight = 1)
        self.main.columnconfigure(2, weight = 1)
        self.main.columnconfigure(3, weight = 1)
        self.main.columnconfigure(4, weight = 1)
        self.main.columnconfigure(5, weight = 1)

        # sets menu bar
        print(f'log: main menu bar set')
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Change Name",command=self.changeName)
        self.filemenu.add_command(label="Change Location",command=self.changeClinicLocation)
        self.filemenu.add_command(label="Change Contact",command=self.changeClinicContact)
        self.filemenu.add_command(label="Close",command=self.on_closing)
        self.menubar.add_cascade(menu=self.filemenu,label="Options")
        self.main.config(menu=self.menubar)

        # main label (clinic name)
        print(f'log: main label set')
        self.var_mainLabelText = StringVar(None)
        self.mainLabel = ttk.Label(self.main,
                                  text=self.fetchName('name'),
                                  font=self.mainFont)
        self.mainLocation = ttk.Label(self.main,
                                  text=f"Location: {self.fetchName('loc')}",
                                  font=self.subFont)
        self.mainContact = ttk.Label(self.main,
                                  text=f"Contact Number: {self.fetchName('cont')}",
                                  font=self.subFont)
        
        #side buttons
        #self.button_ClinicInfo = ttk.Button(self.main,
        #                                text = "Clinic Info",
        #                                command = self.ClinicInfo,
        #                                width = 30
        #                                ).grid(column=0,row=3,columnspan=2,sticky='ns',padx=10,pady=5)
        print(f'log: setting main buttons...')
        self.button_PatientList = ttk.Button(self.main,
                                        text = "Patient List",
                                        command = self.PatientList,
                                        width = 30
                                        ).grid(column=0,row=4,columnspan=2,sticky='ns',padx=10,pady=5)
        self.button_AddRemovePatients = ttk.Button(self.main,
                                        text = "Add Patients",
                                        command = self.AddPatient,
                                        width = 30
                                        ).grid(column=0,row=5,columnspan=2,sticky='ns',padx=10,pady=5)
        self.button_ModifyPatientInfo = ttk.Button(self.main,
                                        text = "Modify Patient Info",
                                        command = self.ModifyPatients,
                                        width = 30
                                        ).grid(column=0,row=6,columnspan=2,sticky='ns',padx=10,pady=5)
        self.button_CheckDonorStatus = ttk.Button(self.main,
                                        text = "Check Donor Status",
                                        command = None,
                                        width = 30
                                        ).grid(column=0,row=7,columnspan=2,sticky='ns',padx=10,pady=5)
        self.button_RequestDonor = ttk.Button(self.main,
                                        text = "Request Donor",
                                        command = None,
                                        width = 30,
                                        ).grid(column=0,row=8,columnspan=2,sticky='s',padx=10,pady=10,ipady=10)
        self.button_debugDonors = ttk.Button(self.main,
                                        text = "DEBUG: modify donors",
                                        command = None,
                                        width = 30
                                        ).grid(column=0,row=10,columnspan=2,sticky='ns',padx=10,pady=5)
        print(f'log: main buttons set')
        #main display
        #self.display = ttk.Label(self.main,
        #                         width=83,
        #                         #height=24,
        #                         text = '',
        #                         font = 'Consolas 10',
        #                         relief="groove")
        #draw window
        self.mainLabel.grid(column=0,
                            row=0,
                            columnspan=3,
                            sticky='ns',
                            pady=10)
        self.mainLocation.grid(column=0,
                            row=1,
                            sticky='ns',
                            pady=2)
        self.mainContact.grid(column=0,
                            row=2,
                            sticky='ns',
                            pady=2)

        #self.display.grid(column=2,
        #                  row=2,
        #                  columnspan=4,
        #                  rowspan=9,
        #                  sticky='nw',
        #                  pady=15,
        #                  padx=15)

        self.main.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.main.mainloop()

    #---------------button functions-------------------------------------------------

    #def ClinicInfo(self):
    #    self.infoWindow = ThemedTk(theme='yaru')
    #    self.infoWindow.title('Clinic Info')
    #    self.infoWindow.resizable(0,0)
    #    self.infoName = ttk.Label(self.infoWindow,
    #                              text=self.fetchName('name'),
    #                              font=self.mainFont).pack(padx=10,side='top')
    #    self.infoLoc = ttk.Label(self.infoWindow,
    #                              text=self.fetchName('loc'),
    #                              font=self.subFont).pack(padx=10, pady=2)
    #    self.infoCont = ttk.Label(self.infoWindow,
    #                              text=self.fetchName('cont'),
    #                              font=self.subFont).pack(padx=10, pady=2, side='bottom')
    #    self.infoWindow.mainloop()

    def PatientList(self):
        print(f'log: PatientList drawn')
        if self.PLOpened:
            self.PL_onclose()
        self.PLOpened = True
        self.patientList = ThemedTk(theme='yaru')
        self.patientList.title('Patient List')
        self.patientList.resizable(0,0)
        fetch = sqlDB.executeQuery(sql='SELECT * FROM patients').fetchall()
        self.patientList.columnconfigure(0,weight=1)
        self.patientList.columnconfigure(1,weight=2)
        self.patientList.columnconfigure(4,weight=1)
        self.patientList.columnconfigure(5,weight=1)
        self.draw_PatientList(start=1,arg=fetch)
        self.patientList.protocol('WM_DELETE_WINDOW', self.PL_onclose)

    def PL_onclose(self):
        print(f'log: PL_onclose() called')
        self.PLOpened = False
        self.patientList.destroy()

    def drawheader_PatientList(self):
        print(f'log: drawheader_PatientList called')
        ttk.Label(self.patientList,
                  text="Patient No.",
                  font='Consolas 12',
                  width=20,
                  relief='groove').grid(column=0, row=0, ipadx=5,ipady=5,sticky='news')
        ttk.Label(self.patientList,
                  text="Name",
                  font='Consolas 12',
                  relief='groove').grid(column=1, row=0, columnspan=3,ipadx=5,ipady=5,sticky='news')
        ttk.Label(self.patientList,
                  text="Age",
                  font='Consolas 12',
                  width = 4,
                  relief='groove').grid(column=4, row=0,ipadx=5,ipady=5,sticky='nws')
        ttk.Label(self.patientList,
                  text="Blood Type",
                  font='Consolas 12',
                  width = 10,
                  relief='groove').grid(column=5, row=0,ipadx=5,ipady=5,sticky='nws')

    def draw_PatientList(self, start, arg):
        print(f'log: draw_PatientList called')
        self.drawheader_PatientList()
        rowPos = 1
        for i in arg:
            if (rowPos < start):
                rowPos += 1
                continue
            if((rowPos - start) == 15):
                print(f'log: page amount exceeded: break')
                break
            ttk.Label(self.patientList,
                      text=f"Patient #{i.patient_id}",
                      font='Consolas 10',
                      width = 20,
                      relief='groove').grid(column=0, row=rowPos,ipadx=5,ipady=5,sticky='nws')
            ttk.Label(self.patientList,
                      text=f"{i.patient_name}",
                      font='Consolas 10',
                      width = 25,
                      relief='groove').grid(column=1, row=rowPos, columnspan=3,ipadx=5,ipady=5,sticky='nws')
            tk.Label(self.patientList,
                      text=f"{i.patient_age}",
                      font='Consolas 10',
                      width = 5,
                      relief='groove').grid(column=4, row=rowPos,ipadx=5,ipady=5,sticky='ns')
            tk.Label(self.patientList,
                      text=f"{i.blood_type}",
                      font='Consolas 10',
                      width = 13,
                      relief='groove').grid(column=5, row=rowPos,ipadx=5,ipady=5,sticky='ns')
            rowPos += 1
        button_pos = rowPos + 1
        print(f'log: prev next page button drawn')
        if (rowPos%15 == 1):
            self.nextPage = ttk.Button(self.patientList,
                                        text = "Next Page >>",
                                        command = lambda: self.nextpage_PatientList(pos=rowPos,fetch=arg),
                                        width = 20
                                        ).grid(column=1,row=button_pos,sticky='se',padx=20,pady=3)
        if (rowPos != 16):
            self.prevPage = ttk.Button(self.patientList,
                                        text = "<< Prev Page",
                                        command = lambda: self.nextpage_PatientList(pos=((rowPos-(rowPos%16))-15),fetch=arg),
                                        width = 20
                                        ).grid(column=0,row=button_pos,sticky='se',padx=20,pady=3)
        
    def nextpage_PatientList(self,pos,fetch):
        print(f'log: change page called')
        for widgets in self.patientList.winfo_children():
            widgets.destroy()
        self.draw_PatientList(start=pos,arg=fetch)

    def AddPatient(self):
        print(f'log: AddPatient called')
        self.addPatients = ThemedTk(theme='yaru')
        self.addPatients.title('Add Patients')
        self.addPatients.resizable(0,0)
        ttk.Label(self.addPatients,
                  text = 'Patient ID:',
                  font = self.subFont).grid(column=0,row=0,padx=10,pady=3,sticky='news')
        self.patientID = StringVar(self.addPatients)
        entry_ID = ttk.Entry(self.addPatients,
                             textvariable=self.patientID,
                             width=50).grid(column=1,row=0,pady=3,sticky='nw')
        ttk.Label(self.addPatients,
                  text = 'Patient Name:',
                  font = self.subFont).grid(column=0,row=1,padx=10,pady=3,sticky='news')
        self.patientName = StringVar(self.addPatients)
        entry_Name = ttk.Entry(self.addPatients,
                             textvariable=self.patientName,
                             width=50).grid(column=1,row=1,pady=3,sticky='nw')
        ttk.Label(self.addPatients,
                  text = 'Patient Age:',
                  font = self.subFont).grid(column=0,row=2,padx=10,pady=3,sticky='news')
        self.patientAge = StringVar(self.addPatients)
        entry_Name = ttk.Entry(self.addPatients,
                             textvariable=self.patientAge,
                             width=50).grid(column=1,row=2,pady=3,sticky='nw')
        ttk.Label(self.addPatients,
                  text = 'Blood Type:',
                  font = self.subFont).grid(column=0,row=3,padx=10,pady=3,sticky='news')
        options = ['A+','A-','B+','B-','AB+','AB-','O+','O-']
        self.bloodType = StringVar(self.addPatients)
        self.dropdown_type = ttk.OptionMenu(self.addPatients,
                                       self.bloodType,
                                       'A+',
                                       *options).grid(column=1,row=3,pady=3,sticky='nw')
        self.addPatients_button = ttk.Button(self.addPatients,
                                        text = "Add Patient",
                                        command = lambda: self.InsertPatients(ID = self.patientID,
                                                                              NAME = self.patientName,
                                                                              AGE = self.patientAge,
                                                                              TYPE = self.bloodType),
                                        width = 20
                                        ).grid(column=1,row=5,sticky='se',padx=10,pady=3)
    def ModifyPatients(self):
        print(f'log: ModifyPatients called')
        if not self.PLOpened:
            self.PatientList()
        self.modifyPatients = ThemedTk(theme='yaru')
        self.modifyPatients.title('Modify Patients')
        self.modifyPatients.resizable(0,0)
        ttk.Label(self.modifyPatients,
                  text = 'Patient #',
                  font = self.subFont).grid(column=0,row=0,padx=10,pady=3,sticky='news')
        self.patientID = StringVar(self.modifyPatients)
        self.modify_entry_ID = ttk.Entry(self.modifyPatients,
                             textvariable=self.patientID,
                             width=10)
        self.button_modifyPatient = ttk.Button(self.modifyPatients,
                                        text = "Modify",
                                        command = lambda: self.pressed_modify(id = self.patientID.get()),
                                        width = 10)
        self.button_deletePatient = ttk.Button(self.modifyPatients,
                                        text = "Delete",
                                        command = lambda: self.pressed_delete(id = self.patientID.get()),
                                        width = 10)
        self.modify_entry_ID.grid(column=1,row=0,pady=3,sticky='nw')
        self.button_modifyPatient.grid(column=2,row=0,sticky='ns',padx=10,pady=3)
        self.button_deletePatient.grid(column=3,row=0,sticky='ns',padx=10,pady=3)
        self.modifyPatients.mainloop()

    def pressed_modify(self, id):
        print('log: modify pressed')
        self.button_modifyPatient.state(['disabled'])
        self.button_deletePatient.state(['disabled'])
        self.modify_entry_ID.config(state='readonly')
        fetch = sqlDB.executeQuery(sql='SELECT * FROM patients WHERE patient_id = ?',params=id).fetchall()
        self.pressed_modify_drawpatient(id=id, fetch=fetch)
        ttk.Label(self.modifyPatients,
                  text = 'Patient ID:',
                  font = self.subFont).grid(column=0,row=3,padx=10,pady=3,sticky='news')
        self.patientID = StringVar(self.modifyPatients)
        entry_ID = ttk.Entry(self.modifyPatients,
                             textvariable=self.patientID,
                             width=50).grid(column=1,columnspan=3,row=3,pady=3,sticky='nw')
        ttk.Label(self.modifyPatients,
                  text = 'Patient Name:',
                  font = self.subFont).grid(column=0,row=4,padx=10,pady=3,sticky='news')
        self.patientName = StringVar(self.modifyPatients)
        entry_Name = ttk.Entry(self.modifyPatients,
                             textvariable=self.patientName,
                             width=50).grid(column=1,columnspan=3,row=4,pady=3,sticky='nw')
        ttk.Label(self.modifyPatients,
                  text = 'Patient Age:',
                  font = self.subFont).grid(column=0,row=5,padx=10,pady=3,sticky='news')
        self.patientAge = StringVar(self.modifyPatients)
        entry_Name = ttk.Entry(self.modifyPatients,
                             textvariable=self.patientAge,
                             width=50).grid(column=1,columnspan=3,row=5,pady=3,sticky='nw')
        ttk.Label(self.modifyPatients,
                  text = 'Blood Type:',
                  font = self.subFont).grid(column=0,row=6,padx=10,pady=3,sticky='news')
        options = ['A+','A-','B+','B-','AB+','AB-','O+','O-']
        self.bloodType = StringVar(self.modifyPatients)
        self.dropdown_type = ttk.OptionMenu(self.modifyPatients,
                                       self.bloodType,
                                       '',
                                       *options).grid(column=1,row=6,pady=3,sticky='nw')
        self.confirm_modifyPatient = ttk.Button(self.modifyPatients,
                                        text = "Confirm",
                                        command = lambda: self.uspModifyPatients(ID = id,
                                                                              NAME = self.patientName.get(),
                                                                              AGE = self.patientAge.get(),
                                                                              TYPE = self.bloodType.get()),
                                        width = 20
                                        ).grid(column=3,row=7,sticky='se',padx=10,pady=3)

    def pressed_modify_drawpatient(self, id, fetch):
        print(f'log: draw single patient MODIFY')
        ttk.Label(self.modifyPatients,
                  text="Patient No.",
                  font='Consolas 12',
                  relief='groove').grid(column=0, row=1, ipadx=5,ipady=5,sticky='news')
        tk.Label(self.modifyPatients,
                  text="Name",
                  font='Consolas 12',
                  relief='groove').grid(column=1, row=1,ipadx=5,ipady=5,sticky='news')
        ttk.Label(self.modifyPatients,
                  text="Age",
                  font='Consolas 12',
                  width = 4,
                  relief='groove').grid(column=2, row=1,ipadx=5,ipady=5,sticky='news')
        ttk.Label(self.modifyPatients,
                  text="Blood Type",
                  font='Consolas 12',
                  width = 10,
                  relief='groove').grid(column=3, row=1,ipadx=5,ipady=5,sticky='news')
        for i in fetch:
            rowPos = 2
            ttk.Label(self.modifyPatients,
                      text=f"Patient #{i.patient_id}",
                      font='Consolas 10',
                      relief='groove').grid(column=0, row=rowPos,ipadx=5,ipady=5,sticky='news')
            ttk.Label(self.modifyPatients,
                      text=f"{i.patient_name}",
                      font='Consolas 10',
                      relief='groove').grid(column=1, row=rowPos,ipadx=5,ipady=5,sticky='news')
            tk.Label(self.modifyPatients,
                      text=f"{i.patient_age}",
                      font='Consolas 10',
                      width = 5,
                      relief='groove').grid(column=2, row=rowPos,ipadx=5,ipady=5,sticky='news')
            tk.Label(self.modifyPatients,
                      text=f"{i.blood_type}",
                      font='Consolas 10',
                      width = 13,
                      relief='groove').grid(column=3, row=rowPos,ipadx=5,ipady=5,sticky='news')
    def pressed_delete(self, id):
        print(f'log: delete pressed')
        answer = tk.messagebox.askyesno(title='Confirmation',
                                        message='Are you sure you want to DELETE this patient?')
        if answer:
            sqlDB.executeQuery(sql='DELETE patients WHERE patient_id = ?',params = id)
            print(f"log: patient id {id} deleted")
            self.modifyPatients.destroy()
            self.PL_onclose()
            tk.messagebox.showinfo(title='Success',message='Successfully deleted patient')

    def CheckDonorStatus(self):
        pass
    def drawheader_CheckDonorStatus(self):
        print(f'log: drawheader_CheckDonorStatus called')
        ttk.Label(self.patientList,
                  text="Patient No.",
                  font='Consolas 12',
                  width=20,
                  relief='groove').grid(column=0, row=0, ipadx=5,ipady=5,sticky='news')
        ttk.Label(self.patientList,
                  text="Name",
                  font='Consolas 12',
                  relief='groove').grid(column=1, row=0, columnspan=3,ipadx=5,ipady=5,sticky='news')
        ttk.Label(self.patientList,
                  text="Age",
                  font='Consolas 12',
                  width = 4,
                  relief='groove').grid(column=4, row=0,ipadx=5,ipady=5,sticky='nws')
        ttk.Label(self.patientList,
                  text="Blood Type",
                  font='Consolas 12',
                  width = 10,
                  relief='groove').grid(column=5, row=0,ipadx=5,ipady=5,sticky='nws')
    #-----------------------------functions----------------------------------------
    def InsertPatients(self, ID, NAME, AGE, TYPE):
        print(f'log: uspInsertPatients {ID, NAME, AGE, TYPE}')
        answer = tk.messagebox.askyesno(title='Confirmation',
                                        message='Are you sure you want to add this patient?')
        if answer:
            sqlDB.executeQuery(sql='EXEC uspInsertPatients @patient_id=?, @patient_name=?, @patient_age=?, @blood_type=?',
                               params = (ID.get(),NAME.get(),AGE.get(),TYPE.get()))
            self.addPatients.destroy()
            tk.messagebox.showinfo(title='Success',message='Successfully added patient!')

    def uspModifyPatients(self, ID, NAME, AGE, TYPE):
        print(f'log: uspModifyPatients {ID, NAME, AGE, TYPE}')
        answer = tk.messagebox.askyesno(title='Confirmation',
                                        message='Are you sure you want to modify this patient?')
        if answer:
            sqlDB.executeQuery(sql='EXEC uspModifyPatients @patient_id=?, @patient_name=?, @patient_age=?, @blood_type=?',
                               params = (ID,NAME,AGE,TYPE))
            self.modifyPatients.destroy()
            self.PL_onclose()
            tk.messagebox.showinfo(title='Success',message='Successfully modified patient!')

    def on_closing(self):
        print(f'log: closed')
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.main.destroy()

    def fetchName(self,arg):
        if arg == 'name':
            #fetch clinic name
            print(f'log: fetched name')
            fetch = sqlDB.callProc(procname="uspFetchName").fetchone()
            result = fetch[0]
            return result
        if arg == 'loc':
            #fetch clinic loc
            print(f'log: fetched loc')
            fetch = sqlDB.executeQuery(sql='SELECT clinic_location FROM clinic_info WHERE ID = 1').fetchone()
            result = fetch[0]
            return result
        if arg == 'cont':
            #fetch clinic contact
            print(f'log: fetched cont')
            fetch = sqlDB.executeQuery(sql='SELECT contact_info FROM clinic_info WHERE ID = 1').fetchone()
            result = fetch[0]
            return result

    def changeName(self):
        try:
            var_changeNameText = simpledialog.askstring("","Enter new name:",parent=self.main)
            print(f'debug: changed name to {var_changeNameText}') #log
            sqlDB.executeQuery(sql='EXEC uspChangeName @new_name=?',params = var_changeNameText)
            self.mainLabel.config(text = self.fetchName('name'))
        except Exception:
            pass
    def changeClinicLocation(self):
        try:
            var_changeNameText = simpledialog.askstring("","Enter new location:",parent=self.main)
            print(f'debug: changed location to {var_changeNameText}') #log
            sqlDB.executeQuery(sql='EXEC uspChangeLocation @new_loc=?',params = var_changeNameText)
            self.mainLocation.config(text = f"Location: {self.fetchName('loc')}")
        except Exception:
            pass
    def changeClinicContact(self):
        try:
            var_changeNameText = simpledialog.askstring("","Enter new contact:",parent=self.main)
            print(f'debug: changed contact to {var_changeNameText}') #log
            sqlDB.executeQuery(sql='EXEC uspChangeContact @new_cont=?',params = var_changeNameText)
            self.mainContact.config(text = f"Contact Number: {self.fetchName('cont')}")
        except Exception:
            pass

    def search_okButton(self):
        if(self.var_searchEntry.get() == ""):
            messagebox.showinfo(message="Empty Field!")
        else:
            print(self.var_searchEntry.get())


if __name__ == '__main__':
    GUI()
