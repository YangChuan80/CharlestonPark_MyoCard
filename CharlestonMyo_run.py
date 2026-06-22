#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkf
import sys

FONT_NAME = 'tahoma'
LABEL_FONT = (FONT_NAME, 9)
EDIT_FONT = (FONT_NAME, 9)


# In[2]:


import sqlite3


# In[3]:


import datetime


# In[ ]:





# In[4]:


DB_file = 'Entity_DB.sqlite'
conn = sqlite3.connect(DB_file)

conn.execute('PRAGMA journal_mode=WAL') 
#WAL (Write-Ahead Logging) 模式：
#WAL 是 SQLite 的一种日志模式，用于替代传统的回滚日志模式，可以显著提高并发性能。

cur = conn.cursor()


# In[5]:


sqlstr = '''SELECT *
FROM HCM JOIN Patients ON HCM.CitizenID = Patients.CitizenID
ORDER BY HCM.id_in_HCM
'''


# In[6]:


spreadsheet = cur.execute(sqlstr)


# In[7]:


spreadsheet


# In[8]:


combination = []
for row in spreadsheet:
    combination.append(row)


# In[9]:


cur.execute('SELECT * FROM HCM')
headers_HCM = [item[0] for item in cur.description]


# In[10]:


cur.execute('SELECT * FROM Patients')
headers_patients = [item[0] for item in cur.description]


# In[11]:


headers = headers_HCM + headers_patients


# In[12]:


headers


# In[13]:


len(headers)


# In[14]:


## Helper functions
#### Table related

def OnDoubleClick(event):
    global idglb
    try:
        item = table.selection()[0]
        value = table.item(item, 'values')    
        iden = value[0]

        #/// Here is a Database visit
        ExtractID(iden)     
        idglb = iden

    except:
        pass


# In[15]:


def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))


# In[16]:


#### Function related

def refreshDB():
    global conn, cur, desc, headers, combination

    conn.close()
    conn = sqlite3.connect(DB_file)
    cur = conn.cursor()

    cur.execute('SELECT * FROM HCM')
    headers_HCM = [item[0] for item in cur.description]

    cur.execute('SELECT * FROM Patients')
    headers_patients = [item[0] for item in cur.description]

    headers = headers_HCM + headers_patients

    sqlstr = '''SELECT * FROM HCM JOIN Patients 
    ON HCM.CitizenID = Patients.CitizenID
    ORDER BY HCM.id_in_HCM
    '''
    spreadsheet = cur.execute(sqlstr)

    combination = []
    for row in spreadsheet:
        combination.append(row)  


# In[17]:


def ExtractID(iden): 
    global conn, cur

    conn.close()
    conn = sqlite3.connect(DB_file)
    cur = conn.cursor()

    sqlstr = '''SELECT * FROM HCM 
    JOIN Patients ON HCM.CitizenID = Patients.CitizenID 
    WHERE HCM.id_in_HCM = ?    
    '''
    cur.execute(sqlstr, (iden,))
    rowSelected = cur.fetchone()

    item = {}    
    for i in range(len(rowSelected)):
        item[headers[i]] = rowSelected[i]
    display_in_text(item)




# In[18]:


# Display in Table

def display_in_table(combination):
    for row in combination:
        table.insert("", "end", values=row)
    num = str(len(combination))
    text_num.delete('1.0', tk.END)
    text_num.insert('1.0', num)


# In[19]:


# Display in the text widget

def display_in_text(item):

    # //// HCM ///////////////////////////////

    text_id_in_HCM.delete('1.0', tk.END)
    text_id_in_HCM.insert('1.0', item['id_in_HCM'])      

    text_PatientName_in_HCM.delete('1.0', tk.END)
    text_PatientName_in_HCM.insert('1.0', item['PatientName_in_HCM'])   

    text_EnrollmentDate.delete('1.0', tk.END)
    text_EnrollmentDate.insert('1.0', item['EnrollmentDate'])       

    combo_IsObstructiveResting.set(item['IsObstructiveResting'])

    combo_IsObstructiveValsalva.set(item['IsObstructiveValsalva']) 

    text_Diabetes.delete('1.0', tk.END)
    text_Diabetes.insert('1.0', item['Diabetes'])

    text_Hypertension.delete('1.0', tk.END)
    text_Hypertension.insert('1.0', item['Hypertension'])

    text_Stroke.delete('1.0', tk.END)
    text_Stroke.insert('1.0', item['Stroke'])

    text_Renal.delete('1.0', tk.END)
    text_Renal.insert('1.0', item['Renal'])

    combo_IsDyspnea.set(item['IsDyspnea'])

    combo_IsChestPain.set(item['IsChestPain']) 

    combo_IsSyncope.set(item['IsSyncope']) 

    combo_NYHA.set(item['NYHA']) 

    text_QualityOfLifeScore.delete('1.0', tk.END)
    text_QualityOfLifeScore.insert('1.0', item['QualityOfLifeScore'])

    # //// Patients ///////////////////////////////

    text_id_in_patients.delete('1.0', tk.END)
    text_id_in_patients.insert('1.0', item['id_in_patients'])

    text_PatientName_in_patients.delete('1.0', tk.END)
    text_PatientName_in_patients.insert('1.0', item['PatientName_in_patients'])

    text_InPatientID.delete('1.0', tk.END)
    text_InPatientID.insert('1.0', item['InPatientID'])

    text_CitizenID.delete('1.0', tk.END)
    text_CitizenID.insert('1.0', item['CitizenID'])

    text_BirthDate.delete('1.0', tk.END)
    text_BirthDate.insert('1.0', item['BirthDate'])  

    #text_Gender.delete('1.0', tk.END)
    #text_Gender.insert('1.0', item['Gender'])   

    combo_Gender.set(item['Gender'])

    text_PatientName_CN.delete('1.0', tk.END)
    text_PatientName_CN.insert('1.0', item['PatientName_CN'])

    #text_ProbandName.delete('1.0', tk.END)
    #text_ProbandName.insert('1.0', item['ProbandName'])

    #text_proband_id.delete('1.0', tk.END)
    #text_proband_id.insert('1.0', item['proband_id'])

    #text_RelationshipOfProband.delete('1.0', tk.END)
    #text_RelationshipOfProband.insert('1.0', item['RelationshipOfProband']) 


    text_Diagnosis1.delete('1.0', tk.END)
    text_Diagnosis1.insert('1.0', item['Diagnosis1'])

    text_Diagnosis2.delete('1.0', tk.END)
    text_Diagnosis2.insert('1.0', item['Diagnosis2'])

    text_Diagnosis3.delete('1.0', tk.END)
    text_Diagnosis3.insert('1.0', item['Diagnosis3'])

    text_Diagnosis4.delete('1.0', tk.END)
    text_Diagnosis4.insert('1.0', item['Diagnosis4'])

    text_Diagnosis5.delete('1.0', tk.END)
    text_Diagnosis5.insert('1.0', item['Diagnosis5'])  

    text_Telephone1.delete('1.0', tk.END)
    text_Telephone1.insert('1.0', item['Telephone1'])

    text_Telephone2.delete('1.0', tk.END)
    text_Telephone2.insert('1.0', item['Telephone2'])


    text_Comments.delete('1.0', tk.END)
    text_Comments.insert('1.0', item['Comments'])


# In[20]:


def clear():
    for i in table.get_children():
        table.delete(i)


# In[21]:


def browse():
    clear()
    refreshDB()
    display_in_table(combination)


# In[22]:


def update_HCM():
    pass


# In[23]:


def delete_HCM():
    pass


# In[24]:


