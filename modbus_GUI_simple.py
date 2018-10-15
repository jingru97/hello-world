#!/usr/bin/env python

import socket, struct, time, re, sys, difflib, os, threading, datetime, ssl
#from Tkinter import *
from tkinter import *
from tkinter import ttk
#from Tkinter import font
from tkinter import font
#import Tix
import tkinter.tix

isFile=0
#Open and read the configuration file, putting the lines in a list
try:
    with open("values.txt") as f:
        isFile=1
        content = f.readlines()
except IOError:
    print ("No values.txt in working directory")
        
TCP_PORT = 502
BUFFER_SIZE = 0

#Make the test results green or red
def color_test(passfail):

    #Get the number of lines by looking at the last character in the text box
    numlines = int(t.index('end').split('.')[0])-1
        
    #Make the result green if passed and red if failed
    if passfail==1:
        
        #Add a tag to "Test Passed"
        t.tag_add("test1",str(numlines)+'.0',str(numlines)+'.11')
        
        #Configure the tag to make the text green
        t.tag_config("test1",foreground='green')
    
    elif passfail==2:
        
        #Add a tag to "Test Failed"
        t.tag_add("test2",str(numlines)+'.0',str(numlines)+'.11')
        
        #Configure the tag to make the text red
        t.tag_config("test2",foreground='red')
        
    #Add a newline character
    outputstr='\n'
    
    #Insert the newline to the end of the text box
    t.insert(END,outputstr)

#Same as above function but for "Test X Passed" or "Test X Failed"
def color_test2(passfail):

    numlines = int(t.index('end').split('.')[0])-1
        
    
    if passfail==1:
        t.tag_add("test3",str(numlines)+'.7',str(numlines)+'.14')
        t.tag_config("test3",foreground='green')
    elif passfail==2:
        t.tag_add("test4",str(numlines)+'.7',str(numlines)+'.14')
        t.tag_config("test4",foreground='red')
        
    outputstr='\n'
    t.insert(END,outputstr)


#Stops a loop
def stopLoop():
    loopStop.set('1')



#Send a CIP request in a loop
def runLoop():
    global responsefile
    responsefile = open("response_times.txt", "w")

    loopStop.set('0')
    
    loop_count = loop_count_ent.get()
    
    if loop_count == "":
        loop_count = 5
    else:
        loop_count = int(loop_count)
    
    t.insert(END,"\nRunning...Press ctrl+C on the command line to stop\n")
    

    x=0
    while x < loop_count:

        root.update()
        #time.sleep(1.5)
    
        if loopStop.get() == '1':
            break
    
        if x==0:
            numlines = int(t.index('end').split('.')[0])-1
            t.delete(str(numlines-1)+'.0',str(numlines)+'.0')

        if loopStop.get() == '0':
            
            t.insert(END,"\nIteration #"+str(x+1)+"\n")
            
            sendModbus()
            
            loop_delay = loop_ent.get()
            
            if loop_delay == "":
                loop_delay = 0
            
            time.sleep(float(loop_delay) * 0.001)
            #time.sleep(2)

        if loop_count_ent.get() == "":
            x=0
        else:
            x+=1


    doResponses()



# Calculate and output the response time min, max, and avg
def doResponses():

    global responsetimes
    global responsefile

    for x in range(0, len(responsetimes)):

        if x == 0:
            min = float(responsetimes[x])
            max = float(responsetimes[x])
            avg = float(responsetimes[x])
            total = float(responsetimes[x])
        else:
            if float(responsetimes[x]) < min:
                min = float(responsetimes[x])
            if float(responsetimes[x]) > max:
                max = float(responsetimes[x])
            total += float(responsetimes[x])
            avg = total / (x + 1)

    if len(responsetimes) > 0:
        t.insert(END, "Response time min = " + str(min) + "\n")
        t.insert(END, "Response time max = " + str(max) + "\n")
        t.insert(END, "Response time avg = " + str(avg) + "\n")
        responsefile.write("Response time min = " + str(min) + "\n")
        responsefile.write("Response time max = " + str(max) + "\n")
        responsefile.write("Response time avg = " + str(avg) + "\n")

    responsefile.close()


#Run from a file in a loop
def runFileLoop():
    global responsefile
    responsefile = open("response_times.txt", "w")


    loopStop.set('0')
    
    loop_count = loop_count_ent.get()
    
    if loop_count == "":
        loop_count = 5
    else:
        loop_count = int(loop_count)
    
    t.insert(END,"\nRunning...Press ctrl+C on the command line to stop\n")

    x=0
    while x < loop_count:
    
        root.update()
        
        if loopStop.get() == '1':
            break
    
    
        if x==0:
            numlines = int(t.index('end').split('.')[0])-1
            t.delete(str(numlines-1)+'.0',str(numlines)+'.0')
    
        if loopStop.get() == '0':
            
            t.insert(END,"\nIteration #"+str(x+1)+"\n")
            
            runFromFile()
            
            loop_delay = loop_ent.get()
            
            if loop_delay == "":
                loop_delay = 0
            
            time.sleep(float(loop_delay) * 0.001)
            #time.sleep(2)

        if loop_count_ent.get() == "":
            x=0
        else:
            x+=1
    
#Function to compare what is in the output text box to a results file
def diff_outputs():

    #Open what is in the filename entry for reading
    with open(filename3_entry.get(),'r') as f3:
    
        #Get the entire contents of the text box (from row 1, column 0 to the end) and put it in a variable called "output"
        output = t.get("1.0",END)
        
        #Remove the file "diff_temp" if it exists
        try:
            os.remove('diff_temp')
        except WindowsError:
            pass
            
        #Delay for 1 second and create a blank file called "diff_temp"
        time.sleep(1)
        f5=open('diff_temp','a')
        f5.close()
        
        #Open diff_temp for reading and writing, write the textbox output to it, and put the lines in a list
        with open('diff_temp','r+') as f4:
            f4.write(output)
            f4.seek(0)
            output_lines = f4.readlines()
        
        #Put the lines of the file in a list
        #output_lines = output.strip().splitlines()
        file_lines = f3.readlines()
        
        #Diff the file and the output
        diff = difflib.unified_diff(output_lines,file_lines,fromfile='output',tofile='file',n=0)
        
        #for line in diff:
        #    print (line)

        #Remove diff_temp2 if it exists
        try:
            os.remove('diff_temp2')
        except WindowsError:
            pass
        
        #Create a blank diff_temp2
        time.sleep(1)
        f6=open('diff_temp2','a')
        f6.close()
        
        #Put the diff in diff_temp2 and put the lines in the variable diff_lines
        with open('diff_temp2','r+') as f7:
            for line in diff:
                f7.write(line)
            f7.seek(0)
            diff_lines = f7.readlines()
        
        #diff_lines = diff
        
        diff_lines2 = diff_lines

        #Insert the diff into the textbox
        for line in diff_lines2:
            
            #if not (line.startswith('---') or line.startswith('+++') or line.startswith('@@')):
            t2.insert(END,line)

        for z in range(3,len(diff_lines)):
            
            if diff_lines[z][0] == '+':
                break
                
       # print (z)
            
        if z==4:
            
            #Make the differences in the diff red
            #i corresponds to the line number
            #j iterates from 0,1,2 after the third line and we do our calculations when it is 1
            #k is the element in the line
            #i=0
            j=0
            for i in range(0,len(diff_lines)):
                #i+=1
                
                
                if j==2:
                    j=0
                elif j==1:
                    j+=1
                elif (i!=0 and i!=1 and i!=2):
                    if j==0:
                        j+=1

                difference=0
                #remember_k_start=0
                #remember_k_end=0
                if j==1:
                    
                    #Iterate through every character in the line
                    for k in range(0,len(diff_lines[i])):
                        
                        try:
                            #Compare a single character between two lines
                            #When we find a difference, set the variable "difference" to 1
                            #and remember the value of k
                            #Then when we reach a similarity again, set "difference" to 0
                            #and use the value of k that we saved along with the current value of k
                            #to specify the region that is different that we want to make red
                            #We catch an IndexError if the two lines are different size, and if this is the case
                            #then we make the remainder in the bigger line red
                            if diff_lines[i][k] != diff_lines[i+1][k]:
                                
                                if difference==0:
                                    remember_k_start=k
                                difference=1
                                
                                
                            elif difference==1:
                                difference=0
                                remember_k_end=k
                                t2.tag_add("test5",str(i+1)+'.'+str(remember_k_start),str(i+1)+'.'+str(remember_k_end))
                                t2.tag_config("test5",foreground="red")
                                t2.tag_add("test5",str(i+2)+'.'+str(remember_k_start),str(i+2)+'.'+str(remember_k_end))
                                t2.tag_config("test5",foreground="red")
                        except IndexError:
                            if len(diff_lines[i]) > len(diff_lines[i+1]):
                                if difference==1:
                                    t2.tag_add("test5",str(i+1)+'.'+str(remember_k_start),str(i+1)+'.'+str(len(diff_lines[i])-1))
                                    t2.tag_config("test5",foreground="red")
                                else:
                                    t2.tag_add("test5",str(i+1)+'.'+str(k),str(i+1)+'.'+str(len(diff_lines[i])-1))
                                    t2.tag_config("test5",foreground="red")
                            elif len(diff_lines[i+1]) > len(diff_lines[i]):
                                if difference==1:
                                    t2.tag_add("test5",str(i+2)+'.'+str(remember_k_start),str(i+2)+'.'+str(len(diff_lines[i+1])-1))
                                    t2.tag_config("test5",foreground="red")
                                else:
                                    t2.tag_add("test5",str(i+2)+'.'+str(k),str(i+2)+'.'+str(len(diff_lines[i+1])-1))
                                    t2.tag_config("test5",foreground="red")
                
        else:
            
            #j=z
            j=3
            
            for i in range(3,len(diff_lines)):
            
                if z==len(diff_lines):
                    break
            
                difference=0
            
                #Iterate through every character in the line
                for k in range(0,len(diff_lines[j])):
                    
                    try:
                        #Compare a single character between two lines
                        #When we find a difference, set the variable "difference" to 1
                        #and remember the value of k
                        #Then when we reach a similarity again, set "difference" to 0
                        #and use the value of k that we saved along with the current value of k
                        #to specify the region that is different that we want to make red
                        #We catch an IndexError if the two lines are different size, and if this is the case
                        #then we make the remainder in the bigger line red
                        if diff_lines[j][k] != diff_lines[z][k]:
                            
                            if difference==0:
                                remember_k_start=k
                            difference=1
                            
                            
                        elif difference==1:
                            difference=0
                            remember_k_end=k
                            t2.tag_add("test5",str(j+1)+'.'+str(remember_k_start),str(j+1)+'.'+str(remember_k_end))
                            t2.tag_config("test5",foreground="red")
                            t2.tag_add("test5",str(z+1)+'.'+str(remember_k_start),str(z+1)+'.'+str(remember_k_end))
                            t2.tag_config("test5",foreground="red")
                    except IndexError:
                        if len(diff_lines[j]) > len(diff_lines[z]):
                            if difference==1:
                                t2.tag_add("test5",str(j+1)+'.'+str(remember_k_start),str(j+1)+'.'+str(len(diff_lines[j])-1))
                                t2.tag_config("test5",foreground="red")
                            else:
                                t2.tag_add("test5",str(j+1)+'.'+str(k),str(j+1)+'.'+str(len(diff_lines[j])-1))
                                t2.tag_config("test5",foreground="red")
                        elif len(diff_lines[z]) > len(diff_lines[j]):
                            if difference==1:
                                t2.tag_add("test5",str(z+1)+'.'+str(remember_k_start),str(z+1)+'.'+str(len(diff_lines[z])-1))
                                t2.tag_config("test5",foreground="red")
                            else:
                                t2.tag_add("test5",str(z+1)+'.'+str(k),str(z+1)+'.'+str(len(diff_lines[z])-1))
                                t2.tag_config("test5",foreground="red")
            
                j+=1
                z+=1


# Run from file and do a compare
def runAndCompare():
    compares = 0
    passes = 0
    fails = 0

    global responsefile
    responsefile = open("response_times.txt", "w")

    global runAndCompare_var
    runAndCompare_var = 1
    comparefile_op.set('1')
    runFromFile()
    runAndCompare_var = 0

    responsefile.close()


reqsRan = 0
reqsRead = 0
#Execute tests that are in a previous output file
def runFromFile():

    global reqsRan
    global reqsRead

    individual=0
    sessions=0

    with open(filename2_entry.get(),"r") as f2:
        
        file_contents = f2.readlines()
        
    reached_end=0
    half_op.set('0')
    toggleAll()
    
    for line in file_contents:
        
        if line[0]=='(' and sessions == 0 and reqsRead >= reqsRan:
            
            reqsRead+=1
            
            if reached_end==1:
                reached_end=0
            
            readchar=''
            i=1
            num=''
            while readchar != ')':
                
                readchar = line[i]
                if readchar==')':
                    break
                
                num+=readchar
                
                i+=1
                
            if num=='1':
                cl.setstatus('CL1.Item1',"on")
            elif num=='2':
                cl.setstatus('CL1.Item2',"on")
            elif num=='3':
                cl.setstatus('CL1.Item3',"on")
            elif num=='4':
                cl.setstatus('CL1.Item4',"on")
            elif num=='5':
                cl.setstatus('CL1.Item5',"on")
            elif num=='6':
                cl.setstatus('CL1.Item6',"on")
            elif num=='7':
                cl.setstatus('CL1.Item7',"on")
            elif num=='8':
                cl.setstatus('CL1.Item8',"on")
            elif num=='9':
                cl.setstatus('CL1.Item9',"on")
            elif num=='10':
                cl.setstatus('CL2.Item1',"on")
            elif num=='11':
                cl.setstatus('CL2.Item2',"on")
            elif num=='12':
                cl.setstatus('CL2.Item3',"on")
            elif num=='13':
                cl.setstatus('CL2.Item4',"on")
            elif num=='14':
                cl.setstatus('CL2.Item5',"on")
            elif num=='15':
                cl.setstatus('CL2.Item6',"on")
            elif num=='16':
                cl.setstatus('CL2.Item7',"on")
            elif num=='17':
                cl.setstatus('CL2.Item8',"on")
            elif num=='18':
                cl.setstatus('CL2.Item9',"on")
            elif num=='19':
                cl.setstatus('CL2.Item10',"on")
            elif num=='20':
                cl.setstatus('CL2.Item11',"on")
            elif num=='21':
                cl.setstatus('CL3.Item1',"on")
            elif num=='22':
                cl.setstatus('CL3.Item2',"on")
            elif num=='23':
                cl.setstatus('CL3.Item3',"on")
            elif num=='24':
                cl.setstatus('CL3.Item4',"on")
            elif num=='25':
                cl.setstatus('CL4',"on")
            elif num=='26':
                cl.setstatus('CL5',"on")
            elif num=='27':
                cl.setstatus('CL6',"on")
            elif num=='28':
                cl.setstatus('CL7',"on")
            elif num=='29':
                cl.setstatus('CL8',"on")
            elif num=='30':
                cl.setstatus('CL9',"on")
            elif num=='31':
                cl.setstatus('CL10',"on")
            elif num=='32':
                cl.setstatus('CL11',"on")
            elif num=='33':
                cl.setstatus('CL12',"on")
            elif num=='34':
                cl.setstatus('CL13',"on")
            elif num=='35':
                cl.setstatus('CL14',"on")
                reached_end=1
                line2=""
                requ=""
                i2=0
                while line2 != "\n":
                    
                    line2 = file_contents[file_contents.index(line)+2+i2]
                    i2+=1
                    if line2=="\n":
                        break
                        
                    requ+=line2
                    
                    
                testlist = requ.split(" ")

                outputstring=""
                for x in range(7,len(testlist)):

                    ele = testlist[x]
                    if len(ele)==3:      
                        ele=ele[0:2]+'0'+ele[2]

                    outputstring+= ele[2:]
                
                custom_ent.set(outputstring)
                sendModbus()
                half_op.set('0')
                toggleAll()
                
                
        elif line[0:4] == 'Test' and (line[0:6] != 'Test P' and line[0:6] != 'Test F') and reached_end==0:
            
            reached_end=1
            sendModbus()
            half_op.set('0')
            toggleAll()
        
                
        elif individual == 0 and line[0] == "O":
        
            reqsRan = 0
            reqsRead = 0
            sessions = 1
            
            d = 8
            num=''
            while line[d] != ' ':
                num+=line[d]
                d+=1
            
            sessions_ent.set(num)
            
            
        #insertstr = "\nRunning "+loop_count_ent.get()+" iterations, delay "+loop_ent.get()+", closeopen "+closeopen_op.get()+", tests "
        elif individual == 0 and line[0:2] == "Ru":
        
            d = 8
            num=''
            while line[d] != ' ':
                num+=line[d]
                d+=1
            
            loop_count_ent.set(num)
            
            d+=19
            num=''
            while line[d] != ",":
                num+=line[d]
                d+=1
                
            loop_ent.set(num)
            
            d+=12
            num=''
            while line[d] != ",":
                num+=line[d]
                d+=1
                #print (line[d])
                
            closeopen_op.set(num)
            
            d+=8
            num=''
            selectionsstr=line[d:]
            selections=selectionsstr.split(",")
            
            for num in selections:
                
                if num=='1':
                    cl.setstatus('CL1.Item1',"on")
                elif num=='2':
                    cl.setstatus('CL1.Item2',"on")
                elif num=='3':
                    cl.setstatus('CL1.Item3',"on")
                elif num=='4':
                    cl.setstatus('CL1.Item4',"on")
                elif num=='5':
                    cl.setstatus('CL1.Item5',"on")
                elif num=='6':
                    cl.setstatus('CL1.Item6',"on")
                elif num=='7':
                    cl.setstatus('CL1.Item7',"on")
                elif num=='8':
                    cl.setstatus('CL1.Item8',"on")
                elif num=='9':
                    cl.setstatus('CL1.Item9',"on")
                elif num=='10':
                    cl.setstatus('CL2.Item1',"on")
                elif num=='11':
                    cl.setstatus('CL2.Item2',"on")
                elif num=='12':
                    cl.setstatus('CL2.Item3',"on")
                elif num=='13':
                    cl.setstatus('CL2.Item4',"on")
                elif num=='14':
                    cl.setstatus('CL2.Item5',"on")
                elif num=='15':
                    cl.setstatus('CL2.Item6',"on")
                elif num=='16':
                    cl.setstatus('CL2.Item7',"on")
                elif num=='17':
                    cl.setstatus('CL2.Item8',"on")
                elif num=='18':
                    cl.setstatus('CL2.Item9',"on")
                elif num=='19':
                    cl.setstatus('CL2.Item10',"on")
                elif num=='20':
                    cl.setstatus('CL2.Item11',"on")
                elif num=='21':
                    cl.setstatus('CL3.Item1',"on")
                elif num=='22':
                    cl.setstatus('CL3.Item2',"on")
                elif num=='23':
                    cl.setstatus('CL3.Item3',"on")
                elif num=='24':
                    cl.setstatus('CL3.Item4',"on")
                elif num=='25':
                    cl.setstatus('CL4',"on")
                elif num=='26':
                    cl.setstatus('CL5',"on")
                elif num=='27':
                    cl.setstatus('CL6',"on")
                elif num=='28':
                    cl.setstatus('CL7',"on")
                elif num=='29':
                    cl.setstatus('CL8',"on")
                elif num=='30':
                    cl.setstatus('CL9',"on")
                elif num=='31':
                    cl.setstatus('CL10',"on")
                elif num=='32':
                    cl.setstatus('CL11',"on")
                elif num=='33':
                    cl.setstatus('CL12',"on")
                elif num=='34':
                    cl.setstatus('CL13',"on")

            mult_sessions()
            half_op.set('0')
            toggleAll()
            
        elif line[0:16] == 'Closing sessions':
            sessions = 0

#Clear the text in a textbox
def clearText():

    t.delete(1.0,END)

def clearText2():

    t2.delete(1.0,END)

#Function to write the contents of the textbox to a file
def saveToFile():

    f = open(filename_ent.get(), "w")
    f.write(t.get("1.0", END))
    f.close()



def saveToFile2():

    f = open(filenamediff_ent.get(), "w")
    f.write(t2.get("1.0", END))
    f.close()

    #with open(filenamediff_ent.get(), "w") as f:
        #f.write(t2.get("1.0", END))



