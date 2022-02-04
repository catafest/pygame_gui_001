import random

#from datetime import datetime
from datetime import datetime, timedelta
import names

import sqlite3
from sqlite3 import Error

from os.path import exists

import os
workingpath = os.path.dirname(os.path.abspath(__file__))

allnames = []

def genBirthday():
    year = str(random.randint(1944, 2018))
    #month = random.randint(1, 12)
    months =['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month = random.choice(months)
    day = str(random.randint(1, 28))
    birth_date = day+":"+month+":"+year
    return str(birth_date)

def getNamesNr(namesnr, gender='female'):
    for i in range(namesnr):
        rand_name = names.get_full_name(gender)
        allnames.append(rand_name)
    return(allnames)

def create_update_DB(namesnr):
    try:
        con = sqlite3.connect(workingpath+'\patients.db')      
        cursorObj = con.cursor()
        cursorObj.execute("CREATE TABLE IF NOT EXISTS patients(id integer PRIMARY KEY, fn text, sn text, dbay text, symptoms text, doctor text, cured text,hospital text)")

        allnames = getNamesNr(namesnr=5, gender='female')
        records =[]
        
        for i in range(len(allnames)):
            fn = allnames[i].split(" ")[0]
            sn = allnames[i].split(" ")[1]
            print("fn = ", fn, "sn = ", sn)
            diseaseL = ["Allergies","Colds and Flu","Conjunctivitis or pink eye","Diarrhea","Headaches","Mononucleosis","Stomach Aches"]
            symptomsL =["Eye irritation",
                        "Runny nose",
                        "Stuffy nose",
                        "Puffy, watery eyes",
                        "Sneezing",
                        "Inflamed, itchy nose and throat",
                        "Allergens that are consumed",
                        "Hives or skin rashes",
                        "Diarrhea, ",
                        "Nausea, ",
                        "Vomiting, ",
                        "Excessing gas, ",
                        "Indigestion",
                        "Tingling",
                        "Swelling of the lips, face, or tongue",
                        "Itchiness",
                        "Difficulty breathing or wheezing",
                        "Fainting or lightheadedness"]
            doctorL = ["without a doctor", "Dr. Concern"]
            curedL = ["with treatment","sick","suffer from dizziness","suffers from stomach","has migraine","suffers from leg pain","his hand hurts","suffers from chest pain","heart hurts"]
            hospitalL = ["released and returned","interned","just arrived"]
            symptoms = random.choice(symptomsL)
            doctor = random.choice(doctorL)
            cured = random.choice(curedL)
            hospital = random.choice(hospitalL)
            bday = genBirthday()
            records.append((i+1,fn,sn,bday,symptoms,doctor,cured,hospital))    
        #print(records)
        query  = ('INSERT OR IGNORE INTO patients VALUES(?,?,?,?,?,?,?,?);')
        cursorObj.executemany(query,records)
        con.commit()
    except Error:
        print(Error)

def getRowDB():
    con = sqlite3.connect(workingpath+'\patients.db')
    q = "SELECT id , fn , sn , dbay, symptoms , doctor , cured ,hospital from patients"
    my_cursor=con.execute(q)
    data_rows=my_cursor.fetchall()
    print(type(data_rows)) # <class 'list'>
    ll = []
    for row in data_rows:
        #ll.append(row[0],row[1],row[2],row[3],row[4],row[5], row[6],row[7])
        ll.append(row)
    return data_rows

print("workingpath is "+workingpath)
file_exists = exists(workingpath+'\patients.db')
if file_exists == False:
    print("File "+workingpath+"\patients.db not exist and will be created!")
    create_update_DB(namesnr=10)  
else:
    print("File "+workingpath+"\patients.db exist!")

#getRows = getRowDB()

