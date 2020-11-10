import xml
import logging
import pandas as pd
from bs4 import BeautifulSoup as bs
import re
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import tkinter as tk
import tkinter.messagebox as msg
import os
from tkinter import filedialog
from tkinter.filedialog import askopenfile,askopenfilename,asksaveasfile
from openpyxl.styles import Alignment
#==================================================================================================================#


OptionList = ["LTE FDD & TDD --> GSM"]#,"LTE FDD & TDD --> UMTS","UMTS --> LTE FDD & TDD","GSM --> LTE FDD & TDD"]

#Started
def lte2gsm():
    before = '''
    <raml>
    <cmData type="actual">
            '''
    umts_xml = '''
        <managedObject class="LNADJW" version="FL17SP_1701_03_1701_02" distName="{}" operation="create">
      <p name="targetCellDn">{}</p>
    </managedObject>
    '''
    gsm_xml = '''
    	    <managedObject class="LNADJG" version="FL17SP_1701_03_1701_02" distName="{}" operation="create">
      <p name="targetCellDn">{}</p>
    </managedObject>
    '''

    df_cell = pd.read_excel(fileinexcel,sheet_name=4)
    
    g4 = []

    for i in range(len(df_cell)):
        if df_cell['Technology'][i] =="4G":
            g4.append(df_cell['DN'][i])
    MRBTS = []

    for i in g4:
        k = re.findall(r'MRBTS-\d+',i)[0][6:]
        if k not in MRBTS:
            MRBTS.append(k)

    def content():
        g2 = []
        g3 = []
        g4 = []
        g5 = []

        for i in range(len(df_cell)):
            if df_cell['Technology'][i] =="2G":
                g2.append(df_cell['DN'][i])
            elif df_cell['Technology'][i] =="3G":
                g3.append(df_cell['DN'][i])
            elif df_cell['Technology'][i] =="4G":
                g4.append(df_cell['DN'][i])
            elif df_cell['Technology'][i] =="5G":
                g5.append(df_cell['DN'][i])

        cell_data = {

        }
        cell_data["4G"]=g4
        cell_data["5G"]=g5
        cell_data["2G"]=g2
        cell_data["3G"]=g3

        # print(cell_data["2G"])
        # print(cell_data["3G"])
        targetCellDn = []
        targetCellDn_1 = []
        targetCellDn_distName = []
        targetCellDn_1_distName = []

        with open(fileinxml,'r') as file_in:
            content = file_in.read()
        soup = bs(content,'xml')
        
        pattern1 = re.compile('^PLMN-PLMN/MRBTS-'+mr+'.*LNADJW-\d+')
        pattern2 = re.compile('^PLMN-PLMN/MRBTS-'+mr+'.*LNADJG-\d+')
        LNADJW = soup.find_all('managedObject',{'distName':pattern1})
        LNADJG = soup.find_all('managedObject',{'distName':pattern2})
        dn = []
        dn2 = []

        for i in LNADJG:
            k = i.find('p',{'name':'targetCellDn'}).string
            if k in cell_data["2G"]:
                cell_data["2G"].remove(k)

        for j in LNADJW:
            k = j.find('p',{'name':'targetCellDn'}).string
            if k in cell_data["3G"]:
                cell_data["3G"].remove(k)
        # print(cell_data["2G"])
        # print(cell_data["3G"])
            ##########################################################################################################
        if len(LNADJW)==0:
            for i in range(len(cell_data["3G"])):
                print(umts_xml.format("PLMN-PLMN/MRBTS-{MRBTS}/LNBTS-{MRBTS}/LNADJW-".format(MRBTS =mr)+str(i),cell_data['3G'][i]),file=file_out)
        else:
            for i in LNADJW:
                dns = re.findall(r'LNADJW-\d+',i['distName'])[0][7:]#
                if dns not in dn:
                    dn.append(dns)
            for i in range(len(cell_data['3G'])):
                def checkdn(num):
                    if str(num) not in dn:
                        print(umts_xml.format("PLMN-PLMN/MRBTS-{MRBTS}/LNBTS-{MRBTS}/LNADJW-".format(MRBTS =mr)+str(num),cell_data['3G'][i]),file=file_out)
                        dn.append(str(num))
                    else:
                        checkdn(num+1)
                checkdn(i)
            #########################################################################################################
        
        if len(LNADJG)==0:
            for i in range(len(cell_data["2G"])):
                print(gsm_xml.format("PLMN-PLMN/MRBTS-{MRBTS}/LNBTS-{MRBTS}/LNADJG-".format(MRBTS=mr)+str(i),cell_data['2G'][i]),file=file_out)
        else:
            for i in LNADJG:
                dns2 = re.findall(r'LNADJG-\d+',i['distName'])[0][7:]
                if dns2 not in dn2:
                    dn2.append(dns2)
            for i in range(len(cell_data['2G'])):
                def checkdn2(num):
                    if str(num) not in dn2:
                        print(gsm_xml.format("PLMN-PLMN/MRBTS-{MRBTS}/LNBTS-{MRBTS}/LNADJG-".format(MRBTS=mr)+str(num),cell_data['2G'][i]),file=file_out)
                        dn2.append(str(num))
                    else:
                        checkdn2(num+1)
                checkdn2(i)    
            #########################################################################################################
    for mr in MRBTS:
        with open("LTE_to_GSM"+mr+'.xml','a') as file_out:
            print(before,file=file_out)
            content()
        with open("LTE_to_GSM"+mr+'.xml','r') as file_in:
            content2 = file_in.read()
        soup = bs(content2,'xml')

        with open("LTE_to_GSM"+mr+'.xml','w') as file_2:
            file_2.truncate(0)
            print(soup,file=file_2)
    msg.showinfo("Completed!", "Files generated")
#completed     

def lte2umts():
    pass

def umts2lte():
    pass

def gsm2lte():
    pass



def option():
    msg.showinfo("Attention!", "Pleasse select technology from menu")

def selected(valu):
    msg.showinfo("Selected Files!",[str("\n"+i).split("/")[-1][0:-5] for i in valu])

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Amdocs Update tech")
    root.geometry("400x300")
    # root.geometry("895x500")
    root.configure(bg='#209ffa')
    # root.wm_iconbitmap('Amdocs_logo.ico')


    variable = tk.StringVar(root)
    variable.set("Technology")
    opt = tk.OptionMenu(root, variable, *OptionList)
    opt.config(width=20,font=('consolas', 8))
    opt.grid(row = 1, column = 2)

    style = ttk.Style()
    style.theme_use('xpnative')
    style.configure("black.Horizontal.TProgressbar", background='green')
    # gpw_l1 = tk.Label(root, text="Progress Bar",bg="White", fg="green").grid(row=6, column=1)
    
    # progress = Progressbar(root, orient = HORIZONTAL,length = 100, mode = 'determinate',style='black.Horizontal.TProgressbar')

    # my_label = tk.Label(root, text = "Excel path 1: ")
    # my_label.grid(row = 1, column = 1)
    # excel_path_entry = tk.Entry(root)
    # excel_path_entry.grid(row = 1, column = 2,padx=5,pady=10,ipady=3,ipadx=100)

    def fullsitexml():
        global fileinxml
        fileinxml = filedialog.askopenfilename(filetypes =[('XML Files', '*.xml')])
        # selected(filein)
    def excel_file():
        global fileinexcel
        fileinexcel = filedialog.askopenfilename(filetypes =[('Excel Files', '*.xlsx')])
        # selected(filein)

    pre_report_button = tk.Button(root, text = "Input full XML", command = fullsitexml,activeforeground = "Green",activebackground = "White",pady=1,bg="#4203c9",fg="white").place(x = 50,y = 60)#250,200
    pre_report_button = tk.Button(root, text = "Input Excel Data", command = excel_file,activeforeground = "Green",activebackground = "White",pady=1,bg="#4203c9",fg="white").place(x = 150,y = 60)#250,200

    # my_label = tk.Label(root, text = "Excel Name 1: ")
    # my_label.grid(row = 4, column = 1)
    # excel_name_entry = tk.Entry(root)
    # excel_name_entry.grid(row = 4, column = 2,padx=5,pady=10,ipady=3,ipadx=250)


    # my_label = tk.Label(root, text = "XML name : ")
    # my_label.grid(row = 6, column = 1)
    # xml_name_entry = tk.Entry(root)
    # xml_name_entry.grid(row = 6, column = 2,padx=5,pady=10,ipady=3,ipadx=250)


    def callback(*args):
        if variable.get()=="LTE FDD & TDD --> GSM":
            # progress.grid(row = 10, column = 2,pady = 42,ipadx=0,ipady=3)
            fun = lte2gsm
        elif variable.get()=="LTE FDD & TDD --> UMTS":
            # progress.grid(row = 10, column = 2,pady = 42,ipadx=0,ipady=3)
            fun = lte2umts
        elif variable.get()=="UMTS --> LTE FDD & TDD":
        #special for 2G/GSM
            # progress.grid(row = 10, column = 2,pady = 42,ipadx=0,ipady=3)
            fun = umts2lte
        elif variable.get()=="GSM --> LTE FDD & TDD":
        #special for 2G/GSM
            # progress.grid(row = 10, column = 2,pady = 42,ipadx=0,ipady=3)
            fun = gsm2lte
        else:
            fun = nothing
        my_button = tk.Button(root, text = "Generate XML", command = fun,activeforeground = "Green",activebackground = "White",pady=1).place(x = 100,y = 120)#280,400
    variable.trace("w", callback)
    my_button = tk.Button(root, text = "Generate XML",command = option,activeforeground = "Green",activebackground = "White",pady=1).place(x = 100,y = 120)#280,400
    btn1 = tk.Button(root, text = 'Quit !', command = root.destroy,activeforeground = "Red",activebackground = "White",pady=1).place(x = 120,y = 160)#387,450
    root.mainloop()