#Function to toggle all checkboxes
def toggleAll():

    if cl.getstatus('CL0') == 'on':
        cl.setstatus('CL1.Item1',"on")
        cl.setstatus('CL1.Item2',"on")
        cl.setstatus('CL1.Item3',"on")
        cl.setstatus('CL1.Item4',"on")
        cl.setstatus('CL1.Item5',"on")
        cl.setstatus('CL1.Item6',"on")
        cl.setstatus('CL1.Item7',"on")
        cl.setstatus('CL1.Item8',"on")
        cl.setstatus('CL1.Item9',"on")
        cl.setstatus('CL2.Item1',"on")
        cl.setstatus('CL2.Item2',"on")
        cl.setstatus('CL2.Item3',"on")
        cl.setstatus('CL2.Item4',"on")
        cl.setstatus('CL2.Item5',"on")
        cl.setstatus('CL2.Item6',"on")
        cl.setstatus('CL2.Item7',"on")
        cl.setstatus('CL2.Item8',"on")
        cl.setstatus('CL2.Item9',"on")
        cl.setstatus('CL2.Item10',"on")
        cl.setstatus('CL2.Item11',"on")
        cl.setstatus('CL3.Item1',"on")
        cl.setstatus('CL3.Item2',"on")
        cl.setstatus('CL3.Item3',"on")
        cl.setstatus('CL3.Item4',"on")
        cl.setstatus('CL4',"on")
        cl.setstatus('CL5',"on")
        cl.setstatus('CL6',"on")
        cl.setstatus('CL7',"on")
        cl.setstatus('CL8',"on")
        cl.setstatus('CL9',"on")
        cl.setstatus('CL10',"on")
        cl.setstatus('CL11',"on")
        cl.setstatus('CL12',"on")
        cl.setstatus('CL13',"on")

    elif cl.getstatus('CL0') == 'off':
        cl.setstatus('CL1.Item1',"off")
        cl.setstatus('CL1.Item2',"off")
        cl.setstatus('CL1.Item3',"off")
        cl.setstatus('CL1.Item4',"off")
        cl.setstatus('CL1.Item5',"off")
        cl.setstatus('CL1.Item6',"off")
        cl.setstatus('CL1.Item7',"off")
        cl.setstatus('CL1.Item8',"off")
        cl.setstatus('CL1.Item9',"off")
        cl.setstatus('CL2.Item1',"off")
        cl.setstatus('CL2.Item2',"off")
        cl.setstatus('CL2.Item3',"off")
        cl.setstatus('CL2.Item4',"off")
        cl.setstatus('CL2.Item5',"off")
        cl.setstatus('CL2.Item6',"off")
        cl.setstatus('CL2.Item7',"off")
        cl.setstatus('CL2.Item8',"off")
        cl.setstatus('CL2.Item9',"off")
        cl.setstatus('CL2.Item10',"off")
        cl.setstatus('CL2.Item11',"off")
        cl.setstatus('CL3.Item1',"off")
        cl.setstatus('CL3.Item2',"off")
        cl.setstatus('CL3.Item3',"off")
        cl.setstatus('CL3.Item4',"off")
        cl.setstatus('CL4',"off")
        cl.setstatus('CL5',"off")
        cl.setstatus('CL6',"off")
        cl.setstatus('CL7',"off")
        cl.setstatus('CL8',"off")
        cl.setstatus('CL9',"off")
        cl.setstatus('CL10',"off")
        cl.setstatus('CL11',"off")
        cl.setstatus('CL12',"off")
        cl.setstatus('CL13',"off")

mult_sess = 0

responsetimes = []

#Open multiple sessions (sockets) and send the checked modbus requests in a loop
def mult_sessions():
    global responsefile
    responsefile = open("response_times.txt", "w")

    compares=0
    passes=0
    fails=0

    global runAndCompare_var
    runAndCompare_var = 1

    global mult_sess
    outputstr=""

    if int(sessions_ent.get()) > 256:
        t.insert(END,"\nMax sessions is 256\n");
        return

    if comparefile_op.get() == '1':
        global numlocalconn_file

    compare_sel = []
    ftest_lines = []

    compare_sel, ftest_lines = getFilesAndCompares(compare_sel, ftest_lines)


    if closeopen_op.get() == '0':



        loopStop.set('0')
   
        sockets = dict()
    
        socks_status = 0
        socks_status2 = 0
        socks_status3 = 0
        socks_status4 = 0
    
        t.insert(END,"Opening "+sessions_ent.get()+" sessions\n")
        
        for x in range(0,int(sessions_ent.get()) ):

            if ssl_op.get() == '1':
			
                if ( ipChoice.get() != 'IPv4' ):
                    print("Only IPv4 is supported for SSL")
                    break
			
                sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                timeout = timeout_ent.get()

                if timeout == '':
                    sockets[x].settimeout(2.0)
                else:
                    sockets[x].settimeout(float(timeout))
			
			

                if cert_ent.get() == '':
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                else:

                    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                    context.verify_mode = ssl.CERT_REQUIRED

                    if host_ent.get() != '':
                        context.check_hostname = True

                    context.load_verify_locations(cert_ent.get())

                if host_ent.get() != '':
                    sockets[x] = context.wrap_socket(sockets[x], server_hostname=host_ent.get())
                else:
                    sockets[x] = context.wrap_socket(sockets[x])

                sockets[x].connect((TCP_IP.get(), 802))

            else:

                if ( ipChoice.get() == 'IPv4' ):
                    try:
                       # test for IPv4 
                       socket.inet_pton(socket.AF_INET, TCP_IP.get())
                    except socket.error:
                       print(TCP_IP.get(), " is not valid IPv4 address")
                       break
                       
                    sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                    timeout = timeout_ent.get()

                    if timeout == '':
                        sockets[x].settimeout(2.0)
                    else:
                        sockets[x].settimeout(float(timeout))
                    sockets[x].connect((TCP_IP.get(), 502))
                    
                elif ( ipChoice.get() == 'IPv6' ):
                    try:
                       # test for IPv6 
                       socket.inet_pton(socket.AF_INET6, TCP_IP.get())
                    except socket.error:
                       print(TCP_IP.get(), " is not valid IPv6 address")
                       break
                    timeout_var = timeout_ent.get()

                    if timeout == '':
                        timeout_var = 2.0
                    else:
                        timeout_var = float(timeout_var)
                    sockets[x] = socket.create_connection((TCP_IP.get(),502), timeout=timeout_var, source_address=('',0))     

            socks_status, socks_status2, socks_status3, socks_status4 = changeSockets(x, sockets, socks_status,
                                                                                      socks_status2, socks_status3,
                                                                                      socks_status4)

            updateSockets(socks_status, socks_status2, socks_status3, socks_status4)
            
            root.update()
            #time.sleep(1.5)
            
        insertstr = "\nRunning "+loop_count_ent.get()+" iterations, delay "+loop_ent.get()+", closeopen "+closeopen_op.get()+", tests "
        
        if cl.getstatus('CL1.Item1') == 'on':
            insertstr+="1,"
        if cl.getstatus('CL1.Item2') == 'on':
            insertstr+="2,"
        if cl.getstatus('CL1.Item3') == 'on':
            insertstr+="3,"
        if cl.getstatus('CL1.Item4') == 'on':
            insertstr+="4,"
        if cl.getstatus('CL1.Item5') == 'on':
            insertstr+="5,"
        if cl.getstatus('CL1.Item6') == 'on':
            insertstr+='6,'
        if cl.getstatus('CL1.Item7') == 'on':
            insertstr+='7,'
        if cl.getstatus('CL1.Item8') == 'on':
            insertstr+='8,'
        if cl.getstatus('CL1.Item9') == 'on':
            insertstr+='9,'
        if cl.getstatus('CL2.Item1') == 'on':
            insertstr+='10,'
        if cl.getstatus('CL2.Item2') == 'on':
            insertstr+='11,'
        if cl.getstatus('CL2.Item3') == 'on':
            insertstr+='12,'
        if cl.getstatus('CL2.Item4') == 'on':
            insertstr+='13,'
        if cl.getstatus('CL2.Item5') == 'on':
            insertstr+='14,'
        if cl.getstatus('CL2.Item6') == 'on':
            insertstr+='15,'
        if cl.getstatus('CL2.Item7') == 'on':
            insertstr+='16,'
        if cl.getstatus('CL2.Item8') == 'on':
            insertstr+='17,'
        if cl.getstatus('CL2.Item9') == 'on':
            insertstr+='18,'
        if cl.getstatus('CL2.Item10') == 'on':
            insertstr+='19,'
        if cl.getstatus('CL2.Item11') == 'on':
            insertstr+='20,'
        if cl.getstatus('CL3.Item1') == 'on':
            insertstr+='21,'
        if cl.getstatus('CL3.Item2') == 'on':
            insertstr+='22,'
        if cl.getstatus('CL3.Item3') == 'on':
            insertstr+='23,'
        if cl.getstatus('CL3.Item4') == 'on':
            insertstr+='24,'
        if cl.getstatus('CL4') == 'on':
            insertstr+='25,'
        if cl.getstatus('CL5') == 'on':
            insertstr+='26,'
        if cl.getstatus('CL6') == 'on':
            insertstr+='27,'
        if cl.getstatus('CL7') == 'on':
            insertstr+='28,'
        if cl.getstatus('CL8') == 'on':
            insertstr+='29,'
        if cl.getstatus('CL9') == 'on':
            insertstr+='30,'
        if cl.getstatus('CL10') == 'on':
            insertstr+='31,'
        if cl.getstatus('CL11') == 'on':
            insertstr+='32,'
        if cl.getstatus('CL12') == 'on':
            insertstr+='33,'
        if cl.getstatus('CL13') == 'on':
            insertstr+='34,'
    
        insertstr+="\n"
        t.insert(END,insertstr)
            
        loop_count = loop_count_ent.get()
    
        if loop_count == "":
            loop_count = 4
        else:
            loop_count = int(loop_count)
    
        ctr=0
        iter=0
        
        while iter < loop_count:

            for z in range(0, len(compare_sel)):

                if comparefile_op.get() == '1' and compare_sel != '1':
                    parseAttrs(ftest_lines[z])

                    fileDividers(z)

                root.update()
                # time.sleep(1.5)


                if loopStop.get() == '1':

                    t.insert(END,"\nLoop Stopped\n")
                    for y in range(0,len(sockets)):
                        sockets[y].close()

                    t_status.delete('1.0','1.6')
                    t_status2.delete('1.0','1.6')
                    t_status3.delete('1.0','1.10')
                    t_status4.delete('1.0','1.18')

                    break

                t.insert(END, "\nIteration #" + str(ctr + 1) + "\n")

                updateSockets(socks_status, socks_status2, socks_status3, socks_status4)

                root.update()
                # time.sleep(1.5)

                for x in range(0,len(sockets)):

                    t.insert(END,"\nSending Request on session "+str(x+1)+"\n")

                    execute_modbus(sockets[x],compare_sel[z],z)

                loop_delay = loop_ent.get()

                if loop_delay == "":
                    loop_delay = 0

                time.sleep(float(loop_delay) * 0.001)

                saveToFiles(z)


            if loop_count_ent.get() == "":
                iter=1
            elif iter == int(loop_count) - 1:
                t.insert(END,"\nClosing sessions\n")
                for y in range(0,len(sockets)):
                    sockets[y].close()
                iter+=1
            else:
                iter+=1
                
            ctr+=1
            if loopStop.get() == '1':

                t.insert(END, "\nLoop Stopped\n")
                for y in range(0, len(sockets)):
                    sockets[y].close()

                t_status.delete('1.0', '1.6')
                t_status2.delete('1.0', '1.6')
                t_status3.delete('1.0', '1.10')
                t_status4.delete('1.0', '1.18')

                break
            
    elif closeopen_op.get() == '1':
    
        loopStop.set('0')
   
        sockets = dict()
    
        socks_status = 0
        socks_status2 = 0
        socks_status3 = 0
        socks_status4 = 0
    
        t.insert(END,"Opening "+sessions_ent.get()+" sessions\n")
        
        for x in range(0,int(sessions_ent.get()) ):



            if ssl_op.get() == '1':

                if ( ipChoice.get() != 'IPv4' ):
                    print("Only IPv4 is supported for SSL")
                    break

                sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                timeout = timeout_ent.get()

                if timeout == '':
                    sockets[x].settimeout(2.0)
                else:
                    sockets[x].settimeout(float(timeout))

                if cert_ent.get() == '':
                    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                else:

                    context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                    context.verify_mode = ssl.CERT_REQUIRED

                    if host_ent.get() != '':
                        context.check_hostname = True

                    context.load_verify_locations(cert_ent.get())

                if host_ent.get() != '':
                    sockets[x] = context.wrap_socket(sockets[x], server_hostname=host_ent.get())
                else:
                    sockets[x] = context.wrap_socket(sockets[x])

                sockets[x].connect((TCP_IP.get(), 802))

            else:

                if ( ipChoice.get() == 'IPv4' ):
                    try:
                       # test for IPv4 
                       socket.inet_pton(socket.AF_INET, TCP_IP.get())
                    except socket.error:
                       print(TCP_IP.get(), " is not valid IPv4 address")
                       break
                       
                    sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                    timeout = timeout_ent.get()

                    if timeout == '':
                        sockets[x].settimeout(2.0)
                    else:
                        sockets[x].settimeout(float(timeout))
                    sockets[x].connect((TCP_IP.get(), 502))
                    
                elif ( ipChoice.get() == 'IPv6' ):
                    try:
                        # test for IPv6 
                        socket.inet_pton(socket.AF_INET6, TCP_IP.get())
                    except socket.error:
                        print(TCP_IP.get(), " is not valid IPv6 address")
                    break
                    timeout_var = timeout_ent.get()

                    if timeout_var == '':
                        timeout_var = 2.0
                    else:
                        timeout_var = float(timeout_var)
                    sockets[x] = socket.create_connection((TCP_IP.get(),502), timeout=timeout_var, source_address=('',0))



            socks_status, socks_status2, socks_status3, socks_status4 = changeSockets(x, sockets, socks_status,
                                                                                      socks_status2, socks_status3,
                                                                                      socks_status4)

            updateSockets(socks_status, socks_status2, socks_status3, socks_status4)
            
            root.update()
            #time.sleep(1.5)
            
        insertstr = "\nRunning "+loop_count_ent.get()+" iterations, delay "+loop_ent.get()+", closeopen "+closeopen_op.get()+", tests "
            
        if cl.getstatus('CL1.Item1') == 'on':
            insertstr+="1,"
        if cl.getstatus('CL1.Item2') == 'on':
            insertstr+="2,"
        if cl.getstatus('CL1.Item3') == 'on':
            insertstr+="3,"
        if cl.getstatus('CL1.Item4') == 'on':
            insertstr+="4,"
        if cl.getstatus('CL1.Item5') == 'on':
            insertstr+="5,"
        if cl.getstatus('CL1.Item6') == 'on':
            insertstr+='6,'
        if cl.getstatus('CL1.Item7') == 'on':
            insertstr+='7,'
        if cl.getstatus('CL1.Item8') == 'on':
            insertstr+='8,'
        if cl.getstatus('CL1.Item9') == 'on':
            insertstr+='9,'
        if cl.getstatus('CL2.Item1') == 'on':
            insertstr+='10,'
        if cl.getstatus('CL2.Item2') == 'on':
            insertstr+='11,'
        if cl.getstatus('CL2.Item3') == 'on':
            insertstr+='12,'
        if cl.getstatus('CL2.Item4') == 'on':
            insertstr+='13,'
        if cl.getstatus('CL2.Item5') == 'on':
            insertstr+='14,'
        if cl.getstatus('CL2.Item6') == 'on':
            insertstr+='15,'
        if cl.getstatus('CL2.Item7') == 'on':
            insertstr+='16,'
        if cl.getstatus('CL2.Item8') == 'on':
            insertstr+='17,'
        if cl.getstatus('CL2.Item9') == 'on':
            insertstr+='18,'
        if cl.getstatus('CL2.Item10') == 'on':
            insertstr+='19,'
        if cl.getstatus('CL2.Item11') == 'on':
            insertstr+='20,'
        if cl.getstatus('CL3.Item1') == 'on':
            insertstr+='21,'
        if cl.getstatus('CL3.Item2') == 'on':
            insertstr+='22,'
        if cl.getstatus('CL3.Item3') == 'on':
            insertstr+='23,'
        if cl.getstatus('CL3.Item4') == 'on':
            insertstr+='24,'
        if cl.getstatus('CL4') == 'on':
            insertstr+='25,'
        if cl.getstatus('CL5') == 'on':
            insertstr+='26,'
        if cl.getstatus('CL6') == 'on':
            insertstr+='27,'
        if cl.getstatus('CL7') == 'on':
            insertstr+='28,'
        if cl.getstatus('CL8') == 'on':
            insertstr+='29,'
        if cl.getstatus('CL9') == 'on':
            insertstr+='30,'
        if cl.getstatus('CL10') == 'on':
            insertstr+='31,'
        if cl.getstatus('CL11') == 'on':
            insertstr+='32,'
        if cl.getstatus('CL12') == 'on':
            insertstr+='33,'
        if cl.getstatus('CL13') == 'on':
            insertstr+='34,'
    
        insertstr+="\n"
        t.insert(END,insertstr)
            
        loop_count = loop_count_ent.get()
    
        if loop_count == "":
            loop_count = 4
        else:
            loop_count = int(loop_count)
    
        ctr=0
        iter=0
        
        while iter < loop_count:

            for z in range(0, len(compare_sel)):

                if comparefile_op.get() == '1' and compare_sel != '1':
                    parseAttrs(ftest_lines[z])

                    fileDividers(z)


                root.update()
                #time.sleep(1.5)

                if loopStop.get() == '1':

                    t.insert(END,"\nLoop Stopped\n")
                    for y in range(0,len(sockets)):
                        sockets[y].close()
                    t_status.delete('1.0','1.6')
                    t_status2.delete('1.0','1.6')
                    t_status3.delete('1.0','1.10')
                    t_status4.delete('1.0','1.18')
                    break

                t.insert(END,"\nIteration #"+str(ctr+1)+"\n")

                updateSockets(socks_status, socks_status2, socks_status3, socks_status4)

                root.update()
                #time.sleep(1.5)

                for x in range(0,len(sockets)):

                    t.insert(END,"\nClosing, opening, and sending Request on session "+str(x+1)+"\n")

                    sockets[x].close()

                    socks_status, socks_status2, socks_status3, socks_status4 = changeSockets(x, sockets, socks_status,
                                                                                              socks_status2,
                                                                                              socks_status3,
                                                                                              socks_status4)

                    updateSockets(socks_status, socks_status2, socks_status3, socks_status4)

                    root.update()
                    #time.sleep(1.5)

                    loop_delay = loop_ent.get()

                    if loop_delay == "":
                        loop_delay = 0

                    time.sleep(float(loop_delay) * 0.001)



                    if ssl_op.get() == '1':
					
                        if ( ipChoice.get() != 'IPv4' ):
                            print("Only IPv4 is supported for SSL")
                            break
							
                        sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        timeout = timeout_ent.get()

                        if timeout == '':
                            sockets[x].settimeout(2.0)
                        else:
                            sockets[x].settimeout(float(timeout))

                        if cert_ent.get() == '':
                            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                        else:

                            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                            context.verify_mode = ssl.CERT_REQUIRED

                            if host_ent.get() != '':
                                context.check_hostname = True

                            context.load_verify_locations(cert_ent.get())

                        if host_ent.get() != '':
                            sockets[x] = context.wrap_socket(sockets[x], server_hostname=host_ent.get())
                        else:
                            sockets[x] = context.wrap_socket(sockets[x])

                        sockets[x].connect((TCP_IP.get(), 802))

                    else:

                        if ( ipChoice.get() == 'IPv4' ):
                            try:
                                # test for IPv4 
                                socket.inet_pton(socket.AF_INET, TCP_IP.get())
                            except socket.error:
                                print(TCP_IP.get(), " is not valid IPv4 address")
                                break
                                
                            sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                            timeout = timeout_ent.get()

                            if timeout == '':
                                sockets[x].settimeout(2.0)
                            else:
                                sockets[x].settimeout(float(timeout))
                            sockets[x].connect((TCP_IP.get(), 502))
                            
                        elif ( ipChoice.get() == 'IPv6' ):
                            try:
                                # test for IPv6 
                                socket.inet_pton(socket.AF_INET6, TCP_IP.get())
                                
                            except socket.error:
                                print(TCP_IP.get(), " is not valid IPv6 address")
                                break
                            timeout_var = timeout_ent.get()

                            if timeout_var == '':
                                timeout_var = 2.0
                            else:
                                timeout_var = float(timeout)
                            sockets[x] = socket.create_connection((TCP_IP.get(),502), timeout=timeout_var, source_address=('',0))


                    socks_status, socks_status2, socks_status3, socks_status4 = changeSockets(x, sockets, socks_status,
                                                                                              socks_status2,
                                                                                              socks_status3,
                                                                                              socks_status4)

                    updateSockets(socks_status, socks_status2, socks_status3, socks_status4)

                    root.update()
                    #time.sleep(1.5)

                    t.insert(END,"\nSending Request on session "+str(x+1)+"\n")

                    execute_modbus(sockets[x],compare_sel[z],z)

                    saveToFiles(z)


            if loop_count_ent.get() == "":
                iter=1
            elif iter == int(loop_count) - 1:
                t.insert(END,"\nClosing sessions\n")
                for y in range(0,len(sockets)):
                    sockets[y].close()
                iter+=1
            else:
                iter+=1
                
            ctr+=1

            if loopStop.get() == '1':
                t.insert(END, "\nLoop Stopped\n")
                for y in range(0, len(sockets)):
                    sockets[y].close()
                t_status.delete('1.0', '1.6')
                t_status2.delete('1.0', '1.6')
                t_status3.delete('1.0', '1.10')
                t_status4.delete('1.0', '1.18')
                break

    doResponses()

    mult_sess = 1
    # execute_eip()
    mult_sess = 0
    runAndCompare_var = 0



# Indicate whether a socket is on or off by setting a bit to 1 or 0
def changeSockets(x, sockets, socks_status, socks_status2, socks_status3, socks_status4):

    try:
        fileno = sockets[x].fileno()
    except socket.error:
        fileno = -1

    if fileno != -1:

        if x < 16:
            socks_status |= (1 << x)
        elif x > 15 and x < 32:
            socks_status2 |= (1 << (x - 16))
        elif x > 31 and x < 64:
            socks_status3 |= (1 << (x - 32))
        elif x > 63 and x < 128:
            socks_status4 |= (1 << (x - 64))

    elif fileno == -1:

        if x < 16:
            socks_status &= ~(1 << x)
        elif x > 15 and x < 32:
            socks_status2 &= ~(1 << (x - 16))
        elif x > 31 and x < 64:
            socks_status3 &= ~(1 << (x - 32))
        elif x > 63 and x < 128:
            socks_status4 &= ~(1 << (x - 64))

    return socks_status, socks_status2, socks_status3, socks_status4