def HCM():  
    cur.execute('SELECT * FROM HCM')
    headers_HCM = [item[0] for item in cur.description]

    sqlstr = 'SELECT * FROM HCM ORDER BY id_in_HCM'

    spreadsheet = cur.execute(sqlstr)
    combination = []        
    for row in spreadsheet:
        combination.append(row)

    def OnDoubleClick_Samples(event):
        global idglb
        try:
            item = table.selection()[0]
            value = table.item(item, 'values')    
            iden = value[0]
            ExtractID(iden)     
            idglb = iden

        except:
            pass

    def ExtractID(iden): 
        sqlstr = 'SELECT * FROM HCM WHERE id_in_HCM = ?'
        cur.execute(sqlstr, (iden,))
        rowSelected = cur.fetchone()

        item = {}    
        for i in range(len(rowSelected)):
            item[headers[i]] = rowSelected[i]
        display_in_text(item)

    def display_in_table(combination):
        for row in combination:
            table.insert("", "end", values=row)  #新版Python删除第三个参数

    def display_in_text(item):  
        text_id_in_samples.delete('1.0', tk.END)
        text_id_in_samples.insert('1.0', item['id_in_HCM'])

        text_RackNumber.delete('1.0', tk.END)
        text_RackNumber.insert('1.0', item['RackNumber'])  

        combo_SampleType.set(item['SampleType'])

        text_SampleID.delete('1.0', tk.END)
        text_SampleID.insert('1.0', item['SampleID'])

        combo_SampleStatus.set(item['SampleStatus'])

        text_PatientName_in_samples.delete('1.0', tk.END)
        text_PatientName_in_samples.insert('1.0', item['PatientName_in_samples'])

        text_Samples_patient_id.delete('1.0', tk.END)
        text_Samples_patient_id.insert('1.0', item['patient_id'])

    def update_HCM():
        try:        
            text_id_in_samples_gotten = text_id_in_samples.get('1.0', tk.END).rstrip()        
            RackNumber_gotten = text_RackNumber.get('1.0', tk.END).rstrip()
            SampleID_gotten = text_SampleID.get('1.0', tk.END).rstrip()
            SampleType_gotten = combo_SampleType.get().rstrip()
            SampleStatus_gotten = combo_SampleStatus.get().rstrip()
            PatientName_in_samples_gotten = text_PatientName_in_samples.get('1.0', tk.END).rstrip()
            Samples_patient_id_gotten = text_Samples_patient_id.get('1.0', tk.END).rstrip()       

            Question_mark = '(' + '?, ' * 6 + '?)'

            cur.execute('DELETE FROM HCM WHERE id_in_HCM = ?', (text_id_in_samples_gotten,))        
            conn.commit()

            Update_values = (text_id_in_samples_gotten, 
                             RackNumber_gotten, 
                             SampleID_gotten, 
                             SampleType_gotten, 
                             SampleStatus_gotten, 
                             PatientName_in_samples_gotten,
                             Samples_patient_id_gotten)

            Update_Fields = '''(
            id_in_samples, 
            RackNumber, 
            SampleID, 
            SampleType, 
            SampleStatus, 
            PatientName_in_samples, 
            patient_id)
            '''

            #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
            #('201706181718000444', 'PatientName, 'Serum'))

            cur.execute('INSERT INTO Samples '+ Update_Fields + ' VALUES ' + Question_mark, 
                        Update_values)
            conn.commit()  

            #messagebox.showinfo("Updated", "Sample information successfully updated!") 

            # //////////////////// Refresh the Table ///////////////////////////////////////////////////
            # Clear the table
            for i in table.get_children():
                table.delete(i)

            # Refresh the whole database
            refreshDB()

            # Refresh variable combination

            sqlstr = 'SELECT * FROM HCM ORDER BY id_in_HCM'
            spreadsheet = cur.execute(sqlstr)
            combination = []        
            for row in spreadsheet:
                combination.append(row)

            # Display the table
            display_in_table(combination)

        except:
            pass

    def delete_sample():
        id_in_samples_gotten = text_id_in_samples.get('1.0', tk.END).rstrip()

        if id_in_samples_gotten == '':
            messagebox.showinfo("Empty", "There's no sample to delete. Please make sure.")

        else:           
            result = messagebox.askquestion('Delete', 'Are you sure to delete this sample?', 
                                            icon='warning')

            if result == 'yes':
                cur.execute('DELETE FROM Samples WHERE id_in_samples = ?', (id_in_samples_gotten,))        
                conn.commit()            
                messagebox.showinfo("Deleted", "Sample has been deleted!")

                # //////////////////// Refresh the Table ///////////////////////////////////////////////////
                # Clear the table
                for i in table.get_children():
                    table.delete(i)

                # Refresh the whole database
                refreshDB()

                # Refresh variable combination

                sqlstr = 'SELECT * FROM Samples ORDER BY id_in_samples'
                spreadsheet = cur.execute(sqlstr)
                combination = []        
                for row in spreadsheet:
                    combination.append(row)

                # Display the table        
                display_in_table(combination)

    def sampleIDSearch():
        PatientName_Search_gotten = text_SampleID_search.get('1.0', tk.END).rstrip()

        sqlstr = '''SELECT * FROM Samples WHERE SampleID = ?  
        '''
        cur.execute(sqlstr, (PatientName_Search_gotten,))
        items = cur.fetchall()

        for i in table.get_children():
            table.delete(i)

        display_in_table(items)

    def patientNameSearch():
        PatientName_Search_gotten = text_PatientName_search.get('1.0', tk.END).rstrip()

        sqlstr = '''SELECT * FROM Samples WHERE PatientName_in_samples = ? 
        '''
        cur.execute(sqlstr, (PatientName_Search_gotten,))
        items = cur.fetchall()

        for i in table.get_children():
            table.delete(i)

        display_in_table(items) 


    def browse():
        # Refresh the whole database
        refreshDB()

        # Refresh variable combination

        sqlstr = 'SELECT * FROM Samples ORDER BY id_in_samples'
        spreadsheet = cur.execute(sqlstr)
        combination = []        
        for row in spreadsheet:
            combination.append(row)

        # Display the table
        display_in_table(combination)


    # /////// Main Flow ////////////////////////////

    root_HCM = tk.Toplevel(root)    

    # set the dimensions of the screen 
    # and where it is placed
    root_HCM.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    #root.attributes('-fullscreen', True)
    root_HCM.title('HCM Records')

   # /////// Multicolumn Listbox /////////////////////////
    table = ttk.Treeview(root_HCM, height="20", columns=headers_HCM, selectmode="extended")
    table.pack(padx=10, pady=20, ipadx=1200, ipady=200)

    # 动态设置列宽，无需固定 header_width
    i = 1
    for header in headers_HCM:
        # 计算列宽：表头文字宽度 + 50像素边距
        col_width = tkf.Font().measure(header.title()) + 50
        table.heading('#'+str(i), text=header.title(), anchor=tk.W, 
                      command=lambda c=header: sortby(table, c, 0))
        table.column('#'+str(i), stretch=tk.NO, minwidth=0, width=col_width)
        i += 1
    table.column('#0', stretch=tk.NO, minwidth=0, width=0)       

    table.bind("<Double-1>", OnDoubleClick_Samples)
    #///////////////////////////////////////////////////////////////////////////////////////////

    # Scrollbar////////////////////////////////////////////////////////////////////////////////////////
    vsb = ttk.Scrollbar(table, orient = "vertical",  command = table.yview)
    hsb = ttk.Scrollbar(table, orient = "horizontal", command = table.xview)
    ## Link scrollbars activation to top-level object
    table.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
    ## Link scrollbar also to every columns
    map(lambda col: col.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set), table)
    vsb.pack(side = tk.RIGHT, fill = tk.Y)
    hsb.pack(side = tk.BOTTOM, fill = tk.X)

    # ///////////////Samples///////////////

    y_origin = 540
    gain = 50
    i = 0

    # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_Patients=tk.Label(root_HCM,width=130, height=9 , relief='raised', borderwidth=1)
    label_Patients.place(x=10,y=y_origin+i*gain-40)

    # ///////////// Routine Edits////////////////

    text_id_in_samples = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_id_in_samples.place(x=820, y=y_origin+i*gain)
    label_id_in_samples = tk.Label(root_HCM, text='id_samples:', font=LABEL_FONT)
    label_id_in_samples.place(x=820,y=y_origin+i*gain-25)

    text_RackNumber = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_RackNumber.place(x=40, y=y_origin+i*gain)
    label_RackNumber = tk.Label(root_HCM, text='Rack Number:', font=LABEL_FONT)
    label_RackNumber.place(x=40,y=y_origin+i*gain-25)

    text_SampleID = tk.Text(root_HCM, width=26, height=1, font=EDIT_FONT, wrap='none')
    text_SampleID.place(x=240, y=y_origin+i*gain)
    label_SampleID = tk.Label(root_HCM, text='Sample ID:', font=LABEL_FONT)
    label_SampleID.place(x=240,y=y_origin+i*gain-25)

    combo_SampleType = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_SampleType.place(x=440, y=y_origin+i*gain)
    label_SampleType = tk.Label(root_HCM, text='Sample Type:', font=LABEL_FONT)
    label_SampleType.place(x=440,y=y_origin+i*gain-25)
    combo_SampleType['values'] = ('WholeBlood', 'BloodCells', 'Serum')
    combo_SampleType['state'] = 'readonly'

    combo_SampleStatus = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_SampleStatus.place(x=640, y=y_origin+i*gain)
    label_SampleStatus = tk.Label(root_HCM, text='Sample Status:', font=LABEL_FONT)
    label_SampleStatus.place(x=640,y=y_origin+i*gain-25)
    combo_SampleStatus['values'] = ('-80Frozen', '-20Frozen', '4Refrigeration', 'RoomTemperature')
    combo_SampleStatus['state'] = 'readonly'

    i = 1

    text_PatientName_in_samples = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_in_samples.place(x=40, y=y_origin+i*gain)
    label_PatientName_in_samples = tk.Label(root_HCM, text='Patient Name:', font=LABEL_FONT)
    label_PatientName_in_samples.place(x=40,y=y_origin+i*gain-25)

    text_Samples_patient_id = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_Samples_patient_id.place(x=240, y=y_origin+i*gain)
    label_patient_id = tk.Label(root_HCM, text='Patient ID:', font=LABEL_FONT)
    label_patient_id.place(x=240,y=y_origin+i*gain-25)  

    # //////// Search Area ////////////

    i = -0.7

    button_browse = ttk.Button(root_HCM, text='Browse', width=8, command=browse)
    button_browse.place(x=1250, y=y_origin+i*gain-5)

    i = 0.3

    text_SampleID_search = tk.Text(root_HCM, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_SampleID_search.place(x=1050, y=y_origin+i*gain)
    label_SampleID_search = tk.Label(root_HCM, text='Sample ID:', font=LABEL_FONT)
    label_SampleID_search.place(x=1050,y=y_origin+i*gain-25)

    button_InPatientID_search = ttk.Button(root_HCM, text='Search', width=8, command=sampleIDSearch)
    button_InPatientID_search.place(x=1250, y=y_origin+i*gain-5)

    i = 1.3

    text_PatientName_search = tk.Text(root_HCM, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_search.place(x=1050, y=y_origin+i*gain)
    label_PatientName_search = tk.Label(root_HCM, text='Paitnet Name:', font=LABEL_FONT)
    label_PatientName_search.place(x=1050,y=y_origin+i*gain-25)

    button_PatientName_search = ttk.Button(root_HCM, text='Search', width=8, command=patientNameSearch)
    button_PatientName_search.place(x=1250, y=y_origin+i*gain-5)   

    # ////// Buttons //////////////////////////

    button_update_sample = ttk.Button(root_HCM, text='Update', width=10, command=update_HCM)
    button_update_sample.place(x=640, y=590)

    button_delete_sample = ttk.Button(root_HCM, text='Delete', width=10, command=delete_HCM)
    button_delete_sample.place(x=800, y=590)

    button_exit = ttk.Button(root_HCM, text='Exit', width=8, command=root_HCM.destroy)
    button_exit.place(x=1250, y=670)

    # ///// Browse Automatically /////////////////////

    display_in_table(combination)

    show_modal_window(root_HCM, root)


# In[25]:


def patients():   

    cur.execute('SELECT * FROM Patients')
    headers_patients = [item[0] for item in cur.description]

    sqlstr = 'SELECT * FROM Patients ORDER BY id_in_patients'
    spreadsheet = cur.execute(sqlstr)
    combination = []    

    for row in spreadsheet:
        combination.append(row)    



    def OnDoubleClick_Patients(event):
        global idglb
    #try:
        item = table.selection()[0]
        value = table.item(item, 'values')    
        iden = value[0]
        ExtractID(iden)     
        idglb = iden

    #except:
        #pass


    def ExtractID(iden): 
        sqlstr = 'SELECT * FROM Patients WHERE id_in_patients = ?'
        cur.execute(sqlstr, (iden,))
        rowSelected = cur.fetchone()

        item = {}    
        for i in range(len(rowSelected)):
            item[headers_patients[i]] = rowSelected[i]
        display_in_text(item)

    # Display in Table /////////////////////////////////////////////////
    def display_in_table(combination):
        for row in combination:
            table.insert("", "end", values=row)

        num = str(len(combination))
        text_num.delete('1.0', tk.END)
        text_num.insert('1.0', num)


    # Dispaly in Text /////////////////////////////////////////////////////    
    def display_in_text(item): 
        text_id_in_patients.delete('1.0', tk.END)
        text_id_in_patients.insert('1.0', item['id_in_patients'])

        text_PatientName_in_patients.delete('1.0', tk.END)
        text_PatientName_in_patients.insert('1.0', item['PatientName_in_patients'])

        text_InPatientID.delete('1.0', tk.END)
        text_InPatientID.insert('1.0', item['InPatientID'])

        text_CitizenID.delete('1.0', tk.END)
        text_CitizenID.insert('1.0', item['CitizenID'])

        text_BirthDate.delete('1.0', tk.END)
        text_BirthDate.insert('1.0', item['BirthDate'])  

        combo_Gender.set(item['Gender'])   

        text_PatientName_CN.delete('1.0', tk.END)
        text_PatientName_CN.insert('1.0', item['PatientName_CN'])

        text_ProbandName.delete('1.0', tk.END)
        text_ProbandName.insert('1.0', item['ProbandName'])

        text_proband_id.delete('1.0', tk.END)
        text_proband_id.insert('1.0', item['proband_id'])

        text_RelationshipOfProband.delete('1.0', tk.END)
        text_RelationshipOfProband.insert('1.0', item['RelationshipOfProband'])

        text_Telephone.delete('1.0', tk.END)
        text_Telephone.insert('1.0', item['Telephone'])

        text_Comments.delete('1.0', tk.END)
        text_Comments.insert('1.0', item['Comments'])

        text_Diagnosis1.delete('1.0', tk.END)
        text_Diagnosis1.insert('1.0', item['Diagnosis1'])

        text_Diagnosis2.delete('1.0', tk.END)
        text_Diagnosis2.insert('1.0', item['Diagnosis2'])

        text_Diagnosis3.delete('1.0', tk.END)
        text_Diagnosis3.insert('1.0', item['Diagnosis3'])

        text_Diagnosis4.delete('1.0', tk.END)
        text_Diagnosis4.insert('1.0', item['Diagnosis4'])

        text_Diagnosis5.delete('1.0', tk.END)
        text_Diagnosis5.insert('1.0', item['Diagnosis5'])

    def update_patients():
            try:
                id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()
                PatientName_in_patients_gotten = text_PatientName_in_patients.get('1.0', tk.END).rstrip()
                PatientName_CN_gotten = text_PatientName_CN.get('1.0', tk.END).rstrip()                
                Gender_gotten = combo_Gender.get().rstrip()

                ProbandName_gotten = text_ProbandName.get('1.0', tk.END).rstrip()
                proband_id =  text_proband_id.get('1.0', tk.END).rstrip()
                RelationshipOfProband_gotten = text_RelationshipOfProband.get('1.0', tk.END).rstrip()

                InPatientID_gotten = text_InPatientID.get('1.0', tk.END).rstrip()
                CitizenID_gotten = text_CitizenID.get('1.0', tk.END).rstrip()
                BirthDate_gotten = text_BirthDate.get('1.0', tk.END).rstrip() 

                Diagnosis1_gotten = text_Diagnosis1.get('1.0', tk.END).rstrip()
                Diagnosis2_gotten = text_Diagnosis2.get('1.0', tk.END).rstrip()
                Diagnosis3_gotten = text_Diagnosis3.get('1.0', tk.END).rstrip()
                Diagnosis4_gotten = text_Diagnosis4.get('1.0', tk.END).rstrip()
                Diagnosis5_gotten = text_Diagnosis5.get('1.0', tk.END).rstrip()

                Telephone_gotten = text_Telephone.get('1.0', tk.END).rstrip()
                Comments_gotten = text_Comments.get('1.0', tk.END).rstrip()

                Question_mark = '(' + '?, ' * 16 + '?)'

                cur.execute('DELETE FROM Patients WHERE id_in_patients = ?', (id_in_patients_gotten,))        
                conn.commit()

                Update_values = (id_in_patients_gotten,                          
                                 PatientName_in_patients_gotten,
                                 PatientName_CN_gotten, 
                                 Gender_gotten, 

                                 InPatientID_gotten, 
                                 CitizenID_gotten,                         
                                 BirthDate_gotten, 

                                 ProbandName_gotten, 
                                 proband_id, 
                                 RelationshipOfProband_gotten,                            

                                 Diagnosis1_gotten,
                                 Diagnosis2_gotten,
                                 Diagnosis3_gotten,
                                 Diagnosis4_gotten,
                                 Diagnosis5_gotten, 

                                 Telephone_gotten, 
                                 Comments_gotten)

                Update_Fields = '''(id_in_patients, PatientName_in_patients, PatientName_CN, Gender,

                InPatientID, CitizenID, BirthDate, 

                ProbandName, proband_id, RelationshipOfProband, 

                Diagnosis1, Diagnosis2, Diagnosis3, Diagnosis4, Diagnosis5, 
                Telephone, Comments)
                '''

                #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
                #('201706181718000444', 'PatientName, 'Serum'))

                cur.execute('INSERT INTO Patients '+ Update_Fields + ' VALUES ' + Question_mark, 
                            Update_values)
                conn.commit()  

                #messagebox.showinfo("Updated", "Patient's information successfully updated!")

                # //////////////////// Refresh the Table ///////////////////////////////////////////
                # Clear the table
                for i in table.get_children():
                    table.delete(i)

                # Refresh the whole database
                refreshDB()

                # Refresh variable combination

                sqlstr = 'SELECT * FROM Patients ORDER BY id_in_patients'
                spreadsheet = cur.execute(sqlstr)
                combination = []        
                for row in spreadsheet:
                    combination.append(row)

                # Display the table
                display_in_table(combination)

            except:
                pass

    def delete_patient():
        id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()

        if id_in_patients_gotten == '':
            messagebox.showinfo("Empty", "There's no patient's information to delete. Please make sure.")

        else:           
            result = messagebox.askquestion('Delete', 'Are you sure to delete this patient?', 
                                            icon='warning')

            if result == 'yes':
                cur.execute('DELETE FROM Patients WHERE id_in_patients = ?', (id_in_patients_gotten,))        
                conn.commit()            
                messagebox.showinfo("Deleted", "The patient's information has been deleted!")

                # //////////////////// Refresh the Table ///////////////////////////////////////////
                # Clear the table
                for i in table.get_children():
                    table.delete(i)

                # Refresh the whole database
                refreshDB()

                # Refresh variable combination

                sqlstr = 'SELECT * FROM Patients ORDER BY id_in_patients'
                spreadsheet = cur.execute(sqlstr)
                combination = []        
                for row in spreadsheet:
                    combination.append(row)

                # Display the table        
                display_in_table(combination)

    def patientNameSearch():
        PatientName_Search_gotten = text_PatientName_search.get('1.0', tk.END).rstrip()

        sqlstr = '''SELECT * FROM Patients WHERE PatientName_in_patients = ? 
        '''
        cur.execute(sqlstr, (PatientName_Search_gotten,))
        items = cur.fetchall()

        for i in table.get_children():
            table.delete(i)

        display_in_table(items)    

    def inPatientIDSearch():
        InPatientID_Search_gotten = text_InPatientID_search.get('1.0', tk.END).rstrip()        

        sqlstr = '''SELECT * FROM Patients WHERE InPatientID = ?  
        '''
        cur.execute(sqlstr, (InPatientID_Search_gotten,))
        items = cur.fetchall()

        for i in table.get_children():
            table.delete(i)

        display_in_table(items)

    def browse():
        # Refresh the whole database
        refreshDB()

        # Refresh variable combination

        sqlstr = 'SELECT * FROM Patients ORDER BY id_in_patients'
        spreadsheet = cur.execute(sqlstr)
        combination = []        
        for row in spreadsheet:
            combination.append(row)

        # Display the table
        display_in_table(combination)



    # //////////////////////////////////////////////////////
    # /////// Main Flow ////////////////////////////

    root_patients = tk.Toplevel(root)
    root_patients.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    #root.attributes('-fullscreen', True)
    root_patients.title('Patients')
    #root.iconbitmap('CharlestonParkIcon.ico')

    # set the dimensions of the screen 
    # and where it is placed



     ### Multicolumn Listbox

    # Multicolumn Listbox/////////////////////////////////////////////////////////////////////////////
    table = ttk.Treeview(root_patients, height="20", columns=headers_patients, selectmode="extended")
    table.pack(padx=10, pady=20, ipadx=1200, ipady=200)


    i = 1
    header_width = [30] * 21

    for header_patient in headers_patients:
        table.heading('#'+str(i), text=header_patient.title(), anchor=tk.W, command=lambda c=header_patient: sortby(table, c, 0))
        table.column('#'+str(i), stretch=tk.NO, minwidth=0, width=tkf.Font().measure(header_patient.title())+header_width[i-1])
        i+=1    
    table.column('#0', stretch=tk.NO, minwidth=0, width=0)

    table.bind("<Double-1>", OnDoubleClick)
    #///////////////////////////////////////////////////////////////////////////////////////////

    # Scrollbar////////////////////////////////////////////////////////////////////////////////////////
    vsb = ttk.Scrollbar(table, orient = "vertical",  command = table.yview)
    hsb = ttk.Scrollbar(table, orient = "horizontal", command = table.xview)
    ## Link scrollbars activation to top-level object
    table.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
    ## Link scrollbar also to every columns
    map(lambda col: col.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set), table)
    vsb.pack(side = tk.RIGHT, fill = tk.Y)
    hsb.pack(side = tk.BOTTOM, fill = tk.X) 





    # ///////////////Patients///////////////

    y_origin = 530
    gain = 50
    i = 0

     # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_Patients=tk.Label(root_patients,width=230, height=25 , relief='raised', borderwidth=1)
    label_Patients.place(x=10,y=y_origin+i*gain-40)

    # ///////////// Routine Edits////////////////      

    text_id_in_patients = tk.Text(root_patients, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_id_in_patients.place(x=640, y=y_origin+i*gain)
    label_id_in_patients = tk.Label(root_patients, text='id_patients:', font=LABEL_FONT)
    label_id_in_patients.place(x=640,y=y_origin+i*gain-25)

    text_PatientName_CN = tk.Text(root_patients, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_CN.place(x=40, y=y_origin+i*gain)
    label_PatientName_CN = tk.Label(root_patients, text='Patient\'s Chinese Name:', font=LABEL_FONT)
    label_PatientName_CN.place(x=40,y=y_origin+i*gain-25)

    text_PatientName_in_patients = tk.Text(root_patients, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_in_patients.place(x=240, y=y_origin+i*gain)
    label_PatientName_in_patients = tk.Label(root_patients, text='Patient\' Name:', font=LABEL_FONT)
    label_PatientName_in_patients.place(x=240,y=y_origin+i*gain-25)

    text_num = tk.Text(root_patients, width=8, height=1, font=EDIT_FONT, wrap='none')
    text_num.place(x=1120, y=y_origin+i*gain)

    i = 1

    combo_Gender = ttk.Combobox(root_patients, width=20, height=1, font=EDIT_FONT)
    combo_Gender.place(x=40, y=y_origin+i*gain)
    label_Gender = tk.Label(root_patients, text='Gender:', font=LABEL_FONT)
    label_Gender.place(x=40,y=y_origin+i*gain-25)
    combo_Gender['values'] = ('Male', 'Female', 'Other')
    combo_Gender['state'] = 'readonly'

    text_ProbandName = tk.Text(root_patients, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_ProbandName.place(x=240, y=y_origin+i*gain)
    label_ProbandName = tk.Label(root_patients, text='Proband Name:', font=LABEL_FONT)
    label_ProbandName.place(x=240,y=y_origin+i*gain-25)

    text_proband_id = tk.Text(root_patients, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_proband_id.place(x=440, y=y_origin+i*gain)
    label_proband_id = tk.Label(root_patients, text='Proband ID:', font=LABEL_FONT)
    label_proband_id.place(x=440,y=y_origin+i*gain-25)

    text_RelationshipOfProband = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_RelationshipOfProband.place(x=640, y=y_origin+i*gain)
    label_RelationshipOfProband = tk.Label(root_patients, text='Relationship of Proband:', font=LABEL_FONT)
    label_RelationshipOfProband.place(x=640,y=y_origin+i*gain-25)

    i = 2

    text_InPatientID = tk.Text(root_patients, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_InPatientID.place(x=40, y=y_origin+i*gain)
    label_InPatientID = tk.Label(root_patients, text='In-Patient ID:', font=LABEL_FONT)
    label_InPatientID.place(x=40,y=y_origin+i*gain-25)

    text_CitizenID = tk.Text(root_patients, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_CitizenID.place(x=240, y=y_origin+i*gain)
    label_CitizenID = tk.Label(root_patients, text='Citizen ID:', font=LABEL_FONT)
    label_CitizenID.place(x=240,y=y_origin+i*gain-25)

    text_BirthDate = tk.Text(root_patients, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_BirthDate.place(x=440, y=y_origin+i*gain)
    label_BirthDate = tk.Label(root_patients, text='Birth Date:', font=LABEL_FONT)
    label_BirthDate.place(x=440,y=y_origin+i*gain-25)

    i = 3

    text_Diagnosis1 = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis1.place(x=40, y=y_origin+i*gain)
    label_Diagnosis1 = tk.Label(root_patients, text='Diagnosis 1:', font=LABEL_FONT)
    label_Diagnosis1.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis2 = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis2.place(x=340, y=y_origin+i*gain)
    label_Diagnosis2 = tk.Label(root_patients, text='Diagnosis 2:', font=LABEL_FONT)
    label_Diagnosis2.place(x=340,y=y_origin+i*gain-25)

    text_Diagnosis3 = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis3.place(x=640, y=y_origin+i*gain)
    label_Diagnosis3 = tk.Label(root_patients, text='Diagnosis 3:', font=LABEL_FONT)
    label_Diagnosis3.place(x=640,y=y_origin+i*gain-25)

    i = 4

    text_Diagnosis4 = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis4.place(x=40, y=y_origin+i*gain)
    label_Diagnosis4 = tk.Label(root_patients, text='Diagnosis 4:', font=LABEL_FONT)
    label_Diagnosis4.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis5 = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis5.place(x=340, y=y_origin+i*gain)
    label_Diagnosis5 = tk.Label(root_patients, text='Diagnosis 5:', font=LABEL_FONT)
    label_Diagnosis5.place(x=340,y=y_origin+i*gain-25)

    i = 5

    text_Telephone = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Telephone.place(x=40, y=y_origin+i*gain)
    label_Telephone = tk.Label(root_patients, text='Telephone:', font=LABEL_FONT)
    label_Telephone.place(x=40,y=y_origin+i*gain-25)

    i = 6

    text_Comments = tk.Text(root_patients, width=140, height=1, font=EDIT_FONT, wrap='none')
    text_Comments.place(x=40, y=y_origin+i*gain)
    label_Comments = tk.Label(root_patients, text='Comments:', font=LABEL_FONT)
    label_Comments.place(x=40,y=y_origin+i*gain-25)

    # ////// Buttons //////////////////////////

    button_update_sample = ttk.Button(root_patients, text='Update', width=10, command=update_patients)
    button_update_sample.place(x=640, y=670)

    button_delete_sample = ttk.Button(root_patients, text='Delete', width=10, command=delete_patient)
    button_delete_sample.place(x=800, y=670)

    button_exit = ttk.Button(root_patients, text='Exit', width=10, command=root_patients.destroy)
    button_exit.place(x=1250, y=790)

    # //////// Search Area ////////////

    i = 0

    button_browse = ttk.Button(root_patients, text='Browse', width=10, command=browse)
    button_browse.place(x=1240, y=y_origin+i*gain-5)

    i = 2

    text_InPatientID_search = tk.Text(root_patients, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_InPatientID_search.place(x=1060, y=y_origin+i*gain)
    label_InPatientID_search = tk.Label(root_patients, text='Paitnet ID:', font=LABEL_FONT)
    label_InPatientID_search.place(x=1060,y=y_origin+i*gain-25)

    button_InPatientID_search = ttk.Button(root_patients, text='Search', width=8, command=inPatientIDSearch)
    button_InPatientID_search.place(x=1250, y=y_origin+i*gain-5)

    i = 3

    text_PatientName_search = tk.Text(root_patients, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_search.place(x=1060, y=y_origin+i*gain)
    label_PatientName_search = tk.Label(root_patients, text='Paitnet Name:', font=LABEL_FONT)
    label_PatientName_search.place(x=1060,y=y_origin+i*gain-25)

    button_PatientName_search = ttk.Button(root_patients, text='Search', width=8, command=patientNameSearch)
    button_PatientName_search.place(x=1250, y=y_origin+i*gain-5)

    # ///// Browse Automatically /////////////////////

    display_in_table(combination)

    show_modal_window(root_patients, root)


# In[26]:


def update_HCM():   
    try:   

        id_in_HCM_gotten = text_id_in_HCM.get('1.0', tk.END).rstrip()       
        EnrollmentDate_gotten = text_EnrollmentDate.get('1.0', tk.END).rstrip()         
        IsObstructiveResting_gotten = combo_IsObstructiveResting.get().rstrip()
        IsObstructiveValsalva_gotten = combo_IsObstructiveValsalva.get().rstrip()        
        PatientName_in_HCM_gotten = text_PatientName_in_HCM.get('1.0', tk.END).rstrip()
        Diabetes_gotten = text_Diabetes.get('1.0', tk.END).rstrip()
        Hypertension_gotten = text_Hypertension.get('1.0', tk.END).rstrip()       
        Stroke_gotten = text_Stroke.get('1.0', tk.END).rstrip()   
        Renal_gotten = text_Renal.get('1.0', tk.END).rstrip()   
        IsDyspnea_gotten = combo_IsDyspnea.get().rstrip()     
        IsChestPain_gotten = combo_IsChestPain.get().rstrip()     
        IsSyncope_gotten = combo_IsSyncope.get().rstrip()     
        NYHA_gotten = combo_NYHA.get().rstrip()      
        QualityOfLifeScore_gotten = text_QualityOfLifeScore.get('1.0', tk.END).rstrip() 


        update_sql = """
            UPDATE HCM SET
            PatientName_in_HCM = ?,
            EnrollmentDate = ?,
            IsObstructiveResting = ?,
            IsObstructiveValsalva = ?,
            Hypertension = ?,
            Diabetes = ?,
            Stroke = ?,
            Renal = ?,
            IsDyspnea = ?,
            IsChestPain = ?,
            IsSyncope = ?,
            NYHA = ?,
            QualityOfLifeScore = ?
            WHERE id_in_HCM = ?
            """

        update_values = (
            PatientName_in_HCM_gotten,
            EnrollmentDate_gotten,
            IsObstructiveResting_gotten,
            IsObstructiveValsalva_gotten,
            Hypertension_gotten,
            Diabetes_gotten,
            Stroke_gotten,
            Renal_gotten,
            IsDyspnea_gotten,
            IsChestPain_gotten,
            IsSyncope_gotten,
            NYHA_gotten,
            QualityOfLifeScore_gotten,
            id_in_HCM_gotten  # WHERE 条件放在最后
        )

        cur.execute(update_sql, update_values)
        conn.commit()

        messagebox.showinfo("Updated", "HCM Trial information successfully updated!")
        clear()
        refreshDB()
        display_in_table(combination)

    except:
        pass


# In[27]:


def update_patients():
    #try:   
        id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()
        PatientName_CN_gotten = text_PatientName_CN.get('1.0', tk.END).rstrip()     
        PatientName_in_patients_gotten = text_PatientName_in_patients.get('1.0', tk.END).rstrip()  
        Gender_gotten = combo_Gender.get().rstrip()
        BirthDate_gotten = text_BirthDate.get('1.0', tk.END).rstrip() 
        InPatientID_gotten = text_InPatientID.get('1.0', tk.END).rstrip()
        CitizenID_gotten = text_CitizenID.get('1.0', tk.END).rstrip()
        FamilyHistory_gotten = text_FamilyHistory.get('1.0', tk.END).rstrip()
        IsInsurance_gotten = combo_IsInsurance.get().rstrip()
        Marriage_gotten = combo_Marriage.get().rstrip()
        Education_gotten = text_Education.get('1.0', tk.END).rstrip()
        Height_gotten = text_Height.get('1.0', tk.END).rstrip()
        BodyWeight_gotten = text_BodyWeight.get('1.0', tk.END).rstrip()

        Diagnosis1_gotten = text_Diagnosis1.get('1.0', tk.END).rstrip()
        Diagnosis2_gotten = text_Diagnosis2.get('1.0', tk.END).rstrip()
        Diagnosis3_gotten = text_Diagnosis3.get('1.0', tk.END).rstrip()
        Diagnosis4_gotten = text_Diagnosis4.get('1.0', tk.END).rstrip()
        Diagnosis5_gotten = text_Diagnosis5.get('1.0', tk.END).rstrip()        
        Telephone1_gotten = text_Telephone1.get('1.0', tk.END).rstrip()
        Telephone2_gotten = text_Telephone2.get('1.0', tk.END).rstrip()
        Comments_gotten = text_Comments.get('1.0', tk.END).rstrip()

        update_sql = """
            UPDATE PATIENTS SET
            PatientName_CN = ?,
            PatientName_in_patients = ?,
            Gender = ?,
            BirthDate = ?,
            InPatientID = ?,
            CitizenID = ?,
            FamilyHistory = ?,
            IsInsurance = ?,
            Marriage = ?,
            Education = ?,
            Height = ?,
            BodyWeight = ?,            
            Diagnosis1 = ?,
            Diagnosis2 = ?,
            Diagnosis3 = ?,
            Diagnosis4 = ?,
            Diagnosis5 = ?,
            Telephone1 = ?,
            Telephone2 = ?,
            Comments = ?          
            WHERE id_in_patients = ?
            """

        update_values = (
            PatientName_CN_gotten,    
            PatientName_in_patients_gotten,
            Gender_gotten,
            BirthDate_gotten,
            InPatientID_gotten,
            CitizenID_gotten,
            FamilyHistory_gotten,
            IsInsurance_gotten,
            Marriage_gotten,
            Education_gotten,
            Height_gotten,
            BodyWeight_gotten,            
            Diagnosis1_gotten,
            Diagnosis2_gotten,
            Diagnosis3_gotten,
            Diagnosis4_gotten,
            Diagnosis5_gotten,
            Telephone1_gotten,
            Telephone2_gotten,
            Comments_gotten,
            id_in_patients_gotten  # WHERE 条件放在最后
        )

        cur.execute(update_sql, update_values)
        conn.commit()

        messagebox.showinfo("Updated", "The Patient information successfully updated!")
        clear()
        refreshDB()
        display_in_table(combination)


    #except:
        #pass


# In[28]:


def new_HCM():
    root_new_HCM = tk.Toplevel(root)

    w = 1080
    h = 320

    ws = root_new_HCM.winfo_screenwidth()
    hs = root_new_HCM.winfo_screenheight()

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root_new_HCM.geometry('%dx%d+%d+%d' % (w, h, x, y))   
    root_new_HCM.title('New HCM Case')

    # 生成唯一ID（基于时间戳）
    time_text = str(datetime.datetime.now())
    id = ''
    for t in time_text:
        if t not in ' -:.':
            id += t

    def create():
        try:
            # 获取所有字段值
            id_in_HCM_gotten = int(text_id_in_HCM.get('1.0', tk.END).strip())
            PatientName_in_HCM_gotten = text_PatientName_in_HCM.get('1.0', tk.END).strip()
            IsObstructiveResting_gotten = combo_IsObstructiveResting.get().strip()
            IsObstructiveValsalva_gotten = combo_IsObstructiveValsalva.get().strip()
            CitizenID_gotten = text_CitizenID.get('1.0', tk.END).strip()
            EnrollmentDate_gotten = text_EnrollmentDate.get('1.0', tk.END).strip()

            # 检查必填字段
            if not id_in_HCM_gotten:
                messagebox.showwarning("Warning", "ID cannot be empty!")
                return
            if not PatientName_in_HCM_gotten:
                messagebox.showwarning("Warning", "Patient Name cannot be empty!")
                return

            # 修正SQL语句
            update_sql = """
                INSERT INTO HCM (
                    id_in_HCM, 
                    PatientName_in_HCM, 
                    IsObstructiveResting,
                    IsObstructiveValsalva, 
                    CitizenID, 
                    EnrollmentDate
                ) VALUES (?, ?, ?, ?, ?, ?)
            """

            update_values = (
                id_in_HCM_gotten,
                PatientName_in_HCM_gotten,
                IsObstructiveResting_gotten,
                IsObstructiveValsalva_gotten,
                CitizenID_gotten,
                EnrollmentDate_gotten
            )

            cur.execute(update_sql, update_values)
            conn.commit()

            messagebox.showinfo("Success", "HCM record successfully created!")

            # 清理和刷新
            clear()
            refreshDB()
            display_in_table(combination)
            root_new_HCM.destroy()

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", f"Duplicate ID or data type mismatch: {e}")
            print(f"Integrity Error: {e}")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to create record: {e}")
            print(f"SQL Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            import traceback
            traceback.print_exc()

    # UI布局
    y_origin = 100
    gain = 55
    i = 0

    # 背景框
    label_new_HCM = tk.Label(root_new_HCM, width=150, height=10, relief='raised', borderwidth=1)
    label_new_HCM.place(x=10, y=y_origin+i*gain-40)

    # ID字段（自动生成，不可编辑或只读）
    text_id_in_HCM = tk.Text(root_new_HCM, width=26, height=1, font=EDIT_FONT, wrap='none')
    text_id_in_HCM.place(x=40, y=y_origin+i*gain)
    label_id_in_HCM = tk.Label(root_new_HCM, text='HCM ID:', font=LABEL_FONT)
    label_id_in_HCM.place(x=40, y=y_origin+i*gain-25)
    text_id_in_HCM.insert('1.0', id[:16])
    # 如果需要设置为只读：
    # text_id_in_HCM.config(state='disabled')

    text_PatientName_in_HCM = tk.Text(root_new_HCM, width=26, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_in_HCM.place(x=240, y=y_origin+i*gain)
    label_PatientName_HCM = tk.Label(root_new_HCM, text='Patient Name:', font=LABEL_FONT)
    label_PatientName_HCM.place(x=240, y=y_origin+i*gain-25)

    combo_IsObstructiveResting = ttk.Combobox(root_new_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsObstructiveResting.place(x=440, y=y_origin+i*gain)
    label_IsObstructiveResting = tk.Label(root_new_HCM, text='Obstructive during Rest?', font=LABEL_FONT)
    label_IsObstructiveResting.place(x=440, y=y_origin+i*gain-25)
    combo_IsObstructiveResting['values'] = ('Yes', 'No', 'Unknown')
    combo_IsObstructiveResting.set('Unknown')  # 设置默认值

    combo_IsObstructiveValsalva = ttk.Combobox(root_new_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsObstructiveValsalva.place(x=640, y=y_origin+i*gain)
    label_IsObstructiveValsalva = tk.Label(root_new_HCM, text='Obstructive during Valsalva?', font=LABEL_FONT)
    label_IsObstructiveValsalva.place(x=640, y=y_origin+i*gain-25)
    combo_IsObstructiveValsalva['values'] = ('Yes', 'No', 'Unknown')
    combo_IsObstructiveValsalva.set('Unknown')

    i = 1

    text_CitizenID = tk.Text(root_new_HCM, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_CitizenID.place(x=40, y=y_origin+i*gain)
    label_CitizenID = tk.Label(root_new_HCM, text='Citizen ID:', font=LABEL_FONT)
    label_CitizenID.place(x=40, y=y_origin+i*gain-25)

    text_EnrollmentDate = tk.Text(root_new_HCM, width=26, height=1, font=EDIT_FONT, wrap='none')
    text_EnrollmentDate.place(x=440, y=y_origin+i*gain)
    label_EnrollmentDate = tk.Label(root_new_HCM, text='Enrollment Date (YYYY-MM-DD):', font=LABEL_FONT)
    label_EnrollmentDate.place(x=440, y=y_origin+i*gain-25)
    # 可选：自动填充当前日期
    # text_EnrollmentDate.insert('1.0', datetime.datetime.now().strftime('%Y-%m-%d'))

    i = 3

    button_add = ttk.Button(root_new_HCM, text='Create', width=15, command=create)
    button_add.place(x=300, y=y_origin+i*gain)

    button_cancel = ttk.Button(root_new_HCM, text='Cancel', width=15, command=root_new_HCM.destroy)
    button_cancel.place(x=650, y=y_origin+i*gain)

    show_modal_window(root_new_HCM, root)


# In[29]:


def new_patient():
    root_new_patient = tk.Toplevel(root)

    w = 980 # width for the Tk root
    h = 540 # height for the Tk root

    # get screen width and height
    ws = root_new_patient.winfo_screenwidth() # width of the screen
    hs = root_new_patient.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root_new_patient.geometry('%dx%d+%d+%d' % (w, h, x, y))   
    root_new_patient.title('New Patient')

    time_text = str(datetime.datetime.now())
    id = ''
    for t in time_text:
        if t!=' 'and t!= '-' and t != ':' and t != '.':
            id += t

    def create():
        try:            
            PatientName_in_patients_gotten = text_PatientName_in_patients.get('1.0', tk.END).rstrip()
            PatientName_CN_gotten = text_PatientName_CN.get('1.0', tk.END).rstrip()                
            Gender_gotten = combo_Gender.get().rstrip()

            ProbandName_gotten = text_ProbandName.get('1.0', tk.END).rstrip()
            proband_id =  text_proband_id.get('1.0', tk.END).rstrip()
            RelationshipOfProband_gotten = text_RelationshipOfProband.get('1.0', tk.END).rstrip()

            InPatientID_gotten = text_InPatientID.get('1.0', tk.END).rstrip()
            CitizenID_gotten = text_CitizenID.get('1.0', tk.END).rstrip()
            BirthDate_gotten = text_BirthDate.get('1.0', tk.END).rstrip() 

            Diagnosis1_gotten = text_Diagnosis1.get('1.0', tk.END).rstrip()
            Diagnosis2_gotten = text_Diagnosis2.get('1.0', tk.END).rstrip()
            Diagnosis3_gotten = text_Diagnosis3.get('1.0', tk.END).rstrip()
            Diagnosis4_gotten = text_Diagnosis4.get('1.0', tk.END).rstrip()
            Diagnosis5_gotten = text_Diagnosis5.get('1.0', tk.END).rstrip()

            Telephone_gotten = text_Telephone.get('1.0', tk.END).rstrip()
            Comments_gotten = text_Comments.get('1.0', tk.END).rstrip()

            Question_mark = '(' + '?, ' * 15 + '?)'

            Update_values = (PatientName_in_patients_gotten,
                             PatientName_CN_gotten, 
                             Gender_gotten, 

                             InPatientID_gotten, 
                             CitizenID_gotten,                         
                             BirthDate_gotten, 

                             ProbandName_gotten, 
                             proband_id, 
                             RelationshipOfProband_gotten,                            

                             Diagnosis1_gotten,
                             Diagnosis2_gotten,
                             Diagnosis3_gotten,
                             Diagnosis4_gotten,
                             Diagnosis5_gotten, 

                             Telephone_gotten, 
                             Comments_gotten)

            Update_Fields = '''(PatientName_in_patients, PatientName_CN, Gender,

            InPatientID, CitizenID, BirthDate, 

            ProbandName, proband_id, RelationshipOfProband, 

            Diagnosis1, Diagnosis2, Diagnosis3, Diagnosis4, Diagnosis5, 
            Telephone, Comments)
            '''

            #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
            #('201706181718000444', 'PatientName, 'Serum'))

            cur.execute('INSERT INTO Patients '+ Update_Fields + ' VALUES ' + Question_mark, 
                        Update_values)
            conn.commit()  

            messagebox.showinfo("Created", "Patient's information successfully created!")

            clear()
            refreshDB()
            display_in_table(combination)
            root_new_patient.destroy()

        except:
            pass

    # ///////// Main Stream ////////////////////////

    y_origin = 80
    gain = 50
    i = 0

     # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_Patients=tk.Label(root_new_patient,width=135, height=23 , relief='raised', borderwidth=1)
    label_Patients.place(x=10,y=y_origin+i*gain-40)

    # ///////////// Routine Edits////////////////          

    text_PatientName_CN = tk.Text(root_new_patient, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_CN.place(x=40, y=y_origin+i*gain)
    label_PatientName_CN = tk.Label(root_new_patient, text='Patient\'s Chinese Name:', font=LABEL_FONT)
    label_PatientName_CN.place(x=40,y=y_origin+i*gain-25)

    text_PatientName_in_patients = tk.Text(root_new_patient, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_in_patients.place(x=240, y=y_origin+i*gain)
    label_PatientName_in_patients = tk.Label(root_new_patient, text='Patient\' Name:', font=LABEL_FONT)
    label_PatientName_in_patients.place(x=240,y=y_origin+i*gain-25)

    i = 1

    combo_Gender = ttk.Combobox(root_new_patient, width=20, height=1, font=EDIT_FONT)
    combo_Gender.place(x=40, y=y_origin+i*gain)
    label_Gender = tk.Label(root_new_patient, text='Gender:', font=LABEL_FONT)
    label_Gender.place(x=40,y=y_origin+i*gain-25)
    combo_Gender['values'] = ('Male', 'Female', 'Other')
    combo_Gender['state'] = 'readonly'

    text_ProbandName = tk.Text(root_new_patient, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_ProbandName.place(x=240, y=y_origin+i*gain)
    label_ProbandName = tk.Label(root_new_patient, text='Proband Name:', font=LABEL_FONT)
    label_ProbandName.place(x=240,y=y_origin+i*gain-25)

    text_proband_id = tk.Text(root_new_patient, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_proband_id.place(x=440, y=y_origin+i*gain)
    label_proband_id = tk.Label(root_new_patient, text='Proband ID:', font=LABEL_FONT)
    label_proband_id.place(x=440,y=y_origin+i*gain-25)

    text_RelationshipOfProband = tk.Text(root_new_patient, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_RelationshipOfProband.place(x=640, y=y_origin+i*gain)
    label_RelationshipOfProband = tk.Label(root_new_patient, text='Relationship of Proband:', font=LABEL_FONT)
    label_RelationshipOfProband.place(x=640,y=y_origin+i*gain-25)

    i = 2

    text_InPatientID = tk.Text(root_new_patient, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_InPatientID.place(x=40, y=y_origin+i*gain)
    label_InPatientID = tk.Label(root_new_patient, text='In-Patient ID:', font=LABEL_FONT)
    label_InPatientID.place(x=40,y=y_origin+i*gain-25)

    text_CitizenID = tk.Text(root_new_patient, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_CitizenID.place(x=240, y=y_origin+i*gain)
    label_CitizenID = tk.Label(root_new_patient, text='Citizen ID:', font=LABEL_FONT)
    label_CitizenID.place(x=240,y=y_origin+i*gain-25)


    text_BirthDate = tk.Text(root_new_patient, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_BirthDate.place(x=440, y=y_origin+i*gain)
    label_BirthDate = tk.Label(root_new_patient, text='Birth Date:', font=LABEL_FONT)
    label_BirthDate.place(x=440,y=y_origin+i*gain-25)

    i = 3

    text_Diagnosis1 = tk.Text(root_new_patient, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis1.place(x=40, y=y_origin+i*gain)
    label_Diagnosis1 = tk.Label(root_new_patient, text='Diagnosis 1:', font=LABEL_FONT)
    label_Diagnosis1.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis2 = tk.Text(root_new_patient, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis2.place(x=340, y=y_origin+i*gain)
    label_Diagnosis2 = tk.Label(root_new_patient, text='Diagnosis 2:', font=LABEL_FONT)
    label_Diagnosis2.place(x=340,y=y_origin+i*gain-25)

    text_Diagnosis3 = tk.Text(root_new_patient, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis3.place(x=640, y=y_origin+i*gain)
    label_Diagnosis3 = tk.Label(root_new_patient, text='Diagnosis 3:', font=LABEL_FONT)
    label_Diagnosis3.place(x=640,y=y_origin+i*gain-25)

    i = 4

    text_Diagnosis4 = tk.Text(root_new_patient, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis4.place(x=40, y=y_origin+i*gain)
    label_Diagnosis4 = tk.Label(root_new_patient, text='Diagnosis 4:', font=LABEL_FONT)
    label_Diagnosis4.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis5 = tk.Text(root_new_patient, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis5.place(x=340, y=y_origin+i*gain)
    label_Diagnosis5 = tk.Label(root_new_patient, text='Diagnosis 5:', font=LABEL_FONT)
    label_Diagnosis5.place(x=340,y=y_origin+i*gain-25)

    i = 5

    text_Telephone = tk.Text(root_new_patient, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Telephone.place(x=40, y=y_origin+i*gain)
    label_Telephone = tk.Label(root_new_patient, text='Telephone:', font=LABEL_FONT)
    label_Telephone.place(x=40,y=y_origin+i*gain-25)

    i = 6

    text_Comments = tk.Text(root_new_patient, width=140, height=1, font=EDIT_FONT, wrap='none')
    text_Comments.place(x=40, y=y_origin+i*gain)
    label_Comments = tk.Label(root_new_patient, text='Comments:', font=LABEL_FONT)
    label_Comments.place(x=40,y=y_origin+i*gain-25)

    i = 8 

    button_add=ttk.Button(root_new_patient, text='Create', width=15, command=create)
    button_add.place(x=250, y=y_origin+i*gain)

    button_cancel=ttk.Button(root_new_patient, text='Cancel', width=15, command=root_new_patient.destroy)
    button_cancel.place(x=600, y=y_origin+i*gain)      

    show_modal_window(root_new_patient, root)

    #t = datetime.datetime.now()
    #ts = str(datetime.datetime.now())

    #datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')


# In[30]:


def new_followUp():
    root_followUp = tk.Toplevel(root)

    w = 980 # width for the Tk root
    h = 540 # height for the Tk root

    # get screen width and height
    ws = root_followUp.winfo_screenwidth() # width of the screen
    hs = root_followUp.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    root_followUp.geometry('%dx%d+%d+%d' % (w, h, x, y))   
    root_followUp.title('New Patient')

    time_text = str(datetime.datetime.now())
    id = ''
    for t in time_text:
        if t!=' 'and t!= '-' and t != ':' and t != '.':
            id += t

    def create():
        try:            
            PatientName_in_patients_gotten = text_PatientName_in_patients.get('1.0', tk.END).rstrip()
            PatientName_CN_gotten = text_PatientName_CN.get('1.0', tk.END).rstrip()                
            Gender_gotten = combo_Gender.get().rstrip()

            ProbandName_gotten = text_ProbandName.get('1.0', tk.END).rstrip()
            proband_id =  text_proband_id.get('1.0', tk.END).rstrip()
            RelationshipOfProband_gotten = text_RelationshipOfProband.get('1.0', tk.END).rstrip()

            InPatientID_gotten = text_InPatientID.get('1.0', tk.END).rstrip()
            CitizenID_gotten = text_CitizenID.get('1.0', tk.END).rstrip()
            BirthDate_gotten = text_BirthDate.get('1.0', tk.END).rstrip() 

            Diagnosis1_gotten = text_Diagnosis1.get('1.0', tk.END).rstrip()
            Diagnosis2_gotten = text_Diagnosis2.get('1.0', tk.END).rstrip()
            Diagnosis3_gotten = text_Diagnosis3.get('1.0', tk.END).rstrip()
            Diagnosis4_gotten = text_Diagnosis4.get('1.0', tk.END).rstrip()
            Diagnosis5_gotten = text_Diagnosis5.get('1.0', tk.END).rstrip()

            Telephone_gotten = text_Telephone.get('1.0', tk.END).rstrip()
            Comments_gotten = text_Comments.get('1.0', tk.END).rstrip()

            Question_mark = '(' + '?, ' * 15 + '?)'

            Update_values = (PatientName_in_patients_gotten,
                             PatientName_CN_gotten, 
                             Gender_gotten, 

                             InPatientID_gotten, 
                             CitizenID_gotten,                         
                             BirthDate_gotten, 

                             ProbandName_gotten, 
                             proband_id, 
                             RelationshipOfProband_gotten,                            

                             Diagnosis1_gotten,
                             Diagnosis2_gotten,
                             Diagnosis3_gotten,
                             Diagnosis4_gotten,
                             Diagnosis5_gotten, 

                             Telephone_gotten, 
                             Comments_gotten)

            Update_Fields = '''(PatientName_in_patients, PatientName_CN, Gender,

            InPatientID, CitizenID, BirthDate, 

            ProbandName, proband_id, RelationshipOfProband, 

            Diagnosis1, Diagnosis2, Diagnosis3, Diagnosis4, Diagnosis5, 
            Telephone, Comments)
            '''

            #cur.execute('INSERT INTO BloodSamples (SampleID, PatientName, SampleType) VALUES (?, ?, ?)', 
            #('201706181718000444', 'PatientName, 'Serum'))

            cur.execute('INSERT INTO Patients '+ Update_Fields + ' VALUES ' + Question_mark, 
                        Update_values)
            conn.commit()  

            messagebox.showinfo("Created", "Patient's information successfully created!")

            clear()
            refreshDB()
            display_in_table(combination)
            root_new_patient.destroy()

        except:
            pass

    # ///////// Main Stream ////////////////////////

    y_origin = 80
    gain = 50
    i = 0

     # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_Patients=tk.Label(root_followUp,width=135, height=23 , relief='raised', borderwidth=1)
    label_Patients.place(x=10,y=y_origin+i*gain-40)

    # ///////////// Routine Edits////////////////          

    text_PatientName_CN = tk.Text(root_followUp, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_CN.place(x=40, y=y_origin+i*gain)
    label_PatientName_CN = tk.Label(root_followUp, text='Patient\'s Chinese Name:', font=LABEL_FONT)
    label_PatientName_CN.place(x=40,y=y_origin+i*gain-25)

    text_PatientName_in_patients = tk.Text(root_followUp, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_in_patients.place(x=240, y=y_origin+i*gain)
    label_PatientName_in_patients = tk.Label(root_followUp, text='Patient\' Name:', font=LABEL_FONT)
    label_PatientName_in_patients.place(x=240,y=y_origin+i*gain-25)

    i = 1

    combo_Gender = ttk.Combobox(root_followUp, width=20, height=1, font=EDIT_FONT)
    combo_Gender.place(x=40, y=y_origin+i*gain)
    label_Gender = tk.Label(root_followUp, text='Gender:', font=LABEL_FONT)
    label_Gender.place(x=40,y=y_origin+i*gain-25)
    combo_Gender['values'] = ('Male', 'Female', 'Other')
    combo_Gender['state'] = 'readonly'

    text_ProbandName = tk.Text(root_followUp, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_ProbandName.place(x=240, y=y_origin+i*gain)
    label_ProbandName = tk.Label(root_followUp, text='Proband Name:', font=LABEL_FONT)
    label_ProbandName.place(x=240,y=y_origin+i*gain-25)

    text_proband_id = tk.Text(root_followUp, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_proband_id.place(x=440, y=y_origin+i*gain)
    label_proband_id = tk.Label(root_followUp, text='Proband ID:', font=LABEL_FONT)
    label_proband_id.place(x=440,y=y_origin+i*gain-25)

    text_RelationshipOfProband = tk.Text(root_followUp, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_RelationshipOfProband.place(x=640, y=y_origin+i*gain)
    label_RelationshipOfProband = tk.Label(root_followUp, text='Relationship of Proband:', font=LABEL_FONT)
    label_RelationshipOfProband.place(x=640,y=y_origin+i*gain-25)

    i = 2

    text_InPatientID = tk.Text(root_followUp, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_InPatientID.place(x=40, y=y_origin+i*gain)
    label_InPatientID = tk.Label(root_followUp, text='In-Patient ID:', font=LABEL_FONT)
    label_InPatientID.place(x=40,y=y_origin+i*gain-25)

    text_CitizenID = tk.Text(root_followUp, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_CitizenID.place(x=240, y=y_origin+i*gain)
    label_CitizenID = tk.Label(root_followUp, text='Citizen ID:', font=LABEL_FONT)
    label_CitizenID.place(x=240,y=y_origin+i*gain-25)


    text_BirthDate = tk.Text(root_followUp, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_BirthDate.place(x=440, y=y_origin+i*gain)
    label_BirthDate = tk.Label(root_followUp, text='Birth Date:', font=LABEL_FONT)
    label_BirthDate.place(x=440,y=y_origin+i*gain-25)

    i = 3

    text_Diagnosis1 = tk.Text(root_followUp, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis1.place(x=40, y=y_origin+i*gain)
    label_Diagnosis1 = tk.Label(root_followUp, text='Diagnosis 1:', font=LABEL_FONT)
    label_Diagnosis1.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis2 = tk.Text(root_followUp, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis2.place(x=340, y=y_origin+i*gain)
    label_Diagnosis2 = tk.Label(root_followUp, text='Diagnosis 2:', font=LABEL_FONT)
    label_Diagnosis2.place(x=340,y=y_origin+i*gain-25)

    text_Diagnosis3 = tk.Text(root_followUp, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis3.place(x=640, y=y_origin+i*gain)
    label_Diagnosis3 = tk.Label(root_followUp, text='Diagnosis 3:', font=LABEL_FONT)
    label_Diagnosis3.place(x=640,y=y_origin+i*gain-25)

    i = 4

    text_Diagnosis4 = tk.Text(root_followUp, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis4.place(x=40, y=y_origin+i*gain)
    label_Diagnosis4 = tk.Label(root_followUp, text='Diagnosis 4:', font=LABEL_FONT)
    label_Diagnosis4.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis5 = tk.Text(root_followUp, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis5.place(x=340, y=y_origin+i*gain)
    label_Diagnosis5 = tk.Label(root_followUp, text='Diagnosis 5:', font=LABEL_FONT)
    label_Diagnosis5.place(x=340,y=y_origin+i*gain-25)

    i = 5

    text_Telephone = tk.Text(root_followUp, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Telephone.place(x=40, y=y_origin+i*gain)
    label_Telephone = tk.Label(root_followUp, text='Telephone:', font=LABEL_FONT)
    label_Telephone.place(x=40,y=y_origin+i*gain-25)

    i = 6

    text_Comments = tk.Text(root_followUp, width=140, height=1, font=EDIT_FONT, wrap='none')
    text_Comments.place(x=40, y=y_origin+i*gain)
    label_Comments = tk.Label(root_followUp, text='Comments:', font=LABEL_FONT)
    label_Comments.place(x=40,y=y_origin+i*gain-25)

    i = 8 

    button_add=ttk.Button(root_followUp, text='Create', width=15, command=create)
    button_add.place(x=250, y=y_origin+i*gain)

    button_cancel=ttk.Button(root_followUp, text='Cancel', width=15, command=root_followUp.destroy)
    button_cancel.place(x=600, y=y_origin+i*gain)      

    show_modal_window(root_followUp, root)

    #t = datetime.datetime.now()
    #ts = str(datetime.datetime.now())

    #datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')


# In[31]:


def delete_HCM():
    id_in_HCM_gotten = text_id_in_HCM.get('1.0', tk.END).rstrip()

    if id_in_HCM_gotten == '':
        messagebox.showinfo("Empty", "There's no HCM record to delete. Please make sure.")

    else:           
        result = messagebox.askquestion('Delete', 'Are you sure to delete this sample?', icon='warning')

        if result == 'yes':
            cur.execute('DELETE FROM HCM WHERE id_in_HCM = ?', (id_in_HCM_gotten,))        
            conn.commit()            
            messagebox.showinfo("Deleted", "The HCM Record has been deleted!")

            clear()
            refreshDB()
            display_in_table(combination)


# In[32]:


def delete_patient():
    id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()

    if id_in_patients_gotten == '':
        messagebox.showinfo("Empty", "There's no patient information to delete. Please make sure.")

    else:           
        result = messagebox.askquestion('Delete', 
                                        'Are you sure to delete this patient\'s information?', 
                                        icon='warning')

        if result == 'yes':
            cur.execute('DELETE FROM Patients WHERE id_in_patients = ?', 
                        (id_in_patients_gotten,))        
            conn.commit()            
            messagebox.showinfo("Deleted", "The Patient's information has been deleted!")

            clear()
            refreshDB()
            display_in_table(combination)


# In[33]:


def patientNameSearch():
    PatientName_Search_gotten = text_PatientName_Search.get('1.0', tk.END).rstrip()

    sqlstr = '''SELECT * FROM HCM 
    JOIN Patients ON HCM.CitizenID = Patients.CitizenID 
    WHERE Patients.PatientName_in_patients = ? 
    '''

    cur.execute(sqlstr, (PatientName_Search_gotten,))
    items = cur.fetchall()

    clear()
    display_in_table(items)   


# In[34]:


def about():
    about_root = tk.Toplevel(root)

    w = 367 # width for the Tk root
    h = 230 # height for the Tk root

    # get screen width and height
    ws = about_root.winfo_screenwidth() # width of the screen
    hs = about_root.winfo_screenheight() # height of the screen

    # calculate x and y coordinates for the Tk root window
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    # set the dimensions of the screen 
    # and where it is placed
    about_root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    about_root.title('About Charleston Myo')  

    # Controls

    label_author=tk.Label(about_root,text='Charleston Myo Version 1.0', font=LABEL_FONT)
    label_author.place(x=90,y=30)

    label_author=tk.Label(about_root,text='Copyright (C) 2026', font=LABEL_FONT)
    label_author.place(x=125,y=60)

    label_author=tk.Label(about_root,text='Author: Chuan Yang', font=LABEL_FONT)
    label_author.place(x=125,y=90)

    label_author=tk.Label(about_root,text='Shengjing Hospital of China Medical University', font=LABEL_FONT)
    label_author.place(x=50,y=120)


    button_refresh=ttk.Button(about_root, width=15, text='OK', command=about_root.destroy)
    button_refresh.place(x=135, y=170)

    show_modal_window(about_root, root)


# In[35]:


import sys

_tk_poll_after_id = None


def _running_in_notebook():
    try:
        return get_ipython() is not None
    except NameError:
        return False


def _disable_ipython_gui():
    try:
        ip = get_ipython()
        if ip is not None:
            ip.enable_gui(None)
    except Exception:
        pass


def _safe_destroy(window):
    if window is None:
        return
    try:
        window.grab_release()
    except tk.TclError:
        pass
    try:
        if window.winfo_exists():
            window.destroy()
    except tk.TclError:
        pass


def _stop_tk_polling():
    global _tk_poll_after_id
    if _tk_poll_after_id is not None:
        try:
            root.after_cancel(_tk_poll_after_id)
        except tk.TclError:
            pass
        _tk_poll_after_id = None


def _poll_tk_events():
    global _tk_poll_after_id
    try:
        if root.winfo_exists():
            root.update_idletasks()
            root.update()
            _tk_poll_after_id = root.after(50, _poll_tk_events)
    except tk.TclError:
        _tk_poll_after_id = None


def show_modal_window(window, parent):
    window.transient(parent)
    window.protocol('WM_DELETE_WINDOW', lambda w=window: _safe_destroy(w))
    window.grab_set()
    parent.wait_window(window)


def exit_the_main():
    global conn
    _stop_tk_polling()
    _disable_ipython_gui()
    for child in list(root.winfo_children()):
        if isinstance(child, tk.Toplevel):
            _safe_destroy(child)
    try:
        conn.close()
    except Exception:
        pass
    try:
        root.quit()
    except tk.TclError:
        pass
    _safe_destroy(root)


def start_main_window():
    if _running_in_notebook():
        _poll_tk_events()
    else:
        root.mainloop()
        try:
            conn.close()
        except Exception:
            pass
        sys.exit(0)


# ## Main Flow

# In[ ]:


root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.attributes('-fullscreen', True)
root.title('CharlestonPark')
root.protocol('WM_DELETE_WINDOW', exit_the_main)
#root.iconbitmap('CharlestonParkIcon.ico')

### Multicolumn Listbox

# Multicolumn Listbox/////////////////////////////////////////////////////////////////////////////
table = ttk.Treeview(root, height="20", columns=headers, selectmode="extended")
table.pack(padx=10, pady=20, ipadx=1200, ipady=200)


i = 1
header_width = [30] * 83

for header in headers:
    table.heading('#'+str(i), text=header.title(), anchor=tk.W, command=lambda c=header: sortby(table, c, 0))
    table.column('#'+str(i), stretch=tk.NO, minwidth=0, width=tkf.Font().measure(header.title())+header_width[i-1])
    i+=1    
table.column('#0', stretch=tk.NO, minwidth=0, width=0)

table.bind("<Double-1>", OnDoubleClick)
#///////////////////////////////////////////////////////////////////////////////////////////

# Scrollbar////////////////////////////////////////////////////////////////////////////////////////
vsb = ttk.Scrollbar(table, orient = "vertical",  command = table.yview)
hsb = ttk.Scrollbar(table, orient = "horizontal", command = table.xview)
## Link scrollbars activation to top-level object
table.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set)
## Link scrollbar also to every columns
map(lambda col: col.configure(yscrollcommand = vsb.set, xscrollcommand = hsb.set), table)
vsb.pack(side = tk.RIGHT, fill = tk.Y)
hsb.pack(side = tk.BOTTOM, fill = tk.X) 

### Other Controls

# ///////Text Edit/////////////////////////

y_origin = 580
gain = 50
i = 0

# ////////////////// Frame /////////////////////////////////////////////
# ///////////// Raised Label Block ////////////////////////////////////////////////

label_HCM=tk.Label(root,width=230, height=8 , relief='raised', borderwidth=1)
label_HCM.place(x=10,y=540)

label_Patients=tk.Label(root,width=230, height=20 , relief='raised', borderwidth=1)
label_Patients.place(x=15,y=678)

# ///////////// Routine Edits////////////////
# ///////////////HCM///////////////

text_id_in_HCM = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_id_in_HCM.place(x=40, y=y_origin+i*gain)
label_HCM = tk.Label(root, text='Enrollment ID:', font=LABEL_FONT)
label_HCM.place(x=40,y=y_origin+i*gain-25)

text_PatientName_in_HCM = tk.Text(root, width=26, height=1, font=EDIT_FONT, wrap='none')
text_PatientName_in_HCM.place(x=240, y=y_origin+i*gain)
label_PatientName_HCM = tk.Label(root, text='Patient Name:', font=LABEL_FONT)
label_PatientName_HCM.place(x=240,y=y_origin+i*gain-25)

text_EnrollmentDate = tk.Text(root, width=26, height=1, font=EDIT_FONT, wrap='none')
text_EnrollmentDate.place(x=240, y=y_origin+i*gain)
label_EnrollmentDate = tk.Label(root, text='Enrollment Date:', font=LABEL_FONT)
label_EnrollmentDate.place(x=240,y=y_origin+i*gain-25)


# Combobox control
combo_IsObstructiveResting = ttk.Combobox(root, width=20, height=1, font=EDIT_FONT)
combo_IsObstructiveResting.place(x=440, y=y_origin+i*gain)
label_IsObstructiveResting = tk.Label(root, text='Obstructive during Rest?', font=LABEL_FONT)
label_IsObstructiveResting.place(x=440,y=y_origin+i*gain-25)
combo_IsObstructiveResting['values'] = ('Yes', 'No', 'Unknown')
combo_IsObstructiveResting['state'] = 'readonly'

combo_IsObstructiveValsalva = ttk.Combobox(root, width=20, height=1, font=EDIT_FONT)
combo_IsObstructiveValsalva.place(x=640, y=y_origin+i*gain)
label_IsObstructiveValsalva = tk.Label(root, text='Obstructive during Valsalva?', font=LABEL_FONT)
label_IsObstructiveValsalva.place(x=640,y=y_origin+i*gain-25)
combo_IsObstructiveValsalva['values'] = ('Yes', 'No', 'Unknown')
combo_IsObstructiveValsalva['state'] = 'readonly'

text_PatientName_in_HCM = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_PatientName_in_HCM.place(x=840, y=y_origin+i*gain)
label_PatientName_in_HCM = tk.Label(root, text='Patient Name:', font=LABEL_FONT)
label_PatientName_in_HCM.place(x=840,y=y_origin+i*gain-25)

i = 1

text_Diabetes = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_Diabetes.place(x=40, y=y_origin+i*gain)
label_Diabetes = tk.Label(root, text='Diabetes:', font=LABEL_FONT)
label_Diabetes.place(x=40,y=y_origin+i*gain-25)

text_Stroke = tk.Text(root, width=26, height=1, font=EDIT_FONT, wrap='none')
text_Stroke.place(x=240, y=y_origin+i*gain)
label_Stroke = tk.Label(root, text='Stroke:', font=LABEL_FONT)
label_Stroke.place(x=240,y=y_origin+i*gain-25)

text_Renal = tk.Text(root, width=26, height=1, font=EDIT_FONT, wrap='none')
text_Renal.place(x=440, y=y_origin+i*gain)
label_Renal = tk.Label(root, text='Renal Functionality:', font=LABEL_FONT)
label_Renal.place(x=440,y=y_origin+i*gain-25)



# Combobox control
combo_IsDyspnea = ttk.Combobox(root, width=20, height=1, font=EDIT_FONT)
combo_IsDyspnea.place(x=640, y=y_origin+i*gain)
label_IsDyspnea = tk.Label(root, text='Dyspnea?', font=LABEL_FONT)
label_IsDyspnea.place(x=640,y=y_origin+i*gain-25)
combo_IsDyspnea['values'] = ('Yes', 'No', 'Unknown')
combo_IsDyspnea['state'] = 'readonly'

combo_IsChestPain = ttk.Combobox(root, width=20, height=1, font=EDIT_FONT)
combo_IsChestPain.place(x=840, y=y_origin+i*gain)
label_IsChestPain = tk.Label(root, text='Chest Pain?', font=LABEL_FONT)
label_IsChestPain.place(x=840,y=y_origin+i*gain-25)
combo_IsChestPain['values'] = ('Yes', 'No', 'Unknown')
combo_IsChestPain['state'] = 'readonly'

combo_IsSyncope = ttk.Combobox(root, width=20, height=1, font=EDIT_FONT)
combo_IsSyncope.place(x=1010, y=y_origin+i*gain)
label_IsSyncope = tk.Label(root, text='Syncope?', font=LABEL_FONT)
label_IsSyncope.place(x=1010,y=y_origin+i*gain-25)
combo_IsSyncope['values'] = ('Yes', 'No', 'Unknown')
combo_IsSyncope['state'] = 'readonly'

combo_NYHA = ttk.Combobox(root, width=10, height=1, font=EDIT_FONT)
combo_NYHA.place(x=1200, y=y_origin+i*gain)
label_NYHA = tk.Label(root, text='NYHA', font=LABEL_FONT)
label_NYHA.place(x=1200,y=y_origin+i*gain-25)
combo_NYHA['values'] = ('I', 'II', 'III', 'IV')
combo_NYHA['state'] = 'readonly'


text_Hypertension = tk.Text(root, width=15, height=1, font=EDIT_FONT, wrap='none')
text_Hypertension.place(x=1310, y=y_origin+i*gain)
label_Hypertension = tk.Label(root, text='Hypretension:', font=LABEL_FONT)
label_Hypertension.place(x=1310,y=y_origin+i*gain-25)

text_QualityOfLifeScore = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_QualityOfLifeScore.place(x=1450, y=y_origin+i*gain)
label_QualityOfLifeScore = tk.Label(root, text='Quality of Life Score:', font=LABEL_FONT)
label_QualityOfLifeScore.place(x=1450,y=y_origin+i*gain-25)


i = 3

# ///////////////Patients///////////////

text_id_in_patients = tk.Text(root, width=10, height=1, font=EDIT_FONT, wrap='none')
text_id_in_patients.place(x=1340, y=y_origin+i*gain)
label_id_in_patients = tk.Label(root, text='id_patients:', font=LABEL_FONT)
label_id_in_patients.place(x=1340,y=y_origin+i*gain-25)

text_PatientName_CN = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_PatientName_CN.place(x=40, y=y_origin+i*gain)
label_PatientName_CN = tk.Label(root, text='Patient\'s Chinese Name:', font=LABEL_FONT)
label_PatientName_CN.place(x=40,y=y_origin+i*gain-25)

text_PatientName_in_patients = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_PatientName_in_patients.place(x=240, y=y_origin+i*gain)
label_PatientName_in_patients = tk.Label(root, text='Patient\' Name:', font=LABEL_FONT)
label_PatientName_in_patients.place(x=240,y=y_origin+i*gain-25)

combo_Gender = ttk.Combobox(root, width=20, height=1, font=EDIT_FONT)
combo_Gender.place(x=440, y=y_origin+i*gain)
label_Gender = tk.Label(root, text='Gender:', font=LABEL_FONT)
label_Gender.place(x=440,y=y_origin+i*gain-25)
combo_Gender['values'] = ('Male', 'Female', 'Other')
combo_Gender['state'] = 'readonly'

text_BirthDate = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_BirthDate.place(x=640, y=y_origin+i*gain)
label_BirthDate = tk.Label(root, text='Birth Date:', font=LABEL_FONT)
label_BirthDate.place(x=640,y=y_origin+i*gain-25)

text_FamilyHistory = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_FamilyHistory.place(x=840, y=y_origin+i*gain)
label_FamilyHistory = tk.Label(root, text='Family History:', font=LABEL_FONT)
label_FamilyHistory.place(x=840,y=y_origin+i*gain-25)

combo_IsInsurance = ttk.Combobox(root, width=20, height=1, font=EDIT_FONT)
combo_IsInsurance.place(x=1040, y=y_origin+i*gain)
label_IsInsurance = tk.Label(root, text='Medical Insurance:', font=LABEL_FONT)
label_IsInsurance.place(x=1040,y=y_origin+i*gain-25)
combo_IsInsurance['values'] = ('Yes', 'No', 'Suspended', 'Unknown')
combo_IsInsurance['state'] = 'readonly'

text_FamilyHistory = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_FamilyHistory.place(x=840, y=y_origin+i*gain)
label_FamilyHistory = tk.Label(root, text='Family History:', font=LABEL_FONT)
label_FamilyHistory.place(x=840,y=y_origin+i*gain-25)

i = 4

text_InPatientID = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_InPatientID.place(x=40, y=y_origin+i*gain)
label_InPatientID = tk.Label(root, text='In-Patient ID:', font=LABEL_FONT)
label_InPatientID.place(x=40,y=y_origin+i*gain-25)

text_CitizenID = tk.Text(root, width=25, height=1, font=EDIT_FONT, wrap='none')
text_CitizenID.place(x=240, y=y_origin+i*gain)
label_CitizenID = tk.Label(root, text='Citizen ID:', font=LABEL_FONT)
label_CitizenID.place(x=240,y=y_origin+i*gain-25)

combo_Marriage = ttk.Combobox(root, width=20, height=1, font=EDIT_FONT)
combo_Marriage.place(x=440, y=y_origin+i*gain)
label_Marriage = tk.Label(root, text='Marriage:', font=LABEL_FONT)
label_Marriage.place(x=440,y=y_origin+i*gain-25)
combo_Marriage['values'] = ('Single', 'Married', 'Divorce', 'Widowed', 'Unknown')
combo_Marriage['state'] = 'readonly'

text_Education = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_Education.place(x=640, y=y_origin+i*gain)
label_Education = tk.Label(root, text='Education:', font=LABEL_FONT)
label_Education.place(x=640,y=y_origin+i*gain-25)

text_Height = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_Height.place(x=840, y=y_origin+i*gain)
label_Height = tk.Label(root, text='Height:', font=LABEL_FONT)
label_Height.place(x=840,y=y_origin+i*gain-25)

text_BodyWeight = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_BodyWeight.place(x=1040, y=y_origin+i*gain)
label_BodyWeight = tk.Label(root, text='Body Weight:', font=LABEL_FONT)
label_BodyWeight.place(x=1040,y=y_origin+i*gain-25)


i = 5

text_Diagnosis1 = tk.Text(root, width=40, height=1, font=EDIT_FONT, wrap='none')
text_Diagnosis1.place(x=40, y=y_origin+i*gain)
label_Diagnosis1 = tk.Label(root, text='Diagnosis 1:', font=LABEL_FONT)
label_Diagnosis1.place(x=40,y=y_origin+i*gain-25)

text_Diagnosis2 = tk.Text(root, width=40, height=1, font=EDIT_FONT, wrap='none')
text_Diagnosis2.place(x=340, y=y_origin+i*gain)
label_Diagnosis2 = tk.Label(root, text='Diagnosis 2:', font=LABEL_FONT)
label_Diagnosis2.place(x=340,y=y_origin+i*gain-25)

text_Diagnosis3 = tk.Text(root, width=40, height=1, font=EDIT_FONT, wrap='none')
text_Diagnosis3.place(x=640, y=y_origin+i*gain)
label_Diagnosis3 = tk.Label(root, text='Diagnosis 3:', font=LABEL_FONT)
label_Diagnosis3.place(x=640,y=y_origin+i*gain-25)

text_Diagnosis4 = tk.Text(root, width=40, height=1, font=EDIT_FONT, wrap='none')
text_Diagnosis4.place(x=940, y=y_origin+i*gain)
label_Diagnosis4 = tk.Label(root, text='Diagnosis 4:', font=LABEL_FONT)
label_Diagnosis4.place(x=940,y=y_origin+i*gain-25)

text_Diagnosis5 = tk.Text(root, width=40, height=1, font=EDIT_FONT, wrap='none')
text_Diagnosis5.place(x=1240, y=y_origin+i*gain)
label_Diagnosis5 = tk.Label(root, text='Diagnosis 5:', font=LABEL_FONT)
label_Diagnosis5.place(x=1240,y=y_origin+i*gain-25)

i = 6

text_Telephone1 = tk.Text(root, width=40, height=1, font=EDIT_FONT, wrap='none')
text_Telephone1.place(x=40, y=y_origin+i*gain)
label_Telephone1 = tk.Label(root, text='Telephone 1:', font=LABEL_FONT)
label_Telephone1.place(x=40,y=y_origin+i*gain-25)

text_Telephone2 = tk.Text(root, width=40, height=1, font=EDIT_FONT, wrap='none')
text_Telephone2.place(x=340, y=y_origin+i*gain)
label_Telephone2 = tk.Label(root, text='Telephone 2:', font=LABEL_FONT)
label_Telephone2.place(x=340,y=y_origin+i*gain-25)

i = 7

text_Comments = tk.Text(root, width=240, height=2, font=EDIT_FONT, wrap='none')
text_Comments.place(x=40, y=y_origin+i*gain)
label_Comments = tk.Label(root, text='Comments:', font=LABEL_FONT)
label_Comments.place(x=40,y=y_origin+i*gain-25)

# /////Buttons//////////////////////
button_browse=ttk.Button(root, text='HCM...', width=12, command=HCM)
button_browse.place(x=1010, y=500)

button_browse=ttk.Button(root, text='Patients...', width=12, command=patients)
button_browse.place(x=1140, y=500)

button_browse=ttk.Button(root, text='Browse', width=12, command=browse)
button_browse.place(x=1380, y=500)

# ////////////// Record Num/////////////////

text_num = tk.Text(root, width=8, height=1, font=EDIT_FONT, wrap='none')
text_num.place(x=1300, y=500)

# ////////////// Function Button //////////
# HCM Information Update & Delete

button_update_sample = ttk.Button(root, text='Update', width=8, command=update_HCM)
button_update_sample.place(x=1345, y=560)

button_delete_sample = ttk.Button(root, text='Delete', width=8, command=delete_HCM)
button_delete_sample.place(x=1480, y=560)

# Patient Information Update & Delete

button_update_patient = ttk.Button(root, text='Update', width=8, command=update_patients)
button_update_patient.place(x=1345, y=780)

button_delete_patient = ttk.Button(root, text='Delete', width=8, command=delete_patient)
button_delete_patient.place(x=1480, y=780)

# About...

button_about = ttk.Button(root, text='About...', width=9, command=about)
button_about.place(x=1345, y=890)

# Exit

button_exit = ttk.Button(root, text='Exit', width=9, command=exit_the_main)
button_exit.place(x=1480, y=890)

# New

button_new_sample = ttk.Button(root, text='New HCM...', width=12, command=new_HCM)
button_new_sample.place(x=30, y=500)

button_new_patient = ttk.Button(root, text='New Patient...', width=12, command=new_patient)
button_new_patient.place(x=190, y=500)


button_new_patient = ttk.Button(root, text='New Follow-up...', width=20, command=new_followUp)
button_new_patient.place(x=350, y=500)

# ///// Search Edit Box//////////

text_PatientName_Search = tk.Text(root, width=20, height=1, font=EDIT_FONT, wrap='none')
text_PatientName_Search.place(x=570, y=510)
label_PatientName_Search = tk.Label(root, text='Patient\'s Name:', font=LABEL_FONT)
label_PatientName_Search.place(x=570,y=485)

button_PatientName_Search=ttk.Button(root, text='Search', width=15, command=patientNameSearch)
button_PatientName_Search.place(x=750, y=500)



#t = datetime.datetime.now()
#ts = str(datetime.datetime.now())

#datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')

start_main_window()


# In[ ]:




