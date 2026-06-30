#!/usr/bin/env python
# coding: utf-8

# In[793]:


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import tkinter.font as tkf

FONT_NAME = 'tahoma'
LABEL_FONT = (FONT_NAME, 10)
EDIT_FONT = (FONT_NAME, 10)


# In[794]:


import sqlite3


# In[795]:


import datetime


# In[796]:


DB_file = 'Entity_DB.sqlite'
conn = sqlite3.connect(DB_file)

conn.execute('PRAGMA journal_mode=WAL') 
#WAL (Write-Ahead Logging) 模式：
#WAL 是 SQLite 的一种日志模式，用于替代传统的回滚日志模式，可以显著提高并发性能。

cur = conn.cursor()


# In[797]:


sqlstr = '''SELECT *
FROM HCM JOIN Patients ON HCM.CitizenID = Patients.CitizenID
ORDER BY HCM.id_in_HCM
'''


# In[798]:


spreadsheet = cur.execute(sqlstr)


# In[799]:


spreadsheet


# In[800]:


combination = []
for row in spreadsheet:
    combination.append(row)


# In[801]:


cur.execute('SELECT * FROM HCM')
headers_HCM = [item[0] for item in cur.description]


# In[802]:


cur.execute('SELECT * FROM Patients')
headers_patients = [item[0] for item in cur.description]


# In[803]:


headers = headers_HCM + headers_patients


# In[804]:


headers


# In[805]:


len(headers)


# In[806]:


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


# In[807]:


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


# In[808]:


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


# In[809]:


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




# In[810]:


# Display in Table

def display_in_table(combination):
    for row in combination:
        table.insert("", "end", values=row)
    num = str(len(combination))
    text_num.delete('1.0', tk.END)
    text_num.insert('1.0', num)


# In[811]:


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

    text_FamilyHistory.delete('1.0', tk.END)
    text_FamilyHistory.insert('1.0', item['FamilyHistory'])

    combo_Marriage.set(item['Marriage'])

    text_Education.delete('1.0', tk.END)
    text_Education.insert('1.0', item['Education'])

    combo_IsInsurance.set(item['IsInsurance'])

    text_Height.delete('1.0', tk.END)
    text_Height.insert('1.0', item['Height'])

    text_BodyWeight.delete('1.0', tk.END)
    text_BodyWeight.insert('1.0', item['BodyWeight'])


# In[812]:


def clear():
    for i in table.get_children():
        table.delete(i)


# In[813]:


def browse():
    clear()
    refreshDB()
    display_in_table(combination)


# In[814]:


def update_HCM():
    pass


# In[815]:


def delete_HCM():
    pass