#Delete what is in the textbox and then update with the new status of the sockets
def updateSockets(socks_status, socks_status2, socks_status3, socks_status4):

    t_status.delete('1.0','1.6')
    if socks_status != 0:
        t_status.insert(END, "{0:#0{1}x}".format(socks_status,6) )
    t_status2.delete('1.0','1.6')
    if socks_status2 != 0:
        t_status2.insert(END, "{0:#0{1}x}".format(socks_status2,6) )
    t_status3.delete('1.0','1.10')
    if socks_status3 != 0:
        t_status3.insert(END, "{0:#0{1}x}".format(socks_status3,10) )
    t_status4.delete('1.0','1.18')
    if socks_status4 != 0:
        t_status4.insert(END, "{0:#0{1}x}".format(socks_status4,18) )

# Parse what we read from the file to get the attribute to compare to the current run
def parseAttrs(ftest_lines):

    global numlocalconn_file

    for x in range(0, len(ftest_lines)):

        if ftest_lines[x][0:24] == "Number local connects = ":
            numlocalconn_file = int(ftest_lines[x][24:])

compares = 0
passes = 0
fails = 0

# Function to output dividers between files
def fileDividers(z):

    if compare_ent.get()[-4:] == '.ini':

        t2.insert(END,
                  "\n====================================================\nFile " + fcomparefiles[z] + "\n")

    else:

        if compare_ent.get() != '' and z == 0:
            t2.insert(END,
                      "\n======================================================File " + compare_ent.get() + "\n")
        if compare_ent2.get() != '' and z == 1:
            t2.insert(END,
                      "\n======================================================\nFile " + compare_ent2.get() + "\n")
        if compare_ent3.get() != '' and z == 2:
            t2.insert(END,
                      "\n======================================================\nFile " + compare_ent3.get() + "\n")
        if compare_ent4.get() != '' and z == 3:
            t2.insert(END,
                      "\n======================================================\nFile " + compare_ent4.get() + "\n")
        if compare_ent5.get() != '' and z == 4:
            t2.insert(END,
                      "\n======================================================\nFile " + compare_ent5.get() + "\n")

    t2.insert(END, "\n--- output\n+++ file\n")




# Get the filenames to compare to and get the CIP objects and attributes to compare
def getFilesAndCompares(compare_sel, ftest_lines):

    if comparefile_op.get() == '1':

        if compare_ent.get()[-4:] == '.ini':

            fcompareini = open(compare_ent.get(), 'r')
            fcomparefiles = fcompareini.read().split(",")
            # ftest_lines = []
            for x in range(0, len(fcomparefiles)):
                file = fcomparefiles[x]
                opened_file = open(file, 'r')
                ftest_lines.append(opened_file.readlines())
        else:

            ftest_lines = []
            if compare_ent.get() != '':
                ftest = open(compare_ent.get(), "r")
                ftest_lines.append(ftest.readlines())
            if compare_ent2.get() != '':
                ftest2 = open(compare_ent2.get(), 'r')
                ftest_lines.append(ftest2.readlines())
            if compare_ent3.get() != '':
                ftest3 = open(compare_ent3.get(), 'r')
                ftest_lines.append(ftest3.readlines())
            if compare_ent4.get() != '':
                ftest4 = open(compare_ent4.get(), 'r')
                ftest_lines.append(ftest4.readlines())
            if compare_ent5.get() != '':
                ftest5 = open(compare_ent5.get(), 'r')
                ftest_lines.append(ftest5.readlines())

                #  compare_sel = []
        for y in range(0, len(ftest_lines)):

            found = 0
            for x in range(0, len(ftest_lines[y])):

                if ftest_lines[y][x][0:7] == "Compare":
                    found = 1
                    compare_sel.append(ftest_lines[y][x][8:].split(","))

            if found == 0:

                output = t.get("1.0", END)
                output = output.splitlines()

                for x in range(0, len(output)):

                    if output[x][0:7] == "Compare":
                        found = 1
                        compare_sel.append(output[x][8:].split(","))

        if len(compare_sel) == 0:
            compare_sel = '1'





    elif comparefile_op.get() == '0':

        compare_sel = '1'



    return compare_sel, ftest_lines




#Function that takes in a request and returns the response
def modbusReq(func_req,sock):

    global responsefile

    starttime = time.perf_counter()
    sock.send(func_req)

    rec = sock.recv(300)
    endtime = time.perf_counter()

    timetaken = endtime - starttime
    timetaken = "%.5f" % timetaken
    t.insert(END,"\nResponse time = "+timetaken+"\n")
    responsetimes.append(timetaken)

    try:
        if 'responsefile' in globals():
            responsefile.write(timetaken + "\n")
    except ValueError:
        pass

    s = struct.Struct(str(len(rec)) + 'B')
    data = s.unpack(rec)

    dataStr = ""

    for z in range(0,len(data)):
        dataStr += '{:02X}'.format(data[z]) + " "

    return (rec, dataStr)


#Main function - Opens a socket and calls the function that sends the checked modbus requests
def sendModbus():


    if comparefile_op.get() == '1':
        global numlocalconn_file


    compare_sel = []
    ftest_lines = []

    compare_sel, ftest_lines = getFilesAndCompares(compare_sel, ftest_lines)

    for z in range(0, len(compare_sel)):

        if comparefile_op.get() == '1' and compare_sel != '1':
            parseAttrs(ftest_lines[z])

            fileDividers(z)




        #sock = ssl.wrap_socket(sockk, ssl_version=ssl.PROTOCOL_TLS)

        if ssl_op.get() == '1':
        
            if ( ipChoice.get() != 'IPv4' ):
                print("Only IPv4 is supported for SSL")
                break
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

            timeout = timeout_ent.get()

            if timeout == '':
                sock.settimeout(2.0)
            else:
                sock.settimeout(float(timeout))

            if cert_ent.get() == '':
                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            else:

                context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                context.verify_mode = ssl.CERT_REQUIRED

                if host_ent.get() != '':
                    context.check_hostname = True

                context.load_verify_locations(cert_ent.get())

            if host_ent.get() != '':
                sock = context.wrap_socket(sock, server_hostname=host_ent.get())
            else:
                sock = context.wrap_socket(sock)

            sock.connect((TCP_IP.get(), 802))

        else:

            if ( ipChoice.get() == 'IPv4' ):
                try:
                    # test for IPv4 
                    socket.inet_pton(socket.AF_INET, TCP_IP.get())
                except socket.error:
                    print(TCP_IP.get(), " is not valid IPv4 address")
                    break
                    
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                timeout = timeout_ent.get()

                if timeout == '':
                    sock.settimeout(2.0)
                else:
                    sock.settimeout(float(timeout))
                sock.connect((TCP_IP.get(), 502))
                
            elif ( ipChoice.get() == 'IPv6' ):
                try:
                    # test for IPv6 
                    socket.inet_pton(socket.AF_INET6, TCP_IP.get())
                except socket.error:
                    print(TCP_IP.get(), " is not valid IPv6 address")
                    break
                timeout_var = timeout_ent.get()

                if timeout_var == '':
                    timeout_var = 2.0
                else:
                    timeout_var = float(timeout_var)
                sock = socket.create_connection((TCP_IP.get(),502), timeout=timeout_var, source_address=('',0))
                    
        if comparefile_op.get() == '1':
            execute_modbus(sock,compare_sel[z],z)
        elif comparefile_op.get() == '0':
            execute_modbus(sock,compare_sel,z)

    
        sock.close()

        saveToFiles(z)





# Saves the output to files during compares
def saveToFiles(z):

    if comparefile_op.get() == '1':

        global endLine
        if compare_ent.get()[-4:] == '.ini':

            # fcompareini = open(compare_ent.get(),'rb')
            # fcomparefiles = fcompareini.read().split(",")

            # Get the current time
            dt = datetime.datetime.now()
            # Convert the current time to a string
            time_now = dt.strftime("%m%d%y_%H%M%S")

            opened_file = open(fcomparefiles[z] + "_output_" + time_now, 'w')

            if z == 0:
                opened_file.write(t.get("1.0", END))
            else:
                opened_file.write(t.get(str(endLine) + ".0", END))

            endLine = int(t.index('end').split('.')[0])

            # t.delete(1.0,END)

        else:

            outfiles = []
            # ftest_lines = []
            if compare_ent.get() != '' and z == 0:
                # Get the current time
                dt = datetime.datetime.now()
                # Convert the current time to a string
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent.get() + "_output_" + time_now, "w")
                file.write(t.get("1.0", END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            if compare_ent2.get() != '' and z == 1:
                dt = datetime.datetime.now()
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent2.get() + "_output_" + time_now, 'w')
                file.write(t.get(str(endLine) + ".0", END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            if compare_ent3.get() != '' and z == 2:
                dt = datetime.datetime.now()
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent3.get() + "_output_" + time_now, 'w')
                file.write(t.get(str(endLine) + ".0", END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            if compare_ent4.get() != '' and z == 3:
                dt = datetime.datetime.now()
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent4.get() + "_output_" + time_now, 'w')
                file.write(t.get(str(endLine) + ".0", END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            if compare_ent5.get() != '' and z == 4:
                dt = datetime.datetime.now()
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent5.get() + "_output_" + time_now, 'w')
                file.write(t.get(str(endLine) + ".0", END))
                file.close()
                endLine = int(t.index('end').split('.')[0])



# Adds "Compare ....." to the output textbox with numbers instead of "....." indicating what is currently checked
def addCompares():

    insertstr = "\nCompare "

    if cl.getstatus('CL1.Item1.3') == 'on':
        insertstr += "1.3,"
    # if cl.getstatus('CL2') == 'on':
    #     insertstr += "2,"
    # if cl.getstatus('CL3') == 'on':
    #     insertstr += "3,"
    # if cl.getstatus('CL4') == 'on':
    #     insertstr += "4,"
    # if cl.getstatus('CL4.1') == 'on':
    #     insertstr += "4.1,"
    # if cl.getstatus('CL4.2') == 'on':
    #     insertstr += "4.2,"
    # if cl.getstatus('CL4.3') == 'on':
    #     insertstr += "4.3,"
    # if cl.getstatus('CL4.4') == 'on':
    #     insertstr += "4.4,"
    # if cl.getstatus('CL4.5') == 'on':
    #     insertstr += "4.5,"
    # if cl.getstatus('CL4.6') == 'on':
    #     insertstr += "4.6,"
    # if cl.getstatus('CL4.7') == 'on':
    #     insertstr += "4.7,"
    # if cl.getstatus('CL4.8') == 'on':
    #     insertstr += "4.8,"
    # if cl.getstatus('CL4.9') == 'on':
    #     insertstr += "4.9,"
    # if cl.getstatus('CL4.10') == 'on':
    #     insertstr += "4.10,"
    # if cl.getstatus('CL4.11') == 'on':
    #     insertstr += "4.11,"
    # if cl.getstatus('CL4.12') == 'on':
    #     insertstr += "4.12,"
    # if cl.getstatus('CL4.13') == 'on':
    #     insertstr += "4.13,"
    # if cl.getstatus('CL4.14') == 'on':
    #     insertstr += "4.14,"
    # if cl.getstatus('CL4.15') == 'on':
    #     insertstr += "4.15,"
    # if cl.getstatus('CL4.16') == 'on':
    #     insertstr += "4.16,"
    # if cl.getstatus('CL4.17') == 'on':
    #     insertstr += "4.17,"
    # if cl.getstatus('CL5') == 'on':
    #     insertstr += "5,"
    # if cl.getstatus('CL6') == 'on':
    #     insertstr += '6,'
    # if cl.getstatus('CL7') == 'on':
    #     insertstr += '7,'
    # if cl.getstatus('CL8') == 'on':
    #     insertstr += '8,'
    # if cl.getstatus('CL9') == 'on':
    #     insertstr += '9,'
    # if cl.getstatus('CL9.1') == 'on':
    #     insertstr += '9.1,'
    # if cl.getstatus('CL9.2') == 'on':
    #     insertstr += '9.2,'
    # if cl.getstatus('CL9.3') == 'on':
    #     insertstr += '9.3,'
    # if cl.getstatus('CL9.4') == 'on':
    #     insertstr += '9.4,'
    # if cl.getstatus('CL9.5') == 'on':
    #     insertstr += '9.5,'
    # if cl.getstatus('CL9.6') == 'on':
    #     insertstr += '9.6,'
    # if cl.getstatus('CL9.7') == 'on':
    #     insertstr += '9.7,'
    # if cl.getstatus('CL9.8') == 'on':
    #     insertstr += '9.8,'
    # if cl.getstatus('CL9.9') == 'on':
    #     insertstr += '9.9,'
    # if cl.getstatus('CL9.10') == 'on':
    #     insertstr += '9.10,'
    # if cl.getstatus('CL9.11') == 'on':
    #     insertstr += '9.11,'
    # if cl.getstatus('CL9.12') == 'on':
    #     insertstr += '9.12,'
    # if cl.getstatus('CL9.13') == 'on':
    #     insertstr += '9.13,'
    # if cl.getstatus('CL9.14') == 'on':
    #     insertstr += '9.14,'
    # if cl.getstatus('CL9.15') == 'on':
    #     insertstr += '9.15,'
    # if cl.getstatus('CL9.16') == 'on':
    #     insertstr += '9.16,'
    # if cl.getstatus('CL9.17') == 'on':
    #     insertstr += '9.17,'
    # if cl.getstatus('CL9.18') == 'on':
    #     insertstr += '9.18,'
    # if cl.getstatus('CL9.19') == 'on':
    #     insertstr += '9.19,'
    # if cl.getstatus('CL9.20') == 'on':
    #     insertstr += '9.20,'
    # if cl.getstatus('CL9.21') == 'on':
    #     insertstr += '9.21,'
    # if cl.getstatus('CL9.22') == 'on':
    #     insertstr += '9.22,'
    # if cl.getstatus('CL9.23') == 'on':
    #     insertstr += '9.23,'
    # if cl.getstatus('CL9.24') == 'on':
    #     insertstr += '9.24,'
    # if cl.getstatus('CL9.25') == 'on':
    #     insertstr += '9.25,'
    # if cl.getstatus('CL9.26') == 'on':
    #     insertstr += '9.26,'
    # if cl.getstatus('CL9.27') == 'on':
    #     insertstr += '9.27,'
    # if cl.getstatus('CL9.28') == 'on':
    #     insertstr += '9.28,'
    # if cl.getstatus('CL10') == 'on':
    #     insertstr += '10,'
    # if cl.getstatus('CL11') == 'on':
    #     insertstr += '11,'
    # if cl.getstatus('CL12') == 'on':
    #     insertstr += '12,'
    # if cl.getstatus('CL13') == 'on':
    #     insertstr += '13,'
    # if cl.getstatus('CL14') == 'on':
    #     insertstr += '14,'
    # if cl.getstatus('CL15') == 'on':
    #     insertstr += '15,'
    # if cl.getstatus('CL15.1') == 'on':
    #     insertstr += '15.1,'
    # if cl.getstatus('CL15.2') == 'on':
    #     insertstr += '15.2,'
    # if cl.getstatus('CL15.3') == 'on':
    #     insertstr += '15.3,'
    # if cl.getstatus('CL15.4') == 'on':
    #     insertstr += '15.4,'
    # if cl.getstatus('CL15.5') == 'on':
    #     insertstr += '15.5,'
    # if cl.getstatus('CL15.6') == 'on':
    #     insertstr += '15.6,'
    # if cl.getstatus('CL15.7') == 'on':
    #     insertstr += '15.7,'
    # if cl.getstatus('CL15.8') == 'on':
    #     insertstr += '15.8,'
    # if cl.getstatus('CL15.9') == 'on':
    #     insertstr += '15.9,'
    # if cl.getstatus('CL15.10') == 'on':
    #     insertstr += '15.10,'
    # if cl.getstatus('CL16') == 'on':
    #     insertstr += '16,'
    # if cl.getstatus('CL17') == 'on':
    #     insertstr += '17,'
    # if cl.getstatus('CL17.1') == 'on':
    #     insertstr += '17.1,'
    # if cl.getstatus('CL18') == 'on':
    #     insertstr += '18,'
    # if cl.getstatus('CL18.1') == 'on':
    #     insertstr += '18.1,'
    # if cl.getstatus('CL19') == 'on':
    #     insertstr += '19,'
    # if cl.getstatus('CL19.1') == 'on':
    #     insertstr += '19.1,'
    # if cl.getstatus('CL20') == 'on':
    #     insertstr += '20,'
    # if cl.getstatus('CL20.1') == 'on':
    #     insertstr += '20.1,'
    # if cl.getstatus('CL20.2') == 'on':
    #     insertstr += '20.2,'
    # if cl.getstatus('CL20.3') == 'on':
    #     insertstr += '20.3,'
    # if cl.getstatus('CL20.4') == 'on':
    #     insertstr += '20.4,'
    # if cl.getstatus('CL20.5') == 'on':
    #     insertstr += '20.5,'
    # if cl.getstatus('CL20.6') == 'on':
    #     insertstr += '20.6,'
    # if cl.getstatus('CL20.7') == 'on':
    #     insertstr += '20.7,'
    # if cl.getstatus('CL20.8') == 'on':
    #     insertstr += '20.8,'
    # if cl.getstatus('CL20.9') == 'on':
    #     insertstr += '20.9,'
    # if cl.getstatus('CL20.10') == 'on':
    #     insertstr += '20.10,'
    # if cl.getstatus('CL20.11') == 'on':
    #     insertstr += '20.11,'
    # if cl.getstatus('CL20.12') == 'on':
    #     insertstr += '20.12,'
    # if cl.getstatus('CL20.13') == 'on':
    #     insertstr += '20.13,'
    # if cl.getstatus('CL20.14') == 'on':
    #     insertstr += '20.14,'
    # if cl.getstatus('CL20.15') == 'on':
    #     insertstr += '20.15,'
    # if cl.getstatus('CL20.16') == 'on':
    #     insertstr += '20.16,'
    # if cl.getstatus('CL20.17') == 'on':
    #     insertstr += '20.17,'
    # if cl.getstatus('CL20.18') == 'on':
    #     insertstr += '20.18,'
    # if cl.getstatus('CL20.19') == 'on':
    #     insertstr += '20.19,'
    # if cl.getstatus('CL20.20') == 'on':
    #     insertstr += '20.20,'
    # if cl.getstatus('CL20.21') == 'on':
    #     insertstr += '20.21,'
    # if cl.getstatus('CL20.22') == 'on':
    #     insertstr += '20.22,'
    # if cl.getstatus('CL20.23') == 'on':
    #     insertstr += '20.23,'
    # if cl.getstatus('CL20.24') == 'on':
    #     insertstr += '20.24,'
    # if cl.getstatus('CL21') == 'on':
    #     insertstr += '21,'

    insertstr += "\n"

    t.insert(END, insertstr)



    
# Function to send modbus requests depending on what is checked
def execute_modbus(sock,compare_sel,z):

    global reqsRan
    global runAndCompare

    global compares
    global passes
    global fails

    global status

    #Initialize the flags that indicate if a test passed or failed
    test1=0
    test2=0
    test3=0
    test3_5=0
    test4=0
    test5=0
    test6=0
    test7=0
    test8=0
    test9=0
    test9_5=0
    test10=0
    test11=0
    test12=0
    test13=0
    test14=0
    test15=0
    test16=0
    test17=0
    test18=0
    test19=0
    test20=0
    test21=0
    test22=0
    test23=0
    test24=0
    test25=0
    test26=0
    test27=0
    test28=0
    test29=0
    test30=0
    test31=0
    test32=0
    test33=0
    test34=0

    insertstr = "\nExecuting cases "

    if cl.getstatus('CL1.Item1') == 'on':
        insertstr += "1,"

    # if cl.getstatus('CL1') == 'on':
    #     insertstr += "1,"
    # if cl.getstatus('CL2') == 'on':
    #     insertstr += "2,"
    # if cl.getstatus('CL3') == 'on':
    #     insertstr += "3,"
    # if cl.getstatus('CL4') == 'on':
    #     insertstr += "4,"
    # if cl.getstatus('CL4.1') == 'on':
    #     insertstr += "4.1,"
    # if cl.getstatus('CL4.2') == 'on':
    #     insertstr += "4.2,"
    # if cl.getstatus('CL4.3') == 'on':
    #     insertstr += "4.3,"
    # if cl.getstatus('CL4.4') == 'on':
    #     insertstr += "4.4,"
    # if cl.getstatus('CL4.5') == 'on':
    #     insertstr += "4.5,"
    # if cl.getstatus('CL4.6') == 'on':
    #     insertstr += "4.6,"
    # if cl.getstatus('CL4.7') == 'on':
    #     insertstr += "4.7,"
    # if cl.getstatus('CL4.8') == 'on':
    #     insertstr += "4.8,"
    # if cl.getstatus('CL4.9') == 'on':
    #     insertstr += "4.9,"
    # if cl.getstatus('CL4.10') == 'on':
    #     insertstr += "4.10,"
    # if cl.getstatus('CL4.11') == 'on':
    #     insertstr += "4.11,"
    # if cl.getstatus('CL4.12') == 'on':
    #     insertstr += "4.12,"
    # if cl.getstatus('CL4.13') == 'on':
    #     insertstr += "4.13,"
    # if cl.getstatus('CL4.14') == 'on':
    #     insertstr += "4.14,"
    # if cl.getstatus('CL4.15') == 'on':
    #     insertstr += "4.15,"
    # if cl.getstatus('CL4.16') == 'on':
    #     insertstr += "4.16,"
    # if cl.getstatus('CL4.17') == 'on':
    #     insertstr += "4.17,"
    # if cl.getstatus('CL5') == 'on':
    #     insertstr += "5,"
    # if cl.getstatus('CL6') == 'on':
    #     insertstr += '6,'
    # if cl.getstatus('CL7') == 'on':
    #     insertstr += '7,'
    # if cl.getstatus('CL8') == 'on':
    #     insertstr += '8,'
    # if cl.getstatus('CL9') == 'on':
    #     insertstr += '9,'
    # if cl.getstatus('CL9') == 'on':
    #     insertstr += '9.1,'
    # if cl.getstatus('CL9.2') == 'on':
    #     insertstr += '9.2,'
    # if cl.getstatus('CL9.3') == 'on':
    #     insertstr += '9.3,'
    # if cl.getstatus('CL9.4') == 'on':
    #     insertstr += '9.4,'
    # if cl.getstatus('CL9.5') == 'on':
    #     insertstr += '9.5,'
    # if cl.getstatus('CL9.6') == 'on':
    #     insertstr += '9.6,'
    # if cl.getstatus('CL9.7') == 'on':
    #     insertstr += '9.7,'
    # if cl.getstatus('CL9.8') == 'on':
    #     insertstr += '9.8,'
    # if cl.getstatus('CL9.9') == 'on':
    #     insertstr += '9.9,'
    # if cl.getstatus('CL9.10') == 'on':
    #     insertstr += '9.10,'
    # if cl.getstatus('CL9.11') == 'on':
    #     insertstr += '9.11,'
    # if cl.getstatus('CL9.12') == 'on':
    #     insertstr += '9.12,'
    # if cl.getstatus('CL9.13') == 'on':
    #     insertstr += '9.13,'
    # if cl.getstatus('CL9.14') == 'on':
    #     insertstr += '9.14,'
    # if cl.getstatus('CL9.15') == 'on':
    #     insertstr += '9.15,'
    # if cl.getstatus('CL9.16') == 'on':
    #     insertstr += '9.16,'
    # if cl.getstatus('CL9.17') == 'on':
    #     insertstr += '9.17,'
    # if cl.getstatus('CL9.18') == 'on':
    #     insertstr += '9.18,'
    # if cl.getstatus('CL9.19') == 'on':
    #     insertstr += '9.19,'
    # if cl.getstatus('CL9.20') == 'on':
    #     insertstr += '9.20,'
    # if cl.getstatus('CL9.21') == 'on':
    #     insertstr += '9.21,'
    # if cl.getstatus('CL9.22') == 'on':
    #     insertstr += '9.22,'
    # if cl.getstatus('CL9.23') == 'on':
    #     insertstr += '9.23,'
    # if cl.getstatus('CL9.24') == 'on':
    #     insertstr += '9.24,'
    # if cl.getstatus('CL9.25') == 'on':
    #     insertstr += '9.25,'
    # if cl.getstatus('CL9.26') == 'on':
    #     insertstr += '9.26,'
    # if cl.getstatus('CL9.27') == 'on':
    #     insertstr += '9.27,'
    # if cl.getstatus('CL9.28') == 'on':
    #     insertstr += '9.28,'
    # if cl.getstatus('CL10') == 'on':
    #     insertstr += '10,'
    # if cl.getstatus('CL11') == 'on':
    #     insertstr += '11,'
    # if cl.getstatus('CL12') == 'on':
    #     insertstr += '12,'
    # if cl.getstatus('CL13') == 'on':
    #     insertstr += '13,'
    # if cl.getstatus('CL14') == 'on':
    #     insertstr += '14,'
    # if cl.getstatus('CL15') == 'on':
    #     insertstr += '15,'
    # if cl.getstatus('CL15.1') == 'on':
    #     insertstr += '15.1,'
    # if cl.getstatus('CL15.2') == 'on':
    #     insertstr += '15.2,'
    # if cl.getstatus('CL15.3') == 'on':
    #     insertstr += '15.3,'
    # if cl.getstatus('CL15.4') == 'on':
    #     insertstr += '15.4,'
    # if cl.getstatus('CL15.5') == 'on':
    #     insertstr += '15.5,'
    # if cl.getstatus('CL15.6') == 'on':
    #     insertstr += '15.6,'
    # if cl.getstatus('CL15.7') == 'on':
    #     insertstr += '15.7,'
    # if cl.getstatus('CL15.8') == 'on':
    #     insertstr += '15.8,'
    # if cl.getstatus('CL15.9') == 'on':
    #     insertstr += '15.9,'
    # if cl.getstatus('CL15.10') == 'on':
    #     insertstr += '15.10,'
    # if cl.getstatus('CL16') == 'on':
    #     insertstr += '16,'
    # if cl.getstatus('CL17') == 'on':
    #     insertstr += '17,'
    # if cl.getstatus('CL17.1') == 'on':
    #     insertstr += '17.1,'
    # if cl.getstatus('CL18') == 'on':
    #     insertstr += '18,'
    # if cl.getstatus('CL18.1') == 'on':
    #     insertstr += '18.1,'
    # if cl.getstatus('CL19') == 'on':
    #     insertstr += '19,'
    # if cl.getstatus('CL19.1') == 'on':
    #     insertstr += '19.1,'
    # if cl.getstatus('CL20') == 'on':
    #     insertstr += '20,'
    # if cl.getstatus('CL20.1') == 'on':
    #     insertstr += '20.1,'
    # if cl.getstatus('CL20.2') == 'on':
    #     insertstr += '20.2,'
    # if cl.getstatus('CL20.3') == 'on':
    #     insertstr += '20.3,'
    # if cl.getstatus('CL20.4') == 'on':
    #     insertstr += '20.4,'
    # if cl.getstatus('CL20.5') == 'on':
    #     insertstr += '20.5,'
    # if cl.getstatus('CL20.6') == 'on':
    #     insertstr += '20.6,'
    # if cl.getstatus('CL20.7') == 'on':
    #     insertstr += '20.7,'
    # if cl.getstatus('CL20.8') == 'on':
    #     insertstr += '20.8,'
    # if cl.getstatus('CL20.9') == 'on':
    #     insertstr += '20.9,'
    # if cl.getstatus('CL20.10') == 'on':
    #     insertstr += '20.10,'
    # if cl.getstatus('CL20.11') == 'on':
    #     insertstr += '20.11,'
    # if cl.getstatus('CL20.12') == 'on':
    #     insertstr += '20.12,'
    # if cl.getstatus('CL20.13') == 'on':
    #     insertstr += '20.13,'
    # if cl.getstatus('CL20.14') == 'on':
    #     insertstr += '20.14,'
    # if cl.getstatus('CL20.15') == 'on':
    #     insertstr += '20.15,'
    # if cl.getstatus('CL20.16') == 'on':
    #     insertstr += '20.16,'
    # if cl.getstatus('CL20.17') == 'on':
    #     insertstr += '20.17,'
    # if cl.getstatus('CL20.18') == 'on':
    #     insertstr += '20.18,'
    # if cl.getstatus('CL20.19') == 'on':
    #     insertstr += '20.19,'
    # if cl.getstatus('CL20.20') == 'on':
    #     insertstr += '20.20,'
    # if cl.getstatus('CL20.21') == 'on':
    #     insertstr += '20.21,'
    # if cl.getstatus('CL20.22') == 'on':
    #     insertstr += '20.22,'
    # if cl.getstatus('CL20.23') == 'on':
    #     insertstr += '20.23,'
    # if cl.getstatus('CL20.24') == 'on':
    #     insertstr += '20.24,'
    # if cl.getstatus('CL21') == 'on':
    #     insertstr += '21,'

    insertstr += "\n"

    t.insert(END, insertstr)



    #Pack the input we get for unit id into a byte string
    unitId = struct.pack("B", int(unitId_input.get()))

    resp.set("")

    #Check if the first checkbox is checked, and if it is then send the request, get the response, and run the test
    if cl.getstatus('CL1.Item1')=='on':

        if z == 0 or runAndCompare_var == 1:

            reqsRan+=1

            #Modbus request
            req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x65"

            #Send the request and get the response
            output, dataStr = modbusReq(req,sock)

            outputstr=""
            #Print the name of the test, the request, and the response

            outputstr+= "\n(1) Modbus Messaging Statistics (0x65)\n\n" + " ".join('{:02X}'.format(n) for n in req) + "\n\n" + dataStr

            passfail=0

            if output[7:13] == b"\x08\x00\x15\x00\x65\x1e" and ((output[15:19] == b"\x00\x00\x00\x01") or (output[15:19] == b"\x00\x00\x00\x02") or (output[15:19] == b"\x00\x00\x00\x03")):
                #print ("\nTest Passed\n")
                outputstr+="\n\nTest Passed"
                test1=1
                passfail=1
            else:
                #print ("\n\nTest Failed")
                outputstr+="\n\nTest Failed"
                test1=2
                passfail=2


            test1len = len(output)


            #Insert the string we created into the textbox
            #resp.set(outputstr)

            t.insert(END,outputstr)

            color_test(passfail)
            outputstr=''

            if test1==1:

                servicestatus = struct.unpack(">I",output[15:19])
                outputstr+= "\nService Status = "+str(servicestatus[0])

                maxnumconn = struct.unpack(">I",output[19:23])
                outputstr+= "\nMax number of connects = "+str(maxnumconn[0])

                global numlocalconn
                numlocalconn = struct.unpack(">I",output[23:27])
                outputstr+= "\nNumber local connects = "+str(numlocalconn[0])

                numremconn = struct.unpack(">I",output[27:31])
                outputstr+= "\nNumber remote connects = "+str(numremconn[0])

                nummbmsgsin = struct.unpack(">I",output[31:35])
                outputstr+= "\nNumber MB msgs in = "+str(nummbmsgsin[0])

                nummbmsgsout = struct.unpack(">I",output[35:39])
                outputstr+= "\nNumber MB msgs out = "+str(nummbmsgsout[0])

                nummbmsgserrors = struct.unpack(">I",output[39:43])
                outputstr+= "\nNumber MB msgs errors = "+str(nummbmsgserrors[0])


                outputstr+="\n"
                t.insert(END,outputstr)

        insertstr=''
        found=0

        if comparefile_op.get() == '1':

            if numlocalconn_file != numlocalconn[0] and "1.3" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Number local connects = " + str(numlocalconn[0])
                insertstr += "\n+Number local connects supported = " + str(numlocalconn_file)

            elif numlocalconn_file == numlocalconn[0] and "1.3" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nNumber local connects Passed"


        if found == 1:
            insertstr+="\n\nCompares = "+str(compares)+"\nPasses = "+str(passes)+"\nFails = "+str(fails)+"\n"
            insertstr= "\n(1) Modbus Messaging Statistics\n"+insertstr
            t2.insert(END,insertstr)


    if cl.getstatus('CL1.Item2')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x15\x00\x66\x01\x01"
        
        outputstr=""
        
        output, dataStr = modbusReq(req,sock)
        outputstr+= "\n(2) Modbus Messaging Statistics Connections (0x66)\n\n"
        outputstr += " ".join('{:02X}'.format(n) for n in req) + "\n\n"

        outputstr+= dataStr

        passfail=0
        if (output[7:12] == b"\x08\x00\x15\x00\x66") and ((output[23:27] == b"\x00\x00\x00\x00") or (output[23:27] == b"\x00\x00\x00\x01") or (output[23:27] == b"\x00\x00\x00\x02") or (output[23:27] == b"\x00\x00\x00\x03")):
            outputstr+= "\n\nTest Passed"
            test2=1
            passfail=1
        else:
            outputstr+= "\n\nTest Failed"
            test2=2
            passfail=2

        test2len = len(output)

        #resp.set(resp.get() + outputstr)
        t.insert(END,outputstr)
        
        color_test(passfail)
        
    if cl.getstatus('CL1.Item3')=='on':

        reqsRan+=1

        outputstr=""

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x67"
        
        output, dataStr = modbusReq(req,sock)
        outputstr+="\n(3) Reset Messaging Counters (0x67)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+= dataStr
        
        passfail=0
        if output[7:12]==b"\x08\x00\x15\x00\x67":
            outputstr+="\n\nTest Passed"
            test3=1
            passfail=1
        else:
            outputstr+="\n\nTest Failed"
            test3=2
            passfail=2

        test3len = len(output)

        t.insert(END,outputstr)
        color_test(passfail)



    if cl.getstatus('CL1.Item3_5') == 'on':

        reqsRan += 1

        # Modbus request
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x68"

        # Send the request and get the response
        output, dataStr = modbusReq(req, sock)

        outputstr = ""
        # Print the name of the test, the request, and the response

        outputstr += "\n(1.5) Scanning Status\n\n" + " ".join(
            '{:02X}'.format(n) for n in req) + "\n\n" + dataStr

        passfail = 0

        if output[7:13] == b"\x08\x00\x15\x00\x68\x16":
            # print ("\nTest Passed\n")
            outputstr += "\n\nTest Passed"
            test3_5 = 1
            passfail = 1
        else:
            # print ("\n\nTest Failed")
            outputstr += "\n\nTest Failed"
            test3_5 = 2
            passfail = 2

        # Insert the string we created into the textbox
        # resp.set(outputstr)

        t.insert(END, outputstr)

        color_test(passfail)
        outputstr=''


        if test3_5==1:

            scannerstatus = struct.unpack(">I",output[15:19])
            outputstr+= "\nScanner Status = "+str(scannerstatus[0])

            scannermaxdev = struct.unpack(">I",output[19:23])
            outputstr+= "\nScanner Max device = "+str(scannermaxdev[0])

            scannerpolleddev = struct.unpack(">I",output[23:27])
            outputstr+= "\nScanner Polled device = "+str(scannerpolleddev[0])

            scannertranssend = struct.unpack(">I",output[27:31])
            outputstr+= "\nScanner Trans send = "+str(scannertranssend[0])

            scannerglobhealth = struct.unpack(">I",output[31:35])
            outputstr+= "\nScanner Global Health = "+str(scannerglobhealth[0])

            outputstr+= "\n"
            t.insert(END,outputstr)




    if cl.getstatus('CL1.Item4')=='on':

        reqsRan+=1
    
        outputstr=""

        req = b"\x00\x00\x00\x00\x00\x07" + unitId + b"\x08\x00\x15\x00\x6D\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr+="\n(4) DHCP Statistics (0x6D)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"

        outputstr+=dataStr

        passfail=0
        if (output[7:12] == b"\x08\x00\x15\x00\x6d") and ((output[13:15]==b"\x00\x01") or (output[13:15]==b"\x00\x02")):
            outputstr+="\n\nTest Passed"
            test4=1
            passfail=1
        else:
            outputstr+="\n\nTest Failed"
            test4=2
            passfail=2

        test4len = len(output)

        t.insert(END,outputstr)
        color_test(passfail)
        
    if cl.getstatus('CL1.Item5')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x6E"
        
        output, dataStr = modbusReq(req,sock)
        
        outputstr=""
        
        outputstr+="\n(5) SMTP Statistics (0x6E)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        passfail=0
        if output[7:13]==b"\x08\x00\x15\x00\x6e\x2a":
            outputstr+="\n\nTest Passed"
            test5=1
            passfail=1
        else:
            outputstr+="\n\nTest Failed (might not be implemented)"
            test5=2
            passfail=2

        test5len = len(output)

        t.insert(END,outputstr)
        color_test(passfail)

    if cl.getstatus('CL1.Item6')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x6F"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(6) NTP Statistics (0x6F)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        passfail=0
        if output[7:13]==b"\x08\x00\x15\x00\x6f\x46":
            outputstr+="\n\nTest Passed"
            test6=1
            passfail=1
        else:
            outputstr+="\n\nTest Failed"
            test6=2
            passfail=2

        test6len = len(output)

        t.insert(END,outputstr)
        color_test(passfail)
        
    if cl.getstatus('CL1.Item7')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x70"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(7) Firmware Version (0x70)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr 
        
        passfail=0
        if output[7:13]==b"\x08\x00\x15\x00\x70\x06":
            outputstr+="\n\nTest Passed"
            test7=1
            passfail=1
        else:
            outputstr+="\n\nTest Failed"
            test7=2
            passfail=2

        test7len = len(output)

        t.insert(END,outputstr)
        color_test(passfail)
        
    if cl.getstatus('CL1.Item8')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x71"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(8) Get Basic Switch Info (0x71)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr    
        
        if output[7:13]==b"\x08\x00\x15\x00\x71\x27":
            outputstr+="\n\nTest Passed"
            test8=1
            
        else:
            outputstr+="\n\nTest Failed"
            test8=2

        test8len = len(output)

        t.insert(END,outputstr)
        color_test(test8)

    if cl.getstatus('CL1.Item9')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x07" + unitId + b"\x08\x00\x15\x00\x72"

        if custom_ent.get() == "":
            req += bytes([0])
        else:
            req += bytes([int(custom_ent.get())])

        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(9) Get RSTP Port of Switch Info (0x72)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:13]==b"\x08\x00\x15\x00\x72\x2f":
            outputstr+="\n\nTest Passed"
            test9=1
        else:
            outputstr+="\n\nTest Failed"
            test9=2

        test9len = len(output)

        t.insert(END,outputstr)
        color_test(test9)


    if cl.getstatus('CL1.Item10')=='on':

        reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x75"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(9.5) Get Bandwidth (0x75)\n\n"
        outputstr += " ".join('{:02X}'.format(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:12] == b"\x08\x00\x15\x00\x75":
            outputstr += "\n\nTest Passed"
            test9_5 = 1
        else:
            outputstr += "\n\nTest Failed"
            test9_5 = 2

        t.insert(END, outputstr)
        color_test(test9_5)
        outputstr=''

        if test9_5==1:

            percentmpcu = struct.unpack(">I",output[13:17])
            outputstr+= "\nPercent of MCPU used per second = "+str(percentmpcu[0])

            numEIPscannerInPPS = struct.unpack(">I",output[17:21])
            outputstr+= "\nNumber EIP scanner input pps = "+str(numEIPscannerInPPS[0])

            numEIPscannerOutPPS = struct.unpack(">I",output[21:25])
            outputstr+= "\nNumber EIP scanner output pps = "+str(numEIPscannerOutPPS[0])

            numModscannerInPPS = struct.unpack(">I",output[25:29])
            outputstr+= "\nNumber Modbus scanner input pps = "+str(numModscannerInPPS[0])

            numModscannerOutPPS = struct.unpack(">I",output[29:33])
            outputstr+= "\nNumber Modbus scanner output pps = "+str(numModscannerOutPPS[0])

            numEIPadapterInPPS = struct.unpack(">I",output[33:37])
            outputstr+= "\nNumber EIP adapter input pps = "+str(numEIPadapterInPPS[0])

            numEIPadapterOutPPS = struct.unpack(">I",output[37:41])
            outputstr+= "\nNumber EIP adapter output pps = "+str(numEIPadapterOutPPS[0])

            numModuleCapPPS = struct.unpack(">I",output[41:45])
            outputstr+= "\nNumber of Module Capacity pps = "+str(numModuleCapPPS[0])

            numClientEIPMsgAPS = struct.unpack(">I",output[45:49])
            outputstr+= "\nNumber Client EIP msg activity per second = "+str(numClientEIPMsgAPS[0])

            numClientModMsgAPS = struct.unpack(">I",output[49:53])
            outputstr+= "\nNumber Client Modbus msg activity per second = "+str(numClientModMsgAPS[0])

            numServerEIPMsgAPS = struct.unpack(">I",output[53:57])
            outputstr+= "\nNumber Server EIP msg activity per second = "+str(numServerEIPMsgAPS[0])

            numServerModMsgAPS = struct.unpack(">I",output[57:61])
            outputstr+= "\nNumber Server Modbus msg activity per second = "+str(numServerModMsgAPS[0])

            numbroadpack = struct.unpack(">I",output[61:65])
            outputstr+= "\nNumber of broadcast packets from the network per second = "+str(numbroadpack[0])

            nummultipack = struct.unpack(">I",output[65:69])
            outputstr+= "\nNumber of multicast packets from the network per second = "+str(nummultipack[0])

            numunipack = struct.unpack(">I",output[69:73])
            outputstr+= "\nNumber of unicast packets from the network per second = "+str(numunipack[0])

            numuselesspack = struct.unpack(">I",output[73:77])
            outputstr+= "\nNumber of useless packets from the network per second = "+str(numuselesspack[0])

            numdroppack = struct.unpack(">I",output[77:81])

            outputstr+= "\nNumber of dropped packets from the network per second = "+str(numdroppack[0])


            outputstr += "\n"
            t.insert(END, outputstr)



    if cl.getstatus('CL2.Item1')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x09" + unitId + b"\x08\x00\x16\x00\x01\x01\x00\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(10) Read Basic Network Diagnostics (1/0x100)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x01\x01\x00":
            #outputstr+="\n\nTest Passed"
            test10=1
        else:
            #outputstr+="\n\nTest Failed"
            test10=2

        test10len = len(output)

        t.insert(END,outputstr)
        color_test(test10)
        outputstr=''

        if test10==1:

            basicnetworkdiagvalid = struct.unpack(">I",output[17:21])
            outputstr+= "\nBasic Network Diagnostics Validity = "+'{:08X}'.format(basicnetworkdiagvalid[0])+'h'
            if '{:08X}'.format(basicnetworkdiagvalid[0])+'h' == '0003FFFFh':
                outputstr+= "\nTest Passed\n"
                test10_1=1
            else:
                outputstr+= "\nTest Failed\n"
                test10_1=2

            communicationglobstat = struct.unpack(">H",output[21:23])
            outputstr+= "\nCommunication Global Status = "+'{:04X}'.format(communicationglobstat[0])+'h'
            if '{:04X}'.format(communicationglobstat[0])+'h' == '0002h':
                outputstr+= "\nTest Passed\n"
                test10_2 = 1
            else:
                outputstr+= "\nTest Failed\n"
                test10_2=2


            supportedcommserv = struct.unpack(">H",output[23:25])
            outputstr+= "\nSupported Communication Services = "+'{:04X}'.format(supportedcommserv[0])+'h'
            if '{:04X}'.format(supportedcommserv[0])+'h' == '0001h':
                outputstr+= "\nTest Passed\n"
                test10_3 = 1
            else:
                outputstr+= "\nTest Failed\n"
                test10_3=2


            statuscommserv = struct.unpack(">H",output[25:27])
            outputstr+= "\nStatus of Communication Services = "+'{:04X}'.format(statuscommserv[0])+'h'
            if '{:04X}'.format(statuscommserv[0])+'h' == '0002h':
                outputstr+= "\nTest Passed\n"
                test10_4 = 1
            else:
                outputstr+= "\nTest Failed\n"
                test10_4 = 2


            ipaddr = struct.unpack(">I",output[27:31])
            ipaddrhex = '{:08X}'.format(ipaddr[0])
            outputstr+= "\nIP Address = "+str(int(ipaddrhex[0:2],16))+'.'+str(int(ipaddrhex[2:4],16))+'.'+str(int(ipaddrhex[4:6],16))+'.'+str(int(ipaddrhex[6:8],16))
            if str(int(ipaddrhex[0:2],16))+'.'+str(int(ipaddrhex[2:4],16))+'.'+str(int(ipaddrhex[4:6],16))+'.'+str(int(ipaddrhex[6:8],16)) == TCP_IP.get():
                outputstr+= "\nTest Passed\n"
                test10_5 = 1
            else:
                outputstr+= "\nTest Failed\n"
                test10_5 = 2


            submask = struct.unpack(">I",output[31:35])
            submaskhex = '{:08X}'.format(submask[0])
            outputstr+= "\nSubnet Mask = "+str(int(submaskhex[0:2],16))+'.'+str(int(submaskhex[2:4],16))+'.'+str(int(submaskhex[4:6],16))+'.'+str(int(submaskhex[6:8],16))
            outputstr+= "\nCannot be tested\n"


            defaultgate = struct.unpack(">I",output[35:39])
            defaultgatehex = '{:08X}'.format(defaultgate[0])
            outputstr+= "\nDefault Gateway = "+str(int(defaultgatehex[0:2],16))+'.'+str(int(defaultgatehex[2:4],16))+'.'+str(int(defaultgatehex[4:6],16))+'.'+str(int(defaultgatehex[6:8],16))
            outputstr+= "\nCannot be tested\n"


            macaddr = struct.unpack("6B",output[39:45])
            outputstr+= "\nMAC Address = " + '{:02X}'.format(macaddr[0])+':'+'{:02X}'.format(macaddr[1])+':'+'{:02X}'.format(macaddr[2])+':'+'{:02X}'.format(macaddr[3])+':'+'{:02X}'.format(macaddr[4])+':'+'{:02X}'.format(macaddr[5])
            outputstr+= "\nCannot be tested\n"


            etherframeform = struct.unpack("6B",output[45:51])
            outputstr+="\nEther Frame Format Capability = "
            addstr=''
            for x in etherframeform:
                addstr+='{:02X}'.format(x) + " "
            outputstr+=addstr
            if addstr == "00 01 00 01 00 01":
                outputstr+= "\nTest Failed\n"
                test10_6 = 2
            else:
                outputstr+= "\nTest Failed\n"
                test10_6 = 2


            etherrcvframes = struct.unpack(">I",output[51:55])
            outputstr+= "\nEther Rcv Frames = "+ str(etherrcvframes[0])

            etherxmitframes = struct.unpack(">I",output[55:59])
            outputstr+= "\nEther Xmit Frames = "+str(etherxmitframes[0])

            nummbopenclientconn = struct.unpack(">H",output[59:61])
            outputstr+= "\nNum MB Open Client Connections = "+str(nummbopenclientconn[0])
            if str(nummbopenclientconn[0]) == '0':
                outputstr+= "\nTest Passed\n"
                test10_7 = 1
            else:
                outputstr+= "\nTest Failed\n"
                test10_7=2


            nummbopenserverconn = struct.unpack(">H",output[61:63])
            outputstr+= "\nNum MB Open Server Connections = "+str(nummbopenserverconn[0])
            if str(nummbopenserverconn[0]) == '2':
                outputstr+= "\nTest Passed\n"
                test10_8 = 1
            else:
                outputstr+= "\nTest Failed\n"
                test10_8 = 2


            nummberrormsgssent = struct.unpack(">I",output[63:67])
            outputstr+= "\nNum MB Error Msgs Sent = "+str(nummberrormsgssent[0])
            if str(nummberrormsgssent[0]) == '0':
                outputstr+= "\nTest Passed\n"
                test10_9 = 1
            else:
                outputstr+= "\nTest Failed\n"
                test10_9 = 2


            nummbmsgssent = struct.unpack(">I",output[67:71])
            outputstr+= "\nNum MB Msgs Sent = "+str(nummbmsgssent[0])

            nummbmsgsrcvd = struct.unpack(">I",output[71:75])
            outputstr+= "\nNum MB Msgs Rcvd = "+str(nummbmsgsrcvd[0])

            outputstr+= "\nDevice Name = " + output[75:91].decode("ascii")

            # x=75
            # while output[x] != 0:
            #     outputstr+= bytes([output[x]]).decode("ascii")
            #     x+=1
            #
            # x+=1

            ipassnmode = struct.unpack(">I",output[91:95])
            outputstr+= "\nIP Assignment Mode Capability / Operational = "+'{:08X}'.format(ipassnmode[0])+'h'
            if '{:08X}'.format(ipassnmode[0])+'h' == '00030008h':
                outputstr+= "\nTest Failed\n"
                test10_10=2
            else:
                outputstr+= "\nTest Failed\n"
                test10_10=2


            if test10_1==1 and test10_2==1 and test10_3==1 and test10_4==1 and test10_5==1 and test10_6==1 and test10_7==1 and test10_8==1 and test10_9==1 and test10_10==1:
                outputstr+= "\nAll tests passed"
            elif test10_1==2 and test10_2==2 and test10_3==2 and test10_4==2 and test10_5==2 and test10_6==2 and test10_7==2 and test10_8==2 and test10_9==2 and test10_10==2:
                outputstr+= "\nAll tests failed"
                test10=2
            else:
                test10=2
                outputstr+="\n\nPassed:\n"

                if test10_1==1:
                    outputstr+= "\nBasic Network Diagnostics Validity"
                if test10_2 == 1:
                    outputstr += "\nCommunication Global Status"
                if test10_3 == 1:
                    outputstr += "\nSupported Communication Services"
                if test10_4==1:
                    outputstr+="\nStatus of Communication Services"
                if test10_5 == 1:
                    outputstr += "\nIP Address"
                if test10_6==1:
                    outputstr+="\nEther Frame Format Capability"
                if test10_7==1:
                    outputstr+="\nNum MB Open Client Connections"
                if test10_8==1:
                    outputstr+="\nNum MB Open Server Connections"
                if test10_9==1:
                    outputstr+="\nNum MB Error Msgs Sent"
                if test10_10==1:
                    outputstr+="\nIP Assignment Mode Capability / Operational"

                outputstr+="\n\nFailed:\n"

                if test10_1==2:
                    outputstr += "\nBasic Network Diagnostics Validity"
                if test10_2==2:
                    outputstr+="\nCommunication Global Status"
                if test10_3==2:
                    outputstr+="\nSupported Communication Services"
                if test10_4==2:
                    outputstr+="\nStatus of Communication Services"
                if test10_5==2:
                    outputstr+="\nIP Address"
                if test10_6==2:
                    outputstr+="\nEther Frame Format Capability"
                if test10_7==2:
                    outputstr+="\nNum MB Open Client Connections"
                if test10_8==2:
                    outputstr+="\nNum MB Open Server Connections"
                if test10_9==2:
                    outputstr+="\nNum MB Error Msgs Sent"
                if test10_10==2:
                    outputstr+="\nIP Assignment Mode Capability / Operational"

            outputstr+="\n\nSubnet Mask, Default Gateway, MAC Address, Ether Rcv Frames, Ether Xmit Frames, Num MB Msgs Sent, Num MB Msgs Rcvd, Device Name were not tested."


            outputstr+="\n"
            t.insert(END,outputstr)




    if cl.getstatus('CL2.Item2')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x09" + unitId + b"\x08\x00\x16\x00\x01\x02"

        if custom_ent.get() == "":
            addition = b'\x00'
        else:
            addition = struct.pack('B',int(custom_ent.get()))

        req += addition + b'\x00'

        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(11) Read Port Diagnostic Data (1/0x200)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"

        outputstr+=dataStr
        
        if output[7:13]==b"\x08\x00\x16\x00\x01\x02":
            #outputstr+="\n\nTest Passed"
            test11=1
        else:
            #outputstr+="\n\nTest Failed"
            test11=2

        test11len = len(output)

        t.insert(END,outputstr)
        color_test(test11)
        outputstr=''

        if test11==1:

            portdiagdatavalid = struct.unpack(">H",output[17:19])
            outputstr+="\nPort Diagnostics Data Validity = "+'{:04X}'.format(portdiagdatavalid[0]) + 'h'
            if '{:04X}'.format(portdiagdatavalid[0]) + 'h' == '07FFh':
                outputstr+= "\nTest Passed\n"
                test11_1=1
            else:
                outputstr+= "\nTest Failed\n"
                test11_1=2

            outputstr+= "\nLogical/Physical Port Number = "+bytes([output[19]]).hex() + " " + bytes([output[20]]).hex()
            if bytes([output[19]]).hex() + " " + bytes([output[20]]).hex() == '01 00':
                outputstr+= "\nTest Failed\n"
                test11_2=2
            else:
                outputstr+= "\nTest Failed\n"
                test11_2=2


            outputstr+= "\nEther Control Capability = "+bytes([output[21]]).hex() + " " + bytes([output[22]]).hex()
            if bytes([output[21]]).hex() + " " + bytes([output[22]]).hex() == '20 19':
                outputstr+= "\nTest Failed\n"
                test11_3=2
            else:
                outputstr+= "\nTest Failed\n"
                test11_3=2


            linkspdcap = struct.unpack(">H",output[23:25])
            outputstr+= "\nLink Speed Capability = "+str(linkspdcap[0])
            if str(linkspdcap[0]) == '100':
                outputstr+= "\nTest Passed\n"
                test11_4=1
            else:
                outputstr+= "\nTest Failed\n"
                test11_4=2

            outputstr+= "\nEther Control Configuration = "+bytes([output[25]]).hex() + " " + bytes([output[26]]).hex()
            if bytes([output[25]]).hex() + " " + bytes([output[26]]).hex() == '00 09':
                outputstr+= "\nTest Failed\n"
                test11_5=2
            else:
                outputstr+= "\nTest Failed\n"
                test11_5=2


            linkspdconf = struct.unpack(">H",output[27:29])
            outputstr+= "\nLink Speed Configuration = "+str(linkspdconf[0])
            if str(linkspdconf[0]) == '100':
                outputstr+= "\nTest Passed\n"
                test11_6 = 1
            else:
                outputstr+= "\nTest Failed\n"
                test11_6 = 2


            outputstr+= "\nEther Control Operational = "+bytes([output[29]]).hex() + " " + bytes([output[30]]).hex()
            if bytes([output[29]]).hex() + " " + bytes([output[30]]).hex() == '00 09':
                outputstr+= "\nTest Failed\n"
                test11_7 = 2
            else:
                test11_7=2
                outputstr+= "\nTest Failed\n"


            linkspdoper = struct.unpack(">H",output[31:33])
            outputstr+= "\nLink Speed Operational = "+str(linkspdoper[0])
            if str(linkspdoper[0]) == '100':
                outputstr+= "\nTest Passed\n"
                test11_8=1
            else:
                outputstr+= "\nTest Failed\n"
                test11_8=2


            outputstr+= "\nPort MAC Address = "
            addstr=''
            for x in range(0,6):
                if x<5:
                    addstr+=output[33+x:33+x+1].hex()+':'
                else:
                    addstr+=output[33+x:33+x+1].hex()
            outputstr+=addstr
            outputstr+= "\nCannot be tested\n"


            outputstr+= "\nMedia Counters = "

            for x in range(0,72):
                outputstr+=output[39+x:39+x+1].hex() + ' '
            outputstr+= "\nCannot be tested\n"


            interfacelength = struct.unpack(">H",output[111:113])
            outputstr+= "\nInterface Label Length = "+str(interfacelength[0])
            if str(interfacelength[0])=='18':
                outputstr+="\nTest Passed\n"
                test11_9=1
            else:
                outputstr+="\nTest Failed\n"
                test11_9=2


            outputstr+= "\nInterface Label = " + output[113:113+interfacelength[0]].decode("ascii")
            if output[113:113+interfacelength[0]].decode("ascii") == 'Internal Interface':
                outputstr+='\nTest Passed\n'
                test11_10=1
            else:
                outputstr+="\nTest Failed\n"
                test11_10=2


            outputstr+= "\nInterface Counters = "

            for x in range(113+interfacelength[0],len(output)):
                outputstr+= output[x:x+1].hex() + ' '




            if test11_1==1 and test11_2==1 and test11_3==1 and test11_4==1 and test11_5==1 and test11_6==1 and test11_7==1 and test11_8==1 and test11_9==1 and test11_10==1:
                outputstr+= "\nAll tests passed"
            elif test11_1==2 and test11_2==2 and test11_3==2 and test11_4==2 and test11_5==2 and test11_6==2 and test11_7==2 and test11_8==2 and test11_9==2 and test11_10==2:
                outputstr+= "\nAll tests failed"
                test11=2
            else:
                test11=2
                outputstr+="\n\nPassed:\n"

                if test11_1==1:
                    outputstr+= "\nPort Diagnostics Data Validity"
                if test11_2 == 1:
                    outputstr += "\nLogical/Physical Port Number"
                if test11_3 == 1:
                    outputstr += "\nEther Control Capability"
                if test11_4==1:
                    outputstr+="\nLink Speed Capability"
                if test11_5 == 1:
                    outputstr += "\nEther Control Configuration"
                if test11_6==1:
                    outputstr+="\nLink Speed Configuration"
                if test11_7==1:
                    outputstr+="\nEther Control Operational"
                if test11_8==1:
                    outputstr+="\nLink Speed Operational"
                if test11_9==1:
                    outputstr+="\nInterface Label Length"
                if test11_10==1:
                    outputstr+="\nInterface Label"


                outputstr+="\n\nFailed:\n"

                if test11_1==2:
                    outputstr += "\nPort Diagnostics Data Validity"
                if test11_2==2:
                    outputstr+="\nLogical/Physical Port Number"
                if test11_3==2:
                    outputstr+="\nEther Control Capability"
                if test11_4==2:
                    outputstr+="\nLink Speed Capability"
                if test11_5==2:
                    outputstr+="\nEther Control Configuration"
                if test11_6==2:
                    outputstr+="\nLink Speed Configuration"
                if test11_7==2:
                    outputstr+="\nEther Control Operational"
                if test11_8==2:
                    outputstr+="\nLink Speed Operational"
                if test11_9==2:
                    outputstr+="\nInterface Label Length"
                if test11_10==2:
                    outputstr+="\nInterface Label"

            outputstr+="\n\nPort MAC Address, Media Counters, Interface Counters were not tested."


            outputstr += "\n"
            t.insert(END, outputstr)


    if cl.getstatus('CL2.Item3')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x09" + unitId + b"\x08\x00\x16\x00\x01\x03\x00\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(12) Read Modbus TCP/Port 502 Diag Data (1/0x300)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x01\x03\x00":
            #outputstr+="\n\nTest Passed"
            test12=1
        else:
            #outputstr+="\n\nTest Failed"
            test12=2

        test12len = len(output)

        t.insert(END,outputstr)
        color_test(test12)
        outputstr=''

        if test12==1:

            outputstr+= "\nModbus TCP/Port 502 Diag Validity = "+output[17:21].hex() + 'h'
            if output[17:21].hex() + 'h' == '00 00 1F 88':
                outputstr+="\nTest Passed\n"
                test12_1 = 1
            else:
                outputstr+="\nTest Failed\n"
                test12_1=2


            outputstr+= "\nPort 502 Status = "+output[21:23].hex() + 'h'
            if output[21:23].hex() + 'h' == '00 02':
                outputstr+="\nTest Failed\n"
                test12_2=2
            else:
                outputstr+="\nTest Failed\n"
                test12_2=2


            nummbopenconn = struct.unpack(">H",output[23:25])
            outputstr+= "\nNum MB Open Connections = "+str(nummbopenconn[0])
            if str(nummbopenconn[0]) == '2':
                outputstr+="\nTest Passed\n"
                test12_3=1
            else:
                outputstr+="\nTest Failed\n"
                test12_3=2



            nummbmsgssent = struct.unpack(">I",output[25:29])
            outputstr+= "\nNum MB Msgs Sent = "+str(nummbmsgssent[0])
            outputstr+="\nCannot be tested\n"

            nummbmsgsrcvd = struct.unpack(">I",output[29:33])
            outputstr+= "\nNum MB Msgs Received = "+str(nummbmsgsrcvd[0])
            outputstr+= "\nCannot be tested\n"

            nummbopenclientconn = struct.unpack(">H",output[33:35])
            outputstr+= "\nNum MB Open Client Connections = "+str(nummbopenclientconn[0])
            if str(nummbopenclientconn[0]) == '0':
                outputstr+="\nTest Passed\n"
                test12_4=1
            else:
                test12_4=2
                outputstr+="\nTest Failed\n"


            nummbopenserverconn = struct.unpack(">H",output[35:37])
            outputstr+= "\nNum MB Open Server Connections = "+str(nummbopenserverconn[0])
            if str(nummbopenserverconn[0])=='2':
                outputstr+="\nTest Passed\n"
                test12_5=1
            else:
                test12_5=2
                outputstr+="\nTest Failed\n"



            nummberrormsgssent = struct.unpack(">I",output[37:41])
            outputstr+= "\nNum MB Error Msgs Sent = "+str(nummberrormsgssent[0])
            outputstr+= "\nCannot be tested\n"




            if test12_1==1 and test12_2==1 and test12_3==1 and test12_4==1 and test12_5==1:
                outputstr+= "\nAll tests passed"
            elif test12_1==2 and test12_2==2 and test12_3==2 and test12_4==2 and test12_5==2:
                outputstr+= "\nAll tests failed"
                test12=2
            else:
                test12=2
                outputstr+="\n\nPassed:\n"

                if test12_1==1:
                    outputstr+= "\nModbus TCP/Port 502 Diag Validity"
                if test12_2 == 1:
                    outputstr += "\nPort 502 Status"
                if test12_3 == 1:
                    outputstr += "\nNum MB Open Connections"
                if test12_4==1:
                    outputstr+="\nNum MB Open Client Connections"
                if test12_5 == 1:
                    outputstr += "\nNum MB Open Server Connections"



                outputstr+="\n\nFailed:\n"

                if test12_1==2:
                    outputstr += "\nModbus TCP/Port 502 Diag Validity"
                if test12_2==2:
                    outputstr+="\nPort 502 Status"
                if test12_3==2:
                    outputstr+="\nNum MB Open Connections"
                if test12_4==2:
                    outputstr+="\nNum MB Open Client Connections"
                if test12_5==2:
                    outputstr+="\nNum MB Open Server Connections"


            outputstr+="\n\nNum MB Msgs Sent, Num MB Msgs Received, Num MB Error Msgs Sent were not tested."




            outputstr+="\n"
            t.insert(END,outputstr)




    if cl.getstatus('CL2.Item4')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x09" + unitId + b"\x08\x00\x16\x00\x01\x04\x00\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(13) Read Modbus TCP/Port Connection Data (1/0x400)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x01\x04\x00":
            #outputstr+="\n\nTest Passed"
            test13=1
        else:
            #outputstr+="\n\nTest Failed"
            test13=2

        test13len = len(output)

        t.insert(END,outputstr)
        color_test(test13)
        outputstr=''

        if test13==1:

            outputstr+= "\nConnection Table Validity = "+output[17:19].hex() + 'h'
            if output[17:19].hex() + 'h' == '0007h':
                outputstr+="\nTest Passed\n"
                test13_1=1
            else:
                outputstr+="\nTest Failed\n"
                test13_1=2


            numentries = struct.unpack(">H",output[19:21])
            outputstr+= "\nNumber of Entries = " + str(numentries[0])
            if str(numentries[0]) == '2':
                outputstr+="\nTest Passed\n"
                test13_2=1
            else:
                outputstr+="\nTest Failed\n"
                test13_2=2

            startentind = struct.unpack(">H",output[21:23])
            outputstr+= "\nStarting Entry Index = "+str(startentind[0])
            if str(startentind[0]) == '1':
                outputstr+="\nTest Passed\n"
                test13_3=1
            else:
                outputstr+="\nTest Failed\n"
                test13_3=2




            if test13_1==1 and test13_2==1 and test13_3==1:
                outputstr+= "\nAll tests passed"
            elif test13_1==2 and test13_2==2 and test13_3==2:
                outputstr+= "\nAll tests failed"
                test13=2
            else:
                test13=2
                outputstr+="\n\nPassed:\n"

                if test13_1==1:
                    outputstr+= "\nConnection Table Validity"
                if test13_2 == 1:
                    outputstr += "\nNumber of Entries"
                if test13_3 == 1:
                    outputstr += "\nStarting Entry Index"




                outputstr+="\n\nFailed:\n"

                if test13_1==2:
                    outputstr += "\nConnection Table Validity"
                if test13_2==2:
                    outputstr+="\nNumber of Entries"
                if test13_3==2:
                    outputstr+="\nStarting Entry Index"



            outputstr+="\n\nEntries were not tested."




            outputstr+="\n"
            t.insert(END,outputstr)



    if cl.getstatus('CL2.Item5')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x01\x7F\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(14) Read Data Structures Offsets (1/0x7F00)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr

        if output[7:14]==b"\x08\x00\x16\x00\x01\x7f\x00":
            outputstr+="\n\nTest Passed"
            test14=1
        else:
            outputstr+="\n\nTest Failed"
            test14=2

        test14len = len(output)

        t.insert(END,outputstr)
        color_test(test14)


    if cl.getstatus('CL2.Item55')=='on':

        reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x0a" + unitId + b"\x08\x00\x16\x00\x01\x80\x00\x00\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr=""
        outputstr+="\n(14.5) FDR Client Diagnostics Data\n\n"
        outputstr += " ".join('{:02X}'.format(n) for n in req) + "\n\n"

        outputstr+=dataStr
        test55=0
        if output[7:16] == b"\x08\x00\x16\x00\x01\x80\x00\x00\x00":
            #outputstr+="\n\nTest Passed"
            test55=1
        else:
            #outputstr+="\n\nTest Failed"
            test55=2

        t.insert(END,outputstr)
        color_test(test55)
        outputstr=""

        if test55==1:

            outputstr+= "\nFDR Client Diagnostics Validity = "+output[17:21].hex() + 'h'
            if output[17:21].hex() + 'h' == '0FC79E80h':
                outputstr+="\nTest Passed\n"
                test55_1=1
            else:
                outputstr+="\nTest Failed\n"
                test55_1=2

            outputstr+= "\nFDR Client Status = "+output[21:23].hex() + 'h'
            if output[21:23].hex() + 'h' == '0036h':
                outputstr+="\nTest Failed\n"
                test55_2=2
            else:
                outputstr+="\nTest Failed\n"
                test55_2=2

            outputstr+= "\nDevice Name = "+output[23:39].decode("ascii")
            outputstr+="\nCannot be tested\n"


            outputstr+= "\nDevice Parameters Status = "+output[39:41].hex() + 'h'



            ipaddr = struct.unpack(">I",output[41:45])
            ipaddrhex = '{:08X}'.format(ipaddr[0])
            outputstr+= "\nIP Address = "+str(int(ipaddrhex[0:2],16))+'.'+str(int(ipaddrhex[2:4],16))+'.'+str(int(ipaddrhex[4:6],16))+'.'+str(int(ipaddrhex[6:8],16))
            if str(int(ipaddrhex[0:2],16))+'.'+str(int(ipaddrhex[2:4],16))+'.'+str(int(ipaddrhex[4:6],16))+'.'+str(int(ipaddrhex[6:8],16)) == TCP_IP.get():
                outputstr+="\nTest Passed\n"
                test55_3=1
            else:
                test55_3=2
                outputstr+="\nTest Failed\n"



            submask = struct.unpack(">I",output[45:49])
            submaskhex = '{:08X}'.format(submask[0])
            outputstr+= "\nSubnet Mask = "+str(int(submaskhex[0:2],16))+'.'+str(int(submaskhex[2:4],16))+'.'+str(int(submaskhex[4:6],16))+'.'+str(int(submaskhex[6:8],16))

            defaultgate = struct.unpack(">I",output[49:53])
            defaultgatehex = '{:08X}'.format(defaultgate[0])
            outputstr+= "\nDefault Gateway = "+str(int(defaultgatehex[0:2],16))+'.'+str(int(defaultgatehex[2:4],16))+'.'+str(int(defaultgatehex[4:6],16))+'.'+str(int(defaultgatehex[6:8],16))

            paramserveripaddr = struct.unpack(">I",output[53:57])
            paramserveripaddrhex = '{:08X}'.format(paramserveripaddr[0])
            outputstr+= "\nParameter Server IP Address = "+str(int(paramserveripaddrhex[0:2],16))+'.'+str(int(paramserveripaddrhex[2:4],16))+'.'+str(int(paramserveripaddrhex[4:6],16))+'.'+str(int(paramserveripaddrhex[6:8],16))

            outputstr+= "\nIP Assignment Mode Capability / Operational = "+output[57:61].hex()
            outputstr+= "\nFDR Error Code = "+output[61:63].hex() + 'h'

            numautobackupscompl = struct.unpack(">H",output[63:65])
            outputstr+= "\nNum Automatic Backups Completed = "+str(numautobackupscompl[0])

            numusertrigbackcompl = struct.unpack(">H",output[65:67])
            outputstr+= "\nNum User Triggered Backups Completed = "+str(numusertrigbackcompl[0])

            numautorestcompl = struct.unpack(">H",output[67:69])
            outputstr+= "\nNum Automatic Restores Complete = "+str(numautorestcompl[0])

            numusertrigrestcompl = struct.unpack(">H",output[69:71])
            outputstr+= "\nNum User Triggered Restores Completed = "+str(numusertrigrestcompl[0])

            numftpbackresterr = struct.unpack(">H",output[71:73])
            outputstr+= "\nNum FTP/TFTP Backup/Restore Errors = "+str(numftpbackresterr[0])




            if test55_1==1 and test55_2==1 and test55_3==1:
                outputstr+= "\nAll tests passed"
            elif test55_1==2 and test55_2==2 and test55_3==2:
                outputstr+= "\nAll tests failed"
                test55=2
            else:
                test55=2
                outputstr+="\n\nPassed:\n"

                if test55_1==1:
                    outputstr+= "\nFDR Client Diagnostics Validity"
                if test55_2 == 1:
                    outputstr += "\nFDR Client Status"
                if test55_3 == 1:
                    outputstr += "\nIP Address"




                outputstr+="\n\nFailed:\n"

                if test55_1==2:
                    outputstr += "\nFDR Client Diagnostics Validity"
                if test55_2==2:
                    outputstr+="\nFDR Client Status"
                if test55_3==2:
                    outputstr+="\nIP Address"



            outputstr+="\n\nDevice Name, Device Parameters Status, Subnet Mask, Default Gateway, Parameter Server IP Address, IP Assignment Mode Capability / Operational, FDR Error Code, Num Automatic Backups Completed, Num User Triggered Backups Completed, Num Automatic Restores Complete, Num User Triggered Restores Completed, Num FTP/TFTP Backup/Restore Errors were not tested."




            outputstr+="\n"
            t.insert(END,outputstr)






    if cl.getstatus('CL2.Item6')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x02\x01\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=''
        outputstr+="\n(15) Clear Diag data for Network (2/0x100)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x02\x01\x00":
            outputstr+="\n\nTest Passed"
            test15=1
        else:
            outputstr+="\n\nTest Failed"
            test15=2

        test15len = len(output)

        t.insert(END,outputstr)
        color_test(test15)

    if cl.getstatus('CL2.Item7')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x02\x02\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(16) Clear Diag data for Ethernet Port (2/0x200)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x02\x02\x00":
            outputstr+="\n\nTest Passed"
            test16=1
        else:
            outputstr+="\n\nTest Failed"
            test16=2

        test16len = len(output)

        t.insert(END,outputstr)
        color_test(test16)

    if cl.getstatus('CL2.Item8')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x02\x03\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(17) Clear Diag data for MB Port 502 (2/0x300)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x02\x03\x00":
            outputstr+="\n\nTest Passed"
            test17=1
        else:
            outputstr+="\n\nTest Failed"
            test17=2

        test17len = len(output)

        t.insert(END,outputstr)
        color_test(test17)

    if cl.getstatus('CL2.Item9')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x02\x04\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(18) Clear Diag data for Connection table (2/0x400)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x02\x04\x00":
            outputstr+="\n\nTest Passed"
            test18=1
        else:
            outputstr+="\n\nTest Failed"
            test18=2

        test18len = len(output)

        t.insert(END,outputstr)
        color_test(test18)

    if cl.getstatus('CL2.Item10')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x03\x00\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(19) Clear All Diagnostic Data (3/0)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x03\x00\x00":
            outputstr+="\n\nTest Passed"
            test19=1
        else:
            outputstr+="\n\nTest Failed"
            test19=2

        test19len = len(output)

        t.insert(END,outputstr)
        color_test(test19)

    if cl.getstatus('CL2.Item11')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x04\x00\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(20) List Ports (4/0)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:14]==b"\x08\x00\x16\x00\x04\x00\x00":
            outputstr+="\n\nTest Passed"
            test20=1
        else:
            outputstr+="\n\nTest Failed"
            test20=2

        test20len = len(output)

        t.insert(END,outputstr)
        color_test(test20)

    if cl.getstatus('CL3.Item1')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x2B\x0E\x01\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(21) Read Basic Object Device ID (0E/1/0)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if isFile:
        
            if output[7:10]==b"\x2b\x0e\x01" and output[16:36].decode("utf-8") + "\n" == content[0] and output[38:50].decode("utf-8") + "\n" == content[1] and output[52:58].decode("utf-8") + "\n" == content[2]:
                outputstr+="\n\nTest Passed"
                test21=1
            else:
                outputstr+="\n\nTest Failed"
                test21=2
        else:
            if output[7:10]==b"\x2b\x0e\x01" :
                outputstr+="\n\nTest Passed"
                test21=1
            else:
                outputstr+="\n\nTest Failed"
                test21=2

        test21len = len(output)

        t.insert(END,outputstr)
        color_test(test21)

    if cl.getstatus('CL3.Item2')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x2B\x0E\x02\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(22) Read Regular Object Device ID (0E/2/0)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:10]==b"\x2b\x0e\x02":
            outputstr+="\n\nTest Passed"
            test22=1
        else:
            outputstr+="\n\nTest Failed"
            test22=2

        test22len = len(output)

        t.insert(END,outputstr)
        color_test(test22)

    if cl.getstatus('CL3.Item3')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x2B\x0E\x03\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(23) Read Extended Object Device ID (0E/3/0)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:10]==b"\x2b\x0e\x03":
            outputstr+="\n\nTest Passed"
            test23=1
        else:
            outputstr+="\n\nTest Failed"
            test23=2

        test23len = len(output)

        t.insert(END,outputstr)
        color_test(test23)

    if cl.getstatus('CL3.Item4')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x2B\x0E\x04\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(24) Read Individual Object of Device ID (0E/4/0)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:10]==b"\x2b\x0e\x04":
            outputstr+="\n\nTest Passed"
            test24=1
        else:
            outputstr+="\n\nTest Failed"
            test24=2

        test24len = len(output)

        t.insert(END,outputstr)
        color_test(test24)

    if cl.getstatus('CL4')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x06\xFF\x03\x00\x63\x00\x05"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(25) Modbus Read Register Command FC 3 Unit Id 255\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[5:9]==b"\x0d\xff\x03\x0a":
            outputstr+="\n\nTest Passed"
            test25=1
        else:
            outputstr+="\n\nTest Failed"
            test25=2

        test25len = len(output)

        t.insert(END,outputstr)
        color_test(test25)

    if cl.getstatus('CL5')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x01\x00\x00\x00\x05"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(26) Read Coils (FC 1)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[0:9]==(b"\x00\x00\x00\x00\x00\x04" + unitId + b"\x01\x01"):
            outputstr+="\n\nTest Passed"
            test26=1
        else:
            outputstr+="\n\nTest Failed"
            test26=2

        test26len = len(output)

        t.insert(END,outputstr)
        color_test(test26)

    if cl.getstatus('CL6')=='on':
        
        reqsRan+=1
        
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x02\x00\x00\x00\x05"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(27) Read Inputs (FC 2)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"

        outputstr+=dataStr
        
        if output[0:9]==(b"\x00\x00\x00\x00\x00\x04" + unitId + b"\x02\x01"):
            outputstr+="\n\nTest Passed"
            test27=1
        else:
            outputstr+="\n\nTest Failed"
            test27=2

        test27len = len(output)

        t.insert(END,outputstr)
        color_test(test27)

    if cl.getstatus('CL7')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x03\x00\x64\x00\x01"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(28) Read Holding Registers (FC 3)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[0:9]==(b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x03\x02"):
            outputstr+="\n\nTest Passed"
            test28=1
        else:
            outputstr+="\n\nTest Failed"
            test28=2

        test28len = len(output)

        t.insert(END,outputstr)
        color_test(test28)

    if cl.getstatus('CL8')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x04\x00\x64\x00\x01"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(29) Read Input Registers (FC 4)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[0:9]==(b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x04\x02"):
            outputstr+="\n\nTest Passed"
            test29=1
        else:
            outputstr+="\n\nTest Failed"
            test29=2

        test29len = len(output)

        t.insert(END,outputstr)
        color_test(test29)

    if cl.getstatus('CL9')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x05\x01\x00\xff\x00"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(30) Write Single Coil (FC 5)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:]==b"\x05\x01\x00\xff\x00":
            outputstr+="\n\nTest Passed"
            test30=1
        else:
            outputstr+="\n\nTest Failed"
            test30=2

        test30len = len(output)

        t.insert(END,outputstr)
        color_test(test30)

    if cl.getstatus('CL10')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x06\x01\x00\x00\x01"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(31) Write Single Register (FC 6)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:]==b"\x06\x01\x00\x00\x01":
            outputstr+="\n\nTest Passed"
            test31=1
        else:
            outputstr+="\n\nTest Failed"
            test31=2

        test31len = len(output)

        t.insert(END,outputstr)
        color_test(test31)

    if cl.getstatus('CL11')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x0f\x00\x64\x00\x02\x01\x66"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(32) Write Multiple Coils (FC 15)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:]==b"\x0f\x00\x64\x00\x02":
            outputstr+="\n\nTest Passed"
            test32=1
        else:
            outputstr+="\n\nTest Failed"
            test32=2

        test32len = len(output)

        t.insert(END,outputstr)
        color_test(test32)

    if cl.getstatus('CL12')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x0b" + unitId + b"\x10\x00\x64\x00\x02\x04\x3a\xbe\x5f\xc6"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(33) Write Multiple Registers (FC 16)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr
        
        if output[7:]==b"\x10\x00\x64\x00\x02":
            outputstr+="\n\nTest Passed"
            test33=1
        else:
            outputstr+="\n\nTest Failed"
            test33=2

        test33len = len(output)

        t.insert(END,outputstr)
        color_test(test33)

    if cl.getstatus('CL13')=='on':

        reqsRan+=1
    
        req = b"\x00\x00\x00\x00\x00\x0d" + unitId + b"\x17\x00\x64\x00\x01\x00\x64\x00\x01\x02\x2d\xd6"
        
        output, dataStr = modbusReq(req,sock)
        outputstr=""
        outputstr+="\n(34) Read/Write Multiple Registers (FC 23)\n\n"
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        outputstr+=dataStr

        if output[7:]==b"\x17\x02\x2d\xd6":
            outputstr+="\n\nTest Passed"
            test34=1
        else:
            outputstr+="\n\nTest Failed"
            test34=2

        test34len = len(output)

        t.insert(END,outputstr)
        color_test(test34)

    #Send a custom modbus request and get the response
    if cl.getstatus('CL14')=='on':

        reqsRan+=1
    
        #Prompt user for the frame starting with the function code, i.e. 0800150003 would be function code 8 (diagnostic), sub function code 21, and operation code 3
        frame = custom_ent.get()
        
        #Get the length of the frame string
        frameLen = int(len(frame))
        
        #Calculate the number of bytes in the frame
        lengthField = frameLen//2
        
        #Initialize the argument list
        argsList = []
        
        #The transaction id and protocol id are 0, length is the number of bytes in the inputted frame plus 1 for the unit id
        #and get the unit id that was given by user input at the beginning
        argsList.append("0, 0, " + str(lengthField + 1) + ", " + unitId_input.get() + ", ")
        
        #Loop through the frame, grabbing two characters at a time, convert them from hex to decimal, and add them to the argument list
        for x in range(0,int(frameLen)//2):
            
            if x==((frameLen//2)-1):
                argsList.append("int('0x' + frame[" + str(x*2) + ":" + str(x*2+2) + "], 16))")
            else:
                argsList.append("int('0x' + frame[" + str(x*2) + ":" + str(x*2+2) + "], 16), ")
        
        #> means big endian. H means word (two bytes), for the transaction id, protocol id, and length
        #B means bytes, and we take the length plus one for the unit id
        #The result is the 3H corresponds to the first three arguments, and the _B corresponds to the rest of the frame
        #to pack into a byte string
        packStr = '>3H ' + str(frameLen//2 + 1) + 'B'
        
        #Create the string to execute with argsList
        evalStr = "struct.pack(packStr, "
        
        for y in range(0, len(argsList)):
            
            evalStr = evalStr + argsList[y]
        
        #Execute the command struct.pack.... with all the arguments to create the request
        outputstr=""
        
        outputstr+="\n(35) Custom request\n\n"
        
        try:
            req = eval(evalStr)
        except SyntaxError:
            outputstr+="Invalid frame\n\n"
        
        outputstr+=" ".join('{:02X}'.format(n) for n in req) + "\n\n"
        
        #Send the request and get the response
        output, dataStr = modbusReq(req,sock)

        outputstr+=dataStr+"\n\n"

        t.insert(END,outputstr)

    if cl.getstatus('CL15') == 'on':

        input_file = open("input.txt",'r')
        input_lines = input_file.readlines()

        for line in input_lines:

            reqsRan += 1

            if line[-1] == '\n':
                customframe = line[:-1]
            else:
                customframe = line


            beginning = b'\x00\x00\x00\x00' + struct.pack('>H',(int(len(customframe)))//2 + 1) + struct.pack('B',int(unitId_input.get()))

            fullframe = beginning
            ind = 0
            while ind < len(customframe) - 1:

                addition = struct.pack('B',int(customframe[ind:ind+2],16))

                fullframe = fullframe + addition

                if ind+2 == len(customframe) or ind+1 == len(customframe):
                    break

                ind+=2


            outputstr = ""

            outputstr += "\n(36) Custom request\n"

            outputstr += " ".join('{:02X}'.format(n) for n in fullframe) + "\n\n"

            # Send the request and get the response
            output, dataStr = modbusReq(fullframe, sock)

            outputstr += dataStr + "\n\n"

            t.insert(END, outputstr)



        input_file.close()


    t.insert(END,"\n")
        
    #Print the appropriate test results
        
    if cl.getstatus('CL1.Item1')=='on':
        if test1==1:
            t.insert(END,"\nTest 1 Passed: Modbus Messaging Statistics (0x65)")
            color_test2(1)
        elif test1==2:
            t.insert(END,"\nTest 1 Failed: Modbus Messaging Statistics (0x65)")
            color_test2(2)
        elif test1==0:
            t.insert(END,"\nTest 1 didn't run: Modbus Messaging Statistics (0x65)\n")


        #43 = pass
        if test1len == 43:
            t.insert(END,"Test 1 length = "+str(test1len) + " (pass)\n")
        else:
            t.insert(END,"Test 1 length = "+str(test1len) + " (fail)\n")



    if cl.getstatus('CL1.Item2')=='on':
        if test2==1:
            t.insert(END,"Test 2 Passed: Modbus Messaging Statistics Connections (0x66)")
            color_test2(1)
        elif test2==2:
            t.insert(END,"Test 2 Failed: Modbus Messaging Statistics Connections (0x66)")
            color_test2(2)
        elif test2==0:
            t.insert(END,"Test 2 didn't run: Modbus Messaging Statistics Connections (0x66)\n")

        t.insert(END,"Test 2 length = " + str(test2len) + "\n")


    if cl.getstatus('CL1.Item3')=='on':
        if test3==1:
            t.insert(END,"Test 3 Passed: Reset Messaging Counters (0x67)")
            color_test2(1)
        elif test3==2:
            t.insert(END,"Test 3 Failed: Reset Messaging Counters (0x67)")
            color_test2(2)
        elif test3==0:
            t.insert(END,"Test 3 didn't run: Reset Messaging Counters (0x67)\n")

        #12 = pass
        if test3len == 12:
            t.insert(END,"Test 3 length = "+str(test3len) + " (pass)\n")
        else:
            t.insert(END,"Test 3 length = "+str(test3len) + " (fail)\n")

    if cl.getstatus('CL1.Item3_5')=='on':
        if test3_5==1:
            t.insert(END,"Test 3.5 Passed: Scanning Status")
            color_test2(1)
        elif test3_5==2:
            t.insert(END,"Test 3.5 Failed: Scanning Status")
            color_test2(2)
        elif test3_5==0:
            t.insert(END,"Test 3.5 didn't run: Scanning Status\n")

        
    if cl.getstatus('CL1.Item4')=='on':
        if test4==1:
            t.insert(END,"Test 4 Passed: DHCP Statistics (0x6D)")
            color_test2(1)
        elif test4==2:
            t.insert(END,"Test 4 Failed: DHCP Statistics (0x6D)")
            color_test2(2)
        elif test4==0:
            t.insert(END,"Test 4 didn't run: DHCP Statistics (0x6D)\n")

        t.insert(END,"Test 4 length = " + str(test4len) + "\n")


    if cl.getstatus('CL1.Item5')=='on':
        if test5==1:
            t.insert(END,"Test 5 Passed: SMTP Statistics (0x6E)")
            color_test2(1)
        elif test5==2:
            t.insert(END,"Test 5 Failed: SMTP Statistics (0x6E) (might not be implemented)")
            color_test2(2)
        elif test5==0:
            t.insert(END,"Test 5 didn't run: SMTP Statistics (0x6E)\n")

        t.insert(END,"Test 5 length = " + str(test5len) + "\n")

    if cl.getstatus('CL1.Item6')=='on':
        if test6==1:
            t.insert(END,"Test 6 Passed: NTP Statistics (0x6F)")
            color_test2(1)
        elif test6==2:
            t.insert(END,"Test 6 Failed: NTP Statistics (0x6F)")
            color_test2(2)
        elif test6==0:
            t.insert(END,"Test 6 didn't run: NTP Statistics (0x6F)\n")

        t.insert(END,"Test 6 length = " + str(test6len) + "\n")


    if cl.getstatus('CL1.Item7')=='on':
        if test7==1:
            t.insert(END,"Test 7 Passed: Firmware Version (0x70)")
            color_test2(1)
        elif test7==2:
            t.insert(END,"Test 7 Failed: Firmware Version (0x70)")
            color_test2(2)
        elif test7==0:
            t.insert(END,"Test 7 didn't run: Firmware Version (0x70)\n")

        # 19 = pass
        if test7len == 19:
            t.insert(END,"Test 7 length = " + str(test7len) + " (pass)\n")
        else:
            t.insert(END,"Test 7 length = " + str(test7len) + " (fail)\n")


    if cl.getstatus('CL1.Item8')=='on':
        if test8==1:
            t.insert(END,"Test 8 Passed: Get Basic Switch Info (0x71)")
            color_test2(1)
        elif test8==2:
            t.insert(END,"Test 8 Failed: Get Basic Switch Info (0x71)")
            color_test2(2)
        elif test8==0:
            t.insert(END,"Test 8 didn't run: Get Basic Switch Info (0x71)\n")

        # 52 = pass
        if test8len == 52:
            t.insert(END,"Test 8 length = " + str(test8len) + " (pass)\n")
        else:
            t.insert(END,"Test 8 length = " + str(test8len) + " (fail)\n")
            
    if cl.getstatus('CL1.Item9')=='on':
        if test9==1:
            t.insert(END,"Test 9 Passed: Get RSTP Port of Switch Info (0x72)")
            color_test2(1)
        elif test9==2:
            t.insert(END,"Test 9 Failed: Get RSTP Port of Switch Info (0x72)")
            color_test2(2)
        elif test9==0:
            t.insert(END,"Test 9 didn't run: Get RSTP Port of Switch Info (0x72)\n")

        t.insert(END,"Test 9 length = " + str(test9len) + "\n")


    if cl.getstatus('CL1.Item10')=='on':
        if test9_5==1:
            t.insert(END,"Test 9.5 Passed: Get Bandwidth")
            color_test2(1)
        elif test9_5==2:
            t.insert(END,"Test 9.5 Failed: Get Bandwidth")
            color_test2(2)
        elif test9_5==0:
            t.insert(END,"Test 9.5 didn't run: Get Bandwidth\n")

    if cl.getstatus('CL2.Item1')=='on':
        if test10==1:
            t.insert(END,"Test 10 Passed: Read Basic Network Diagnostics (1/0x100)")
            color_test2(1)
        elif test10==2:
            t.insert(END,"Test 10 Failed: Read Basic Network Diagnostics (1/0x100)")
            color_test2(2)
        elif test10==0:
            t.insert(END,"Test 10 didn't run: Read Basic Network Diagnostics (1/0x100)\n")

        # 95 = pass
        if test10len == 95:
            t.insert(END,"Test 10 length = " + str(test10len) + " (pass)\n")
        else:
            t.insert(END,"Test 10 length = " + str(test10len) + " (fail)\n")


    if cl.getstatus('CL2.Item2')=='on':
        if test11==1:
            t.insert(END,"Test 11 Passed: Read Port Diagnostic Data (1/0x200)")
            color_test2(1)
        elif test11==2:
            t.insert(END,"Test 11 Failed: Read Port Diagnostic Data (1/0x200)")
            color_test2(2)
        elif test11==0:
            t.insert(END,"Test 11 didn't run: Read Port Diagnostic Data (1/0x200)\n")

        t.insert(END,"Test 11 length = " + str(test11len) + "\n")


    if cl.getstatus('CL2.Item3')=='on':
        if test12==1:
            t.insert(END,"Test 12 Passed: Read Modbus TCP/Port 502 Diag Data (1/0x300)")
            color_test2(1)
        elif test12==2:
            t.insert(END,"Test 12 Failed: Read Modbus TCP/Port 502 Diag Data (1/0x300)")
            color_test2(2)
        elif test12==0:
            t.insert(END,"Test 12 didn't run: Read Modbus TCP/Port 502 Diag Data (1/0x300)\n")

        # 53 = pass
        if test12len == 53:
            t.insert(END,"Test 12 length = " + str(test12len) + " (pass)\n")
        else:
            t.insert(END,"Test 12 length = " + str(test12len) + " (fail)\n")


    if cl.getstatus('CL2.Item4')=='on':
        if test13==1:
            t.insert(END,"Test 13 Passed: Read Modbus TCP/Port Connection Data (1/0x400)")
            color_test2(1)
        elif test13==2:
            t.insert(END,"Test 13 Failed: Read Modbus TCP/Port Connection Data (1/0x400)")
            color_test2(2)
        elif test13==0:
            t.insert(END,"Test 13 didn't run: Read Modbus TCP/Port Connection Data (1/0x400)\n")

        t.insert(END,"Test 13 length = " + str(test13len) + "\n")


    if cl.getstatus('CL2.Item5')=='on':
        if test14==1:
            t.insert(END,"Test 14 Passed: Read Data Structures Offsets (1/0x7F00)")
            color_test2(1)
        elif test14==2:
            t.insert(END,"Test 14 Failed: Read Data Structures Offsets (1/0x7F00)")
            color_test2(2)
        elif test14==0:
            t.insert(END,"Test 14 didn't run: Read Data Structures Offsets (1/0x7F00)\n")

        # 35 = pass
        if test14len == 35:
            t.insert(END,"Test 14 length = " + str(test14len) + " (pass)\n")
        else:
            t.insert(END,"Test 14 length = " + str(test14len) + " (fail)\n")



    if cl.getstatus('CL2.Item55')=='on':
        if test55==1:
            t.insert(END,"Test 14.5 Passed: FDR Client Diagnostics Data")
            color_test2(1)
        elif test55==2:
            t.insert(END,"Test 14.5 Failed: FDR Client Diagnostics Data")
            color_test2(2)
        elif test55==0:
            t.insert(END,"Test 14.5 didn't run: FDR Client Diagnostics Data\n")





    if cl.getstatus('CL2.Item6')=='on':
        if test15==1:
            t.insert(END,"Test 15 Passed: Clear Diag data for Network (2/0x100)")
            color_test2(1)
        elif test15==2:
            t.insert(END,"Test 15 Failed: Clear Diag data for Network (2/0x100)")
            color_test2(2)
        elif test15==0:
            t.insert(END,"Test 15 didn't run: Clear Diag data for Network (2/0x100)\n")


        # 14 = pass
        if test15len == 14:
            t.insert(END,"Test 15 length = " + str(test15len) + " (pass)\n")
        else:
            t.insert(END,"Test 15 length = " + str(test15len) + " (fail)\n")


    if cl.getstatus('CL2.Item7')=='on':
        if test16==1:
            t.insert(END,"Test 16 Passed: Clear Diag data for Ethernet Port (2/0x200)")
            color_test2(1)
        elif test16==2:
            t.insert(END,"Test 16 Failed: Clear Diag data for Ethernet Port (2/0x200)")
            color_test2(2)
        elif test16==0:
            t.insert(END,"Test 16 didn't run: Clear Diag data for Ethernet Port (2/0x200)\n")

        # 14 = pass
        if test16len == 14:
            t.insert(END,"Test 16 length = " + str(test16len) + " (pass)\n")
        else:
            t.insert(END,"Test 16 length = " + str(test16len) + " (fail)\n")


    if cl.getstatus('CL2.Item8')=='on':
        if test17==1:
            t.insert(END,"Test 17 Passed: Clear Diag data for MB Port 502 (2/0x300)")
            color_test2(1)
        elif test17==2:
            t.insert(END,"Test 17 Failed: Clear Diag data for MB Port 502 (2/0x300)")
            color_test2(2)
        elif test17==0:
            t.insert(END,"Test 17 didn't run: Clear Diag data for MB Port 502 (2/0x300)\n")

        # 14 = pass
        if test17len == 14:
            t.insert(END,"Test 17 length = " + str(test17len) + " (pass)\n")
        else:
            t.insert(END,"Test 17 length = " + str(test17len) + " (fail)\n")



    if cl.getstatus('CL2.Item9')=='on':
        if test18==1:
            t.insert(END,"Test 18 Passed: Clear Diag data for Connection table (2/0x400)")
            color_test2(1)
        elif test18==2:
            t.insert(END,"Test 18 Failed: Clear Diag data for Connection table (2/0x400)")
            color_test2(2)
        elif test18==0:
            t.insert(END,"Test 18 didn't run: Clear Diag data for Connection table (2/0x400)\n")

        # 14 = pass
        if test18len == 14:
            t.insert(END,"Test 18 length = " + str(test18len) + " (pass)\n")
        else:
            t.insert(END,"Test 18 length = " + str(test18len) + " (fail)\n")


    if cl.getstatus('CL2.Item10')=='on':
        if test19==1:
            t.insert(END,"Test 19 Passed: Clear All Diagnostic Data (3/0)")
            color_test2(1)
        elif test19==2:
            t.insert(END,"Test 19 Failed: Clear All Diagnostic Data (3/0)")
            color_test2(2)
        elif test19==0:
            t.insert(END,"Test 19 didn't run: Clear All Diagnostic Data (3/0)\n")

        # 14 = pass
        if test19len == 14:
            t.insert(END,"Test 19 length = " + str(test19len) + " (pass)\n")
        else:
            t.insert(END,"Test 19 length = " + str(test19len) + " (fail)\n")


    if cl.getstatus('CL2.Item11')=='on':
        if test20==1:
            t.insert(END,"Test 20 Passed: List Ports (4/0)")
            color_test2(1)
        elif test20==2:
            t.insert(END,"Test 20 Failed: List Ports (4/0)")
            color_test2(2)
        elif test20==0:
            t.insert(END,"Test 20 didn't run: List Ports (4/0)\n")

        t.insert(END,"Test 20 length = " + str(test20len) + "\n")


    if cl.getstatus('CL3.Item1')=='on':
        if test21==1:
            t.insert(END,"Test 21 Passed: Read Basic Object Device ID (0E/1/0)")
            color_test2(1)
        elif test21==2:
            t.insert(END,"Test 21 Failed: Read Basic Object Device ID (0E/1/0)")
            color_test2(2)
        elif test21==0:
            t.insert(END,"Test 21 didn't run: Read Basic Object Device ID (0E/1/0)\n")

        t.insert(END,"Test 21 length = " + str(test21len) + "\n")

    if cl.getstatus('CL3.Item2')=='on':
        if test22==1:
            t.insert(END,"Test 22 Passed: Read Regular Object Device ID (0E/2/0)")
            color_test2(1)
        elif test22==2:
            t.insert(END,"Test 22 Failed: Read Regular Object Device ID (0E/2/0)")
            color_test2(2)
        elif test22==0:
            t.insert(END,"Test 22 didn't run: Read Regular Object Device ID (0E/2/0)\n")

        t.insert(END,"Test 22 length = " + str(test22len) + "\n")

    if cl.getstatus('CL3.Item3')=='on':
        if test23==1:
            t.insert(END,"Test 23 Passed: Read Extended Object Device ID (0E/3/0)")
            color_test2(1)
        elif test23==2:
            t.insert(END,"Test 23 Failed: Read Extended Object Device ID (0E/3/0)")
            color_test2(2)
        elif test23==0:
            t.insert(END,"Test 23 didn't run: Read Extended Object Device ID (0E/3/0)\n")

        t.insert(END,"Test 23 length = " + str(test23len) + "\n")

    if cl.getstatus('CL3.Item4')=='on':
        if test24==1:
            t.insert(END,"Test 24 Passed: Read Individual Object of Device ID (0E/4/0)")
            color_test2(1)
        elif test24==2:
            t.insert(END,"Test 24 Failed: Read Individual Object of Device ID (0E/4/0)")
            color_test2(2)
        elif test24==0:
            t.insert(END,"Test 24 didn't run: Read Individual Object of Device ID (0E/4/0)\n")

        t.insert(END,"Test 24 length = " + str(test24len) + "\n")

    if cl.getstatus('CL4')=='on':
        if test25==1:
            t.insert(END,"Test 25 Passed: Modbus Read Register Command FC 3 Unit Id 255")
            color_test2(1)
        elif test25==2:
            t.insert(END,"Test 25 Failed: Modbus Read Register Command FC 3 Unit Id 255")
            color_test2(2)
        elif test25==0:
            t.insert(END,"Test 25 didn't run: Modbus Read Register Command FC 3 Unit Id 255\n")

        t.insert(END,"Test 25 length = " + str(test25len) + "\n")

    if cl.getstatus('CL5')=='on':
        if test26==1:
            t.insert(END,"Test 26 Passed: Read Coils (FC 1)")
            color_test2(1)
        elif test26==2:
            t.insert(END,"Test 26 Failed: Read Coils (FC 1)")
            color_test2(2)
        elif test26==0:
            t.insert(END,"Test 26 didn't run: Read Coils (FC 1)\n")

        t.insert(END,"Test 26 length = " + str(test26len) + "\n")

    if cl.getstatus('CL6')=='on':
        if test27==1:
            t.insert(END,"Test 27 Passed: Read Inputs (FC 2)")
            color_test2(1)
        elif test27==2:
            t.insert(END,"Test 27 Failed: Read Inputs (FC 2)")
            color_test2(2)
        elif test27==0:
            t.insert(END,"Test 27 didn't run: Read Inputs (FC 2)\n")

        t.insert(END,"Test 27 length = " + str(test27len) + "\n")

    if cl.getstatus('CL7')=='on':
        if test28==1:
            t.insert(END,"Test 28 Passed: Read Holding Registers (FC 3)")
            color_test2(1)
        elif test28==2:
            t.insert(END,"Test 28 Failed: Read Holding Registers (FC 3)")
            color_test2(2)
        elif test28==0:
            t.insert(END,"Test 28 didn't run: Read Holding Registers (FC 3)\n")

        t.insert(END,"Test 28 length = " + str(test28len) + "\n")

    if cl.getstatus('CL8')=='on':
        if test29==1:
            t.insert(END,"Test 29 Passed: Read Input Registers (FC 4)")
            color_test2(1)
        elif test29==2:
            t.insert(END,"Test 29 Failed: Read Input Registers (FC 4)")
            color_test2(2)
        elif test29==0:
            t.insert(END,"Test 29 didn't run: Read Input Registers (FC 4)\n")

        t.insert(END,"Test 29 length = " + str(test29len) + "\n")

    if cl.getstatus('CL9')=='on':
        if test30==1:
            t.insert(END,"Test 30 Passed: Write Single Coil (FC 5)")
            color_test2(1)
        elif test30==2:
            t.insert(END,"Test 30 Failed: Write Single Coil (FC 5)")
            color_test2(2)
        elif test30==0:
            t.insert(END,"Test 30 didn't run: Write Single Coil (FC 5)\n")

        t.insert(END,"Test 30 length = " + str(test30len) + "\n")

    if cl.getstatus('CL10')=='on':
        if test31==1:
            t.insert(END,"Test 31 Passed: Write Single Register (FC 6)")
            color_test2(1)
        elif test31==2:
            t.insert(END,"Test 31 Failed: Write Single Register (FC 6)")
            color_test2(2)
        elif test31==0:
            t.insert(END,"Test 31 didn't run: Write Single Register (FC 6)\n")   

        t.insert(END,"Test 31 length = " + str(test31len) + "\n")

    if cl.getstatus('CL11')=='on':
        if test32==1:
            t.insert(END,"Test 32 Passed: Write Multiple Coils (FC 15)")
            color_test2(1)
        elif test32==2:
            t.insert(END,"Test 32 Failed: Write Multiple Coils (FC 15)")
            color_test2(2)
        elif test32==0:
            t.insert(END,"Test 32 didn't run: Write Multiple Coils (FC 15)\n")

        t.insert(END,"Test 32 length = " + str(test32len) + "\n")

    if cl.getstatus('CL12')=='on':
        if test33==1:
            t.insert(END,"Test 33 Passed: Write Multiple Registers (FC 16)")
            color_test2(1)
        elif test33==2:
            t.insert(END,"Test 33 Failed: Write Multiple Registers (FC 16)")
            color_test2(2)
        elif test33==0:
            t.insert(END,"Test 33 didn't run: Write Multiple Registers (FC 16)\n")

        t.insert(END,"Test 33 length = " + str(test33len) + "\n")

    if cl.getstatus('CL13')=='on':
        if test34==1:
            t.insert(END,"Test 34 Passed: Read/Write Multiple Registers (FC 23)")
            color_test2(1)
        elif test34==2:
            t.insert(END,"Test 34 Failed: Read/Write Multiple Registers (FC 23)")
            color_test2(2)
        elif test34==0:
            t.insert(END,"Test 34 didn't run: Read/Write Multiple Registers (FC 23)\n")

        t.insert(END,"Test 34 length = " + str(test34len) + "\n")

def change_dropdown(*args):
    print( ipChoice.get())
    print(TCP_IP.get())
	
#Initialize the GUI
root = tkinter.tix.Tk()
root.title("Modbus Tests")

#Create a font of size 10
s = ttk.Style()

myFont = font.Font(size=10)

s.configure('Test.TCheckbutton',font=myFont)

#Create the first scrollbar
yscrollbar = Scrollbar(root)
yscrollbar.grid(row=0, column=1, sticky=N+S)

#Create a canvas object and configure the scrollbar for it
canvas = Canvas(root, width=400,height=700,
                yscrollcommand=yscrollbar.set)

canvas.grid(row=0, column=0,sticky=NW)

yscrollbar.config(command=canvas.yview)

#Create a frame inside the canvas
frame = Frame(canvas)
frame.grid(row=0,column=0,sticky=NW)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

#Initialize checkbox variables
half_op = StringVar()
half2_op = StringVar()
first_op = StringVar()
second_op = StringVar()
third_op = StringVar()
fourth_op = StringVar()
fifth_op = StringVar()
sixth_op = StringVar()
seventh_op = StringVar()
eighth_op = StringVar()
ninth_op = StringVar()
tenth_op = StringVar()
eleventh_op = StringVar()
twelvth_op = StringVar()
thirteenth_op = StringVar()
fourteenth_op = StringVar()
fifteenth_op = StringVar()
sixteenth_op = StringVar()
seventeenth_op = StringVar()
eighteenth_op = StringVar()
nineteenth_op = StringVar()
twentieth_op = StringVar()
twentyfirst_op = StringVar()
twentysecond_op = StringVar()
twentythird_op = StringVar()
twentyfourth_op = StringVar()
twentyfifth_op = StringVar()
twentysixth_op = StringVar()
twentyseventh_op = StringVar()
twentyeighth_op = StringVar()
twentyninth_op = StringVar()
thirtieth_op = StringVar()
thirtyfirst_op = StringVar()
thirtysecond_op = StringVar()
thirtythird_op = StringVar()
thirtyfourth_op = StringVar()
thirtyfifth_op = StringVar()
thirtysixth_op = StringVar()



ttk.Button(frame, text="Toggle All", command=toggleAll).grid(column=0, row=0, sticky=NW)


cl = tkinter.tix.CheckList(frame, width=400,height=500)


cl.grid(column=0, row=1, sticky=NW)

cl.hlist.add("CL0", text="(0) Check/Uncheck All")
cl.hlist.add("CL1", text="(1) FC 8/21")
cl.hlist.add("CL1.Item1", text="Modbus Messaging Statistics (0x65)")
cl.hlist.add("CL1.Item1.3", text="Number local connects")
cl.hlist.add("CL1.Item2", text="Modbus Messaging Statistics Connections (0x66)")
cl.hlist.add("CL1.Item3", text="Reset Messaging Counters (0x67)")
cl.hlist.add("CL1.Item3_5", text="Scanning Status (0x68)")
cl.hlist.add("CL1.Item4", text="DHCP Statistics (0x6D)")
cl.hlist.add("CL1.Item5", text="SMTP Statistics (0x6E)")
cl.hlist.add("CL1.Item6", text="NTP Statistics (0x6F)")
cl.hlist.add("CL1.Item7", text="Firmware Version (0x70)")
cl.hlist.add("CL1.Item8", text="Get Basic Switch Info (0x71)")
cl.hlist.add("CL1.Item9", text="Get RSTP Port of Switch Info (0x72)")
cl.hlist.add("CL1.Item10", text="Get Bandwidth (0x75)")
cl.hlist.add("CL2", text="(2) FC 8/22")
cl.hlist.add("CL2.Item1", text="Read Basic Network Diagnostics (1/0x100)")
cl.hlist.add("CL2.Item2", text="Read Port Diagnostic Data (1/0x200)")
cl.hlist.add("CL2.Item3", text="Read Modbus TCP/Port 502 Diag Data (1/0x300)")
cl.hlist.add("CL2.Item4", text="Read Modbus TCP/Port Connection Data (1/0x400)")
cl.hlist.add("CL2.Item5", text="Read Data Structures Offsets (1/0x7F00)")
cl.hlist.add("CL2.Item55", text="FDR Client Diagnostics Data (1/0x8000)")
cl.hlist.add("CL2.Item6", text="Clear Diag data for Network (2/0x100)")
cl.hlist.add("CL2.Item7", text="Clear Diag data for Ethernet Port (2/0x200)")
cl.hlist.add("CL2.Item8", text="Clear Diag data for MB Port 502 (2/0x300)")
cl.hlist.add("CL2.Item9", text="Clear Diag data for Connection table (2/0x400)")
cl.hlist.add("CL2.Item10", text="Clear All Diagnostic Data (3/0)")
cl.hlist.add("CL2.Item11", text="List Ports (4/0)")
cl.hlist.add("CL3", text="(3) FC 2B")
cl.hlist.add("CL3.Item1", text="Read Basic Object Device ID (0E/1/0)")
cl.hlist.add("CL3.Item2", text="Read Regular Object Device ID (0E/2/0)")
cl.hlist.add("CL3.Item3", text="Read Extended Object Device ID (0E/3/0)")
cl.hlist.add("CL3.Item4", text="Read Individual Object of Device ID (0E/4/0)")
cl.hlist.add("CL4", text="(4) Modbus Read Register Command FC 3 Unit Id 255")
cl.hlist.add("CL5", text="(5) Read Coils (FC 1)")
cl.hlist.add("CL6", text="(6) Read Inputs (FC 2)")
cl.hlist.add("CL7", text="(7) Read Holding Registers (FC 3)")
cl.hlist.add("CL8", text="(8) Read Input Registers (FC 4)")
cl.hlist.add("CL9", text="(9) Write Single Coil (FC 5)")
cl.hlist.add("CL10", text="(10) Write Single Register (FC 6)")
cl.hlist.add("CL11", text="(11) Write Multiple Coils (FC 15)")
cl.hlist.add("CL12", text="(12) Write Multiple Registers (FC 16)")
cl.hlist.add("CL13", text="(13) Read/Write Multiple Registers (FC 23)")
cl.hlist.add("CL14", text="(14) Custom request")
cl.hlist.add("CL15", text="(15) From file")


cl.setstatus("CL0","off")
cl.setstatus("CL1","off")
cl.setstatus("CL1.Item1","off")
cl.setstatus("CL1.Item1.3","off")
cl.setstatus("CL1.Item2","off")
cl.setstatus("CL1.Item3","off")
cl.setstatus("CL1.Item3_5","off")
cl.setstatus("CL1.Item4","off")
cl.setstatus("CL1.Item5","off")
cl.setstatus("CL1.Item6","off")
cl.setstatus("CL1.Item7","off")
cl.setstatus("CL1.Item8","off")
cl.setstatus("CL1.Item9","off")
cl.setstatus("CL1.Item10","off")
cl.setstatus("CL2","off")
cl.setstatus("CL2.Item1","off")
cl.setstatus("CL2.Item2","off")
cl.setstatus("CL2.Item3","off")
cl.setstatus("CL2.Item4","off")
cl.setstatus("CL2.Item5","off")
cl.setstatus("CL2.Item55","off")
cl.setstatus("CL2.Item6","off")
cl.setstatus("CL2.Item7","off")
cl.setstatus("CL2.Item8","off")
cl.setstatus("CL2.Item9","off")
cl.setstatus("CL2.Item10","off")
cl.setstatus("CL2.Item11","off")
cl.setstatus("CL3","off")
cl.setstatus("CL3.Item1","off")
cl.setstatus("CL3.Item2","off")
cl.setstatus("CL3.Item3","off")
cl.setstatus("CL3.Item4","off")
cl.setstatus("CL4","off")
cl.setstatus("CL5","off")
cl.setstatus("CL6","off")
cl.setstatus("CL7","off")
cl.setstatus("CL8","off")
cl.setstatus("CL9","off")
cl.setstatus("CL10","off")
cl.setstatus("CL11","off")
cl.setstatus("CL12","off")
cl.setstatus("CL13","off")
cl.setstatus("CL14","off")
cl.setstatus("CL15","off")

#cl.setstatus("CL0.Item1", "off")

#cl.setmode("CL0",mode="open")

cl.autosetmode()


#def test(cl):

#    print cl.getstatus("CL1")




# #Create the checkboxes
# check05 = ttk.Checkbutton(frame, text='(0) Check/Uncheck All', style = 'Test.TCheckbutton', variable=half_op, onvalue='1', offvalue='0', command=toggleAll).grid(column=0, row=0, sticky=NW)
# check = ttk.Checkbutton(frame, text='(1) Modbus Messaging Statistics (8/21/0x65)', style = 'Test.TCheckbutton', variable=first_op, onvalue='1', offvalue='0').grid(column=0, row=1, sticky=(N, W))
# check2 = ttk.Checkbutton(frame, text='(2) Modbus Messaging Statistics Connections (8/21/0x66)', style = 'Test.TCheckbutton', variable=second_op, onvalue='1', offvalue='0').grid(column=0, row=2, sticky=NW)
# check3 = ttk.Checkbutton(frame, text='(3) Reset Messaging Counters (8/21/0x67)', style = 'Test.TCheckbutton', variable=third_op, onvalue='1', offvalue='0').grid(column=0, row=3, sticky=NW)
# check4 = ttk.Checkbutton(frame, text='(4) DHCP Statistics (8/21/0x6D)', style = 'Test.TCheckbutton', variable=fourth_op, onvalue='1', offvalue='0').grid(column=0, row=4, sticky=NW)
# check5 = ttk.Checkbutton(frame, text='(5) SMTP Statistics (8/21/0x6E)', style = 'Test.TCheckbutton', variable=fifth_op, onvalue='1', offvalue='0').grid(column=0, row=5, sticky=NW)
# check6 = ttk.Checkbutton(frame, text='(6) NTP Statistics (8/21/0x6F)', style = 'Test.TCheckbutton', variable=sixth_op, onvalue='1', offvalue='0').grid(column=0, row=6, sticky=NW)
# check7 = ttk.Checkbutton(frame, text='(7) Firmware Version (8/21/0x70)', style = 'Test.TCheckbutton', variable=seventh_op, onvalue='1', offvalue='0').grid(column=0, row=7, sticky=NW)
# check8 = ttk.Checkbutton(frame, text='(8) Get Basic Switch Info (8/21/0x71)', style = 'Test.TCheckbutton', variable=eighth_op, onvalue='1', offvalue='0').grid(column=0, row=8, sticky=NW)
# check9 = ttk.Checkbutton(frame, text='(9) Get RSTP Port of Switch Info (8/21/0x72)', style = 'Test.TCheckbutton', variable=ninth_op, onvalue='1', offvalue='0').grid(column=0, row=9, sticky=NW)
# check10 = ttk.Checkbutton(frame, text='(10) Read Basic Network Diagnostics (8/22/1/0x100)', style = 'Test.TCheckbutton', variable=tenth_op, onvalue='1', offvalue='0').grid(column=0, row=10, sticky=NW)
# check11 = ttk.Checkbutton(frame, text='(11) Read Port Diagnostic Data (8/22/1/0x200)', style = 'Test.TCheckbutton', variable=eleventh_op, onvalue='1', offvalue='0').grid(column=0, row=11, sticky=NW)
# check12 = ttk.Checkbutton(frame, text='(12) Read Modbus TCP/Port 502 Diag Data (8/22/1/0x300)', style = 'Test.TCheckbutton', variable=twelvth_op, onvalue='1', offvalue='0').grid(column=0, row=12, sticky=NW)
# check13 = ttk.Checkbutton(frame, text='(13) Read Modbus TCP/Port Connection Data (8/22/1/0x400)', style = 'Test.TCheckbutton', variable=thirteenth_op, onvalue='1', offvalue='0').grid(column=0, row=13, sticky=NW)
# check14 = ttk.Checkbutton(frame, text='(14) Read Data Structures Offsets (8/22/1/0x7F00)', style = 'Test.TCheckbutton', variable=fourteenth_op, onvalue='1', offvalue='0').grid(column=0, row=14, sticky=NW)
# check15 = ttk.Checkbutton(frame, text='(15) Clear Diag data for Network (8/22/2/0x100)', style = 'Test.TCheckbutton', variable=fifteenth_op, onvalue='1', offvalue='0').grid(column=0, row=15, sticky=NW)
# check16 = ttk.Checkbutton(frame, text='(16) Clear Diag data for Ethernet Port (8/22/2/0x200)', style = 'Test.TCheckbutton', variable=sixteenth_op, onvalue='1', offvalue='0').grid(column=0, row=16, sticky=NW)
# check17 = ttk.Checkbutton(frame, text='(17) Clear Diag data for MB Port 502 (8/22/2/0x300)', style = 'Test.TCheckbutton', variable=seventeenth_op, onvalue='1', offvalue='0').grid(column=0, row=17, sticky=NW)
# check18 = ttk.Checkbutton(frame, text='(18) Clear Diag data for Connection table (8/22/2/0x400)', style = 'Test.TCheckbutton', variable=eighteenth_op, onvalue='1', offvalue='0').grid(column=0, row=18, sticky=NW)
# check19 = ttk.Checkbutton(frame, text='(19) Clear All Diagnostic Data (8/22/3/0)', style = 'Test.TCheckbutton', variable=nineteenth_op, onvalue='1', offvalue='0').grid(column=0, row=19, sticky=NW)
# check20 = ttk.Checkbutton(frame, text='(20) List Ports (8/22/4/0)', style = 'Test.TCheckbutton', variable=twentieth_op, onvalue='1', offvalue='0').grid(column=0, row=20, sticky=NW)
# check21 = ttk.Checkbutton(frame, text='(21) Read Basic Object Device ID (2B/0E/1/0)', style = 'Test.TCheckbutton', variable=twentyfirst_op, onvalue='1', offvalue='0').grid(column=0, row=21, sticky=NW)
# check22 = ttk.Checkbutton(frame, text='(22) Read Regular Object Device ID (2B/0E/2/0)', style = 'Test.TCheckbutton', variable=twentysecond_op, onvalue='1', offvalue='0').grid(column=0, row=22, sticky=NW)
# check23 = ttk.Checkbutton(frame, text='(23) Read Extended Object Device ID (2B/0E/3/0)', style = 'Test.TCheckbutton', variable=twentythird_op, onvalue='1', offvalue='0').grid(column=0, row=23, sticky=NW)
# check24 = ttk.Checkbutton(frame, text='(24) Read Individual Object of Device ID (2B/0E/4/0)', style = 'Test.TCheckbutton', variable=twentyfourth_op, onvalue='1', offvalue='0').grid(column=0, row=24, sticky=NW)
# check25 = ttk.Checkbutton(frame, text='(25) Modbus Read Register Command FC 3 Unit Id 255', style = 'Test.TCheckbutton', variable=twentyfifth_op, onvalue='1', offvalue='0').grid(column=0, row=25, sticky=NW)
# check26 = ttk.Checkbutton(frame, text='(26) Read Coils (FC 1)', style = 'Test.TCheckbutton', variable=twentysixth_op, onvalue='1', offvalue='0').grid(column=0, row=26, sticky=NW)
# check27 = ttk.Checkbutton(frame, text='(27) Read Inputs (FC 2)', style = 'Test.TCheckbutton', variable=twentyseventh_op, onvalue='1', offvalue='0').grid(column=0, row=27, sticky=NW)
# check28 = ttk.Checkbutton(frame, text='(28) Read Holding Registers (FC 3)', style = 'Test.TCheckbutton', variable=twentyeighth_op, onvalue='1', offvalue='0').grid(column=0, row=28, sticky=NW)
# check29 = ttk.Checkbutton(frame, text='(29) Read Input Registers (FC 4)', style = 'Test.TCheckbutton', variable=twentyninth_op, onvalue='1', offvalue='0').grid(column=0, row=29, sticky=NW)
# check30 = ttk.Checkbutton(frame, text='(30) Write Single Coil (FC 5)', style = 'Test.TCheckbutton', variable=thirtieth_op, onvalue='1', offvalue='0').grid(column=0, row=30, sticky=NW)
# check31 = ttk.Checkbutton(frame, text='(31) Write Single Register (FC 6)', style = 'Test.TCheckbutton', variable=thirtyfirst_op, onvalue='1', offvalue='0').grid(column=0, row=31, sticky=NW)
# check32 = ttk.Checkbutton(frame, text='(32) Write Multiple Coils (FC 15)', style = 'Test.TCheckbutton', variable=thirtysecond_op, onvalue='1', offvalue='0').grid(column=0, row=32, sticky=NW)
# check33 = ttk.Checkbutton(frame, text='(33) Write Multiple Registers (FC 16)', style = 'Test.TCheckbutton', variable=thirtythird_op, onvalue='1', offvalue='0').grid(column=0, row=33, sticky=NW)
# check34 = ttk.Checkbutton(frame, text='(34) Read/Write Multiple Registers (FC 23)', style = 'Test.TCheckbutton', variable=thirtyfourth_op, onvalue='1', offvalue='0').grid(column=0, row=34, sticky=NW)
# #check35 = ttk.Checkbutton(frame, text='(35) Run all tests', style = 'Test.TCheckbutton', variable=thirtyfifth_op, onvalue='1', offvalue='0', command=toggleAll).grid(column=0, row=35, sticky=NW)
# check36 = ttk.Checkbutton(frame, text='(35) Custom request', style = 'Test.TCheckbutton', variable=thirtysixth_op, onvalue='1', offvalue='0').grid(column=0, row=35, sticky=NW)

t_status = Text(frame,width=7,height=1,wrap=WORD,font=myFont)
t_status.grid(column=0,row=2)
ttk.Label(frame, text="1-16").grid(column=0, row=2, padx=(120,1))

t_status2 = Text(frame,width=7,height=1,wrap=WORD,font=myFont)
t_status2.grid(column=0,row=3)
ttk.Label(frame, text="17-32").grid(column=0, row=3, padx=(125,1))

t_status3 = Text(frame,width=11,height=1,wrap=WORD,font=myFont)
t_status3.grid(column=0,row=4)
ttk.Label(frame, text="33-64").grid(column=0, row=4, padx=(135,1))

t_status4 = Text(frame,width=20,height=1,wrap=WORD,font=myFont)
t_status4.grid(column=0,row=5)
ttk.Label(frame, text="65-128").grid(column=0, row=5, padx=(200,1))

selections = StringVar()

if first_op.get() == '1':
    selections.set("1")

#Initialize all the entry variables
custom_ent = StringVar()

resp = StringVar()

unitId_input = StringVar()

TCP_IP = StringVar()

filename_ent=StringVar()

#Create the second scrollbar
yscrollbar2 = Scrollbar(root)
yscrollbar2.grid(row=0, column=3, sticky=N+S)

#Create a second canvas and attach the scrollbar to it
canvas2 = Canvas(root, width=400,height=700,
                yscrollcommand=yscrollbar2.set)

canvas2.grid(row=0, column=2, sticky=NE)

yscrollbar2.config(command=canvas2.yview)

#Create a frame inside the canvas
mainframe = Frame(canvas2, padx=0)
mainframe.grid(column=1,row=0, sticky=NE)

mainframe.rowconfigure(0, weight=1)
mainframe.columnconfigure(0, weight=1)

#Create a dropdown for IP address choice : IPv4, IPv6
ipChoice = StringVar()
ipChoices = {'IPv4', 'IPv6'}
ipChoice.set('IPv4') # Default choice
ipChoice.trace('w', change_dropdown)

dropDownMenu = OptionMenu(mainframe, ipChoice, *ipChoices)
dropDownMenu.grid(column=0, row=0, sticky=NW)

#Create the labels, entries, buttons, and textbox for the right side

ttk.Label(mainframe, text="IP: ").grid(column=0, row=0, sticky=NE)

ip_entry = ttk.Entry(mainframe, width=15, textvariable=TCP_IP)
ip_entry.grid(column=0, row=1, sticky=NE)

ttk.Label(mainframe, text="Unit ID: ").grid(column=0, row=2, sticky=NE)

unitId_entry = ttk.Entry(mainframe, width=15, textvariable=unitId_input)
unitId_entry.grid(column=0, row=3, sticky=NE)

ttk.Label(mainframe, text="Custom Frame: ").grid(column=0, row=4, sticky=NE)

custom_entry = ttk.Entry(mainframe, width=15, textvariable=custom_ent)
custom_entry.grid(column=0, row=5, sticky=NE)

yscrollbar3=Scrollbar(mainframe)
yscrollbar3.grid(column=1,row=7,sticky=NS)

t = Text(mainframe,width=40,height=20,yscrollcommand=yscrollbar3.set,wrap=WORD,font=myFont)
t.grid(column=0,row=7,sticky=NE)

yscrollbar3.config(command=t.yview)

ttk.Button(mainframe, text="Send Modbus Request", command=sendModbus).grid(column=0, row=6, sticky=NE)

ttk.Label(mainframe, text="Loop count").grid(column=0, row=1, sticky=NW)

loop_count_ent = StringVar()
loop_count_entry = ttk.Entry(mainframe, width=10, textvariable=loop_count_ent)
loop_count_entry.grid(column=0, row=2, sticky=NW)

ttk.Label(mainframe, text="Delay(ms):").grid(column=0, row=3, sticky=NW)

loop_ent = StringVar()
loopStop = StringVar()
loop_entry = ttk.Entry(mainframe, width=10, textvariable=loop_ent)
loop_entry.grid(column=0, row=4, sticky=NW)

ttk.Button(mainframe, text="Run in loop", command=runLoop).grid(column=0, row=5, sticky=NW)

ttk.Button(mainframe, text="Stop loop", command=stopLoop).grid(column=0, row=6, sticky=NW)


ttk.Label(mainframe, text="Certificate path: ").grid(column=0, row=1, sticky=N)

cert_ent = StringVar()
cert_entry = ttk.Entry(mainframe, width=10, textvariable=cert_ent)
cert_entry.grid(column=0, row=2, sticky=N)

ttk.Label(mainframe, text="Host name: ").grid(column=0, row=3, sticky=N)

host_ent = StringVar()
host_entry = ttk.Entry(mainframe, width=10, textvariable=host_ent)
host_entry.grid(column=0, row=4, sticky=N)

ssl_op = StringVar()
ssl_op.set('0')
check_ssl = ttk.Checkbutton(mainframe, text='SSL', style = 'Test.TCheckbutton', variable=ssl_op, onvalue='1', offvalue='0').grid(column=0, row=0, sticky=(N))



ttk.Button(mainframe, text="Add Compares", command=addCompares).grid(column=0, row=5, sticky=N)

ttk.Button(mainframe, text="Clear", command=clearText).grid(column=0, row=8, sticky=NW)

ttk.Label(mainframe, text="# of sessions").grid(column=0, row=9, sticky=NW)

sessions_ent = StringVar()
sessions_entry = ttk.Entry(mainframe, width=10, textvariable=sessions_ent)
sessions_entry.grid(column=0, row=10, sticky=NW)

ttk.Button(mainframe, text="Run sessions", command=mult_sessions).grid(column=0, row=11, sticky=NW)





closeopen_op = StringVar()
closeopen_op.set('0')
check_closeopen = ttk.Checkbutton(mainframe, text='Close/Open', style = 'Test.TCheckbutton', variable=closeopen_op, onvalue='1', offvalue='0').grid(column=0, row=12, sticky=(N, W))



comparefile_op = StringVar()
comparefile_op.set('0')
check_compare = ttk.Checkbutton(mainframe, text='Compare to file(s)', style = 'Test.TCheckbutton', variable=comparefile_op, onvalue='1', offvalue='0').grid(column=0, row=13, sticky=(N, W))

compare_ent = StringVar()
compare_entry = ttk.Entry(mainframe, width=15, textvariable=compare_ent)
compare_entry.grid(column=0, row=14, sticky=NW)
compare_ent2 = StringVar()
compare_ent3 = StringVar()
compare_ent4 = StringVar()
compare_ent5 = StringVar()
compare_entry2 = ttk.Entry(mainframe, width=15, textvariable=compare_ent2)
compare_entry2.grid(column=0, row=15, sticky=NW)
compare_entry3 = ttk.Entry(mainframe, width=15, textvariable=compare_ent3)
compare_entry3.grid(column=0, row=16, sticky=NW)
compare_entry4 = ttk.Entry(mainframe, width=15, textvariable=compare_ent4)
compare_entry4.grid(column=0, row=17, sticky=NW)
compare_entry5 = ttk.Entry(mainframe, width=15, textvariable=compare_ent5)
compare_entry5.grid(column=0, row=18, sticky=NW)

ttk.Button(mainframe, text="Run and compare", command=runAndCompare).grid(column=0, row=19, sticky=NW)

ttk.Label(mainframe, text="Timeout: ").grid(column=0, row=8, sticky=N)

timeout_ent = StringVar()
timeout_entry = ttk.Entry(mainframe, width=15, textvariable=timeout_ent)
timeout_entry.grid(column=0, row=9, sticky=N)


ttk.Label(mainframe, text="Filename: ").grid(column=0, row=8, sticky=NE)

filename_entry = ttk.Entry(mainframe, width=15, textvariable=filename_ent)
filename_entry.grid(column=0, row=9, sticky=NE)

ttk.Button(mainframe, text="Save output to file", command=saveToFile).grid(column=0, row=10, sticky=NE)

filename2_entry=StringVar()

ttk.Label(mainframe, text="Filename: ").grid(column=0, row=11, sticky=NE)

filename_entry = ttk.Entry(mainframe, width=15, textvariable=filename2_entry)
filename_entry.grid(column=0, row=12, sticky=NE)

ttk.Button(mainframe, text="Run test from file", command=runFromFile).grid(column=0, row=13, sticky=NE)

ttk.Button(mainframe, text="Run in loop", command=runFileLoop).grid(column=0, row=14, sticky=NE)

frame3 = Frame(root)
frame3.grid(row=0,column=4)

ttk.Label(frame3, text="Filename: ").grid(column=0, row=0, sticky=NE)

filename3_entry = StringVar()

filename3_entry_obj = ttk.Entry(frame3, width=15, textvariable=filename3_entry)
filename3_entry_obj.grid(column=0, row=1, sticky=NE)

ttk.Button(frame3, text="Diff output with file", command=diff_outputs).grid(column=0, row=2, sticky=NE)

yscrollbar4=Scrollbar(frame3)
yscrollbar4.grid(column=1,row=3,sticky=NS)

t2 = Text(frame3,width=30,height=20,yscrollcommand=yscrollbar4.set,wrap=WORD,font=myFont)
t2.grid(column=0,row=3,sticky=NE)

yscrollbar4.config(command=t2.yview)

ttk.Button(frame3, text="Clear", command=clearText2).grid(column=0, row=4, sticky=NW)


ttk.Label(frame3, text="Filename: ").grid(column=0, row=4, sticky=NE)

filenamediff_ent = StringVar()

filenamediff_entry = ttk.Entry(frame3, width=15, textvariable=filenamediff_ent)
filenamediff_entry.grid(column=0, row=5, sticky=NE)

ttk.Button(frame3, text="Save diff to file", command=saveToFile2).grid(column=0, row=6, sticky=NE)


resp.set("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

#Create windows with the frames inside the canvases
canvas.create_window(0,0,anchor=NW,window=frame)

frame.update_idletasks()

canvas.config(scrollregion=canvas.bbox("all"))

canvas2.create_window(0,0,anchor=NE,window=mainframe)
mainframe.update_idletasks()

canvas2.config(scrollregion=canvas2.bbox("all"))

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

#Run the GUI
root.mainloop()