# In[816]:


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
            item[headers_HCM[i]] = rowSelected[i]
        display_in_text(item)

    def display_in_table(combination):
        for row in combination:
            table.insert("", "end", values=row)  #新版Python删除第三个参数

    def display_in_text(item):  
        text_id_in_HCM.delete('1.0', tk.END)
        text_id_in_HCM.insert('1.0', item['id_in_HCM'])

        text_PatientName_in_HCM.delete('1.0', tk.END)
        text_PatientName_in_HCM.insert('1.0', item['PatientName_in_HCM'])

        text_EnrollmentDate.delete('1.0', tk.END)
        text_EnrollmentDate.insert('1.0', item['EnrollmentDate'])

        combo_IsObstructiveResting.set(item['IsObstructiveResting'])
        combo_IsObstructiveValsalva.set(item['IsObstructiveValsalva'])

        text_Hypertension.delete('1.0', tk.END)
        text_Hypertension.insert('1.0', item['Hypertension'])

        text_Diabetes.delete('1.0', tk.END)
        text_Diabetes.insert('1.0', item['Diabetes'])

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

        text_CitizenID.delete('1.0', tk.END)
        text_CitizenID.insert('1.0', item['CitizenID'])

        text_WBC.delete('1.0', tk.END)
        text_WBC.insert('1.0', item['WBC'])

        text_PLT.delete('1.0', tk.END)
        text_PLT.insert('1.0', item['PLT'])

        text_HGB.delete('1.0', tk.END)
        text_HGB.insert('1.0', item['HGB'])

        text_PDW.delete('1.0', tk.END)
        text_PDW.insert('1.0', item['PDW'])

        text_AlbG.delete('1.0', tk.END)
        text_AlbG.insert('1.0', item['AlbG'])

        text_GLB.delete('1.0', tk.END)
        text_GLB.insert('1.0', item['GLB'])

        text_ALT.delete('1.0', tk.END)
        text_ALT.insert('1.0', item['ALT'])

        text_AST.delete('1.0', tk.END)
        text_AST.insert('1.0', item['AST'])

        text_GGT.delete('1.0', tk.END)
        text_GGT.insert('1.0', item['GGT'])

        text_BilT.delete('1.0', tk.END)
        text_BilT.insert('1.0', item['BilT'])

        text_BilD.delete('1.0', tk.END)
        text_BilD.insert('1.0', item['BilD'])

        text_PreAlbG.delete('1.0', tk.END)
        text_PreAlbG.insert('1.0', item['PreAlbG'])

        text_CysC.delete('1.0', tk.END)
        text_CysC.insert('1.0', item['CysC'])

        text_Crea.delete('1.0', tk.END)
        text_Crea.insert('1.0', item['Crea'])

        text_Urea.delete('1.0', tk.END)
        text_Urea.insert('1.0', item['Urea'])

        text_INR.delete('1.0', tk.END)
        text_INR.insert('1.0', item['INR'])

        text_DDimer.delete('1.0', tk.END)
        text_DDimer.insert('1.0', item['DDimer'])

        text_Trig.delete('1.0', tk.END)
        text_Trig.insert('1.0', item['Trig'])

        text_Chol.delete('1.0', tk.END)
        text_Chol.insert('1.0', item['Chol'])

        text_HDL.delete('1.0', tk.END)
        text_HDL.insert('1.0', item['HDL'])

        text_LDL.delete('1.0', tk.END)
        text_LDL.insert('1.0', item['LDL'])

        text_nonLDL.delete('1.0', tk.END)
        text_nonLDL.insert('1.0', item['nonLDL'])

        text_ApoA.delete('1.0', tk.END)
        text_ApoA.insert('1.0', item['ApoA'])

        text_ApoB.delete('1.0', tk.END)
        text_ApoB.insert('1.0', item['ApoB'])

        text_LPa.delete('1.0', tk.END)
        text_LPa.insert('1.0', item['LPa'])

        text_TnT.delete('1.0', tk.END)
        text_TnT.insert('1.0', item['TnT'])

        text_ProBNP.delete('1.0', tk.END)
        text_ProBNP.insert('1.0', item['ProBNP'])

        text_Glu.delete('1.0', tk.END)
        text_Glu.insert('1.0', item['Glu'])

        text_HbA1c.delete('1.0', tk.END)
        text_HbA1c.insert('1.0', item['HbA1c'])

        text_SG.delete('1.0', tk.END)
        text_SG.insert('1.0', item['SG'])

        text_Ratio_UrineAlbu_Crea.delete('1.0', tk.END)
        text_Ratio_UrineAlbu_Crea.insert('1.0', item['Ratio_UrineAlbu_Crea'])

        text_HR_average.delete('1.0', tk.END)
        text_HR_average.insert('1.0', item['HR_average'])

        combo_IsAtrialFibrillation.set(item['IsAtrialFibrillation'])
        combo_IsVentricularPrematureBeat.set(item['IsVentricularPrematureBeat'])
        combo_TypeVentricularTachycardia.set(item['TypeVentricularTachycardia'])
        combo_LGE.set(item['LGE'])

        text_CCB.delete('1.0', tk.END)
        text_CCB.insert('1.0', item['CCB'])

        text_BetaBlocker.delete('1.0', tk.END)
        text_BetaBlocker.insert('1.0', item['BetaBlocker'])

        text_OtherMedication.delete('1.0', tk.END)
        text_OtherMedication.insert('1.0', item['OtherMedication'])

        combo_Rehospitalization.set(item['Rehospitalization'])
        combo_AnginaRecurrent.set(item['AnginaRecurrent'])
        combo_AtrialFibrillationRecurrent.set(item['AtrialFibrillationRecurrent'])
        combo_Mortality.set(item['Mortality'])
        combo_AblationAlcohol.set(item['AblationAlcohol'])
        combo_AblationRF.set(item['AblationRF'])
        combo_Pacemaker.set(item['Pacemaker'])
        combo_Myectomy.set(item['Myectomy'])

        text_Genetic.delete('1.0', tk.END)
        text_Genetic.insert('1.0', item['Genetic'])

    def update_HCM():
        try:        
            id_in_HCM_gotten = text_id_in_HCM.get('1.0', tk.END).rstrip()
            PatientName_in_HCM_gotten = text_PatientName_in_HCM.get('1.0', tk.END).rstrip()
            EnrollmentDate_gotten = text_EnrollmentDate.get('1.0', tk.END).rstrip()
            IsObstructiveResting_gotten = combo_IsObstructiveResting.get().rstrip()
            IsObstructiveValsalva_gotten = combo_IsObstructiveValsalva.get().rstrip()
            Hypertension_gotten = text_Hypertension.get('1.0', tk.END).rstrip()
            Diabetes_gotten = text_Diabetes.get('1.0', tk.END).rstrip()
            Stroke_gotten = text_Stroke.get('1.0', tk.END).rstrip()
            Renal_gotten = text_Renal.get('1.0', tk.END).rstrip()
            IsDyspnea_gotten = combo_IsDyspnea.get().rstrip()
            IsChestPain_gotten = combo_IsChestPain.get().rstrip()
            IsSyncope_gotten = combo_IsSyncope.get().rstrip()
            NYHA_gotten = combo_NYHA.get().rstrip()
            QualityOfLifeScore_gotten = text_QualityOfLifeScore.get('1.0', tk.END).rstrip()
            CitizenID_gotten = text_CitizenID.get('1.0', tk.END).rstrip()
            WBC_gotten = text_WBC.get('1.0', tk.END).rstrip()
            PLT_gotten = text_PLT.get('1.0', tk.END).rstrip()
            HGB_gotten = text_HGB.get('1.0', tk.END).rstrip()
            PDW_gotten = text_PDW.get('1.0', tk.END).rstrip()
            AlbG_gotten = text_AlbG.get('1.0', tk.END).rstrip()
            GLB_gotten = text_GLB.get('1.0', tk.END).rstrip()
            ALT_gotten = text_ALT.get('1.0', tk.END).rstrip()
            AST_gotten = text_AST.get('1.0', tk.END).rstrip()
            GGT_gotten = text_GGT.get('1.0', tk.END).rstrip()
            BilT_gotten = text_BilT.get('1.0', tk.END).rstrip()
            BilD_gotten = text_BilD.get('1.0', tk.END).rstrip()
            PreAlbG_gotten = text_PreAlbG.get('1.0', tk.END).rstrip()
            CysC_gotten = text_CysC.get('1.0', tk.END).rstrip()
            Crea_gotten = text_Crea.get('1.0', tk.END).rstrip()
            Urea_gotten = text_Urea.get('1.0', tk.END).rstrip()
            INR_gotten = text_INR.get('1.0', tk.END).rstrip()
            DDimer_gotten = text_DDimer.get('1.0', tk.END).rstrip()
            Trig_gotten = text_Trig.get('1.0', tk.END).rstrip()
            Chol_gotten = text_Chol.get('1.0', tk.END).rstrip()
            HDL_gotten = text_HDL.get('1.0', tk.END).rstrip()
            LDL_gotten = text_LDL.get('1.0', tk.END).rstrip()
            nonLDL_gotten = text_nonLDL.get('1.0', tk.END).rstrip()
            ApoA_gotten = text_ApoA.get('1.0', tk.END).rstrip()
            ApoB_gotten = text_ApoB.get('1.0', tk.END).rstrip()
            LPa_gotten = text_LPa.get('1.0', tk.END).rstrip()
            TnT_gotten = text_TnT.get('1.0', tk.END).rstrip()
            ProBNP_gotten = text_ProBNP.get('1.0', tk.END).rstrip()
            Glu_gotten = text_Glu.get('1.0', tk.END).rstrip()
            HbA1c_gotten = text_HbA1c.get('1.0', tk.END).rstrip()
            SG_gotten = text_SG.get('1.0', tk.END).rstrip()
            Ratio_UrineAlbu_Crea_gotten = text_Ratio_UrineAlbu_Crea.get('1.0', tk.END).rstrip()
            HR_average_gotten = text_HR_average.get('1.0', tk.END).rstrip()
            IsAtrialFibrillation_gotten = combo_IsAtrialFibrillation.get().rstrip()
            IsVentricularPrematureBeat_gotten = combo_IsVentricularPrematureBeat.get().rstrip()
            TypeVentricularTachycardia_gotten = combo_TypeVentricularTachycardia.get().rstrip()
            LGE_gotten = combo_LGE.get().rstrip()
            CCB_gotten = text_CCB.get('1.0', tk.END).rstrip()
            BetaBlocker_gotten = text_BetaBlocker.get('1.0', tk.END).rstrip()
            OtherMedication_gotten = text_OtherMedication.get('1.0', tk.END).rstrip()
            Rehospitalization_gotten = combo_Rehospitalization.get().rstrip()
            AnginaRecurrent_gotten = combo_AnginaRecurrent.get().rstrip()
            AtrialFibrillationRecurrent_gotten = combo_AtrialFibrillationRecurrent.get().rstrip()
            Mortality_gotten = combo_Mortality.get().rstrip()
            AblationAlcohol_gotten = combo_AblationAlcohol.get().rstrip()
            AblationRF_gotten = combo_AblationRF.get().rstrip()
            Pacemaker_gotten = combo_Pacemaker.get().rstrip()
            Myectomy_gotten = combo_Myectomy.get().rstrip()
            Genetic_gotten = text_Genetic.get('1.0', tk.END).rstrip()

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
                QualityOfLifeScore = ?,
                WBC = ?,
                PLT = ?,
                HGB = ?,
                PDW = ?,
                AlbG = ?,
                GLB = ?,
                ALT = ?,
                AST = ?,
                GGT = ?,
                BilT = ?,
                BilD = ?,
                PreAlbG = ?,
                CysC = ?,
                Crea = ?,
                Urea = ?,
                INR = ?,
                DDimer = ?,
                Trig = ?,
                Chol = ?,
                HDL = ?,
                LDL = ?,
                nonLDL = ?,
                ApoA = ?,
                ApoB = ?,
                LPa = ?,
                TnT = ?,
                ProBNP = ?,
                Glu = ?,
                HbA1c = ?,
                SG = ?,
                Ratio_UrineAlbu_Crea = ?,
                HR_average = ?,
                IsAtrialFibrillation = ?,
                IsVentricularPrematureBeat = ?,
                TypeVentricularTachycardia = ?,
                LGE = ?,
                CCB = ?,
                BetaBlocker = ?,
                OtherMedication = ?,
                Rehospitalization = ?,
                AnginaRecurrent = ?,
                AtrialFibrillationRecurrent = ?,
                Mortality = ?,
                AblationAlcohol = ?,
                AblationRF = ?,
                Pacemaker = ?,
                Myectomy = ?,
                CitizenID = ?,
                Genetic = ?
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
                WBC_gotten,
                PLT_gotten,
                HGB_gotten,
                PDW_gotten,
                AlbG_gotten,
                GLB_gotten,
                ALT_gotten,
                AST_gotten,
                GGT_gotten,
                BilT_gotten,
                BilD_gotten,
                PreAlbG_gotten,
                CysC_gotten,
                Crea_gotten,
                Urea_gotten,
                INR_gotten,
                DDimer_gotten,
                Trig_gotten,
                Chol_gotten,
                HDL_gotten,
                LDL_gotten,
                nonLDL_gotten,
                ApoA_gotten,
                ApoB_gotten,
                LPa_gotten,
                TnT_gotten,
                ProBNP_gotten,
                Glu_gotten,
                HbA1c_gotten,
                SG_gotten,
                Ratio_UrineAlbu_Crea_gotten,
                HR_average_gotten,
                IsAtrialFibrillation_gotten,
                IsVentricularPrematureBeat_gotten,
                TypeVentricularTachycardia_gotten,
                LGE_gotten,
                CCB_gotten,
                BetaBlocker_gotten,
                OtherMedication_gotten,
                Rehospitalization_gotten,
                AnginaRecurrent_gotten,
                AtrialFibrillationRecurrent_gotten,
                Mortality_gotten,
                AblationAlcohol_gotten,
                AblationRF_gotten,
                Pacemaker_gotten,
                Myectomy_gotten,
                CitizenID_gotten,
                Genetic_gotten,
                id_in_HCM_gotten
            )

            cur.execute(update_sql, update_values)
            conn.commit()

            messagebox.showinfo("Updated", "HCM record successfully updated!")

            # //////////////////// Refresh the Table ///////////////////////////////////////////////////
            for i in table.get_children():
                table.delete(i)

            refreshDB()

            sqlstr = 'SELECT * FROM HCM ORDER BY id_in_HCM'
            spreadsheet = cur.execute(sqlstr)
            combination = []        
            for row in spreadsheet:
                combination.append(row)

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

    def citizenIDSearch():
        citizenID_Search_gotten = text_citizenID_search.get('1.0', tk.END).rstrip()

        sqlstr = '''SELECT * FROM HCM WHERE CitizenID = ?  
        '''
        cur.execute(sqlstr, (citizenID_Search_gotten,))
        items = cur.fetchall()

        for i in table.get_children():
            table.delete(i)

        display_in_table(items)

    def patientNameSearch():
        PatientName_Search_gotten = text_PatientName_search.get('1.0', tk.END).rstrip()

        sqlstr = '''SELECT * FROM HCM WHERE PatientName_in_HCM = ? 
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

    root_HCM = tk.Tk()    

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

    # ///////////////HCMs///////////////

    y_origin = 540
    gain = 50
    i = 0

    # ///////////// Raised Label Block ////////////////////////////////////////////////

    label_Patients=tk.Label(root_HCM,width=230, height=27 , relief='raised', borderwidth=1)
    label_Patients.place(x=10,y=y_origin+i*gain-40)

    # ///////////// Routine Edits////////////////
    x_start = 40
    x_gap = 180
    label_offset = 25

    text_id_in_HCM = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_id_in_HCM.place(x=x_start, y=y_origin+i*gain)
    label_id_in_HCM = tk.Label(root_HCM, text='id_in_HCM:', font=LABEL_FONT)
    label_id_in_HCM.place(x=x_start, y=y_origin+i*gain-label_offset)


    text_PatientName_in_HCM = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_in_HCM.place(x=x_start + x_gap, y=y_origin+i*gain)
    label_PatientName_in_HCM = tk.Label(root_HCM, text='Patient Name:', font=LABEL_FONT)
    label_PatientName_in_HCM.place(x=x_start + x_gap, y=y_origin+i*gain-label_offset)

    text_EnrollmentDate = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_EnrollmentDate.place(x=x_start + 2*x_gap, y=y_origin+i*gain)
    label_EnrollmentDate = tk.Label(root_HCM, text='EnrollmentDate:', font=LABEL_FONT)
    label_EnrollmentDate.place(x=x_start + 2*x_gap, y=y_origin+i*gain-label_offset)

    combo_IsObstructiveResting = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsObstructiveResting.place(x=x_start + 3*x_gap, y=y_origin+i*gain)
    label_IsObstructiveResting = tk.Label(root_HCM, text='Is Obstructive Resting:', font=LABEL_FONT)
    label_IsObstructiveResting.place(x=x_start + 3*x_gap, y=y_origin+i*gain-label_offset)
    combo_IsObstructiveResting['values'] = ('Yes', 'No', 'N/A')
    combo_IsObstructiveResting['state'] = 'readonly'

    combo_IsObstructiveValsalva = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsObstructiveValsalva.place(x=x_start + 4*x_gap, y=y_origin+i*gain)
    label_IsObstructiveValsalva = tk.Label(root_HCM, text='IsObstructiveValsalva:', font=LABEL_FONT)
    label_IsObstructiveValsalva.place(x=x_start + 4*x_gap, y=y_origin+i*gain-label_offset)
    combo_IsObstructiveValsalva['values'] = ('Yes', 'No', 'N/A')
    combo_IsObstructiveValsalva['state'] = 'readonly'



    text_Hypertension = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_Hypertension.place(x=x_start + 5*x_gap, y=y_origin+i*gain)
    label_Hypertension = tk.Label(root_HCM, text='Hypertension:', font=LABEL_FONT)
    label_Hypertension.place(x=x_start + 5*x_gap, y=y_origin+i*gain-label_offset)

    text_Diabetes = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_Diabetes.place(x=x_start + 6*x_gap, y=y_origin+i*gain)
    label_Diabetes = tk.Label(root_HCM, text='Diabetes:', font=LABEL_FONT)
    label_Diabetes.place(x=x_start + 6*x_gap, y=y_origin+i*gain-label_offset)

    text_Stroke = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_Stroke.place(x=x_start + 7*x_gap, y=y_origin+i*gain)
    label_Stroke = tk.Label(root_HCM, text='Stroke:', font=LABEL_FONT)
    label_Stroke.place(x=x_start + 7*x_gap, y=y_origin+i*gain-label_offset)

    text_Renal = tk.Text(root_HCM, width=16, height=1, font=EDIT_FONT, wrap='none')
    text_Renal.place(x=x_start + 8*x_gap, y=y_origin+i*gain)
    label_Renal = tk.Label(root_HCM, text='Renal:', font=LABEL_FONT)
    label_Renal.place(x=x_start + 8*x_gap, y=y_origin+i*gain-label_offset)


    i = 1

    combo_IsDyspnea = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsDyspnea.place(x=x_start + 0*x_gap, y=y_origin+i*gain)
    label_IsDyspnea = tk.Label(root_HCM, text='Is Dyspnea?', font=LABEL_FONT)
    label_IsDyspnea.place(x=x_start + 0*x_gap, y=y_origin+i*gain-label_offset)
    combo_IsDyspnea['values'] = ('Yes', 'No', 'N/A')
    combo_IsDyspnea['state'] = 'readonly'

    combo_IsChestPain = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsChestPain.place(x=x_start + 1*x_gap, y=y_origin+i*gain)
    label_IsChestPain = tk.Label(root_HCM, text='Is Chest Pain?', font=LABEL_FONT)
    label_IsChestPain.place(x=x_start + 1*x_gap, y=y_origin+i*gain-label_offset)
    combo_IsChestPain['values'] = ('Yes', 'No', 'N/A')
    combo_IsChestPain['state'] = 'readonly'

    combo_IsSyncope = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsSyncope.place(x=x_start + 2*x_gap, y=y_origin+i*gain)
    label_IsSyncope = tk.Label(root_HCM, text='Is Syncope?', font=LABEL_FONT)
    label_IsSyncope.place(x=x_start + 2*x_gap, y=y_origin+i*gain-label_offset)
    combo_IsSyncope['values'] = ('Yes', 'No', 'N/A')
    combo_IsSyncope['state'] = 'readonly'

    combo_NYHA = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_NYHA.place(x=x_start + 3*x_gap, y=y_origin+i*gain)
    label_NYHA = tk.Label(root_HCM, text='NYHA:', font=LABEL_FONT)
    label_NYHA.place(x=x_start + 3*x_gap, y=y_origin+i*gain-label_offset)
    combo_NYHA['values'] = ('I', 'II', 'III', 'IV', 'N/A')
    combo_NYHA['state'] = 'readonly'

    text_QualityOfLifeScore = tk.Text(root_HCM, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_QualityOfLifeScore.place(x=x_start + 4*x_gap, y=y_origin+i*gain)
    label_QualityOfLifeScore = tk.Label(root_HCM, text='Quality of Life Score:', font=LABEL_FONT)
    label_QualityOfLifeScore.place(x=x_start + 4*x_gap, y=y_origin+i*gain-label_offset)

    text_CitizenID = tk.Text(root_HCM, width=16, height=1, font=EDIT_FONT, wrap='none')
    text_CitizenID.place(x=x_start + 6*x_gap, y=y_origin+i*gain)
    label_CitizenID = tk.Label(root_HCM, text='Citizen ID:', font=LABEL_FONT)
    label_CitizenID.place(x=x_start + 6*x_gap, y=y_origin+i*gain-label_offset)


    i = 2
    x_start = 40
    x_gap = 92
    label_offset = 25

    text_WBC = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_WBC.place(x=x_start + 0*x_gap, y=y_origin+i*gain)
    label_WBC = tk.Label(root_HCM, text='WBC:', font=LABEL_FONT)
    label_WBC.place(x=x_start + 0*x_gap, y=y_origin+i*gain-label_offset)

    text_PLT = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_PLT.place(x=x_start + 1*x_gap, y=y_origin+i*gain)
    label_PLT = tk.Label(root_HCM, text='PLT:', font=LABEL_FONT)
    label_PLT.place(x=x_start + 1*x_gap, y=y_origin+i*gain-label_offset)

    text_HGB = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_HGB.place(x=x_start + 2*x_gap, y=y_origin+i*gain)
    label_HGB = tk.Label(root_HCM, text='HGB:', font=LABEL_FONT)
    label_HGB.place(x=x_start + 2*x_gap, y=y_origin+i*gain-label_offset)


    text_PDW = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_PDW.place(x=x_start + 3*x_gap, y=y_origin+i*gain)
    label_PDW = tk.Label(root_HCM, text='PDW:', font=LABEL_FONT)
    label_PDW.place(x=x_start + 3*x_gap, y=y_origin+i*gain-label_offset)


    text_AlbG = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_AlbG.place(x=x_start + 4*x_gap, y=y_origin+i*gain)
    label_AlbG = tk.Label(root_HCM, text='AlbG:', font=LABEL_FONT)
    label_AlbG.place(x=x_start + 4*x_gap, y=y_origin+i*gain-label_offset)


    text_GLB = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_GLB.place(x=x_start + 5*x_gap, y=y_origin+i*gain)
    label_GLB = tk.Label(root_HCM, text='GLB:', font=LABEL_FONT)
    label_GLB.place(x=x_start + 5*x_gap, y=y_origin+i*gain-label_offset)


    text_ALT = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_ALT.place(x=x_start + 6*x_gap, y=y_origin+i*gain)
    label_ALT = tk.Label(root_HCM, text='ALT:', font=LABEL_FONT)
    label_ALT.place(x=x_start + 6*x_gap, y=y_origin+i*gain-label_offset)


    text_AST = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_AST.place(x=x_start + 7*x_gap, y=y_origin+i*gain)
    label_AST = tk.Label(root_HCM, text='AST:', font=LABEL_FONT)
    label_AST.place(x=x_start + 7*x_gap, y=y_origin+i*gain-label_offset)


    text_GGT = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_GGT.place(x=x_start + 8*x_gap, y=y_origin+i*gain)
    label_GGT = tk.Label(root_HCM, text='GGT:', font=LABEL_FONT)
    label_GGT.place(x=x_start + 8*x_gap, y=y_origin+i*gain-label_offset)


    text_BilT = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_BilT.place(x=x_start + 9*x_gap, y=y_origin+i*gain)
    label_BilT = tk.Label(root_HCM, text='BilT:', font=LABEL_FONT)
    label_BilT.place(x=x_start + 9*x_gap, y=y_origin+i*gain-label_offset)


    text_BilD = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_BilD.place(x=x_start + 10*x_gap, y=y_origin+i*gain)
    label_BilD = tk.Label(root_HCM, text='BilD:', font=LABEL_FONT)
    label_BilD.place(x=x_start + 10*x_gap, y=y_origin+i*gain-label_offset)


    text_PreAlbG = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_PreAlbG.place(x=x_start + 11*x_gap, y=y_origin+i*gain)
    label_PreAlbG = tk.Label(root_HCM, text='PreAlbG:', font=LABEL_FONT)
    label_PreAlbG.place(x=x_start + 11*x_gap, y=y_origin+i*gain-label_offset)

    text_CysC = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_CysC.place(x=x_start + 12*x_gap, y=y_origin+i*gain)
    label_CysC = tk.Label(root_HCM, text='CysC:', font=LABEL_FONT)
    label_CysC.place(x=x_start + 12*x_gap, y=y_origin+i*gain-label_offset)

    text_Crea = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_Crea.place(x=x_start + 13*x_gap, y=y_origin+i*gain)
    label_Crea = tk.Label(root_HCM, text='Crea:', font=LABEL_FONT)
    label_Crea.place(x=x_start + 13*x_gap, y=y_origin+i*gain-label_offset)

    text_Urea = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_Urea.place(x=x_start + 14*x_gap, y=y_origin+i*gain)
    label_Urea = tk.Label(root_HCM, text='Urea:', font=LABEL_FONT)
    label_Urea.place(x=x_start + 14*x_gap, y=y_origin+i*gain-label_offset)

    text_INR = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_INR.place(x=x_start + 15*x_gap, y=y_origin+i*gain)
    label_INR = tk.Label(root_HCM, text='INR:', font=LABEL_FONT)
    label_INR.place(x=x_start + 15*x_gap, y=y_origin+i*gain-label_offset)

    text_DDimer = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_DDimer.place(x=x_start + 16*x_gap, y=y_origin+i*gain)
    label_DDimer = tk.Label(root_HCM, text='D-Dimer:', font=LABEL_FONT)
    label_DDimer.place(x=x_start + 16*x_gap, y=y_origin+i*gain-label_offset)

    i = 3
    x_start = 40
    x_gap = 92
    label_offset = 25


    text_Trig = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_Trig.place(x=x_start + 0*x_gap, y=y_origin+i*gain)
    label_Trig = tk.Label(root_HCM, text='Trig:', font=LABEL_FONT)
    label_Trig.place(x=x_start + 0*x_gap, y=y_origin+i*gain-label_offset)

    text_Chol = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_Chol.place(x=x_start + 1*x_gap, y=y_origin+i*gain)
    label_Chol = tk.Label(root_HCM, text='Chol:', font=LABEL_FONT)
    label_Chol.place(x=x_start + 1*x_gap, y=y_origin+i*gain-label_offset)

    text_HDL = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_HDL.place(x=x_start + 2*x_gap, y=y_origin+i*gain)
    label_HDL = tk.Label(root_HCM, text='HDL:', font=LABEL_FONT)
    label_HDL.place(x=x_start + 2*x_gap, y=y_origin+i*gain-label_offset)

    text_LDL = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_LDL.place(x=x_start + 3*x_gap, y=y_origin+i*gain)
    label_LDL = tk.Label(root_HCM, text='LDL:', font=LABEL_FONT)
    label_LDL.place(x=x_start + 3*x_gap, y=y_origin+i*gain-label_offset)

    text_nonLDL = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_nonLDL.place(x=x_start + 4*x_gap, y=y_origin+i*gain)
    label_nonLDL = tk.Label(root_HCM, text='nonLDL:', font=LABEL_FONT)
    label_nonLDL.place(x=x_start + 4*x_gap, y=y_origin+i*gain-label_offset)

    text_ApoA = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_ApoA.place(x=x_start + 5*x_gap, y=y_origin+i*gain)
    label_ApoA = tk.Label(root_HCM, text='ApoA:', font=LABEL_FONT)
    label_ApoA.place(x=x_start + 5*x_gap, y=y_origin+i*gain-label_offset)

    text_ApoB = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_ApoB.place(x=x_start + 6*x_gap, y=y_origin+i*gain)
    label_ApoB = tk.Label(root_HCM, text='ApoB:', font=LABEL_FONT)
    label_ApoB.place(x=x_start + 6*x_gap, y=y_origin+i*gain-label_offset)

    text_LPa = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_LPa.place(x=x_start + 7*x_gap, y=y_origin+i*gain)
    label_LPa = tk.Label(root_HCM, text='LPa:', font=LABEL_FONT)
    label_LPa.place(x=x_start + 7*x_gap, y=y_origin+i*gain-label_offset)

    text_TnT = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_TnT.place(x=x_start + 8*x_gap, y=y_origin+i*gain)
    label_TnT = tk.Label(root_HCM, text='TnT:', font=LABEL_FONT)
    label_TnT.place(x=x_start + 8*x_gap, y=y_origin+i*gain-label_offset)

    text_ProBNP = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_ProBNP.place(x=x_start + 9*x_gap, y=y_origin+i*gain)
    label_ProBNP = tk.Label(root_HCM, text='ProBNP:', font=LABEL_FONT)
    label_ProBNP.place(x=x_start + 9*x_gap, y=y_origin+i*gain-label_offset)

    text_Glu = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_Glu.place(x=x_start + 10*x_gap, y=y_origin+i*gain)
    label_Glu = tk.Label(root_HCM, text='Glu:', font=LABEL_FONT)
    label_Glu.place(x=x_start + 10*x_gap, y=y_origin+i*gain-label_offset)

    text_HbA1c = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_HbA1c.place(x=x_start + 11*x_gap, y=y_origin+i*gain)
    label_HbA1c = tk.Label(root_HCM, text='HbA1c:', font=LABEL_FONT)
    label_HbA1c.place(x=x_start + 11*x_gap, y=y_origin+i*gain-label_offset)

    text_SG = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_SG.place(x=x_start + 12*x_gap, y=y_origin+i*gain)
    label_SG = tk.Label(root_HCM, text='SG:', font=LABEL_FONT)
    label_SG.place(x=x_start + 12*x_gap, y=y_origin+i*gain-label_offset)

    text_Ratio_UrineAlbu_Crea = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_Ratio_UrineAlbu_Crea.place(x=x_start + 13*x_gap, y=y_origin+i*gain)
    label_Ratio_UrineAlbu_Crea = tk.Label(root_HCM, text='Ratio_UrineAlbu_Crea:', font=LABEL_FONT)
    label_Ratio_UrineAlbu_Crea.place(x=x_start + 13*x_gap, y=y_origin+i*gain-label_offset)

    i = 4
    x_start = 40
    x_gap = 200
    label_offset = 25

    text_HR_average = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_HR_average.place(x=x_start + 0*x_gap, y=y_origin+i*gain)
    label_HR_average = tk.Label(root_HCM, text='Average HR:', font=LABEL_FONT)
    label_HR_average.place(x=x_start + 0*x_gap, y=y_origin+i*gain-label_offset)

    combo_IsAtrialFibrillation = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsAtrialFibrillation.place(x=x_start + 1*x_gap, y=y_origin+i*gain)
    label_IsAtrialFibrillation = tk.Label(root_HCM, text='IsAtrialFibrillation:', font=LABEL_FONT)
    label_IsAtrialFibrillation.place(x=x_start + 1*x_gap, y=y_origin+i*gain-label_offset)
    combo_IsAtrialFibrillation['values'] = ('Yes', 'No', 'Unknown', 'N/A')
    combo_IsAtrialFibrillation['state'] = 'readonly'

    combo_IsVentricularPrematureBeat = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_IsVentricularPrematureBeat.place(x=x_start + 2*x_gap, y=y_origin+i*gain)
    label_IsVentricularPrematureBeat = tk.Label(root_HCM, text='Has Ventricular Premature Beat?', font=LABEL_FONT)
    label_IsVentricularPrematureBeat.place(x=x_start + 2*x_gap, y=y_origin+i*gain-label_offset)
    combo_IsVentricularPrematureBeat['values'] = ('Yes', 'No', 'Unknown', 'N/A')
    combo_IsVentricularPrematureBeat['state'] = 'readonly'


    combo_TypeVentricularTachycardia = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_TypeVentricularTachycardia.place(x=x_start + 3*x_gap, y=y_origin+i*gain)
    label_TypeVentricularTachycardia = tk.Label(root_HCM, text='Type of Ventricular Tachycardia', font=LABEL_FONT)
    label_TypeVentricularTachycardia.place(x=x_start + 3*x_gap, y=y_origin+i*gain-label_offset)
    combo_TypeVentricularTachycardia['values'] = ('Monomorphic VT', 'Polymorphic VT',  'Unknown', 'N/A')
    combo_TypeVentricularTachycardia['state'] = 'readonly'

    combo_LGE = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_LGE.place(x=x_start + 4*x_gap, y=y_origin+i*gain)
    label_LGE = tk.Label(root_HCM, text='Cardial Magnetic', font=LABEL_FONT)
    label_LGE.place(x=x_start + 4*x_gap, y=y_origin+i*gain-label_offset)
    combo_LGE['values'] = ('LGE', 'None LGE',  'Unknown', 'N/A')
    combo_LGE['state'] = 'readonly'

    text_CCB = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_CCB.place(x=x_start + 5*x_gap, y=y_origin+i*gain)
    label_CCB = tk.Label(root_HCM, text='CCB:', font=LABEL_FONT)
    label_CCB.place(x=x_start + 5*x_gap, y=y_origin+i*gain-label_offset)

    text_BetaBlocker = tk.Text(root_HCM, width=10, height=1, font=EDIT_FONT, wrap='none')
    text_BetaBlocker.place(x=x_start + 6*x_gap, y=y_origin+i*gain)
    label_BetaBlocker = tk.Label(root_HCM, text='Beta-Blocker:', font=LABEL_FONT)
    label_BetaBlocker.place(x=x_start + 6*x_gap, y=y_origin+i*gain-label_offset)

    text_OtherMedication = tk.Text(root_HCM, width=15, height=1, font=EDIT_FONT, wrap='none')
    text_OtherMedication.place(x=x_start + 7*x_gap, y=y_origin+i*gain)
    label_OtherMedication = tk.Label(root_HCM, text='Other Medication:', font=LABEL_FONT)
    label_OtherMedication.place(x=x_start + 7*x_gap, y=y_origin+i*gain-label_offset)

    i = 5
    x_start = 40
    x_gap = 200
    label_offset = 25

    combo_Rehospitalization = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_Rehospitalization.place(x=x_start + 0*x_gap, y=y_origin+i*gain)
    label_Rehospitalization = tk.Label(root_HCM, text='Rehospitalization', font=LABEL_FONT)
    label_Rehospitalization.place(x=x_start + 0*x_gap, y=y_origin+i*gain-label_offset)
    combo_Rehospitalization['values'] = ('Yes', 'No',  'Unknown', 'N/A')
    combo_Rehospitalization['state'] = 'readonly'

    combo_AnginaRecurrent = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_AnginaRecurrent.place(x=x_start + 1*x_gap, y=y_origin+i*gain)
    label_AnginaRecurrent = tk.Label(root_HCM, text='Angina Recurrent?', font=LABEL_FONT)
    label_AnginaRecurrent.place(x=x_start + 1*x_gap, y=y_origin+i*gain-label_offset)
    combo_AnginaRecurrent['values'] = ('Yes', 'No',  'Unknown', 'N/A')
    combo_AnginaRecurrent['state'] = 'readonly'

    combo_AtrialFibrillationRecurrent = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_AtrialFibrillationRecurrent.place(x=x_start + 2*x_gap, y=y_origin+i*gain)
    label_AtrialFibrillationRecurrent = tk.Label(root_HCM, text='Atrial Fibrillation Recurrent?', font=LABEL_FONT)
    label_AtrialFibrillationRecurrent.place(x=x_start + 2*x_gap, y=y_origin+i*gain-label_offset)
    combo_AtrialFibrillationRecurrent['values'] = ('Yes', 'No',  'Unknown', 'N/A')
    combo_AtrialFibrillationRecurrent['state'] = 'readonly'

    combo_Mortality = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_Mortality.place(x=x_start + 3*x_gap, y=y_origin+i*gain)
    label_Mortality = tk.Label(root_HCM, text='Mortality?', font=LABEL_FONT)
    label_Mortality.place(x=x_start + 3*x_gap, y=y_origin+i*gain-label_offset)
    combo_Mortality['values'] = ('Yes', 'No',  'Unknown', 'N/A')
    combo_Mortality['state'] = 'readonly'

    combo_AblationAlcohol = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_AblationAlcohol.place(x=x_start + 4*x_gap, y=y_origin+i*gain)
    label_AblationAlcohol = tk.Label(root_HCM, text='Alcohol Ablation?', font=LABEL_FONT)
    label_AblationAlcohol.place(x=x_start + 4*x_gap, y=y_origin+i*gain-label_offset)
    combo_AblationAlcohol['values'] = ('Yes', 'No',  'Unknown', 'N/A')
    combo_AblationAlcohol['state'] = 'readonly'

    combo_AblationRF = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_AblationRF.place(x=x_start + 5*x_gap, y=y_origin+i*gain)
    label_AblationRF = tk.Label(root_HCM, text='RF Ablation?', font=LABEL_FONT)
    label_AblationRF.place(x=x_start + 5*x_gap, y=y_origin+i*gain-label_offset)
    combo_AblationRF['values'] = ('Yes', 'No',  'Unknown', 'N/A')
    combo_AblationRF['state'] = 'readonly'

    combo_Pacemaker = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_Pacemaker.place(x=x_start + 6*x_gap, y=y_origin+i*gain)
    label_Pacemaker = tk.Label(root_HCM, text='Pacemaker?', font=LABEL_FONT)
    label_Pacemaker.place(x=x_start + 6*x_gap, y=y_origin+i*gain-label_offset)
    combo_Pacemaker['values'] = ('Yes', 'No',  'Unknown', 'N/A')
    combo_Pacemaker['state'] = 'readonly'

    combo_Myectomy = ttk.Combobox(root_HCM, width=20, height=1, font=EDIT_FONT)
    combo_Myectomy.place(x=x_start + 7*x_gap, y=y_origin+i*gain)
    label_Myectomy = tk.Label(root_HCM, text='Myectomy?', font=LABEL_FONT)
    label_Myectomy.place(x=x_start + 7*x_gap, y=y_origin+i*gain-label_offset)
    combo_Myectomy['values'] = ('Yes', 'No',  'Unknown', 'N/A')
    combo_Myectomy['state'] = 'readonly'

    i = 6
    x_start = 40
    x_gap = 200
    label_offset = 25

    text_Genetic = tk.Text(root_HCM, width=220, height=2, font=EDIT_FONT, wrap='none')
    text_Genetic.place(x=x_start + 0*x_gap, y=y_origin+i*gain)
    label_Genetic = tk.Label(root_HCM, text='Genetic:', font=LABEL_FONT)
    label_Genetic.place(x=x_start + 0*x_gap, y=y_origin+i*gain-label_offset)   


    # //////// Search Area ////////////

    i = -0.7

    button_browse = ttk.Button(root_HCM, text='Browse', width=8, command=browse)
    button_browse.place(x=1640, y=y_origin+i*gain-5)

    i = 0.3

    text_CitizenID_search = tk.Text(root_HCM, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_CitizenID_search.place(x=1640, y=y_origin+i*gain)
    label_CitizenID_search = tk.Label(root_HCM, text='Citizen ID:', font=LABEL_FONT)
    label_CitizenID_search.place(x=1640,y=y_origin+i*gain-25)

    button_citizenID_search = ttk.Button(root_HCM, text='Search', width=8, command=citizenIDSearch)
    button_citizenID_search.place(x=1840, y=y_origin+i*gain-5)

    i = 1.3

    text_PatientName_search = tk.Text(root_HCM, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_PatientName_search.place(x=1640, y=y_origin+i*gain)
    label_PatientName_search = tk.Label(root_HCM, text='Paitnet Name:', font=LABEL_FONT)
    label_PatientName_search.place(x=1640,y=y_origin+i*gain-25)

    button_PatientName_search = ttk.Button(root_HCM, text='Search', width=8, command=patientNameSearch)
    button_PatientName_search.place(x=1840, y=y_origin+i*gain-5)   

    # ////// Buttons //////////////////////////

    button_update_HCM = ttk.Button(root_HCM, text='Update', width=10, command=update_HCM)
    button_update_HCM.place(x=1640, y=790)

    button_delete_HCM = ttk.Button(root_HCM, text='Delete', width=10, command=delete_HCM)
    button_delete_HCM.place(x=1800, y=790)

    button_exit = ttk.Button(root_HCM, text='Exit', width=8, command=root_HCM.destroy)
    button_exit.place(x=1640, y=880)

    # ///// Browse Automatically /////////////////////

    display_in_table(combination)

    root_HCM.mainloop()


# In[817]:


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
        try:
            item = table.selection()[0]
            value = table.item(item, 'values')    
            iden = value[0]
            ExtractID(iden)     
            idglb = iden
        except:
            pass

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
        def val(key):
            v = item.get(key)
            return '' if v is None else v

        text_id_in_patients.delete('1.0', tk.END)
        text_id_in_patients.insert('1.0', val('id_in_patients'))

        text_PatientName_in_patients.delete('1.0', tk.END)
        text_PatientName_in_patients.insert('1.0', val('PatientName_in_patients'))

        text_InPatientID.delete('1.0', tk.END)
        text_InPatientID.insert('1.0', val('InPatientID'))

        text_CitizenID.delete('1.0', tk.END)
        text_CitizenID.insert('1.0', val('CitizenID'))

        text_BirthDate.delete('1.0', tk.END)
        text_BirthDate.insert('1.0', val('BirthDate'))

        combo_Gender.set(val('Gender'))

        text_PatientName_CN.delete('1.0', tk.END)
        text_PatientName_CN.insert('1.0', val('PatientName_CN'))

        text_Telephone.delete('1.0', tk.END)
        text_Telephone.insert('1.0', val('Telephone1'))

        text_Comments.delete('1.0', tk.END)
        text_Comments.insert('1.0', val('Comments'))

        text_Diagnosis1.delete('1.0', tk.END)
        text_Diagnosis1.insert('1.0', val('Diagnosis1'))

        text_Diagnosis2.delete('1.0', tk.END)
        text_Diagnosis2.insert('1.0', val('Diagnosis2'))

        text_Diagnosis3.delete('1.0', tk.END)
        text_Diagnosis3.insert('1.0', val('Diagnosis3'))

        text_Diagnosis4.delete('1.0', tk.END)
        text_Diagnosis4.insert('1.0', val('Diagnosis4'))

        text_Diagnosis5.delete('1.0', tk.END)
        text_Diagnosis5.insert('1.0', val('Diagnosis5'))

    def update_patients():
            try:
                id_in_patients_gotten = text_id_in_patients.get('1.0', tk.END).rstrip()
                PatientName_in_patients_gotten = text_PatientName_in_patients.get('1.0', tk.END).rstrip()
                PatientName_CN_gotten = text_PatientName_CN.get('1.0', tk.END).rstrip()                
                Gender_gotten = combo_Gender.get().rstrip()

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

                update_sql = """
                    UPDATE Patients SET
                    PatientName_in_patients = ?,
                    PatientName_CN = ?,
                    Gender = ?,
                    InPatientID = ?,
                    CitizenID = ?,
                    BirthDate = ?,
                    Diagnosis1 = ?,
                    Diagnosis2 = ?,
                    Diagnosis3 = ?,
                    Diagnosis4 = ?,
                    Diagnosis5 = ?,
                    Telephone1 = ?,
                    Comments = ?
                    WHERE id_in_patients = ?
                    """

                update_values = (
                    PatientName_in_patients_gotten,
                    PatientName_CN_gotten,
                    Gender_gotten,
                    InPatientID_gotten,
                    CitizenID_gotten,
                    BirthDate_gotten,
                    Diagnosis1_gotten,
                    Diagnosis2_gotten,
                    Diagnosis3_gotten,
                    Diagnosis4_gotten,
                    Diagnosis5_gotten,
                    Telephone_gotten,
                    Comments_gotten,
                    id_in_patients_gotten
                )

                cur.execute(update_sql, update_values)
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

    root_patients = tk.Tk()
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

    for header_patient in headers_patients:
        table.heading('#'+str(i), text=header_patient.title(), anchor=tk.W, command=lambda c=header_patient: sortby(table, c, 0))
        col_width = tkf.Font().measure(header_patient.title()) + 50
        table.column('#'+str(i), stretch=tk.NO, minwidth=0, width=col_width)
        i+=1    
    table.column('#0', stretch=tk.NO, minwidth=0, width=0)

    table.bind("<Double-1>", OnDoubleClick_Patients)
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

    label_Patients=tk.Label(root_patients,width=140, height=25 , relief='raised', borderwidth=1)
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


    text_InPatientID = tk.Text(root_patients, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_InPatientID.place(x=240, y=y_origin+i*gain)
    label_InPatientID = tk.Label(root_patients, text='In-Patient ID:', font=LABEL_FONT)
    label_InPatientID.place(x=240,y=y_origin+i*gain-25)

    text_CitizenID = tk.Text(root_patients, width=25, height=1, font=EDIT_FONT, wrap='none')
    text_CitizenID.place(x=440, y=y_origin+i*gain)
    label_CitizenID = tk.Label(root_patients, text='Citizen ID:', font=LABEL_FONT)
    label_CitizenID.place(x=440,y=y_origin+i*gain-25)

    text_BirthDate = tk.Text(root_patients, width=20, height=1, font=EDIT_FONT, wrap='none')
    text_BirthDate.place(x=640, y=y_origin+i*gain)
    label_BirthDate = tk.Label(root_patients, text='Birth Date:', font=LABEL_FONT)
    label_BirthDate.place(x=640,y=y_origin+i*gain-25)

    i = 2

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

    i = 3

    text_Diagnosis4 = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis4.place(x=40, y=y_origin+i*gain)
    label_Diagnosis4 = tk.Label(root_patients, text='Diagnosis 4:', font=LABEL_FONT)
    label_Diagnosis4.place(x=40,y=y_origin+i*gain-25)

    text_Diagnosis5 = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Diagnosis5.place(x=340, y=y_origin+i*gain)
    label_Diagnosis5 = tk.Label(root_patients, text='Diagnosis 5:', font=LABEL_FONT)
    label_Diagnosis5.place(x=340,y=y_origin+i*gain-25)

    i = 4

    text_Telephone = tk.Text(root_patients, width=40, height=1, font=EDIT_FONT, wrap='none')
    text_Telephone.place(x=40, y=y_origin+i*gain)
    label_Telephone = tk.Label(root_patients, text='Telephone:', font=LABEL_FONT)
    label_Telephone.place(x=40,y=y_origin+i*gain-25)

    i = 5

    text_Comments = tk.Text(root_patients, width=130, height=3, font=EDIT_FONT, wrap='none')
    text_Comments.place(x=40, y=y_origin+i*gain)
    label_Comments = tk.Label(root_patients, text='Comments:', font=LABEL_FONT)
    label_Comments.place(x=40,y=y_origin+i*gain-25)

    # ////// Buttons //////////////////////////

    button_update_patient = ttk.Button(root_patients, text='Update', width=10, command=update_patients)
    button_update_patient.place(x=1060, y=750)

    button_delete_patient = ttk.Button(root_patients, text='Delete', width=10, command=delete_patient)
    button_delete_patient.place(x=1250, y=750)

    button_exit = ttk.Button(root_patients, text='Exit', width=10, command=root_patients.destroy)
    button_exit.place(x=1060, y=830)

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

    root_patients.mainloop()


# In[818]:


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


# In[819]:


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


# In[820]:


def new_HCM():
    root_new_HCM = tk.Tk()

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

    root_new_HCM.mainloop()


# In[821]:


def new_patient():
    root_new_patient = tk.Tk()

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

    root_new_patient.mainloop()

    #t = datetime.datetime.now()
    #ts = str(datetime.datetime.now())

    #datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')


# In[822]:


def new_followUp():
    root_followUp = tk.Tk()

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

    button_cancel=ttk.Button(root_followUp, text='Cancel', width=15, command=root_new_patient.destroy)
    button_cancel.place(x=600, y=y_origin+i*gain)      

    root_followUp.mainloop()

    #t = datetime.datetime.now()
    #ts = str(datetime.datetime.now())

    #datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')


# In[823]:


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


# In[824]:


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


# In[825]:


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


# In[826]:


def about():
    about_root=tk.Tk()

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

    about_root.mainloop()


# In[827]:


def exit_the_main():    
    root.quit()
    root.destroy()


# ## Main Flow

# In[828]:


root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#root.attributes('-fullscreen', True)
root.title('CharlestonPark')
#root.iconbitmap('CharlestonParkIcon.ico')

### Multicolumn Listbox

# Multicolumn Listbox/////////////////////////////////////////////////////////////////////////////
table = ttk.Treeview(root, height="20", columns=headers, selectmode="extended")
table.pack(padx=10, pady=20, ipadx=1200, ipady=200)


i = 1

for header in headers:
    table.heading('#'+str(i), text=header.title(), anchor=tk.W, command=lambda c=header: sortby(table, c, 0))
    col_width = tkf.Font().measure(header.title()) + 50
    table.column('#'+str(i), stretch=tk.NO, minwidth=0, width=col_width)
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

text_Comments = tk.Text(root, width=125, height=1, font=EDIT_FONT, wrap='none')
text_Comments.place(x=650, y=y_origin+i*gain)
label_Comments = tk.Label(root, text='Comments:', font=LABEL_FONT)
label_Comments.place(x=650,y=y_origin+i*gain-25)

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
button_about.place(x=1680, y=810)

# Exit

button_exit = ttk.Button(root, text='Exit', width=9, command=exit_the_main)
button_exit.place(x=1680, y=880)

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

root.mainloop()

conn.close()

#t = datetime.datetime.now()
#ts = str(datetime.datetime.now())

#datetime.datetime.strptime(ts, '%Y%m%d%I%M%S%f')


# In[ ]:




