#!/usr/bin/env python

import socket, struct, time, difflib, os, threading, datetime, ssl
from tkinter import *
#from Tkinter import ttk
from tkinter import ttk
#from Tkinter import font
#import tkFont
from tkinter import font
import tkinter.tix
#from time import time
# import enip
# from enip import Connection, ConnectionConfig, Scanner, ScannerEventHandler
# from enip import Assembly, Direction, Scanner, ScannerEventHandler
# from enip import CipObject, EthernetLinkObject, Service, ConnectionType



TCP_PORT = 44818



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

# Make the response bold
def bold_response():

    #Get the number of lines by looking at the last character in the text box
    numlines = int(t.index('end').split('.')[0])-2

    #tfont = tkFont(t['font'])
    #tfont2 = TkDefaultFont
    #tfont.config(weight='bold')
    #t['font'] = tfont
    
    #Add a tag to "Test Failed"
    t.tag_add("bold",str(numlines)+'.0',str(numlines)+'.23')
    
    #Configure the tag to make the text red
    t.tag_config("bold",font="Helvetica 10 bold")
        
    #Add a newline character
    #outputstr='\n'
    
    #Insert the newline to the end of the text box
    #t.insert(END,outputstr)
    

#Stops a loop
def stopLoop():
    loopStop.set('1')


#Send a CIP request in a loop
def runLoop():

    compares=0
    passes=0
    fails=0

    global responsefile
    responsefile = open("response_times.txt","w")

    loopStop.set('0')
    
    loop_count = loop_count_ent.get()

    #t.insert(END,"\nRunning...Press ctrl+C on the command line to stop\n")
    
    if loop_count_ent.get() == "":
        loop_count = 2
    else:
        loop_count = int(loop_count)
    
    x=0
    while x < loop_count:
        
        root.update()
        #time.sleep(1.5)
                
        if loopStop.get() == '1':
            break
        
        #if x==0:
         #   numlines = int(t.index('end').split('.')[0])-1
         #   t.delete(str(numlines-1)+'.0',str(numlines)+'.0')
        
        if loopStop.get() == '0':

            t.insert(END,"\nIteration #"+str(x+1)+"\n")
        
            sendCIP()
            
            loop_delay = loop_ent.get()
            
            if loop_delay == "":
                loop_delay = 0
            
            time.sleep(float(loop_delay) * 0.001)
        
        if loop_count_ent.get() == "":
            x=1
        else:
            x+=1

    doResponses()
            

#Calculate and output the response time min, max, and avg
def doResponses():

    global responsetimes
    global responsefile
    
    for x in range(0,len(responsetimes)):
        
        if x==0:
            min=float(responsetimes[x])
            max=float(responsetimes[x])
            avg=float(responsetimes[x])
            total = float(responsetimes[x])
        else:
            if float(responsetimes[x]) < min:
                min = float(responsetimes[x])
            if float(responsetimes[x]) > max:
                max = float(responsetimes[x])
            total+=float(responsetimes[x])
            avg= total / (x+1)
            
    if len(responsetimes) > 0:
    
        t.insert(END,"Response time min = " + str(min) + "\n")
        t.insert(END,"Response time max = " + str(max) + "\n")
        t.insert(END,"Response time avg = " + str(avg) + "\n")
        responsefile.write("Response time min = " + str(min) + "\n")
        responsefile.write("Response time max = " + str(max) + "\n")
        responsefile.write("Response time avg = " + str(avg) + "\n")
            
            
    responsefile.close()
            

#Run from a file in a loop
def runFileLoop():


    compares=0
    passes=0
    fails=0


    global responsefile
    responsefile = open("response_times.txt","w")

    loopStop.set('0')
    
    loop_count = loop_count_ent.get()

    
    #t.insert(END,"\nRunning...Press ctrl+C on the command line to stop\n")
    
    if loop_count_ent.get() == "":
        loop_count = 2
    else:
        loop_count = int(loop_count)
    
    x=0
    while x < loop_count:
        
        root.update()
        #time.sleep(1.5)
        
        if loopStop.get() == '1':
            break
        
       # if x==0:
       #     numlines = int(t.index('end').split('.')[0])-1
       #     t.delete(str(numlines-1)+'.0',str(numlines)+'.0')
        
        if loopStop.get() == '0':

            t.insert(END,"\nIteration #"+str(x+1)+"\n")
        
            runFromFile()
            
            loop_delay = loop_ent.get()
            
            if loop_delay == "":
                loop_delay = 0
            
            time.sleep(float(loop_delay) * 0.001)
        
        if loop_count_ent.get() == "":
            x=1
        else:
            x+=1
    
    doResponses()
    
    
#Removes an attribute from a diff if it is unchecked
def removeUnchecked(diff_lines):

    x = 0
    #for x in range(0,len(diff_lines)):
    while x < len(diff_lines):
    
        if diff_lines[x][1:42] == "Attr 2: Max EIP TCP Connections opened = ":
            if cl.getstatus("CL4.8") == "off":
                del diff_lines[x-1]
                del diff_lines[x-1]
                del diff_lines[x-1]
                x-=1
            else:
                x+=1
        else:
            x+=1
    
    return diff_lines
    
#Function to compare what is in the output text box to a results file
def diff_outputs():

    #Open what is in the filename entry for reading
    with open(filename3_entry.get(),'r') as f3:
    
        #Get the entire contents of the text box (from row 1, column 0 to the end) and put it in a variable called "output"
        output = t.get("1.0",END)
        
        #Remove the file "diff_temp" if it exists
        #try:
        #    os.remove('diff_temp')
        #except WindowsError:
        #    pass
            
        #Delay for 1 second and create a blank file called "diff_temp"
        #time.sleep(1)
        #f5=open('diff_temp','a')
        #f5.close()
        
        #Open diff_temp for reading and writing, write the textbox output to it, and put the lines in a list
        #with open('diff_temp','r+') as f4:
        #    f4.write(output)
        #    f4.seek(0)
        #    output_lines = f4.readlines()
        output_lines = output.splitlines(1)
        #Put the lines of the file in a list
        #output_lines = output.strip().splitlines()
        file_lines = f3.readlines()
        
        #Diff the file and the output
        diff = difflib.unified_diff(output_lines,file_lines,fromfile='output',tofile='file',n=0)


        #Remove diff_temp2 if it exists
        #try:
        #    os.remove('diff_temp2')
        #except WindowsError:
        #    pass
        
        #Create a blank diff_temp2
        #time.sleep(1)
        #f6=open('diff_temp2','a')
        #f6.close()
        
        #Put the diff in diff_temp2 and put the lines in the variable diff_lines
        #with open('diff_temp2','r+') as f7:
        #    for line in diff:
        #        f7.write(line)
        #    f7.seek(0)
         #   diff_lines = f7.readlines()
        
        diff_lines = []
        for line in diff:
            diff_lines.append(line)
        

        diff_lines = removeUnchecked(diff_lines)
            
        
        diff_lines2 = diff_lines

        #Insert the diff into the textbox
        for line in diff_lines2:
            
            #if not (line.startswith('---') or line.startswith('+++') or line.startswith('@@')):
            t2.insert(END,line)

        for z in range(3,len(diff_lines)):
            
            if diff_lines[z][0] == '+':
                break
            
        if z==4:
            
            #Make the differences in the diff red
            #i corresponds to the line number
            #j iterates from 0,1,2 after the third line and we do our calculations when it is 1
            #k is the element in the line
            #i=0
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
            
            
runAndCompare_var = 0


#Run from file and do a compare
def runAndCompare():

    compares=0
    passes=0
    fails=0

    global responsefile 
    responsefile = open("response_times.txt","w")

    global runAndCompare_var
    runAndCompare_var = 1
    comparefile_op.set('1')
    runFromFile()
    runAndCompare_var = 0
    
    responsefile.close()

            
            
reqsRan = 0
reqsRead = 0
testnum=0
#Execute tests that are in a previous output file
def runFromFile():
    global testnum
    global reqsRan
    global reqsRead
    global runAndCompare_var
    
    
    individual=0
    sessions=0
    reqsRan = 0
    reqsRead = 0
    

    file_contents = []
   
    if runAndCompare_var == 0:

        opened_file = open(filename2_entry.get(),"r")
        file_contents.append(opened_file.readlines())
        
    elif runAndCompare_var == 1:
        
        if compare_ent.get()[-4:] == '.ini':
            
            fcompareini = open(compare_ent.get(),'r')
            files = fcompareini.read().split(",")
            ftest_contents = []
            for file in files:
                opened_file = open(file,'r')
                file_contents.append(opened_file.readlines() )
        else:
        
            if compare_ent.get() != '':
                ftest = open(compare_ent.get(),"r")
                file_contents.append(ftest.readlines())
            if compare_ent2.get() != '':
                ftest2 = open(compare_ent2.get(),'r')
                file_contents.append(ftest2.readlines())
            if compare_ent3.get() != '':
                ftest3 = open(compare_ent3.get(),'r')
                file_contents.append(ftest3.readlines())
            if compare_ent4.get() != '':
                ftest4 = open(compare_ent4.get(),'r')
                file_contents.append(ftest4.readlines())
            if compare_ent5.get() != '':
                ftest5 = open(compare_ent5.get(),'r')
                file_contents.append(ftest5.readlines())
    
        
    reached_end=0
    cl.setstatus("CL0", "off")
    toggleAll()


    for x in range(0,len(file_contents)):
        for y in range(0,len(file_contents[x])):
            line = file_contents[x][y]
            
            
            if line[0]=='(':
                reqsRead +=1
            
            
            if line[0]=='(' and sessions == 0 and reqsRead > reqsRan:
                
                
                #reqsRead +=1
                
                individual=1
                
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
                    cl.setstatus('CL1','on')
                elif num=='2':
                    cl.setstatus('CL2','on')
                elif num=='3':
                    cl.setstatus('CL3','on')
                elif num=='4':
                    cl.setstatus('CL4','on')
                elif num=='5':
                    cl.setstatus('CL5','on')
                elif num=='6':
                    cl.setstatus('CL6','on')
                elif num=='7':
                    cl.setstatus('CL7','on')
                elif num=='8':
                    cl.setstatus('CL8','on')
                elif num=='9':
                    cl.setstatus('CL9','on')
                elif num=='10':
                    cl.setstatus('CL10','on')
                elif num=='11':
                    cl.setstatus('CL11','on')
                elif num=='12':
                    cl.setstatus('CL12','on')
                elif num=='13':
                    cl.setstatus('CL13','on')
                elif num=='14':
                    cl.setstatus('CL14','on')
                elif num=='15':
                    cl.setstatus('CL15','on')
                elif num=='16':
                    cl.setstatus('CL16','on')
                elif num=='17':
                    cl.setstatus('CL17','on')
                elif num=='18':
                    cl.setstatus('CL18','on')
                elif num=='19':
                    cl.setstatus('CL19','on')
                elif num=='20':
                    cl.setstatus('CL20','on')
                elif num=='21':
                    cl.setstatus('CL21','on')
                elif num=='22':
                    cl.setstatus('CL22','on')
                    reached_end=1

                    requ = file_contents[file_contents.index(line)+9]
                    
                    testlist = requ[1:].split(" ")

                    outputstring=""
                    
                    ele_service=testlist[40]
                    
                    ele_class_1 =testlist[45]
                    ele_class_1=ele_class_1[2:]
                    ele_class_2=testlist[44]
                    ele_class_2=ele_class_2[2:]

                    ele_instance=testlist[47]
                    ele_attribute=testlist[49]
                    
                    if len(ele_service)==3:      
                        ele_service=ele_service[0:2]+'0'+ele_service[2]
                    if len(ele_class_1)==1:      
                        ele_class_1='0'+ele_class_1[0]
                    if len(ele_class_2)==1:      
                        ele_class_2='0'+ele_class_2[0]
                    if len(ele_instance)==3:      
                        ele_instance=ele_instance[0:2]+'0'+ele_instance[2]
                    if len(ele_attribute)==4:      
                        ele_attribute=ele_attribute[0:2]+'0'+ele_attribute[2]
                    
                    ele_service=ele_service[2:]
                    ele_class=ele_class_1+ele_class_2
                    ele_instance=ele_instance[2:]
                    ele_attribute=ele_attribute[2:]
                    
                    service_ent.set(ele_service)
                    class_ent.set(ele_class)
                    instance_ent.set(ele_instance)
                    attribute_ent.set(ele_attribute)
                    
                    sendCIP()
                    #half_op.set('0')
                    #toggleAll()
                    
                    individual = 0
                    
            elif line[0:4] == 'Test' and (line[0:6] != 'Test P' and line[0:6] != 'Test F') and reached_end==0 and sessions == 0:
                
                reached_end=1
                sendCIP()
                #half_op.set('0')
                #toggleAll()
                individual = 0
                
            elif individual == 0 and line[0] == "O":
            
                reqsRead = 0
                reqsRan = 0
            
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
                    
                closeopen_op.set(num)
                
                d+=8
                num=''
                selectionsstr=line[d:]
                selections=selectionsstr.split(",")
                
                for num in selections:
                    
                    if num=='1':
                        cl.setstatus('CL1','on')
                    elif num=='2':
                        cl.setstatus('CL2','on')
                    elif num=='3':
                        cl.setstatus('CL3','on')
                    elif num=='4':
                        cl.setstatus('CL4','on')
                    elif num=='5':
                        cl.setstatus('CL5','on')
                    elif num=='6':
                        cl.setstatus('CL6','on')
                    elif num=='7':
                        cl.setstatus('CL7','on')
                    elif num=='8':
                        cl.setstatus('CL8','on')
                    elif num=='9':
                        cl.setstatus('CL9','on')
                    elif num=='10':
                        cl.setstatus('CL10','on')
                    elif num=='11':
                        cl.setstatus('CL11','on')
                    elif num=='12':
                        cl.setstatus('CL12','on')
                    elif num=='13':
                        cl.setstatus('CL13','on')
                    elif num=='14':
                        cl.setstatus('CL14','on')
                    elif num=='15':
                        cl.setstatus('CL15','on')
                    elif num=='16':
                        cl.setstatus('CL16','on')
                    elif num=='17':
                        cl.setstatus('CL17','on')
                    elif num=='18':
                        cl.setstatus('CL18','on')
                    elif num=='19':
                        cl.setstatus('CL19','on')
                    elif num=='20':
                        cl.setstatus('CL20','on')
                    elif num=='21':
                        cl.setstatus('CL21','on')

                mult_sessions()
                #half_op.set('0')
                #toggleAll()
                
            elif line[0:16] == 'Closing sessions':
                sessions = 0
            
#Function to save the contents of the textbox to a file
def saveToFile():

    f = open(filename_ent.get(), "w")
    f.write(t.get("1.0", END))
    f.close()


    #with open(filename_ent.get(), "w") as f:
        
        #f.write(t.get("1.0",END))

        
def saveToFile2():

    f = open(filenamediff_ent.get(), "w")
    f.write(t2.get("1.0", END))
    f.close()

    #with open(filenamediff_ent.get(), "w") as f:
        
        #f.write(t2.get("1.0",END))
        
#Clear the text in a textbox
def clearText():

    t.delete(1.0,END)
        
def clearText2():

    t2.delete(1.0,END)

    

#Read the message router object and select the checkboxes based on what we read in the response
def MR():


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    timeout = timeout_ent.get()

    if timeout == '':
        sock.settimeout(2.0)
    else:
        sock.settimeout(float(timeout))

    if ssl_op.get() == '1':

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

        sock.connect((TCP_IP.get(), 2221))
    else:

        sock.connect((TCP_IP.get(), TCP_PORT))

    outputstr=""
    sess_hand=b'\x00\x00\x00\x00'
    send_con = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    reg_sess,outputstr = EIP_Reg_Session(sock,outputstr,sess_hand,send_con)

    service_req = b'\x01'
    class_req = b'\x02'
    instance_req = b'\x01'
    
    outputstr=''
    
    outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, b'\x00')
    
    sock.close()
    
    if cip_res[42] == b'\x00':

        x=0
        
        objs = []
        
        while x < len(cip_res[44:]):
    
            objs.append(struct.unpack("<H",cip_res[x+44:x+46])[0])
            x+=2
            

        for z in range(0,len(objs)):
            
            objs[z] = hex(objs[z])
        
        
        for y in objs:
        
            if y == '0x1':
                cl.setstatus('CL15','on')
            elif y == '0x2':
                cl.setstatus('CL16','on')
            elif y == '0x6':
                cl.setstatus('CL17','on')
            elif y == '0x48':
                cl.setstatus('CL18','on')
            elif y == '0xf4':
                cl.setstatus('CL19','on')
            elif y == '0xf5':
                cl.setstatus('CL20','on')
            elif y == '0xf6':
                cl.setstatus('CL21','on')
            elif y == '0x300':
                cl.setstatus('CL1','on')
            elif y == '0x301':
                cl.setstatus('CL2','on')
            elif y == '0x302':
                cl.setstatus('CL3','on')
            elif y == '0x350':
                cl.setstatus('CL4','on')
            elif y == '0x351':
                cl.setstatus('CL5','on')
            elif y == '0x352':
                cl.setstatus('CL6','on')
            elif y == '0x353':
                cl.setstatus('CL7','on')
            elif y == '0x354':
                cl.setstatus('CL8','on')
            elif y == '0x355':
                cl.setstatus('CL9','on')
            elif y == '0x400':
                cl.setstatus('CL10','on')
            elif y == '0x402':
                cl.setstatus('CL11','on')
            elif y == '0x403':
                cl.setstatus('CL12','on')
            elif y == '0x404':
                cl.setstatus('CL13','on')
            elif y == '0x405':
                cl.setstatus('CL14','on')
                

        t.insert(END,objs)
        t.insert(END,'\n')
            
            

    
    
    
#Function to toggle all the checkboxes
def toggleAll():

    if cl.getstatus('CL0')=='on':
        cl.setstatus('CL1','on')
        cl.setstatus('CL2','on')
        cl.setstatus('CL3','on')
        cl.setstatus('CL4','on')
        cl.setstatus('CL5','on')
        cl.setstatus('CL6','on')
        cl.setstatus('CL7','on')
        cl.setstatus('CL8','on')
        cl.setstatus('CL9','on')
        cl.setstatus('CL10','on')
        cl.setstatus('CL11','on')
        cl.setstatus('CL12','on')
        cl.setstatus('CL13','on')
        cl.setstatus('CL14','on')
        cl.setstatus('CL15','on')
        cl.setstatus('CL16','on')
        cl.setstatus('CL17','on')
        cl.setstatus('CL18','on')
        cl.setstatus('CL19','on')
        cl.setstatus('CL20','on')
        cl.setstatus('CL21','on')
        

    if cl.getstatus('CL0')=='off':
        cl.setstatus('CL1','off')
        cl.setstatus('CL2','off')
        cl.setstatus('CL3','off')
        cl.setstatus('CL4','off')
        cl.setstatus('CL5','off')
        cl.setstatus('CL6','off')
        cl.setstatus('CL7','off')
        cl.setstatus('CL8','off')
        cl.setstatus('CL9','off')
        cl.setstatus('CL10','off')
        cl.setstatus('CL11','off')
        cl.setstatus('CL12','off')
        cl.setstatus('CL13','off')
        cl.setstatus('CL14','off')
        cl.setstatus('CL15','off')
        cl.setstatus('CL16','off')
        cl.setstatus('CL17','off')
        cl.setstatus('CL18','off')
        cl.setstatus('CL19','off')
        cl.setstatus('CL20','off')
        cl.setstatus('CL21','off')

#Function to send an EIP Register Session packet
def EIP_Reg_Session(s,outputstr,sess_hand,send_con):


    # ENIP Register Session Packet

    #Encapsulation Header
    EIP_COMMAND_REG_SESSION = b'\x65\x00'
    EIP_LENGTH_1 = b'\x04\x00'
    EIP_SESSION_HANDLE_1 = sess_hand#b'\x00\x00\x00\x00'
    EIP_SUCCESS_1 = b'\x00\x00\x00\x00'
    EIP_SENDER_CONTEXT_1 = send_con#b'\x00\x00\x00\x00\x00\x00\x00\x00'
    EIP_OPTIONS_1 = b'\x00\x00\x00\x00'
    EIP_ENCAP_HEADER_1 = EIP_COMMAND_REG_SESSION + EIP_LENGTH_1 + EIP_SESSION_HANDLE_1 + EIP_SUCCESS_1 + EIP_SENDER_CONTEXT_1 + EIP_OPTIONS_1

    #Command Specific Data
    EIP_PROTOCOL_VER = b'\x01\x00'
    EIP_OPTION_FLAGS = b'\x00\x00'
    EIP_COMMAND_SPEC_DATA_1 = EIP_PROTOCOL_VER + EIP_OPTION_FLAGS

    REG_SESSION_FRAME = EIP_ENCAP_HEADER_1 + EIP_COMMAND_SPEC_DATA_1

    outputstr+="\nRegister EIP Session Frame Request\n"

    #Print the request
    reg_session_send = ""
    for b in REG_SESSION_FRAME:
        reg_session_send += '{:02X}'.format(b) + " "
    outputstr+=reg_session_send + "\n"

    BUFFER_SIZE_REG_SESSION = 82

    timeout = timeout_ent.get()

    if timeout == '':
        s.settimeout(2.0)
    else:
        s.settimeout(float(timeout))

    #Send the request
    s.send(REG_SESSION_FRAME)

    #Receive the response
    reg_session_rec = s.recv(BUFFER_SIZE_REG_SESSION)

    outputstr+="\nRegister EIP Session Response\n"

    #Print the response
    reg_session_rec_str = ""
    for a in reg_session_rec:
        reg_session_rec_str += '{:02X}'.format(a) + " "
    outputstr+=reg_session_rec_str + "\n"

    #s.close()
    
    return reg_session_rec,outputstr

    
responsetimes = []
    

    
#Function to send a CIP packet given the EIP Session data from the above function, the service, class, instance, and attribute
def EIP_CIP(sock, outputstr, reg_session_data, service, class_var, instance_var, attribute_var):

    global responsetimes
    global responsefile
    # EtherNet/IP send data
    # Encapsulation Header
    
    EIP_COMMAND = b'\x6f\x00'
    if service == b'\x0e' and ( (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1) ):
        EIP_LENGTH = b'\x1a\x00'
    elif service == b'\x0e' and len(class_var) == 1 and len(instance_var) == 1:
        EIP_LENGTH = b'\x18\x00'
    elif service == b'\x0e' and len(class_var) == 2 and len(instance_var) == 2:
        EIP_LENGTH = b'\x1c\x00'
    elif service == b'\x01' and len(class_var) == 1 and len(instance_var) == 1:
        EIP_LENGTH = b'\x16\x00'
    elif service == b'\x01' and ( (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1) ):
        EIP_LENGTH = b'\x18\x00'
    elif service == b'\x01' and len(class_var) == 2 and len(instance_var) == 2:
        EIP_LENGTH = b'\x1a\x00'
    else:
        EIP_LENGTH = b'\x1a\x00'
    EIP_SESSION_HANDLE = reg_session_data[4:8]
    EIP_SUCCESS = b'\x00\x00\x00\x00'
    EIP_SENDER_CONTEXT = b'\x41\xa8\x01\x0b\x0b\x01\x00\x00'
    EIP_OPTIONS = b'\x00\x00\x00\x00'
    EIP_ENCAP_HEADER = EIP_COMMAND + EIP_LENGTH + EIP_SESSION_HANDLE + EIP_SUCCESS + EIP_SENDER_CONTEXT + EIP_OPTIONS

    # command specific data
    EIP_INTHAND = b'\x00\x00\x00\x00' # CIP
    EIP_TIMEOUT = b'\x00\x04'
    EIP_ITEM_COUNT = b'\x02\x00'
    EIP_TYPE_ITEM1_ID = b'\x00\x00'
    EIP_TYPE_ITEM1_LEN = b'\x00\x00'
    EIP_TYPE_ITEM2_ID = b'\xb2\x00'
    if service == b'\x0e' and ( (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1) ):
        EIP_TYPE_ITEM2_LEN = b'\x0a\x00'
    elif service == b'\x0e' and len(class_var) == 1 and len(instance_var) == 1:
        EIP_TYPE_ITEM2_LEN = b'\x08\x00'
    elif service == b'\x0e' and len(class_var) == 2 and len(instance_var) == 2:
        EIP_TYPE_ITEM2_LEN = b'\x0c\x00'
    elif service == b'\x01' and len(class_var) == 1 and len(instance_var) == 1:
        EIP_TYPE_ITEM2_LEN = b'\x06\x00'
    elif service == b'\x01' and ( (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1) ):
        EIP_TYPE_ITEM2_LEN = b'\x08\x00'
    elif service == b'\x01' and len(class_var) == 2 and len(instance_var) == 2:
        EIP_TYPE_ITEM2_LEN = b'\x0a\x00'
    else:
        EIP_TYPE_ITEM2_LEN = b'\x0a\x00'
        
    EIP_COMMAND_SPEC_DATA = EIP_INTHAND + EIP_TIMEOUT + EIP_ITEM_COUNT + EIP_TYPE_ITEM1_ID + EIP_TYPE_ITEM1_LEN + EIP_TYPE_ITEM2_ID + EIP_TYPE_ITEM2_LEN

    # CIP
    CIP_SERVICE = service
    
    if service == b'\x0e' and ( (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1) ):
        CIP_REQ_SIZE = b'\x04'
        CIP_REQ_PATH = b'\x21\x00' + class_var + b'\x24' + instance_var + b'\x30' + attribute_var
    elif service == b'\x0e' and len(class_var) == 1 and len(instance_var) == 1:
        CIP_REQ_SIZE = b'\x03'
        CIP_REQ_PATH = b'\x20' + class_var + b'\x24' + instance_var + b'\x30' + attribute_var
    elif service == b'\x0e' and len(class_var) == 2 and len(instance_var) == 2:
        CIP_REQ_SIZE = b'\x05'
        CIP_REQ_PATH = b'\x21\x00' + class_var + b'\x25\x00' + instance_var + b'\x30' + attribute_var
    elif service == b'\x01' and len(class_var) == 1 and len(instance_var) == 1:
        CIP_REQ_SIZE = b'\x02'
        CIP_REQ_PATH = b'\x20' + class_var + b'\x24' + instance_var
    elif service == b'\x01' and ( (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1) ):
        CIP_REQ_SIZE = b'\x03'
        CIP_REQ_PATH = b'\x21\x00' + class_var + b'\x24' + instance_var
    elif service == b'\x01' and len(class_var) == 2 and len(instance_var) == 2:
        CIP_REQ_SIZE = b'\x04'
        CIP_REQ_PATH = b'\x21\x00' + class_var + b'\x25\x00' + instance_var
    else:
        CIP_REQ_SIZE = b'\x04'
        CIP_REQ_PATH = b'\x21\x00' + class_var + b'\x24' + instance_var + b'\x30' + attribute_var #Param 1 Run Forward
        
    CIP = CIP_SERVICE + CIP_REQ_SIZE + CIP_REQ_PATH
        
    # glue all together
    CIP_FRAME = EIP_ENCAP_HEADER + EIP_COMMAND_SPEC_DATA + CIP

    outputstr+="\nCIP Frame Request\n"

    #Print the request
    cip_frame_send = ""
    for b in CIP_FRAME:
        cip_frame_send += '{:02X}'.format(b) + " "
    outputstr+=cip_frame_send + "\n"

    BUFFER_SIZE_CIP = 400

    try:

        timeout = timeout_ent.get()

        if timeout == '':
            sock.settimeout(2.0)
        else:
            sock.settimeout(float(timeout))

        starttime = time.perf_counter()

        #Send the request
        sock.send(CIP_FRAME)

        #Receive the response
        cip_rec = sock.recv(BUFFER_SIZE_CIP)

        timetaken = time.perf_counter() - starttime
        
        
    except socket.timeout:
        outputstr = "Timed out"
        return -1,outputstr
        
    outputstr+="\nCIP Frame Response\n"
    
    #Print the response
    cip_rec_str = ""
    for b in cip_rec:
        cip_rec_str += '{:02X}'.format(b) + " "
    outputstr+=cip_rec_str + "\n"

    
    
    #outputstr+="\nResponse time = %.5f\n" % timetaken
    
    timetaken = "%.5f" % timetaken
    
    responsetimes.append(timetaken)
    
    try:
        if 'responsefile' in globals():
            responsefile.write(timetaken+"\n")
    except ValueError:
        pass
    
    outputstr+="\nResponse time = " + timetaken + "\n"
    
    #s.close()
    
    return cip_rec,outputstr

mult_sess = 0

#Open multiple sessions (sockets) and send the checked CIP requests in a loop
def mult_sessions():

    compares=0
    passes=0
    fails=0

    global runAndCompare_var
    runAndCompare_var = 1

    global responsefile 
    responsefile = open("response_times.txt","w")

    global mult_sess
    outputstr=""
    
    if int(sessions_ent.get()) > 513:
        t.insert(END,"\nMax sessions is 513\n")
        return
    
    
    if comparefile_op.get() == '1':
    
        global protocolssupported_file
        global maxcipioconnsopened_file
        global currentcipioconns_file
        global maxcipexpconnsopened_file
        global currentcipexpconns_file
        global cipconnsopeningerrors_file
        global cipconnstimeouterrors_file
        global maxeiptcpconnsopened_file
        global currenteiptcpconns_file
        global ioproductionctr_file
        global ioconsumptionctr_file
        global ioproductionsenderrorsctr_file
        global ioconsumptionrecverrorsctr_file
        global class3msgsendctr_file
        global class3msgrecvctr_file
        global ucmmmsgsendctr_file
        global ucmmmsgrecvctr_file
        global vendorid_file
        global openreqs_file
        global tagenable_file
        global devicetype_file
        global productcode_file
        global revision_file1
        global revision_file2
        global status2_file
        global status3_file
        global configcapability_file
        global configcontrol_file
        global physlink_file
        global ipaddr_file
        global subnetmask_file
        global gateway_file
        global nameserver_file
        global nameserver2_file
        global domain_file
        global hostname_file
        global safetynetnumdate_file
        global safetynetnumtime_file
        global ttlvalue_file
        global alloccontrol_file
        global reserved_file
        global nummcast_file
        global mcaststartaddr_file
        global selectacd_file
        global acdactivity_file
        global remotemac_file
        global arppdu_file
        global eipquickconn_file
        global encapinacttimeout_file
        global protocolspec_file
        global bridgepriority_file
        global timesincetopchange_file
        global topchangecount_file
        global desroot_file
        global rootcost_file
        global rootport_file
        global maxage_file
        global hellotime_file
        global holdtime_file
        global forwarddelay_file
        global bridgemaxage_file
        global bridgehellotime_file
        global bridgeforwarddelay_file
        global rstpport_file
        global rstppriority_file
        global rstpstate_file
        global rstpenable_file
        global pathcost_file
        global desroot2_file
        global descost_file
        global desbridge_file
        global desport_file
        global forwardtranscount_file
        global portnum_file
        global adminedgeport_file
        global operedgeport_file
        global autoedgeport_file
        
        

    compare_sel = []
    ftest_lines = []
    
    compare_sel, ftest_lines = getFilesAndCompares(compare_sel, ftest_lines)


    if (closeopen_op.get() == '0'):
    
        sockets = dict()
        
        reg_sessions=[]
        
        sess_hand=b'\x00\x00\x00\x00'
        send_con = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        
        socks_status = 0
        socks_status2 = 0
        socks_status3 = 0
        socks_status4 = 0
        
        t.insert(END,"Opening "+sessions_ent.get()+" sessions\n")
        
        for x in range(0,int(sessions_ent.get()) ):
        
            #time.sleep(1)
            
            sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            timeout = timeout_ent.get()

            if timeout == '':
                sockets[x].settimeout(2.0)
            else:
                sockets[x].settimeout(float(timeout))

            if ssl_op.get() == '1':

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

                sockets[x].connect((TCP_IP.get(), 2221))
            else:

                sockets[x].connect((TCP_IP.get(), TCP_PORT))
            
            socks_status, socks_status2, socks_status3, socks_status4 = changeSockets(x, sockets, socks_status, socks_status2, socks_status3, socks_status4)
            
            updateSockets(socks_status, socks_status2, socks_status3, socks_status4)
            
            root.update()
            #time.sleep(1)
            
            #Create an EIP Session
            reg_session,outputstr = EIP_Reg_Session(sockets[x],outputstr,sess_hand,send_con)
        
            t.insert(END,outputstr)
            outputstr=""
        
            reg_sessions.append(reg_session)
    
        insertstr = "\nRunning "+loop_count_ent.get()+" iterations, delay "+loop_ent.get()+", closeopen "+closeopen_op.get()+", tests "
        
        if cl.getstatus('CL1')=='on':
            insertstr+="1,"
        if cl.getstatus('CL2')=='on':
            insertstr+="2,"
        if cl.getstatus('CL3')=='on':
            insertstr+="3,"
        if cl.getstatus('CL4')=='on':
            insertstr+="4,"
        if cl.getstatus('CL5')=='on':
            insertstr+="5,"
        if cl.getstatus('CL6')=='on':
            insertstr+='6,'
        if cl.getstatus('CL7')=='on':
            insertstr+='7,'
        if cl.getstatus('CL8')=='on':
            insertstr+='8,'
        if cl.getstatus('CL9')=='on':
            insertstr+='9,'
        if cl.getstatus('CL10')=='on':
            insertstr+='10,'
        if cl.getstatus('CL11')=='on':
            insertstr+='11,'
        if cl.getstatus('CL12')=='on':
            insertstr+='12,'
        if cl.getstatus('CL13')=='on':
            insertstr+='13,'
        if cl.getstatus('CL14')=='on':
            insertstr+='14,'
        if cl.getstatus('CL15')=='on':
            insertstr+='15,'
        if cl.getstatus('CL16')=='on':
            insertstr+='16,'
        if cl.getstatus('CL17')=='on':
            insertstr+='17,'
        if cl.getstatus('CL18')=='on':
            insertstr+='18,'
        if cl.getstatus('CL19')=='on':
            insertstr+='19,'
        if cl.getstatus('CL20')=='on':
            insertstr+='20,'
        if cl.getstatus('CL21')=='on':
            insertstr+='21,'

    
        insertstr+="\n"
        t.insert(END,insertstr)
    
        loopStop.set('0')
    
        loop_count = loop_count_ent.get()
    
        if loop_count == "":
            loop_count = 4
        else:
            loop_count = int(loop_count)
    
        ctr=0
        iter=0
        while iter < loop_count:
        
        
            for z in range(0,len(compare_sel)):
    
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
                
                for x in range(0,len(reg_sessions)):
                    
                    t.insert(END,"\nSending CIP on session "+str(x+1)+"\n")
                    
                    reg_sess = reg_sessions[x]

                    scanner=''
                    example_handler=''

                    if comparefile_op.get() == '1':
                        execute_eip(sockets[x], reg_sess, compare_sel[z], z, scanner, example_handler)
                    elif comparefile_op.get() == '0':
                        execute_eip(sockets[x], reg_sess, compare_sel, z, scanner, example_handler)
                    
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
                

        
                
    elif (closeopen_op.get() == '1'):
    
        sockets = dict()
        
        reg_sessions=[]
        
        sess_hand=b'\x00\x00\x00\x00'
        send_con = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        
        socks_status = 0
        socks_status2 = 0
        socks_status3 = 0
        socks_status4 = 0

        t.insert(END,"Opening "+sessions_ent.get()+" sessions\n")
        
        for x in range(0,int(sessions_ent.get()) ):
        
            #time.sleep(1)
            
            sockets[x] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            timeout = timeout_ent.get()

            if timeout == '':
                sockets[x].settimeout(2.0)
            else:
                sockets[x].settimeout(float(timeout))

            if ssl_op.get() == '1':

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

                sockets[x].connect((TCP_IP.get(), 2221))
            else:
                sockets[x].connect((TCP_IP.get(), TCP_PORT))
            
            socks_status, socks_status2, socks_status3, socks_status4 = changeSockets(x, sockets, socks_status, socks_status2, socks_status3, socks_status4)
            
            updateSockets(socks_status, socks_status2, socks_status3, socks_status4)
            
            root.update()
            #time.sleep(1.5)
            
            #Create an EIP Session
            reg_session,outputstr = EIP_Reg_Session(sockets[x],outputstr,sess_hand,send_con)
        
            t.insert(END,outputstr)
            outputstr=""
        
            reg_sessions.append(reg_session)
    
        insertstr = "\nRunning "+loop_count_ent.get()+" iterations, delay "+loop_ent.get()+", closeopen "+closeopen_op.get()+", tests "
        
        if cl.getstatus('CL1')=='on':
            insertstr+="1,"
        if cl.getstatus('CL2')=='on':
            insertstr+="2,"
        if cl.getstatus('CL3')=='on':
            insertstr+="3,"
        if cl.getstatus('CL4')=='on':
            insertstr+="4,"
        if cl.getstatus('CL5')=='on':
            insertstr+="5,"
        if cl.getstatus('CL6')=='on':
            insertstr+='6,'
        if cl.getstatus('CL7')=='on':
            insertstr+='7,'
        if cl.getstatus('CL8')=='on':
            insertstr+='8,'
        if cl.getstatus('CL9')=='on':
            insertstr+='9,'
        if cl.getstatus('CL10')=='on':
            insertstr+='10,'
        if cl.getstatus('CL11')=='on':
            insertstr+='11,'
        if cl.getstatus('CL12')=='on':
            insertstr+='12,'
        if cl.getstatus('CL13')=='on':
            insertstr+='13,'
        if cl.getstatus('CL14')=='on':
            insertstr+='14,'
        if cl.getstatus('CL15')=='on':
            insertstr+='15,'
        if cl.getstatus('CL16')=='on':
            insertstr+='16,'
        if cl.getstatus('CL17')=='on':
            insertstr+='17,'
        if cl.getstatus('CL18')=='on':
            insertstr+='18,'
        if cl.getstatus('CL19')=='on':
            insertstr+='19,'
        if cl.getstatus('CL20')=='on':
            insertstr+='20,'
        if cl.getstatus('CL21')=='on':
            insertstr+='21,'
    
        insertstr+="\n"
        t.insert(END,insertstr)
    
        loopStop.set('0')
    
        loop_count = loop_count_ent.get()
    
        if loop_count == "":
            loop_count = 4
        else:
            loop_count = int(loop_count)
        ctr=0
        iter=0
        while iter < loop_count:
        
            for z in range(0,len(compare_sel)):
    
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
                
                for y in range(0,len(reg_sessions)):
                    
                    t.insert(END,"\nClosing, opening, and sending CIP on session "+str(y+1)+"\n")
                    
                    sockets[y].close()
                    
                    socks_status, socks_status2, socks_status3, socks_status4 = changeSockets(y, sockets, socks_status, socks_status2, socks_status3, socks_status4)
                    
                    updateSockets(socks_status, socks_status2, socks_status3, socks_status4)
                    
                    root.update()
                    #time.sleep(1.5)
                    
                    loop_delay = loop_ent.get()
                    
                    if loop_delay == "":
                        loop_delay = 0
                    
                    time.sleep(float(loop_delay) * 0.001)
                         
                    sockets[y] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    timeout = timeout_ent.get()

                    if timeout == '':
                        sockets[y].settimeout(2.0)
                    else:
                        sockets[y].settimeout(float(timeout))

                    if ssl_op.get() == '1':

                        if cert_ent.get() == '':
                            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                        else:
                            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
                            context.verify_mode = ssl.CERT_REQUIRED

                            if host_ent.get() != '':
                                context.check_hostname = True

                            context.load_verify_locations(cert_ent.get())

                        if host_ent.get() != '':
                            sockets[y] = context.wrap_socket(sockets[y], server_hostname=host_ent.get())
                        else:
                            sockets[y] = context.wrap_socket(sockets[y])

                        sockets[y].connect((TCP_IP.get(),2221))
                    else:
                        sockets[y].connect((TCP_IP.get(), TCP_PORT))
                    
                    socks_status, socks_status2, socks_status3, socks_status4 = changeSockets(y, sockets, socks_status, socks_status2, socks_status3, socks_status4)
                    
                    updateSockets(socks_status, socks_status2, socks_status3, socks_status4)
                    
                    root.update()
                    #time.sleep(1.5)
                    
                    reg_session,outputstr = EIP_Reg_Session(sockets[y],outputstr,sess_hand,send_con)
                    
                    t.insert(END,outputstr)
                    outputstr=""
                    
                    reg_sessions[y] = reg_session
                    reg_sess = reg_sessions[y]

                    scanner = ''
                    example_handler = ''

                    if comparefile_op.get() == '1':
                        execute_eip(sockets[y], reg_sess, compare_sel[z], z, scanner, example_handler)
                    elif comparefile_op.get() == '0':
                        execute_eip(sockets[y], reg_sess, compare_sel, z, scanner, example_handler)
                    
                    
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
    #execute_eip()
    mult_sess = 0
    runAndCompare_var = 0


#Indicate whether a socket is on or off by setting a bit to 1 or 0
def changeSockets(x, sockets, socks_status, socks_status2, socks_status3, socks_status4):

    try:
        fileno = sockets[x].fileno()
    except socket.error:
        fileno = -1
        
    if fileno!=-1:
    
        if x < 16:
            socks_status |= (1 << x)
        elif x > 15 and x < 32:
            socks_status2 |= (1 << (x - 16) )
        elif x > 31 and x < 64:
            socks_status3 |= (1 << (x - 32) )
        elif x > 63 and x < 128:
            socks_status4 |= (1 << (x - 64) )

    elif fileno==-1:
        
        if x < 16:
            socks_status &= ~(1 << x)
        elif x > 15 and x < 32:
            socks_status2 &= ~(1 << (x - 16) )
        elif x > 31 and x < 64:
            socks_status3 &= ~(1 << (x - 32) )
        elif x > 63 and x < 128:
            socks_status4 &= ~(1 << (x - 64) )
    
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
    
    
#Parse what we read from the file to get the attribute to compare to the current run
def parseAttrs(ftest_lines):


    global protocolssupported_file
    global maxcipioconnsopened_file
    global currentcipioconns_file
    global maxcipexpconnsopened_file
    global currentcipexpconns_file
    global cipconnsopeningerrors_file
    global cipconnstimeouterrors_file
    global maxeiptcpconnsopened_file
    global currenteiptcpconns_file
    global ioproductionctr_file
    global ioconsumptionctr_file
    global ioproductionsenderrorsctr_file
    global ioconsumptionrecverrorsctr_file
    global class3msgsendctr_file
    global class3msgrecvctr_file
    global ucmmmsgsendctr_file
    global ucmmmsgrecvctr_file
    global vendorid_file
    global openreqs_file
    global tagenable_file
    global devicetype_file
    global productcode_file
    global revision_file1
    global revision_file2
    global status2_file
    global serialnum_file
    global productname_file
    global state_file
    global configconsistency_file
    global heartbeatint_file
    global status3_file
    global configcapability_file
    global configcontrol_file
    global physlink_file
    global ipaddr_file
    global subnetmask_file
    global gateway_file
    global nameserver_file
    global nameserver2_file
    global domain_file
    global hostname_file
    global safetynetnumdate_file
    global safetynetnumtime_file
    global ttlvalue_file
    global alloccontrol_file
    global reserved_file
    global nummcast_file
    global mcaststartaddr_file
    global selectacd_file
    global acdactivity_file
    global remotemac_file
    global arppdu_file
    global eipquickconn_file
    global encapinacttimeout_file
    global protocolspec_file
    global bridgepriority_file
    global timesincetopchange_file
    global topchangecount_file
    global desroot_file
    global rootcost_file
    global rootport_file
    global maxage_file
    global hellotime_file
    global holdtime_file
    global forwarddelay_file
    global bridgemaxage_file
    global bridgehellotime_file
    global bridgeforwarddelay_file
    global rstpport_file
    global rstppriority_file
    global rstpstate_file
    global rstpenable_file
    global pathcost_file
    global desroot2_file
    global descost_file
    global desbridge_file
    global desport_file
    global forwardtranscount_file
    global portnum_file
    global adminedgeport_file
    global operedgeport_file
    global autoedgeport_file
    
    
    
    for x in range(0,len(ftest_lines)):
    
        if ftest_lines[x][0:30] == "Attr 1: Protocols supported = ":
            protocolssupported_file = int(ftest_lines[x][30:])
        if ftest_lines[x][0:57] == "Attr 2 (Connection Diag): Max CIP IO Connection opened = ":
            maxcipioconnsopened_file = int(ftest_lines[x][57:])
        if ftest_lines[x][0:37] == "Attr 2: Current CIP IO Connections = ":
            currentcipioconns_file = int(ftest_lines[x][37:])
        if ftest_lines[x][0:39] == "Attr 2: Max CIP Explicit Connections = ":
            maxcipexpconnsopened_file = int(ftest_lines[x][39:])
        if ftest_lines[x][0:43] == "Attr 2: Current CIP Explicit Connections = ":
            currentcipexpconns_file = int(ftest_lines[x][43:])
        if ftest_lines[x][0:41] == "Attr 2: CIP Connections Opening Errors = ":
            cipconnsopeningerrors_file = int(ftest_lines[x][41:])
        if ftest_lines[x][0:41] == "Attr 2: CIP Connections Timeout Errors = ":
            cipconnstimeouterrors_file = int(ftest_lines[x][41:])
        if ftest_lines[x][0:41] == "Attr 2: Max EIP TCP Connections opened = ":
            maxeiptcpconnsopened_file = int(ftest_lines[x][41:])
        if ftest_lines[x][0:38] == "Attr 2: Current EIP TCP Connections = ":
            currenteiptcpconns_file = int(ftest_lines[x][38:])
        if ftest_lines[x][0:52] == "Attr 3 (IO Messaging Diag): IO Production Counter = ":
            ioproductionctr_file = int(ftest_lines[x][52:])
        if ftest_lines[x][0:33] == "Attr 3: IO Consumption Counter = ":
            ioconsumptionctr_file = int(ftest_lines[x][33:])
        if ftest_lines[x][0:44] == "Attr 3: IO Production Send Errors Counter = ":
            ioproductionsenderrorsctr_file = int(ftest_lines[x][44:])
        if ftest_lines[x][0:48] == "Attr 3: IO Consumption Receive Errors Counter = ":
            ioconsumptionrecverrorsctr_file = int(ftest_lines[x][48:])
        if ftest_lines[x][0:61] == "Attr 4 (Explicit Messaging Diag): Class 3 Msg Send Counter = ":
            class3msgsendctr_file = int(ftest_lines[x][61:])
        if ftest_lines[x][0:38] == "Attr 4: Class 3 Msg Receive Counter = ":
            class3msgrecvctr_file = int(ftest_lines[x][38:])
        if ftest_lines[x][0:32] == "Attr 4: UCMM Msg Send Counter = ":
            ucmmmsgsendctr_file = int(ftest_lines[x][32:])
        if ftest_lines[x][0:35] == "Attr 4: UCMM Msg Receive Counter = ":
            ucmmmsgrecvctr_file = int(ftest_lines[x][35:])
        if ftest_lines[x][0:20] == "Attr 1: Vendor ID = ":
            vendorid_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:24] == "Attr 1: Open Requests = ":
            openreqs_file = int(ftest_lines[x][24:])
        if ftest_lines[x][0:28] == "Attr 1: 802.1Q Tag Enable = ":
            tagenable_file = int(ftest_lines[x][28:])
        if ftest_lines[x][0:20] == "Attr 1: Port Type = ":
            porttype_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:22] == "Attr 2: Device Type = ":
            devicetype_file = int(ftest_lines[x][22:])
        if ftest_lines[x][0:23] == "Attr 3: Product Code = ":
            productcode_file = int(ftest_lines[x][23:])
        if ftest_lines[x][0:25] == "Attr 4: Major Revision = ":
            revision_file1 = int(ftest_lines[x][25:])
        if ftest_lines[x][0:25] == "Attr 4: Minor Revision = ":
            revision_file2 = int(ftest_lines[x][25:])
        if ftest_lines[x][0:17] == "Attr 5: Status = ":
            status2_file = int(ftest_lines[x][17:-2],16)
        if ftest_lines[x][0:24] == "Attr 6: Serial Number = ":
            serialnum_file = int(ftest_lines[x][24:],16)
        if ftest_lines[x][0:23] == "Attr 7: Product Name = ":
            if ftest_lines[x][23:27] == "NULL":
                productname_file = 0
            else:
                productname_file = int(ftest_lines[x][23:])
        if ftest_lines[x][0:16] == "Attr 8: State = ":
            state_file = int(ftest_lines[x][16:],16)
        if ftest_lines[x][0:42] == "Attr 9: Configuration Consistency Value = ":
            configconsistency_file = int(ftest_lines[x][42:])
        if ftest_lines[x][0:30] == "Attr 10: Heartbeat Interval = ":
            heartbeatint_file = int(ftest_lines[x][30:])
        if ftest_lines[x][0:17] == "Attr 1: Status = ":
            status3_file = int(ftest_lines[x][17:])
        if ftest_lines[x][0:35] == "Attr 2: Configuration Capability = ":
            configcapability_file = int(ftest_lines[x][35:],16)
        if ftest_lines[x][0:32] == "Attr 3: Configuration Control = ":
            configcontrol_file = int(ftest_lines[x][32:])
        if ftest_lines[x][0:24] == "Attr 4: Physical Link = ":
            physlink_file = int(ftest_lines[x][24:])
        if ftest_lines[x][0:21] == "Attr 5: IP Address = ":
            ipaddr_file = ftest_lines[x][21:]
        if ftest_lines[x][0:22] == "Attr 5: Subnet mask = ":
            subnetmask_file = ftest_lines[x][22:]
        if ftest_lines[x][0:18] == "Attr 5: Gateway = ":
            gateway_file = ftest_lines[x][18:]
        if ftest_lines[x][0:22] == "Attr 5: Name Server = ":
            nameserver_file = ftest_lines[x][22:]
        if ftest_lines[x][0:23] == "Attr 5: Name Server2 = ":
            nameserver2_file = ftest_lines[x][23:]
        if ftest_lines[x][0:22] == "Attr 5: Domain Name = ":
            domain_file = int(ftest_lines[x][22:])
        if ftest_lines[x][0:20] == "Attr 6: Host Name = ":
            hostname_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:46] == "Attr 7: Safety Network Number (Manual) Date = ":
            safetynetnumdate_file = int(ftest_lines[x][46:],16)
        if ftest_lines[x][0:46] == "Attr 7: Safety Network Number (Manual) Time = ":
            safetynetnumtime_file = int(ftest_lines[x][46:],16)
        if ftest_lines[x][0:20] == "Attr 8: TTL Value = ":
            ttlvalue_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:24] == "Attr 9: Alloc Control = ":
            alloccontrol_file = int(ftest_lines[x][24:])
        if ftest_lines[x][0:19] == "Attr 9: Reserved = ":
            reserved_file = int(ftest_lines[x][19:])
        if ftest_lines[x][0:20] == "Attr 9: Num MCast = ":
            nummcast_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:27] == "Attr 9: MCast Start Addr = ":
            mcaststartaddr_file = ftest_lines[x][27:]
        if ftest_lines[x][0:22] == "Attr 10: Select ACD = ":
            selectacd_file = int(ftest_lines[x][22:])
        if ftest_lines[x][0:24] == "Attr 11: ACD Activity = ":
            acdactivity_file = int(ftest_lines[x][24:])
        if ftest_lines[x][0:21] == "Attr 11: RemoteMAC = ":
            remotemac_file = ftest_lines[x][21:]
        if ftest_lines[x][0:19] == "Attr 11: Arp PDU = ":
            arppdu_file = ftest_lines[x][19:]
        if ftest_lines[x][0:40] == "Attr 12: EtherNet/IP Quick Connection = ":
            eipquickconn_file = int(ftest_lines[x][40:])
        if ftest_lines[x][0:44] == "Attr 13: Encapsulation Inactivity Timeout = ":
            encapinacttimeout_file = int(ftest_lines[x][44:])
        if ftest_lines[x][0:49] == "Attr 1 (Switch Status): Protocol Specification = ":
            protocolspec_file = int(ftest_lines[x][49:])
        if ftest_lines[x][0:26] == "Attr 1: Bridge Priority = ":
            bridgepriority_file = int(ftest_lines[x][26:])
        if ftest_lines[x][0:37] == "Attr 1: Time Since Topology Change = ":
            timesincetopchange_file = int(ftest_lines[x][37:])
        if ftest_lines[x][0:32] == "Attr 1: Topology Change Count = ":
            topchangecount_file = int(ftest_lines[x][32:])
        if ftest_lines[x][0:26] == "Attr 1: Designated Root = ":
            desroot_file = ftest_lines[x][26:]
        if ftest_lines[x][0:20] == "Attr 1: Root Cost = ":
            rootcost_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:20] == "Attr 1: Root Port = ":
            rootport_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:18] == "Attr 1: Max Age = ":
            maxage_file = int(ftest_lines[x][18:])
        if ftest_lines[x][0:21] == "Attr 1: Hello Time = ":
            hellotime_file = int(ftest_lines[x][21:])
        if ftest_lines[x][0:20] == "Attr 1: Hold Time = ":
            holdtime_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:24] == "Attr 1: Forward Delay = ":
            forwarddelay_file = int(ftest_lines[x][24:])
        if ftest_lines[x][0:25] == "Attr 1: Bridge Max Age = ":
            bridgemaxage_file = int(ftest_lines[x][25:])
        if ftest_lines[x][0:28] == "Attr 1: Bridge Hello Time = ":
            bridgehellotime_file = int(ftest_lines[x][28:])
        if ftest_lines[x][0:31] == "Attr 1: Bridge Forward Delay = ":
            bridgeforwarddelay_file = int(ftest_lines[x][31:])
        if ftest_lines[x][0:29] == "Attr 2 (Port Status): Port = ":
            rstpport_file = int(ftest_lines[x][29:])
        if ftest_lines[x][0:19] == "Attr 2: Priority = ":
            rstppriority_file = int(ftest_lines[x][19:])
        if ftest_lines[x][0:16] == "Attr 2: State = ":
            rstpstate_file = int(ftest_lines[x][16:])
        if ftest_lines[x][0:17] == "Attr 2: Enable = ":
            rstpenable_file = int(ftest_lines[x][17:])
        if ftest_lines[x][0:20] == "Attr 2: Path Cost = ":
            pathcost_file = int(ftest_lines[x][20:])
        if ftest_lines[x][0:26] == "Attr 2: Designated Root = ":
            desroot2_file = ftest_lines[x][26:]
        if ftest_lines[x][0:26] == "Attr 2: Designated Cost = ":
            descost_file = int(ftest_lines[x][26:])
        if ftest_lines[x][0:28] == "Attr 2: Designated Bridge = ":
            desbridge_file = ftest_lines[x][28:]
        if ftest_lines[x][0:26] == "Attr 2: Designated Port = ":
            desport_file = ftest_lines[x][26:]
        if ftest_lines[x][0:36] == "Attr 2: Forward Transitions Count = ":
            forwardtranscount_file = int(ftest_lines[x][36:])
        if ftest_lines[x][0:34] == "Attr 3 (Port Mode): Port Number = ":
            portnum_file = int(ftest_lines[x][34:])
        if ftest_lines[x][0:26] == "Attr 3: Admin Edge Port = ":
            adminedgeport_file = int(ftest_lines[x][26:])
        if ftest_lines[x][0:25] == "Attr 3: Oper Edge Port = ":
            operedgeport_file = int(ftest_lines[x][25:])
        if ftest_lines[x][0:25] == "Attr 3: Auto Edge Port = ":
            autoedgeport_file = int(ftest_lines[x][25:])





checksize = 0

#Execute sendCIP() with checksize set to 1 so we check sizes
def checkSizes():

    global checksize
    checksize = 1

    sendCIP()

    checksize = 0

    
compares=0
passes=0
fails=0


#Function to output dividers between files
def fileDividers(z):


    if compare_ent.get()[-4:] == '.ini':

        t2.insert(END,"\n====================================================\nFile "+fcomparefiles[z]+"\n")

    else:
    
        if compare_ent.get() != '' and z==0:
            t2.insert(END,"\n======================================================File "+compare_ent.get()+"\n")
        if compare_ent2.get() != '' and z==1:
            t2.insert(END,"\n======================================================\nFile "+compare_ent2.get()+"\n")
        if compare_ent3.get() != '' and z==2:
            t2.insert(END,"\n======================================================\nFile "+compare_ent3.get()+"\n")
        if compare_ent4.get() != '' and z==3:
            t2.insert(END,"\n======================================================\nFile "+compare_ent4.get()+"\n")
        if compare_ent5.get() != '' and z==4:
            t2.insert(END,"\n======================================================\nFile "+compare_ent5.get()+"\n")


    t2.insert(END,"\n--- output\n+++ file\n")



#Get the filenames to compare to and get the CIP objects and attributes to compare
def getFilesAndCompares(compare_sel,ftest_lines):



    if comparefile_op.get() == '1':
    
    
        if compare_ent.get()[-4:] == '.ini':
            
            fcompareini = open(compare_ent.get(),'r')
            fcomparefiles = fcompareini.read().split(",")
           # ftest_lines = []
            for x in range(0,len(fcomparefiles)):
                file = fcomparefiles[x]
                opened_file = open(file,'rb')
                ftest_lines.append(opened_file.readlines() )
        else:
        
            ftest_lines = []
            if compare_ent.get() != '':
                ftest = open(compare_ent.get(),"r")
                ftest_lines.append(ftest.readlines())
            if compare_ent2.get() != '':
                ftest2 = open(compare_ent2.get(),'r')
                ftest_lines.append(ftest2.readlines())
            if compare_ent3.get() != '':
                ftest3 = open(compare_ent3.get(),'r')
                ftest_lines.append(ftest3.readlines())
            if compare_ent4.get() != '':
                ftest4 = open(compare_ent4.get(),'r')
                ftest_lines.append(ftest4.readlines())
            if compare_ent5.get() != '':
                ftest5 = open(compare_ent5.get(),'r')
                ftest_lines.append(ftest5.readlines())
    
        
      #  compare_sel = []
        for y in range(0,len(ftest_lines)):
    
            found = 0
            for x in range(0,len(ftest_lines[y])):
            
                if ftest_lines[y][x][0:7] == "Compare":
                
                    found = 1
                    compare_sel.append(ftest_lines[y][x][8:].split(",") )
            
            if found == 0:
                
                output = t.get("1.0",END)
                output = output.splitlines()
                
                for x in range(0,len(output)):
            
                    if output[x][0:7] == "Compare":
                
                        found = 1
                        compare_sel.append( output[x][8:].split(",") )
            
        if len(compare_sel) == 0:
        
            compare_sel = '1'
        
    

    
    
    elif comparefile_op.get() == '0':
    
        compare_sel = '1'

        
    return compare_sel,ftest_lines
        
        
#Redundant code to open a text file between calling sendCIP()
def sendCIPReq():

    global responsefile 
    responsefile = open("response_times.txt","w")
    sendCIP()
    responsefile.close()


#Main function - handles compares, opens a socket, sends a register session, and calls the function
#that sends the checked CIP requests
def sendCIP():

    global checksize

    if comparefile_op.get() == '1':
    
        global protocolssupported_file
        global maxcipioconnsopened_file
        global currentcipioconns_file
        global maxcipexpconnsopened_file
        global currentcipexpconns_file
        global cipconnsopeningerrors_file
        global cipconnstimeouterrors_file
        global maxeiptcpconnsopened_file
        global currenteiptcpconns_file
        global ioproductionctr_file
        global ioconsumptionctr_file
        global ioproductionsenderrorsctr_file
        global ioconsumptionrecverrorsctr_file
        global class3msgsendctr_file
        global class3msgrecvctr_file
        global ucmmmsgsendctr_file
        global ucmmmsgrecvctr_file
        global vendorid_file
        global openreqs_file
        global tagenable_file
        global devicetype_file
        global productcode_file
        global revision_file1
        global revision_file2
        global status2_file
        global serialnum_file
        global status3_file
        global configcapability_file
        global configcontrol_file
        global physlink_file
        global ipaddr_file
        global subnetmask_file
        global gateway_file
        global nameserver_file
        global nameserver2_file
        global domain_file
        global hostname_file
        global safetynetnumdate_file
        global safetynetnumtime_file
        global ttlvalue_file
        global alloccontrol_file
        global reserved_file
        global nummcast_file
        global mcaststartaddr_file
        global selectacd_file
        global acdactivity_file
        global remotemac_file
        global arppdu_file
        global eipquickconn_file
        global encapinacttimeout_file
        global protocolspec_file
        global bridgepriority_file
        global timesincetopchange_file
        global topchangecount_file
        global desroot_file
        global rootcost_file
        global rootport_file
        global maxage_file
        global hellotime_file
        global holdtime_file
        global forwarddelay_file
        global bridgemaxage_file
        global bridgehellotime_file
        global bridgeforwarddelay_file
        global rstpport_file
        global rstppriority_file
        global rstpstate_file
        global rstpenable_file
        global pathcost_file
        global desroot2_file
        global descost_file
        global desbridge_file
        global desport_file
        global forwardtranscount_file
        global portnum_file
        global adminedgeport_file
        global operedgeport_file
        global autoedgeport_file
        
        

    compare_sel = []
    ftest_lines = []
    
    compare_sel, ftest_lines = getFilesAndCompares(compare_sel, ftest_lines)
    
    for z in range(0,len(compare_sel)):

        if comparefile_op.get() == '1' and compare_sel != '1':
        
            parseAttrs(ftest_lines[z])

            fileDividers(z)

        #example_handler = ExampleEventHandler3(threading.Event(), threading.Event())

        #scanner = Scanner(address=TCP_IP2.get(), event_handler=example_handler)

        #scanner.run()

        example_handler = ''
        scanner = ''


        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        timeout = timeout_ent.get()

        if timeout == '':
            sock.settimeout(2.0)
        else:
            sock.settimeout(float(timeout))

        if ssl_op.get() == '1':

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

            sock.connect((TCP_IP.get(),2221))

        else:
            sock.connect((TCP_IP.get(), TCP_PORT))

        outputstr=""
        sess_hand=b'\x00\x00\x00\x00'
        send_con = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        reg_session,outputstr = EIP_Reg_Session(sock,outputstr,sess_hand,send_con)
        t.insert(END,outputstr)
        outputstr=""

        #sock=''
        #reg_session=''

        if comparefile_op.get() == '1':
            execute_eip(sock,reg_session,compare_sel[z],z,scanner,example_handler)
        elif comparefile_op.get() == '0':
            execute_eip(sock,reg_session,compare_sel,z,scanner,example_handler)
 
        sock.close()
 
        saveToFiles(z)
  
        #scanner.stop()
#
# #Event handler for unconnected messaging
# class ExampleEventHandler3(ScannerEventHandler):
#     def __init__(self, response_event, invalid_event):
#         self.example_response_event = response_event
#         self.example_invalid_event = invalid_event
#
#     def on_unconnected_response(self, cip_object, address, response):
#         t.insert(END,'Received response for CIP object {} to "{}":\n'.format(cip_object, address))
#         t.insert(END,response)
#         #print('response.interface_counters.rx.octets:', response.interface_counters.rx.octets)
#         self.example_response_event.set()
#
#     def on_unconnected_invalid_address(self, cip_object, address):
#         print('\nExplicit request {} attempted to invalid address "{}".'.format(cip_object, address))
#         self.example_invalid_event.set()

#Saves the output to files during compares
def saveToFiles(z):

    if comparefile_op.get() == '1':
    
        global endLine
        if compare_ent.get()[-4:] == '.ini':
            
            #fcompareini = open(compare_ent.get(),'rb')
            #fcomparefiles = fcompareini.read().split(",")
            
            #Get the current time
            dt = datetime.datetime.now()
            #Convert the current time to a string
            time_now = dt.strftime("%m%d%y_%H%M%S")
            
            opened_file = open(fcomparefiles[z]+"_output_" + time_now,'w')
            
            if z==0:
                opened_file.write(t.get("1.0",END))
            else:
                opened_file.write(t.get(str(endLine)+".0",END))
            
            endLine = int(t.index('end').split('.')[0])
            
            #t.delete(1.0,END)
                
        else:
        
            outfiles = []
            #ftest_lines = []
            if compare_ent.get() != '' and z==0:
                #Get the current time
                dt = datetime.datetime.now()
                #Convert the current time to a string
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent.get() + "_output_" + time_now,"w")
                file.write(t.get("1.0",END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            if compare_ent2.get() != '' and z==1:
                dt = datetime.datetime.now()
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent2.get() + "_output_" + time_now,'w')
                file.write(t.get(str(endLine)+".0",END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            if compare_ent3.get() != '' and z==2:
                dt = datetime.datetime.now()
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent3.get() + "_output_" + time_now,'w')
                file.write(t.get(str(endLine)+".0",END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            if compare_ent4.get() != '' and z==3:
                dt = datetime.datetime.now()
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent4.get() + "_output_" + time_now,'w')
                file.write(t.get(str(endLine)+".0",END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            if compare_ent5.get() != '' and z==4:
                dt = datetime.datetime.now()
                time_now = dt.strftime("%m%d%y_%H%M%S")
                file = open(compare_ent5.get() + "_output_" + time_now,'w')
                file.write(t.get(str(endLine)+".0",END))
                file.close()
                endLine = int(t.index('end').split('.')[0])
            
        
        
        
#I don't think this is used
def loopSession(s,outputstr, reg_session, service_req, class_req, instance_req, attribute_req):

    while 1:
    
        #Send the CIP request and get the response
        cip_res,outputstr = EIP_CIP(s,outputstr, reg_session, service_req, class_req, instance_req, attribute_req)
        
        time.sleep(1)
    
#from timeit import Timer
#from time import time

#Redundant function to send a CIP request and return the response
def requestsendreceive(outputstr, s, reg_sess, service_req, class_req, instance_req, attribute_req):

    #t = Timer("cip_res,outputstr = EIP_CIP(s,outputstr, reg_sess, service_req, class_req, instance_req, attribute_req)", "from __main__ import EIP_CIP")
    
    #print t.timeit(number=1)
    cip_res,outputstr = EIP_CIP(s,outputstr, reg_sess, service_req, class_req, instance_req, attribute_req)

    return outputstr,cip_res
    
    
maxeiptcpconnsopened_file = 0

vendorid_file = 0
openreqs_file = 0
tagenable_file = 0
porttype_file = 0
devicetype_file = 0
productcode_file = 0
revision_file1 = 0
revision_file2 = 0
status2_file = 0
serialnum_file = 0

#Adds "Compare ....." to the output textbox with numbers instead of "....." indicating what is currently checked
def addCompares():


    insertstr="\nCompare "


    if cl.getstatus('CL1')=='on':
        insertstr+="1,"
    if cl.getstatus('CL2')=='on':
        insertstr+="2,"
    if cl.getstatus('CL3')=='on':
        insertstr+="3,"
    if cl.getstatus('CL4')=='on':
        insertstr+="4,"
    if cl.getstatus('CL4.1')=='on':
        insertstr+="4.1,"
    if cl.getstatus('CL4.2')=='on':
        insertstr+="4.2,"
    if cl.getstatus('CL4.3')=='on':
        insertstr+="4.3,"
    if cl.getstatus('CL4.4')=='on':
        insertstr+="4.4,"
    if cl.getstatus('CL4.5')=='on':
        insertstr+="4.5,"
    if cl.getstatus('CL4.6')=='on':
        insertstr+="4.6,"
    if cl.getstatus('CL4.7')=='on':
        insertstr+="4.7,"
    if cl.getstatus('CL4.8')=='on':
        insertstr+="4.8,"
    if cl.getstatus('CL4.9')=='on':
        insertstr+="4.9,"
    if cl.getstatus('CL4.10')=='on':
        insertstr+="4.10,"
    if cl.getstatus('CL4.11')=='on':
        insertstr+="4.11,"
    if cl.getstatus('CL4.12')=='on':
        insertstr+="4.12,"
    if cl.getstatus('CL4.13')=='on':
        insertstr+="4.13,"
    if cl.getstatus('CL4.14')=='on':
        insertstr+="4.14,"
    if cl.getstatus('CL4.15')=='on':
        insertstr+="4.15,"
    if cl.getstatus('CL4.16')=='on':
        insertstr+="4.16,"
    if cl.getstatus('CL4.17')=='on':
        insertstr+="4.17,"
    if cl.getstatus('CL5')=='on':
        insertstr+="5,"
    if cl.getstatus('CL6')=='on':
        insertstr+='6,'
    if cl.getstatus('CL7')=='on':
        insertstr+='7,'
    if cl.getstatus('CL8')=='on':
        insertstr+='8,'
    if cl.getstatus('CL9')=='on':
        insertstr+='9,'
    if cl.getstatus('CL9.1') == 'on':
        insertstr += '9.1,'
    if cl.getstatus('CL9.2') == 'on':
        insertstr += '9.2,'
    if cl.getstatus('CL9.3') == 'on':
        insertstr += '9.3,'
    if cl.getstatus('CL9.4') == 'on':
        insertstr += '9.4,'
    if cl.getstatus('CL9.5') == 'on':
        insertstr += '9.5,'
    if cl.getstatus('CL9.6') == 'on':
        insertstr += '9.6,'
    if cl.getstatus('CL9.7') == 'on':
        insertstr += '9.7,'
    if cl.getstatus('CL9.8') == 'on':
        insertstr += '9.8,'
    if cl.getstatus('CL9.9') == 'on':
        insertstr += '9.9,'
    if cl.getstatus('CL9.10') == 'on':
        insertstr += '9.10,'
    if cl.getstatus('CL9.11') == 'on':
        insertstr += '9.11,'
    if cl.getstatus('CL9.12') == 'on':
        insertstr += '9.12,'
    if cl.getstatus('CL9.13') == 'on':
        insertstr += '9.13,'
    if cl.getstatus('CL9.14') == 'on':
        insertstr += '9.14,'
    if cl.getstatus('CL9.15') == 'on':
        insertstr += '9.15,'
    if cl.getstatus('CL9.16') == 'on':
        insertstr += '9.16,'
    if cl.getstatus('CL9.17') == 'on':
        insertstr += '9.17,'
    if cl.getstatus('CL9.18') == 'on':
        insertstr += '9.18,'
    if cl.getstatus('CL9.19') == 'on':
        insertstr += '9.19,'
    if cl.getstatus('CL9.20') == 'on':
        insertstr += '9.20,'
    if cl.getstatus('CL9.21') == 'on':
        insertstr += '9.21,'
    if cl.getstatus('CL9.22') == 'on':
        insertstr += '9.22,'
    if cl.getstatus('CL9.23') == 'on':
        insertstr += '9.23,'
    if cl.getstatus('CL9.24') == 'on':
        insertstr += '9.24,'
    if cl.getstatus('CL9.25') == 'on':
        insertstr += '9.25,'
    if cl.getstatus('CL9.26') == 'on':
        insertstr += '9.26,'
    if cl.getstatus('CL9.27') == 'on':
        insertstr += '9.27,'
    if cl.getstatus('CL9.28') == 'on':
        insertstr += '9.28,'
    if cl.getstatus('CL10')=='on':
        insertstr+='10,'
    if cl.getstatus('CL11')=='on':
        insertstr+='11,'
    if cl.getstatus('CL12')=='on':
        insertstr+='12,'
    if cl.getstatus('CL13')=='on':
        insertstr+='13,'
    if cl.getstatus('CL14')=='on':
        insertstr+='14,'
    if cl.getstatus('CL15')=='on':
        insertstr+='15,'
    if cl.getstatus('CL15.1')=='on':
        insertstr+='15.1,'
    if cl.getstatus('CL15.2')=='on':
        insertstr+='15.2,'
    if cl.getstatus('CL15.3')=='on':
        insertstr+='15.3,'
    if cl.getstatus('CL15.4')=='on':
        insertstr+='15.4,'
    if cl.getstatus('CL15.5')=='on':
        insertstr+='15.5,'
    if cl.getstatus('CL15.6')=='on':
        insertstr+='15.6,'
    if cl.getstatus('CL15.7')=='on':
        insertstr+='15.7,'
    if cl.getstatus('CL15.8')=='on':
        insertstr+='15.8,'
    if cl.getstatus('CL15.9')=='on':
        insertstr+='15.9,'
    if cl.getstatus('CL15.10')=='on':
        insertstr+='15.10,'
    if cl.getstatus('CL16')=='on':
        insertstr+='16,'
    if cl.getstatus('CL17')=='on':
        insertstr+='17,'
    if cl.getstatus('CL17.1')=='on':
        insertstr+='17.1,'
    if cl.getstatus('CL18')=='on':
        insertstr+='18,'
    if cl.getstatus('CL18.1')=='on':
        insertstr+='18.1,'
    if cl.getstatus('CL19')=='on':
        insertstr+='19,'
    if cl.getstatus('CL19.1')=='on':
        insertstr+='19.1,'
    if cl.getstatus('CL20')=='on':
        insertstr+='20,'
    if cl.getstatus('CL20.1')=='on':
        insertstr+='20.1,'
    if cl.getstatus('CL20.2')=='on':
        insertstr+='20.2,'
    if cl.getstatus('CL20.3')=='on':
        insertstr+='20.3,'
    if cl.getstatus('CL20.4')=='on':
        insertstr+='20.4,'
    if cl.getstatus('CL20.5')=='on':
        insertstr+='20.5,'
    if cl.getstatus('CL20.6')=='on':
        insertstr+='20.6,'
    if cl.getstatus('CL20.7')=='on':
        insertstr+='20.7,'
    if cl.getstatus('CL20.8')=='on':
        insertstr+='20.8,'
    if cl.getstatus('CL20.9')=='on':
        insertstr+='20.9,'
    if cl.getstatus('CL20.10')=='on':
        insertstr+='20.10,'
    if cl.getstatus('CL20.11')=='on':
        insertstr+='20.11,'
    if cl.getstatus('CL20.12')=='on':
        insertstr+='20.12,'
    if cl.getstatus('CL20.13')=='on':
        insertstr+='20.13,'
    if cl.getstatus('CL20.14')=='on':
        insertstr+='20.14,'
    if cl.getstatus('CL20.15')=='on':
        insertstr+='20.15,'
    if cl.getstatus('CL20.16')=='on':
        insertstr+='20.16,'
    if cl.getstatus('CL20.17')=='on':
        insertstr+='20.17,'
    if cl.getstatus('CL20.18')=='on':
        insertstr+='20.18,'
    if cl.getstatus('CL20.19')=='on':
        insertstr+='20.19,'
    if cl.getstatus('CL20.20')=='on':
        insertstr+='20.20,'
    if cl.getstatus('CL20.21')=='on':
        insertstr+='20.21,'
    if cl.getstatus('CL20.22')=='on':
        insertstr+='20.22,'
    if cl.getstatus('CL20.23')=='on':
        insertstr+='20.23,'
    if cl.getstatus('CL20.24')=='on':
        insertstr+='20.24,'
    if cl.getstatus('CL21')=='on':
        insertstr+='21,'
    
    insertstr+="\n"
    
    t.insert(END,insertstr)
    
    
# Function to send CIP requests depending on what is checked
def execute_eip(sock,reg_sess,compare_sel,z,scanner,example_handler):
    
    global reqsRan
    global checksize
    global runAndCompare
    
    global compares
    global passes
    global fails

    global status

    
    #Initialize the flags that indicate the result of a test
    test1=0
    test2=0
    test3=0
    test4=0
    test5=0
    test6=0
    test7=0
    test8=0
    test9=0
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
    
    insertstr = "\nExecuting cases "
    
    if cl.getstatus('CL1')=='on':
        insertstr+="1,"
    if cl.getstatus('CL2')=='on':
        insertstr+="2,"
    if cl.getstatus('CL3')=='on':
        insertstr+="3,"
    if cl.getstatus('CL4')=='on':
        insertstr+="4,"
    if cl.getstatus('CL4.1')=='on':
        insertstr+="4.1,"
    if cl.getstatus('CL4.2')=='on':
        insertstr+="4.2,"
    if cl.getstatus('CL4.3')=='on':
        insertstr+="4.3,"
    if cl.getstatus('CL4.4')=='on':
        insertstr+="4.4,"
    if cl.getstatus('CL4.5')=='on':
        insertstr+="4.5,"
    if cl.getstatus('CL4.6')=='on':
        insertstr+="4.6,"
    if cl.getstatus('CL4.7')=='on':
        insertstr+="4.7,"
    if cl.getstatus('CL4.8')=='on':
        insertstr+="4.8,"
    if cl.getstatus('CL4.9')=='on':
        insertstr+="4.9,"
    if cl.getstatus('CL4.10')=='on':
        insertstr+="4.10,"
    if cl.getstatus('CL4.11')=='on':
        insertstr+="4.11,"
    if cl.getstatus('CL4.12')=='on':
        insertstr+="4.12,"
    if cl.getstatus('CL4.13')=='on':
        insertstr+="4.13,"
    if cl.getstatus('CL4.14')=='on':
        insertstr+="4.14,"
    if cl.getstatus('CL4.15')=='on':
        insertstr+="4.15,"
    if cl.getstatus('CL4.16')=='on':
        insertstr+="4.16,"
    if cl.getstatus('CL4.17')=='on':
        insertstr+="4.17,"
    if cl.getstatus('CL5')=='on':
        insertstr+="5,"
    if cl.getstatus('CL6')=='on':
        insertstr+='6,'
    if cl.getstatus('CL7')=='on':
        insertstr+='7,'
    if cl.getstatus('CL8')=='on':
        insertstr+='8,'
    if cl.getstatus('CL9')=='on':
        insertstr+='9,'
    if cl.getstatus('CL9') == 'on':
        insertstr += '9.1,'
    if cl.getstatus('CL9.2') == 'on':
        insertstr += '9.2,'
    if cl.getstatus('CL9.3') == 'on':
        insertstr += '9.3,'
    if cl.getstatus('CL9.4') == 'on':
        insertstr += '9.4,'
    if cl.getstatus('CL9.5') == 'on':
        insertstr += '9.5,'
    if cl.getstatus('CL9.6') == 'on':
        insertstr += '9.6,'
    if cl.getstatus('CL9.7') == 'on':
        insertstr += '9.7,'
    if cl.getstatus('CL9.8') == 'on':
        insertstr += '9.8,'
    if cl.getstatus('CL9.9') == 'on':
        insertstr += '9.9,'
    if cl.getstatus('CL9.10') == 'on':
        insertstr += '9.10,'
    if cl.getstatus('CL9.11') == 'on':
        insertstr += '9.11,'
    if cl.getstatus('CL9.12') == 'on':
        insertstr += '9.12,'
    if cl.getstatus('CL9.13') == 'on':
        insertstr += '9.13,'
    if cl.getstatus('CL9.14') == 'on':
        insertstr += '9.14,'
    if cl.getstatus('CL9.15') == 'on':
        insertstr += '9.15,'
    if cl.getstatus('CL9.16') == 'on':
        insertstr += '9.16,'
    if cl.getstatus('CL9.17') == 'on':
        insertstr += '9.17,'
    if cl.getstatus('CL9.18') == 'on':
        insertstr += '9.18,'
    if cl.getstatus('CL9.19') == 'on':
        insertstr += '9.19,'
    if cl.getstatus('CL9.20') == 'on':
        insertstr += '9.20,'
    if cl.getstatus('CL9.21') == 'on':
        insertstr += '9.21,'
    if cl.getstatus('CL9.22') == 'on':
        insertstr += '9.22,'
    if cl.getstatus('CL9.23') == 'on':
        insertstr += '9.23,'
    if cl.getstatus('CL9.24') == 'on':
        insertstr += '9.24,'
    if cl.getstatus('CL9.25') == 'on':
        insertstr += '9.25,'
    if cl.getstatus('CL9.26') == 'on':
        insertstr += '9.26,'
    if cl.getstatus('CL9.27') == 'on':
        insertstr += '9.27,'
    if cl.getstatus('CL9.28') == 'on':
        insertstr += '9.28,'
    if cl.getstatus('CL10')=='on':
        insertstr+='10,'
    if cl.getstatus('CL11')=='on':
        insertstr+='11,'
    if cl.getstatus('CL12')=='on':
        insertstr+='12,'
    if cl.getstatus('CL13')=='on':
        insertstr+='13,'
    if cl.getstatus('CL14')=='on':
        insertstr+='14,'
    if cl.getstatus('CL15')=='on':
        insertstr+='15,'
    if cl.getstatus('CL15.1')=='on':
        insertstr+='15.1,'
    if cl.getstatus('CL15.2')=='on':
        insertstr+='15.2,'
    if cl.getstatus('CL15.3')=='on':
        insertstr+='15.3,'
    if cl.getstatus('CL15.4')=='on':
        insertstr+='15.4,'
    if cl.getstatus('CL15.5')=='on':
        insertstr+='15.5,'
    if cl.getstatus('CL15.6')=='on':
        insertstr+='15.6,'
    if cl.getstatus('CL15.7')=='on':
        insertstr+='15.7,'
    if cl.getstatus('CL15.8')=='on':
        insertstr+='15.8,'
    if cl.getstatus('CL15.9')=='on':
        insertstr+='15.9,'
    if cl.getstatus('CL15.10')=='on':
        insertstr+='15.10,'
    if cl.getstatus('CL16')=='on':
        insertstr+='16,'
    if cl.getstatus('CL17')=='on':
        insertstr+='17,'
    if cl.getstatus('CL17.1')=='on':
        insertstr+='17.1,'
    if cl.getstatus('CL18')=='on':
        insertstr+='18,'
    if cl.getstatus('CL18.1')=='on':
        insertstr+='18.1,'
    if cl.getstatus('CL19')=='on':
        insertstr+='19,'
    if cl.getstatus('CL19.1')=='on':
        insertstr+='19.1,'
    if cl.getstatus('CL20')=='on':
        insertstr+='20,'
    if cl.getstatus('CL20.1')=='on':
        insertstr+='20.1,'
    if cl.getstatus('CL20.2')=='on':
        insertstr+='20.2,'
    if cl.getstatus('CL20.3')=='on':
        insertstr+='20.3,'
    if cl.getstatus('CL20.4')=='on':
        insertstr+='20.4,'
    if cl.getstatus('CL20.5')=='on':
        insertstr+='20.5,'
    if cl.getstatus('CL20.6')=='on':
        insertstr+='20.6,'
    if cl.getstatus('CL20.7')=='on':
        insertstr+='20.7,'
    if cl.getstatus('CL20.8')=='on':
        insertstr+='20.8,'
    if cl.getstatus('CL20.9')=='on':
        insertstr+='20.9,'
    if cl.getstatus('CL20.10')=='on':
        insertstr+='20.10,'
    if cl.getstatus('CL20.11')=='on':
        insertstr+='20.11,'
    if cl.getstatus('CL20.12')=='on':
        insertstr+='20.12,'
    if cl.getstatus('CL20.13')=='on':
        insertstr+='20.13,'
    if cl.getstatus('CL20.14')=='on':
        insertstr+='20.14,'
    if cl.getstatus('CL20.15')=='on':
        insertstr+='20.15,'
    if cl.getstatus('CL20.16')=='on':
        insertstr+='20.16,'
    if cl.getstatus('CL20.17')=='on':
        insertstr+='20.17,'
    if cl.getstatus('CL20.18')=='on':
        insertstr+='20.18,'
    if cl.getstatus('CL20.19')=='on':
        insertstr+='20.19,'
    if cl.getstatus('CL20.20')=='on':
        insertstr+='20.20,'
    if cl.getstatus('CL20.21')=='on':
        insertstr+='20.21,'
    if cl.getstatus('CL20.22')=='on':
        insertstr+='20.22,'
    if cl.getstatus('CL20.23')=='on':
        insertstr+='20.23,'
    if cl.getstatus('CL20.24')=='on':
        insertstr+='20.24,'
    if cl.getstatus('CL21')=='on':
        insertstr+='21,'

    insertstr+="\n"
    
    t.insert(END,insertstr)
    
    if cl.getstatus('CL23') == 'on':

        input_file = open("input.txt",'r')
        input_lines = input_file.readlines()

        for line in input_lines:

            line_split = line.split(",")

            reqsRan += 1

            # Ask the user for the service, class, instance, and attribute to build the request packet
            service_req = line_split[0]
            class_req = line_split[1]
            instance_req = line_split[2]
            try:
                attribute_req = line_split[3]
                attribute_req = struct.pack('B', int(attribute_req, 16))
            except IndexError:
                attribute_req = ''

            # Convert the input into byte strings
            service_req = struct.pack('B', int(service_req, 16))
            if len(class_req) > 2:
                class_req = struct.pack('<H', int(class_req, 16))
            else:
                class_req = struct.pack('B', int(class_req, 16))
            if len(instance_req) > 2:
                instance_req = struct.pack('<H', int(instance_req, 16))
            else:
                instance_req = struct.pack('B', int(instance_req, 16))


            outputstr = ""

            outputstr += "\n(22) Custom request\n"
            try:
                outputstr += "Service = " + line_split[0] + ",Class = " + line_split[1] + ",Instance = " + line_split[2] + ",Attribute = " + line_split[3] + "\n"
            except IndexError:
                outputstr += "Service = " + line_split[0] + ",Class = " + line_split[1] + ",Instance = " + line_split[
                    2] + ",Attribute = " + '' + "\n"

            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    attribute_req)

            t.insert(END, outputstr)
            bold_response()
            outputstr = ''



        input_file.close()

    #Custom CIP request
    if cl.getstatus('CL22')=='on':

        reqsRan+=1
    
        #Ask the user for the service, class, instance, and attribute to build the request packet
        service_req = service_ent.get()
        class_req = class_ent.get()
        instance_req = instance_ent.get()
        attribute_req = attribute_ent.get()



        #Convert the input into byte strings
        service_req = struct.pack('B', int(service_req, 16))
        if len(class_req) > 2:
            class_req = struct.pack('<H', int(class_req, 16))
        else:
            class_req = struct.pack('B', int(class_req, 16))
        if len(instance_req) > 2:
            instance_req = struct.pack('<H', int(instance_req, 16))
        else:
            instance_req = struct.pack('B', int(instance_req, 16))

        if attribute_req != '':
            attribute_req = struct.pack('B', int(attribute_req, 16))
        
        caseFound = 0
        if service_req == b'\x0e' and class_req == b'\x00\x03' and instance_req == b'\x01' and attribute_req == b'\x01':
            cl.setstatus("CL1","on")
            caseFound = 1
            t.insert(END,"Custom is case 1")
        elif service_req == b'\x01' and class_req == b'\x01\x03':
            cl.setstatus("CL2","on")
            caseFound = 1
            t.insert(END,"Custom is case 2")
        elif service_req == b'\x01' and class_req == b'\x02\x03' and instance_req == b'\x01' and attribute_req == b'\x01':
            cl.setstatus("CL3","on")
            caseFound = 1
            t.insert(END,"Custom is case 3")
        elif service_req == b'\x01' and class_req == b'\x50\x03' and instance_req == b'\x01' and attribute_req == b'\x01':
            cl.setstatus("CL4","on")
            caseFound = 1
            t.insert(END,"Custom is case 4")
        
        
        if caseFound == 0:
        
            outputstr=""
            
            outputstr+="\n(22) Custom request\n"
            outputstr+="Service = "+service_ent.get()+",Class = "+class_ent.get()+",Instance = "+instance_ent.get()+",Attribute = "+attribute_ent.get()+"\n"
            
            outputstr,cip_res = requestsendreceive(outputstr,sock, reg_sess, service_req, class_req, instance_req, attribute_req)
            
            t.insert(END,outputstr)
            bold_response()
            outputstr=''

    
    #Run the tests depending on which checkboxes are checked
        
    if cl.getstatus('CL1')=='on':
        
        reqsRan+=1
        
       # if runall==1:
       #     selection='2'
        outputstr=""
        outputstr+="\n(1) Module Diagnostic object (0x300)\n"
        
        #Initialize service, class, instance, and attribute for the request
        service_req = b'\x0e'
        class_req = b'\x00\x03'
        instance_req = b'\x01'
        attribute_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req, attribute_req)

        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        #Check if byte 43 is 00 to indicate success
        if cip_res[42] == 0:
            test1=1
            outputstr+="\nTest Passed"
        else:
            test1=2
            outputstr+="\nTest Failed"
            
        getalllen = len(cip_res[44:])
            
        
            
            
        #Insert the string we created into the end of the textbox
        t.insert(END,outputstr)
        color_test(test1)
        
    if cl.getstatus('CL2')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(2) Scanner Diagnostic object (0x301)\n"

        service_req = b'\x01'
        class_req = b'\x01\x03'
        if instance_ent.get() == "":
            instance_req = b'\x11\x01'
        else:
            instance_req = instance_ent.get()
            if len(instance_req) > 2:
                instance_req = struct.pack('<H', int(instance_req, 16))
            else:
                instance_req = struct.pack('B', int(instance_req, 16))
        attribute_req = ''


        outputstr,cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 5:
            instance_req = b'\x01\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        
        if cip_res[42] == 0:
            test2=1
            outputstr+="\nTest Passed"
        else:
            test2=2
            outputstr+="\nTest Failed"
        
        
        
        t.insert(END,outputstr)
        color_test(test2)
        
    if cl.getstatus('CL3')=='on':

        reqsRan+=1

        outputstr=""
        outputstr+="\n(3) Adapter Diagnostic object (0x302)\n"

        service_req = b'\x01'
        class_req = b'\x02\x03'
        instance_req = b'\x01'
        attribute_req = b'\x01'


        #example_cip_object = CipObject(Service.get_attributes_all, class_=0x302)


        #scanner.send_unconnected(dest_addr=TCP_IP.get(), cip_object=example_cip_object)


        #example_handler.example_response_event.wait()



        outputstr,cip_res = requestsendreceive(outputstr,sock, reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test3=1
            outputstr+="\nTest Passed"
        else:
            test3=2
            outputstr+="\nTest Failed"
        
        
        
        t.insert(END,outputstr)
        color_test(test3)
        
    if cl.getstatus('CL4')=='on':

        if z == 0 or runAndCompare_var == 1:
        
            reqsRan+=1
        
            outputstr=""
            outputstr+="\n(4) Ethernet Interface Diagnostic object (0x350)\n"

            service_req = b'\x01'
            class_req = b'\x50\x03'
            instance_req = b'\x01'
            attribute_req = b'\x01'
            
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)

            t.insert(END,outputstr)
            bold_response()
            outputstr=''
            
            if cip_res[42] == 0:
                test4=1
                outputstr+="\nTest Passed"
            else:
                test4=2
                outputstr+="\nTest Failed"
            
            t.insert(END,outputstr)
            color_test(test4)
            outputstr=''
            
            
            if checksize==1 and test4==1:
                
                getalllen=len(cip_res[44:])
                service_req = b'\x0e'
                
                
                attribute_req = b'\x01'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen=len(cip_res[44:])
                
                attribute_req = b'\x02'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req = b'\x03'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req = b'\x04'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                
                if getalllen == getsinglelen:
                    test4=1
                    outputstr+="\nSizes Match"
                else:
                    test4=2
                    outputstr+="\nSizes Don't Match"
                
                t.insert(END,outputstr)
                color_test(test4)
            
            
            
            elif test4==1:
            
                global protocolssupported
                protocolssupported = struct.unpack("<H",cip_res[44:46])
                outputstr+= "\nAttr 1: Protocols supported = " + str(protocolssupported[0])
                
                global maxcipioconnsopened
                maxcipioconnsopened = struct.unpack("<H",cip_res[46:48])
                outputstr+= "\nAttr 2 (Connection Diag): Max CIP IO Connection opened = " + str(maxcipioconnsopened[0])
                
                global currentcipioconns
                currentcipioconns = struct.unpack("<H",cip_res[48:50])
                outputstr+= "\nAttr 2: Current CIP IO Connections = " + str(currentcipioconns[0])
                
                global maxcipexpconnsopened
                maxcipexpconnsopened = struct.unpack("<H",cip_res[50:52])
                outputstr+= "\nAttr 2: Max CIP Explicit Connections = " + str(maxcipexpconnsopened[0])
                
                global currentcipexpconns
                currentcipexpconns = struct.unpack("<H",cip_res[52:54])
                outputstr+= "\nAttr 2: Current CIP Explicit Connections = " + str(currentcipexpconns[0])
                
                global cipconnsopeningerrors
                cipconnsopeningerrors = struct.unpack("<H",cip_res[54:56])
                outputstr+= "\nAttr 2: CIP Connections Opening Errors = " + str(cipconnsopeningerrors[0])
                
                global cipconnstimeouterrors
                cipconnstimeouterrors = struct.unpack("<H",cip_res[56:58])
                outputstr+= "\nAttr 2: CIP Connections Timeout Errors = " + str(cipconnstimeouterrors[0])
                
                global maxeiptcpconnsopened
                maxeiptcpconnsopened = struct.unpack("<H",cip_res[58:60])
                outputstr+= "\nAttr 2: Max EIP TCP Connections opened = " + str(maxeiptcpconnsopened[0])
                

                
                global currenteiptcpconns
                currenteiptcpconns = struct.unpack("<H",cip_res[60:62])
                outputstr+= "\nAttr 2: Current EIP TCP Connections = " + str(currenteiptcpconns[0])
                
                global ioproductionctr
                ioproductionctr = struct.unpack("<I",cip_res[62:66])
                outputstr+= "\nAttr 3 (IO Messaging Diag): IO Production Counter = " + str(ioproductionctr[0])
                
                global ioconsumptionctr
                ioconsumptionctr = struct.unpack("<I",cip_res[66:70])
                outputstr+= "\nAttr 3: IO Consumption Counter = " + str(ioconsumptionctr[0])
                
                global ioproductionsenderrorsctr
                ioproductionsenderrorsctr = struct.unpack("<H",cip_res[70:72])
                outputstr+= "\nAttr 3: IO Production Send Errors Counter = " + str(ioproductionsenderrorsctr[0])
                
                global ioconsumptionrecverrorsctr
                ioconsumptionrecverrorsctr = struct.unpack("<H",cip_res[72:74])
                outputstr+= "\nAttr 3: IO Consumption Receive Errors Counter = " + str(ioconsumptionrecverrorsctr[0])
                
                global class3msgsendctr
                class3msgsendctr = struct.unpack("<I",cip_res[74:78])
                outputstr+= "\nAttr 4 (Explicit Messaging Diag): Class 3 Msg Send Counter = " + str(class3msgsendctr[0])
                
                global class3msgrecvctr
                class3msgrecvctr = struct.unpack("<I",cip_res[78:82])
                outputstr+= "\nAttr 4: Class 3 Msg Receive Counter = " + str(class3msgrecvctr[0])
                
                global ucmmmsgsendctr
                ucmmmsgsendctr = struct.unpack("<I",cip_res[82:86])
                outputstr+= "\nAttr 4: UCMM Msg Send Counter = " + str(ucmmmsgsendctr[0])
                
                global ucmmmsgrecvctr
                ucmmmsgrecvctr = struct.unpack("<I",cip_res[86:90])
                outputstr+= "\nAttr 4: UCMM Msg Receive Counter = " + str(ucmmmsgrecvctr[0])
                
                outputstr+='\n'
                t.insert(END,outputstr)
                
            
        insertstr=''
        found=0
        
        if comparefile_op.get() == '1':
        
        
            if protocolssupported_file != protocolssupported[0] and "4.1" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 1: Protocols supported = " + str(protocolssupported[0])
                insertstr+="\n+Attr 1: Protocols supported = " + str(protocolssupported_file)
                
            elif protocolssupported_file == protocolssupported[0] and "4.1" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 1: Protocols supported Passed"
                
            if maxcipioconnsopened_file != maxcipioconnsopened[0] and "4.2" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2 (Connection Diag): Max CIP IO Connection opened = " + str(maxcipioconnsopened[0])
                insertstr+="\n+Attr 2 (Connection Diag): Max CIP IO Connection opened = " + str(maxcipioconnsopened_file)
                
            elif maxcipioconnsopened_file == maxcipioconnsopened[0] and "4.2" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2 (Connection Diag): Max CIP IO Connection opened Passed"
                
            if currentcipioconns_file != currentcipioconns[0] and "4.3" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: Current CIP IO Connections = " + str(currentcipioconns[0])
                insertstr+="\n+Attr 2: Current CIP IO Connections = " + str(currentcipioconns_file)
                
            elif currentcipioconns_file == currentcipioconns[0] and "4.3" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: Current CIP IO Connections Passed"
                
            if maxcipexpconnsopened_file != maxcipexpconnsopened[0] and "4.4" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: Max CIP Explicit Connections = " + str(maxcipexpconnsopened[0])
                insertstr+="\n+Attr 2: Max CIP Explicit Connections = " + str(maxcipexpconnsopened_file)
                
            elif maxcipexpconnsopened_file == maxcipexpconnsopened[0] and "4.4" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: Max CIP Explicit Connections Passed"
                
            if currentcipexpconns_file != currentcipexpconns[0] and "4.5" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: Current CIP Explicit Connections = " + str(currentcipexpconns[0])
                insertstr+="\n+Attr 2: Current CIP Explicit Connections = " + str(currentcipexpconns_file)
                
            elif currentcipexpconns_file == currentcipexpconns[0] and "4.5" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: Current CIP Explicit Connections Passed"
        
        
            if cipconnsopeningerrors_file != cipconnsopeningerrors[0] and "4.6" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: CIP Connections Opening Errors = " + str(cipconnsopeningerrors[0])
                insertstr+="\n+Attr 2: CIP Connections Opening Errors = " + str(cipconnsopeningerrors_file)
                
            elif cipconnsopeningerrors_file == cipconnsopeningerrors[0] and "4.6" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: CIP Connections Opening Errors Passed"
        
            if cipconnstimeouterrors_file != cipconnstimeouterrors[0] and "4.7" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: CIP Connections Timeout Errors = " + str(cipconnstimeouterrors[0])
                insertstr+="\n+Attr 2: CIP Connections Timeout Errors = " + str(cipconnstimeouterrors_file)
                
            elif cipconnstimeouterrors_file == cipconnstimeouterrors[0] and "4.7" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: CIP Connections Timeout Errors Passed"
            
            if maxeiptcpconnsopened_file != maxeiptcpconnsopened[0] and "4.8" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: Max EIP TCP Connections opened = " + str(maxeiptcpconnsopened[0])
                insertstr+="\n+Attr 2: Max EIP TCP Connections opened = " + str(maxeiptcpconnsopened_file)
                
            elif maxeiptcpconnsopened_file == maxeiptcpconnsopened[0] and "4.8" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: Max EIP TCP Connections opened Passed"
                
            if currenteiptcpconns_file != currenteiptcpconns[0] and "4.9" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: Current EIP TCP Connections = " + str(currenteiptcpconns[0])
                insertstr+="\n+Attr 2: Current EIP TCP Connections = " + str(currenteiptcpconns_file)
                
            elif currenteiptcpconns_file == currenteiptcpconns[0] and "4.9" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: Current EIP TCP Connections Passed"
            
            if ioproductionctr_file != ioproductionctr[0] and "4.10" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 3 (IO Messaging Diag): IO Production Counter = " + str(ioproductionctr[0])
                insertstr+="\n+Attr 3 (IO Messaging Diag): IO Production Counter = " + str(ioproductionctr_file)
                
            elif ioproductionctr_file == ioproductionctr[0] and "4.10" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 3 (IO Messaging Diag): IO Production Counter Passed"
            
            if ioconsumptionctr_file != ioconsumptionctr[0] and "4.11" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 3: IO Consumption Counter = " + str(ioconsumptionctr[0])
                insertstr+="\n+Attr 3: IO Consumption Counter = " + str(ioconsumptionctr_file)
                
            elif ioconsumptionctr_file == ioconsumptionctr[0] and "4.11" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 3: IO Consumption Counter Passed"
            
            if ioproductionsenderrorsctr_file != ioproductionsenderrorsctr[0] and "4.12" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 3: IO Production Send Errors Counter = " + str(ioproductionsenderrorsctr[0])
                insertstr+="\n+Attr 3: IO Production Send Errors Counter = " + str(ioproductionsenderrorsctr_file)
                
            elif ioproductionsenderrorsctr_file == ioproductionsenderrorsctr[0] and "4.12" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 3: IO Production Send Errors Counter Passed"
            
            if ioconsumptionrecverrorsctr_file != ioconsumptionrecverrorsctr[0] and "4.13" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 3: IO Consumption Receive Errors Counter = " + str(ioconsumptionrecverrorsctr[0])
                insertstr+="\n+Attr 3: IO Consumption Receive Errors Counter = " + str(ioconsumptionrecverrorsctr_file)
                
            elif ioconsumptionrecverrorsctr_file == ioconsumptionrecverrorsctr[0] and "4.13" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 3: IO Consumption Receive Errors Counter Passed"
            
            if class3msgsendctr_file != class3msgsendctr[0] and "4.14" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 4 (Explicit Messaging Diag): Class 3 Msg Send Counter = " + str(class3msgsendctr[0])
                insertstr+="\n+Attr 4 (Explicit Messaging Diag): Class 3 Msg Send Counter = " + str(class3msgsendctr_file)
                
            elif class3msgsendctr_file == class3msgsendctr[0] and "4.14" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 4 (Explicit Messaging Diag): Class 3 Msg Send Counter Passed"
            
            if class3msgrecvctr_file != class3msgrecvctr[0] and "4.15" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 4: Class 3 Msg Receive Counter = " + str(class3msgrecvctr[0])
                insertstr+="\n+Attr 4: Class 3 Msg Receive Counter = " + str(class3msgrecvctr_file)
                
            elif class3msgrecvctr_file == class3msgrecvctr[0] and "4.15" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 4: Class 3 Msg Receive Counter Passed"
            
            if ucmmmsgsendctr_file != ucmmmsgsendctr[0] and "4.16" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 4: UCMM Msg Send Counter = " + str(ucmmmsgsendctr[0])
                insertstr+="\n+Attr 4: UCMM Msg Send Counter = " + str(ucmmmsgsendctr_file)
                
            elif ucmmmsgsendctr_file == ucmmmsgsendctr[0] and "4.16" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 4: UCMM Msg Send Counter Passed"
            
            if ucmmmsgrecvctr_file != ucmmmsgrecvctr[0] and "4.17" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 4: UCMM Msg Receive Counter = " + str(ucmmmsgrecvctr[0])
                insertstr+="\n+Attr 4: UCMM Msg Receive Counter = " + str(ucmmmsgrecvctr_file)
                
            elif ucmmmsgrecvctr_file == ucmmmsgrecvctr[0] and "4.17" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 4: UCMM Msg Receive Counter Passed"
            
            
            

        if found == 1:
            insertstr+="\n\nCompares = "+str(compares)+"\nPasses = "+str(passes)+"\nFails = "+str(fails)+"\n"
            insertstr= "\n(4) Ethernet Interface Diagnostic object (0x350)\n"+insertstr
            t2.insert(END,insertstr)
            
            
        
    if cl.getstatus('CL5')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(5) IOScanner Diagnostic object (0x351)\n"

        service_req = b'\x0e'
        class_req = b'\x51\x03'
        instance_req = b'\x01'
        attribute_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test5=1
            outputstr+="\nTest Passed"
        else:
            test5=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test5)
        outputstr=''
        
        
        if checksize==1 and test5==1:
            
            getalllen=len(cip_res[44:])
            service_req = b'\x0e'
            
            
            attribute_req = b'\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen=len(cip_res[44:])
            
            if getalllen == getsinglelen:
                test5=1
                outputstr+="\nSizes Match"
            else:
                test5=2
                outputstr+="\nSizes Don't Match"
            
            t.insert(END,outputstr)
            color_test(test5)
        
        
        elif test5==1:
        
            size = struct.unpack("<H",cip_res[44:46])
            outputstr+="\nAttr 1: IO Status Table: Size = "+str(size[0])

            global status1
            status1 = struct.unpack("<"+str(int(size[0]/2))+"H",cip_res[46:(size[0]+46)])
            outputstr+="\nAttr 1: Status = " + str(status1)
            
            outputstr+='\n'
            t.insert(END,outputstr)
        
    if cl.getstatus('CL6')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(6) EIP I/O Connection Diagnostic object (0x352)\n"

        service_req = b'\x01'
        class_req = b'\x52\x03'
        if instance_ent.get() == "":
            instance_req = b'\x11\x01'
        else:
            instance_req = instance_ent.get()
            if len(instance_req) > 2:
                instance_req = struct.pack('<H', int(instance_req, 16))
            else:
                instance_req = struct.pack('B', int(instance_req, 16))
        attribute_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        
        if cip_res[42] == 5:
            instance_req = b'\x01\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test6=1
            outputstr+="\nTest Passed"
        else:
            test6=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test6)
        outputstr=''
        
        
        if checksize==1 and test6==1:
            
            getalllen=len(cip_res[44:])
            service_req = b'\x0e'
            
            
            attribute_req = b'\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen=len(cip_res[44:])

            attribute_req=b'\x02'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
        
            if getalllen == getsinglelen:
                test6=1
                outputstr+="\nSizes Match"
            else:
                test6=2
                outputstr+="\nSizes Don't Match"
            
            t.insert(END,outputstr)
            color_test(test6)
        
        elif test6==1:
        
            ioprodctr = struct.unpack("<I",cip_res[44:48])
            outputstr+= "\nAttr 1 (IO Com Diag): IO Production Counter = " + str(ioprodctr[0])
            
            ioconsctr = struct.unpack("<I",cip_res[48:52])
            outputstr+= "\nAttr 1: IO Consumption Counter = " + str(ioconsctr[0])
            
            ioprodsenderrsctr = struct.unpack("<H",cip_res[52:54])
            outputstr+= "\nAttr 1: IO Production Send Errors Counter = " + str(ioprodsenderrsctr[0])
            
            ioconsrecverrsctr = struct.unpack("<H",cip_res[54:56])
            outputstr+= "\nAttr 1: IO Consumption Receive Errors Counter = " + str(ioconsrecverrsctr[0])
            
            cipconntimeouterrs = struct.unpack("<H",cip_res[56:58])
            outputstr+= "\nAttr 1: CIP Connection TimeOut Errors = " + str(cipconntimeouterrs[0])
            
            cipconnopeningerrs = struct.unpack("<H",cip_res[58:60])
            outputstr+= "\nAttr 1: CIP Connection Opening Errors = " + str(cipconnopeningerrs[0])
            
            cipconnstate = struct.unpack("<H",cip_res[60:62])
            outputstr+= "\nAttr 1: CIP Connection State = " + str(cipconnstate[0])
            
            ciplasterrgenstatus = struct.unpack("<H",cip_res[62:64])
            outputstr+= "\nAttr 1: CIP Last Error General Status = " + str(ciplasterrgenstatus[0])
            
            ciplasterrextstatus = struct.unpack("<H",cip_res[64:66])
            outputstr+= "\nAttr 1: CIP Last Error Extended Status = " + str(ciplasterrextstatus[0])
            
            inputcomstatus = struct.unpack("<H",cip_res[66:68])
            outputstr+= "\nAttr 1: Input Com Status = " + str(inputcomstatus[0])
            
            outputcomstatus = struct.unpack("<H",cip_res[68:70])
            outputstr+= "\nAttr 1: Output Com Status = " + str(outputcomstatus[0])
            
            prodconnid = struct.unpack("<I",cip_res[70:74])
            outputstr+= "\nAttr 2 (Connection Diag): Production Connection ID = " + str(prodconnid[0])
            
            consconnid = struct.unpack("<I",cip_res[74:78])
            outputstr+= "\nAttr 2: Consumption Connection ID = " + str(consconnid[0])
            
            prodrpi = struct.unpack("<I",cip_res[78:82])
            outputstr+= "\nAttr 2: Production RPI = " + str(prodrpi[0])
            
            prodapi = struct.unpack("<I",cip_res[82:86])
            outputstr+= "\nAttr 2: Production API = " + str(prodapi[0])
            
            consrpi = struct.unpack("<I",cip_res[86:90])
            outputstr+= "\nAttr 2: Consumption RPI = " + str(consrpi[0])
            
            consapi = struct.unpack("<I",cip_res[90:94])
            outputstr+= "\nAttr 2: Consumption API = " + str(consapi[0])
            
            prodconnpara = struct.unpack("<I",cip_res[94:98])
            outputstr+= "\nAttr 2: Production Connection Parameters = " + str(prodconnpara[0])
            
            consconnpara = struct.unpack("<I",cip_res[98:102])
            outputstr+= "\nAttr 2: Consumption Connection Parameters = " + str(consconnpara[0])
            
            localip = struct.unpack("<I",cip_res[102:106])
            outputstr+= "\nAttr 2: Local IP = " + str(localip[0])
            
            localudpport = struct.unpack("<H",cip_res[106:108])
            outputstr+= "\nAttr 2: Local UDP Port = " + str(localudpport[0])
            
            remoteip = struct.unpack("<I",cip_res[108:112])
            outputstr+= "\nAttr 2: Remote IP = " + str(remoteip[0])
            
            remoteudpport = struct.unpack("<H",cip_res[112:114])
            outputstr+= "\nAttr 2: Remote UDP Port = " + str(remoteudpport[0])
            
            prodmulticastip = struct.unpack("<I",cip_res[114:118])
            outputstr+= "\nAttr 2: Production Multicast IP = " + str(prodmulticastip[0])
            
            consmulticastip = struct.unpack("<I",cip_res[118:122])
            outputstr+= "\nAttr 2: Consumption Multicast IP = " + str(consmulticastip[0])
            
            protocolssupported = struct.unpack("<H",cip_res[122:124])
            outputstr+= "\nAttr 2: Protocols supported = " + str(protocolssupported[0])
            
            
            
            outputstr+='\n'
            t.insert(END,outputstr)
        
        
    if cl.getstatus('CL7')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(7) EIP Explicit Connection Diagnostic object (0x353)\n"

        service_req = b'\x01'
        class_req = b'\x53\x03'
        instance_req = b'\x01'
        attribute_req = ''
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test7=1
            outputstr+="\nTest Passed"
        else:
            test7=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test7)
        outputstr=''
        
        
        if checksize==1 and test7==1:
            
            getalllen=len(cip_res[44:])
            service_req = b'\x0e'
            
            
            attribute_req = b'\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen=len(cip_res[44:])

            attribute_req=b'\x02'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x03'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x04'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x05'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x06'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x07'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x08'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])

            if getalllen == getsinglelen:
                test7=1
                outputstr+="\nSizes Match"
            else:
                test7=2
                outputstr+="\nSizes Don't Match"
            
            t.insert(END,outputstr)
            color_test(test7)
        
        elif test7==1:
        
            origconnid = struct.unpack("<I",cip_res[44:48])
            outputstr+= "\nAttr 1: Originator Connection ID = " + str(origconnid[0])
            
            origip = struct.unpack("<I",cip_res[48:52])
            outputstr+= "\nAttr 2: Originator IP = " + str(origip[0])
            
            origtcpport = struct.unpack("<H",cip_res[52:54])
            outputstr+= "\nAttr 3: Originator TCP Port = " + str(origtcpport[0])
            
            targetconnid = struct.unpack("<I",cip_res[54:58])
            outputstr+= "\nAttr 4: Target Connection ID = " + str(targetconnid[0])
            
            targetip = struct.unpack("<I",cip_res[58:62])
            outputstr+= "\nAttr 5: Target IP = " + str(targetip[0])
            
            targettcpport = struct.unpack("<H",cip_res[62:64])
            outputstr+= "\nAttr 6: Target TCP Port = " + str(targettcpport[0])
            
            msgsendctr = struct.unpack("<I",cip_res[64:68])
            outputstr+= "\nAttr 7: Msg Send Counter = " + str(msgsendctr[0])
            
            msgrecvctr = struct.unpack("<I",cip_res[68:72])
            outputstr+= "\nAttr 8: Msg Receive Counter = " + str(msgrecvctr[0])
        
        
        
        
        
        
            outputstr+='\n'
            t.insert(END,outputstr)
        
    if cl.getstatus('CL8')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(8) EIP Explicit Connection List object (0x354)\n"

        service_req = b'\x0e'
        class_req = b'\x54\x03'
        instance_req = b'\x01'
        attribute_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test8=1
            outputstr+="\nTest Passed"
        else:
            test8=2
            outputstr+="\nTest Failed"
        
        
        t.insert(END,outputstr)
        color_test(test8)
        
    if cl.getstatus('CL9')=='on':

        if z == 0 or runAndCompare_var == 1:

            reqsRan+=1

            outputstr=""
            outputstr+="\n(9) RSTP Diagnostic object (0x355)\n"

            service_req = b'\x01'
            class_req = b'\x55\x03'
            instance_req = b'\x01'
            attribute_req = ''

            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)

            t.insert(END,outputstr)
            bold_response()
            outputstr=''

            if cip_res[42] == 0:
                test9=1
                outputstr+="\nTest Passed"
            else:
                test9=2
                outputstr+="\nTest Failed"

            t.insert(END,outputstr)
            color_test(test9)
            outputstr=''

            if test9==1:

                protocolspec = struct.unpack("<H",cip_res[44:46])
                outputstr+= "\nAttr 1 (Switch Status): Protocol Specification = " + str(protocolspec[0])

                bridgepriority = struct.unpack("<I",cip_res[46:50])
                outputstr+= "\nAttr 1: Bridge Priority = " + str(bridgepriority[0])

                timesincetopchange = struct.unpack("<I",cip_res[50:54])
                outputstr+= "\nAttr 1: Time Since Topology Change = " + str(timesincetopchange[0])

                topchangecount = struct.unpack("<I",cip_res[54:58])
                outputstr+= "\nAttr 1: Topology Change Count = " + str(topchangecount[0])

                desrootsize = struct.unpack("<H",cip_res[58:60])
                desroot = struct.unpack(str(desrootsize[0])+"B",cip_res[60:60+desrootsize[0]])
                outputstr+= "\nAttr 1: Designated Root = "

                for x in range(0,len(desroot)):
                    outputstr+= str(hex(desroot[x])[2:]) + " "

                newstart = 60+ desrootsize[0]
                rootcost = struct.unpack("<I",cip_res[newstart:newstart+4])
                outputstr+= "\nAttr 1: Root Cost = " + str(rootcost[0])

                rootport = struct.unpack("<I",cip_res[newstart+4:newstart+8])
                outputstr+= "\nAttr 1: Root Port = " + str(rootport[0])

                maxage = struct.unpack("<H",cip_res[newstart+8:newstart+10])
                outputstr+= "\nAttr 1: Max Age = " + str(maxage[0])

                hellotime = struct.unpack("<H",cip_res[newstart+10:newstart+12])
                outputstr+= "\nAttr 1: Hello Time = " + str(hellotime[0])

                holdtime = struct.unpack("<I",cip_res[newstart+12:newstart+16])
                outputstr+= "\nAttr 1: Hold Time = " + str(holdtime[0])

                forwarddelay = struct.unpack("<H",cip_res[newstart+16:newstart+18])
                outputstr+= "\nAttr 1: Forward Delay = " + str(forwarddelay[0])

                bridgemaxage = struct.unpack("<H",cip_res[newstart+18:newstart+20])
                outputstr+= "\nAttr 1: Bridge Max Age = " + str(bridgemaxage[0])

                bridgehellotime = struct.unpack("<H",cip_res[newstart+20:newstart+22])
                outputstr+= "\nAttr 1: Bridge Hello Time = " + str(bridgehellotime[0])

                bridgeforwarddelay = struct.unpack("<H",cip_res[newstart+22:newstart+24])
                outputstr+= "\nAttr 1: Bridge Forward Delay = " + str(bridgeforwarddelay[0])

                rstpport = struct.unpack("<I",cip_res[newstart+24:newstart+28])
                outputstr+= "\nAttr 2 (Port Status): Port = " + str(rstpport[0])

                rstppriority = struct.unpack("<I",cip_res[newstart+28:newstart+32])
                outputstr+= "\nAttr 2: Priority = " + str(rstppriority[0])

                rstpstate = struct.unpack("<H",cip_res[newstart+32:newstart+34])
                outputstr+= "\nAttr 2: State = " + str(rstpstate[0])

                rstpenable = struct.unpack("<H",cip_res[newstart+34:newstart+36])
                outputstr+= "\nAttr 2: Enable = " + str(rstpenable[0])

                pathcost = struct.unpack("<I",cip_res[newstart+36:newstart+40])
                outputstr+= "\nAttr 2: Path Cost = " + str(pathcost[0])

                desrootsize2 = struct.unpack("<H",cip_res[newstart+40:newstart+42])
                desroot2 = struct.unpack(str(desrootsize2[0])+"B",cip_res[newstart+42:newstart+42+desrootsize2[0]])
                outputstr+= "\nAttr 2: Designated Root = "

                for x in range(0,len(desroot2)):
                    outputstr+= str(hex(desroot2[x])[2:]) + " "

                newstart = newstart+42+desrootsize2[0]

                descost = struct.unpack("<I",cip_res[newstart:newstart+4])
                outputstr+= "\nAttr 2: Designated Cost = " + str(descost[0])

                desbridgesize = struct.unpack("<H",cip_res[newstart+4:newstart+6])
                desbridge = struct.unpack(str(desbridgesize[0])+"B",cip_res[newstart+6:newstart+6+desbridgesize[0]])
                outputstr+= "\nAttr 2: Designated Bridge = "

                for x in range(0,len(desbridge)):
                    outputstr+= str(hex(desbridge[x])[2:]) + " "

                newstart = newstart+6+desbridgesize[0]

                desportsize = struct.unpack("<H",cip_res[newstart:newstart+2])
                desport = struct.unpack(str(desportsize[0])+"B",cip_res[newstart+2:newstart+2+desportsize[0]])
                outputstr+= "\nAttr 2: Designated Port = "

                desportstr = ""
                for x in range(0,len(desport)):
                    desportstr += str('{:02x}'.format(desport[x])) + " "
                    outputstr+= str('{:02x}'.format(desport[x])) + " "

                newstart = newstart+2+desportsize[0]

                forwardtranscount = struct.unpack("<I",cip_res[newstart:newstart+4])
                outputstr+= "\nAttr 2: Forward Transitions Count = " + str(forwardtranscount[0])

                portnum = struct.unpack("<H",cip_res[newstart+4:newstart+6])
                outputstr+= "\nAttr 3 (Port Mode): Port Number = " + str(portnum[0])

                adminedgeport = struct.unpack("<H",cip_res[newstart+6:newstart+8])
                outputstr+= "\nAttr 3: Admin Edge Port = " + str(adminedgeport[0])

                operedgeport = struct.unpack("<H",cip_res[newstart+8:newstart+10])
                outputstr+= "\nAttr 3: Oper Edge Port = " + str(operedgeport[0])

                autoedgeport = struct.unpack("<H",cip_res[newstart+10:newstart+12])
                outputstr+= "\nAttr 3: Auto Edge Port = " + str(autoedgeport[0])

        
                outputstr+='\n'
                t.insert(END,outputstr)
        
        
        
        insertstr=''
        found=0
        
        if comparefile_op.get() == '1':
        
        
            if protocolspec_file != protocolspec[0] and "9.1" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 1 (Switch Status): Protocol Specification = " + str(protocolspec[0])
                insertstr+="\n+Attr 1 (Switch Status): Protocol Specification = " + str(protocolspec_file)
                    
            elif protocolspec_file == protocolspec[0] and "9.1" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 1 (Switch Status): Protocol Specification Passed"

            if bridgepriority_file != bridgepriority[0] and "9.2" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Bridge Priority = " + str(bridgepriority[0])
                insertstr += "\n+Attr 1: Bridge Priority = " + str(bridgepriority_file)

            elif bridgepriority_file == bridgepriority[0] and "9.2" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Bridge Priority Passed"

            if timesincetopchange_file != timesincetopchange[0] and "9.3" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Time Since Topology Change = " + str(timesincetopchange[0])
                insertstr += "\n+Attr 1: Time Since Topology Change = " + str(timesincetopchange_file)

            elif timesincetopchange_file == timesincetopchange[0] and "9.3" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Time Since Topology Change Passed"

            if topchangecount_file != topchangecount[0] and "9.4" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Topology Change Count = " + str(topchangecount[0])
                insertstr += "\n+Attr 1: Topology Change Count = " + str(topchangecount_file)

            elif topchangecount_file == topchangecount[0] and "9.4" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Topology Change Count Passed"

            if desroot_file != desroot[0] and "9.5" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Designated Root = " + str(desroot[0])
                insertstr += "\n+Attr 1: Designated Root = " + str(desroot_file)

            elif desroot_file == desroot[0] and "9.5" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Designated Root Passed"

            if rootcost_file != rootcost[0] and "9.6" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Root Cost = " + str(rootcost[0])
                insertstr += "\n+Attr 1: Root Cost = " + str(rootcost_file)

            elif rootcost_file == rootcost[0] and "9.6" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Root Cost Passed"

            if rootport_file != rootport[0] and "9.7" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Root Port = " + str(rootport[0])
                insertstr += "\n+Attr 1: Root Port = " + str(rootport_file)

            elif rootport_file == rootport[0] and "9.7" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Root Port Passed"

            if maxage_file != maxage[0] and "9.8" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Max Age = " + str(maxage[0])
                insertstr += "\n+Attr 1: Max Age = " + str(maxage_file)

            elif maxage_file == maxage[0] and "9.8" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Max Age Passed"

            if hellotime_file != hellotime[0] and "9.9" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Hello Time = " + str(hellotime[0])
                insertstr += "\n+Attr 1: Hello Time = " + str(hellotime_file)

            elif hellotime_file == hellotime[0] and "9.9" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Hello Time Passed"

            if holdtime_file != holdtime[0] and "9.10" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Hold Time = " + str(holdtime[0])
                insertstr += "\n+Attr 1: Hold Time = " + str(holdtime_file)

            elif holdtime_file == holdtime[0] and "9.10" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Hold Time Passed"

            if forwarddelay_file != forwarddelay[0] and "9.11" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Forward Delay = " + str(forwarddelay[0])
                insertstr += "\n+Attr 1: Forward Delay = " + str(forwarddelay_file)

            elif forwarddelay_file == forwarddelay[0] and "9.11" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Forward Delay Passed"

            if bridgemaxage_file != bridgemaxage[0] and "9.12" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Bridge Max Age = " + str(bridgemaxage[0])
                insertstr += "\n+Attr 1: Bridge Max Age = " + str(bridgemaxage_file)

            elif bridgemaxage_file == bridgemaxage[0] and "9.12" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Bridge Max Age Passed"

            if bridgehellotime_file != bridgehellotime[0] and "9.13" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Bridge Hello Time = " + str(bridgehellotime[0])
                insertstr += "\n+Attr 1: Bridge Hello Time = " + str(bridgehellotime_file)

            elif bridgehellotime_file == bridgehellotime[0] and "9.13" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Bridge Hello Time Passed"

            if bridgeforwarddelay_file != bridgeforwarddelay[0] and "9.14" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 1: Bridge Forward Delay = " + str(bridgeforwarddelay[0])
                insertstr += "\n+Attr 1: Bridge Forward Delay = " + str(bridgeforwarddelay_file)

            elif bridgeforwarddelay_file == bridgeforwarddelay[0] and "9.14" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 1: Bridge Forward Delay Passed"

            if rstpport_file != rstpport[0] and "9.15" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2 (Port Status): Port = " + str(rstpport[0])
                insertstr += "\n+Attr 2 (Port Status): Port = " + str(rstpport_file)

            elif rstpport_file == rstpport[0] and "9.15" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2 (Port Status): Port Passed"

            if rstppriority_file != rstppriority[0] and "9.16" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: Priority = " + str(rstppriority[0])
                insertstr += "\n+Attr 2: Priority = " + str(rstppriority_file)

            elif rstppriority_file == rstppriority[0] and "9.16" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: Priority Passed"

            if rstpstate_file != rstpstate[0] and "9.17" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: State = " + str(rstpstate[0])
                insertstr += "\n+Attr 2: State = " + str(rstpstate_file)

            elif rstpstate_file == rstpstate[0] and "9.17" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: State Passed"

            if rstpenable_file != rstpenable[0] and "9.18" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: Enable = " + str(rstpenable[0])
                insertstr += "\n+Attr 2: Enable = " + str(rstpenable_file)

            elif rstpenable_file == rstpenable[0] and "9.18" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: Enable Passed"

            if pathcost_file != pathcost[0] and "9.19" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: Path Cost = " + str(pathcost[0])
                insertstr += "\n+Attr 2: Path Cost = " + str(pathcost_file)

            elif pathcost_file == pathcost[0] and "9.19" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: Path Cost Passed"

            if desroot2_file != desroot2[0] and "9.20" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: Designated Root = " + str(desroot2[0])
                insertstr += "\n+Attr 2: Designated Root = " + str(desroot2_file)

            elif desroot2_file == desroot2[0] and "9.20" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: Designated Root Passed"

            if descost_file != descost[0] and "9.21" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: Designated Cost = " + str(descost[0])
                insertstr += "\n+Attr 2: Designated Cost = " + str(descost_file)

            elif descost_file == descost[0] and "9.21" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: Designated Cost Passed"

            if desbridge_file != desbridge[0] and "9.22" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: Designated Bridge = " + str(desbridge[0])
                insertstr += "\n+Attr 2: Designated Bridge = " + str(desbridge_file)

            elif desbridge_file == desbridge[0] and "9.22" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: Designated Bridge Passed"

            if desport_file[:-2] != desportstr and "9.23" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: Designated Port = " + str(desportstr)
                insertstr += "\n+Attr 2: Designated Port = " + str(desport_file)

            elif desport_file[:-2] == desportstr and "9.23" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: Designated Port Passed"

            if forwardtranscount_file != forwardtranscount[0] and "9.24" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 2: Forward Transitions Count = " + str(forwardtranscount[0])
                insertstr += "\n+Attr 2: Forward Transitions Count = " + str(forwardtranscount_file)

            elif forwardtranscount_file == forwardtranscount[0] and "9.24" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 2: Forward Transitions Count Passed"

            if portnum_file != portnum[0] and "9.25" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 3 (Port Mode): Port Number = " + str(portnum[0])
                insertstr += "\n+Attr 3 (Port Mode): Port Number = " + str(portnum_file)

            elif portnum_file == portnum[0] and "9.25" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 3 (Port Mode): Port Number = Passed"

            if adminedgeport_file != adminedgeport[0] and "9.26" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 3: Admin Edge Port = " + str(adminedgeport[0])
                insertstr += "\n+Attr 3: Admin Edge Port = " + str(adminedgeport_file)

            elif adminedgeport_file == adminedgeport[0] and "9.26" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 3: Admin Edge Port Passed"

            if operedgeport_file != operedgeport[0] and "9.27" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 3: Oper Edge Port = " + str(operedgeport[0])
                insertstr += "\n+Attr 3: Oper Edge Port = " + str(operedgeport_file)

            elif operedgeport_file == operedgeport[0] and "9.27" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 3: Oper Edge Port Passed"

            if autoedgeport_file != autoedgeport[0] and "9.28" in compare_sel:
                compares += 1
                fails += 1
                found = 1
                insertstr += "\n-Attr 3: Auto Edge Port = " + str(autoedgeport[0])
                insertstr += "\n+Attr 3: Auto Edge Port = " + str(autoedgeport_file)

            elif autoedgeport_file == autoedgeport[0] and "9.28" in compare_sel:
                compares += 1
                passes += 1
                found = 1
                insertstr += "\nAttr 3: Auto Edge Port Passed"





        if found == 1:
            insertstr+="\n\nCompares = "+str(compares)+"\nPasses = "+str(passes)+"\nFails = "+str(fails)+"\n"
            insertstr= "\n(9) RSTP Diagnostic object (0x355)\n"+insertstr
            t2.insert(END,insertstr)
        
        
        
        
    if cl.getstatus('CL10')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(10) Service Port Control object (0x400)\n"

        service_req = b'\x01'
        class_req = b'\x00\x04'
        instance_req = b'\x01'
        attribute_req = ''
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test10=1
            outputstr+="\nTest Passed"
        else:
            test10=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test10)
        outputstr=''
        
        
        if checksize==1 and test10==1:
            
            getalllen=len(cip_res[44:])
            service_req = b'\x0e'
            
            
            attribute_req = b'\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen=len(cip_res[44:])

            attribute_req=b'\x02'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            if getalllen == getsinglelen:
                test10=1
                outputstr+="\nSizes Match"
            else:
                test10=2
                outputstr+="\nSizes Don't Match"
            
            t.insert(END,outputstr)
            color_test(test10)
        
        
        elif test10==1:
        
            portcontrol = struct.unpack("<H",cip_res[44:46])
            outputstr+= "\nAttr 1: Port Control = " + str(portcontrol[0])
            
            mirror = struct.unpack("<H",cip_res[46:48])
            outputstr+= "\nAttr 2: Mirror = " + str(mirror[0])
        
        
        
            outputstr+='\n'
            t.insert(END,outputstr)


    if cl.getstatus('CL11')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(11) Router Diagnostic object (0x402)\n"

        service_req = b'\x0e'
        class_req = b'\x02\x04'
        instance_req = b'\x01'
        attribute_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test11=1
            outputstr+="\nTest Passed"
        else:
            test11=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test11)
        
    if cl.getstatus('CL12')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(12) Routing Table Diagnostic object (0x403)\n"

        service_req = b'\x0e'
        class_req = b'\x03\x04'
        instance_req = b'\x01'
        attribute_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test12=1
            outputstr+="\nTest Passed"
        else:
            test12=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test12)
        
    if cl.getstatus('CL13')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(13) SMTP object (0x404)\n"

        service_req = b'\x01'
        class_req = b'\x04\x04'
        instance_req = b'\x01'
        attribute_req = ''
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test13=1
            outputstr+="\nTest Passed"
        else:
            test13=2
            outputstr+="\nTest Failed"
        
        
        t.insert(END,outputstr)
        color_test(test13)

        
    if cl.getstatus('CL14')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(14) SNTP object (0x405)\n"

        service_req = b'\x01'
        class_req = b'\x05\x04'
        instance_req = b'\x01'
        attribute_req = ''
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
        
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
        
        if cip_res[42] == 0:
            test14=1
            outputstr+="\nTest Passed"
        else:
            test14=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test14)

        if test14 == 1 and len(cip_res)==136:
            primaryntpserver = struct.unpack("<I", cip_res[44:48])
            outputstr += "\nAttr 1 (Network Time Service Configuration): Primary NTP Server IP Address = " + str(
                primaryntpserver[0])

            secondaryntpserver = struct.unpack("<I", cip_res[48:52])
            outputstr += "\nAttr 1: Secondary NTP Server IP Address = " + str(secondaryntpserver[0])

            pollingperiod = struct.unpack("B", bytes([cip_res[52]]))
            outputstr += "\nAttr 1: Polling Period = " + str(pollingperiod[0])

            updatecpumodtime = struct.unpack("B", bytes([cip_res[53]]))
            outputstr += "\nAttr 1: Update CPU with Module Time = " + str(updatecpumodtime[0])

            timezone = struct.unpack("<I", cip_res[54:58])
            outputstr += "\nAttr 1: Time Zone = " + str(timezone[0])

            timezoneoffset = struct.unpack("<H", cip_res[58:60])
            outputstr += "\nAttr 1: Time Zone Offset = " + str(timezoneoffset[0])

            daylightsavingtimebias = struct.unpack("B", bytes([cip_res[60]]))
            outputstr += "\nAttr 1: Daylight saving time bias = " + str(daylightsavingtimebias[0])

            daylightsavingstartdatemonth = struct.unpack("B", bytes([cip_res[61]]))
            outputstr += "\nAttr 1: Daylight Saving Start Date - Month = " + str(daylightsavingstartdatemonth[0])

            daylightsavingstartdateweek = struct.unpack("B", bytes([cip_res[62]]))
            outputstr += "\nAttr 1: Daylight Saving Start Date - week #, day of week = " + str(
                daylightsavingstartdateweek[0])

            daylightsavingstarttime = struct.unpack("<I", cip_res[63:67])
            outputstr += "\nAttr 1: Daylight Saving Start Time = " + str(daylightsavingstarttime[0])

            daylightsavingenddatemonth = struct.unpack("B", bytes([cip_res[67]]))
            outputstr += "\nAttr 1: Daylight Saving End Date - Month = " + str(daylightsavingenddatemonth[0])

            daylightsavingenddateweek = struct.unpack("B", bytes([cip_res[68]]))
            outputstr += "\nAttr 1: Daylight Saving End Date - week #, day of week = " + str(
                daylightsavingenddateweek[0])

            daylightsavingendtime = struct.unpack("<I", cip_res[69:73])
            outputstr += "\nAttr 1: Daylight Saving End Time = " + str(daylightsavingendtime[0])

            reserved = struct.unpack("15B", cip_res[73:88])
            outputstr += "\nAttr 1: Reserved = " + str(reserved[0])

            nettimeservstat = struct.unpack("<I", cip_res[88:92])
            outputstr += "\nAttr 2: Network Time Service Status = " + str(nettimeservstat[0])

            linktontpservstat = struct.unpack("<I", cip_res[92:96])
            outputstr += "\nAttr 3: Link to NTP Server Status = " + str(linktontpservstat[0])

            currentntpserveripaddress = struct.unpack("<I", cip_res[96:100])
            outputstr += "\nAttr 4: Current NTP Server IP Address = " + str(currentntpserveripaddress[0])

            ntpservertype = struct.unpack("<I", cip_res[100:104])
            outputstr += "\nAttr 5: NTP Server Type = " + str(ntpservertype[0])

            ntpservertimequality = struct.unpack("<I", cip_res[104:108])
            outputstr += "\nAttr 6: NTP Server Time Quality = " + str(ntpservertimequality[0])

            numofntpreqsent = struct.unpack("<I", cip_res[108:112])
            outputstr += "\nAttr 7: Number of NTP Requests Sent = " + str(numofntpreqsent[0])

            numofcommerrors = struct.unpack("<I", cip_res[112:116])
            outputstr += "\nAttr 8: Number of Communication Errors = " + str(numofcommerrors[0])

            numofntpresprecv = struct.unpack("<I", cip_res[116:120])
            outputstr += "\nAttr 9: Number of NTP Responses Received = " + str(numofntpresprecv[0])

            lasterror = struct.unpack("<H", cip_res[120:122])
            outputstr += "\nAttr 10: Last Error = " + str(lasterror[0])

            currentdateandtime = struct.unpack("<IH", cip_res[122:128])
            outputstr += "\nAttr 11: Current Date and Time = " + str(currentdateandtime[0])

            currentdate = struct.unpack("<H",cip_res[126:128])
            currentdatedate = (datetime.datetime(1972,1,1) + datetime.timedelta(days=currentdate[0])).date()
            outputstr += "\nCurrent Date = "+str(currentdatedate)
            currenttime = struct.unpack("<I",cip_res[122:126])
            outputstr += "\nCurrent Time = " + str((datetime.datetime.min + datetime.timedelta(milliseconds=currenttime[0])).time())


            daylightsavingsstatus = struct.unpack("<I", cip_res[128:132])
            outputstr += "\nAttr 12: Daylight Savings Status = " + str(daylightsavingsstatus[0])

            timesincelastupdate = struct.unpack("<I", cip_res[132:136])
            outputstr += "\nAttr 13: Time Since Last Update = " + str(timesincelastupdate[0])










            outputstr+='\n'

            t.insert(END,outputstr)

    if cl.getstatus('CL15')=='on':

        if z==0 or runAndCompare_var == 1:

            reqsRan+=1

            outputstr=""
            outputstr+="\n(15) Identity object (0x01)\n"

            service_req = b'\x01'
            class_req = b'\x01'
            instance_req = b'\x01'

            #example_cip_object = CipObject(Service.get_attributes_all, class_=0x01)


            #scanner.send_unconnected(dest_addr=TCP_IP.get(), cip_object=example_cip_object)


            #example_handler.example_response_event.wait()


            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    b'\x00')

            t.insert(END, outputstr)
            bold_response()
            outputstr = ''

            if cip_res[42] == 0:
                test15=1
                outputstr+="\nTest Passed"
            else:
                test15=2
                outputstr+="\nTest Failed"

            t.insert(END,outputstr)
            color_test(test15)
            outputstr=""


            if checksize==1 and test15==1:

                getalllen=len(cip_res[44:])
                service_req = b'\x0e'


                attribute_req = b'\x01'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen=len(cip_res[44:])

                attribute_req=b'\x02'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                attribute_req=b'\x03'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                attribute_req=b'\x04'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                attribute_req=b'\x05'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                attribute_req=b'\x06'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                attribute_req=b'\x07'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                attribute_req=b'\x08'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                attribute_req=b'\x09'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                attribute_req=b'\x0a'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])

                if getalllen == getsinglelen:
                    test15=1
                    outputstr+="\nSizes Match"
                else:
                    test15=2
                    outputstr+="\nSizes Don't Match"

                t.insert(END,outputstr)
                color_test(test15)



            elif test15==1:

                global vendorid
                vendorid = struct.unpack('<H',cip_res[44:46])
                outputstr+= '\nAttr 1: Vendor ID = '+str(vendorid[0])

                global devicetype
                devicetype = struct.unpack('<H',cip_res[46:48])
                outputstr+= '\nAttr 2: Device Type = '+str(devicetype[0])

                global productcode
                productcode = struct.unpack('<H',cip_res[48:50])
                outputstr+= '\nAttr 3: Product Code = '+str(productcode[0])

                global revision
                revision = struct.unpack('2B',cip_res[50:52])
                outputstr+='\nAttr 4: Major Revision = '+str(revision[0])
                outputstr+= '\nAttr 4: Minor Revision = '+str(revision[1])

                global status2
                status2 = struct.unpack('<H',cip_res[52:54])
                outputstr+='\nAttr 5: Status = '+str(hex(status2[0]))

                global serialnum
                serialnum = struct.unpack("<I",cip_res[54:58])
                outputstr+='\nAttr 6: Serial Number = '+str(hex(serialnum[0]))


                global productname
                productname = struct.unpack("B",bytes([cip_res[58]])  )
                if productname[0] == 0:
                    outputstr+='\nAttr 7: Product Name = NULL'
                else:
                    outputstr+='\nAttr 7: Product Name = '+str(chr(productname[0]))


                global state
                state = struct.unpack("B",bytes([cip_res[59]])  )
                outputstr+='\nAttr 8: State = ' + str(hex(state[0]))

                global configconsistency
                configconsistency = struct.unpack("<H",cip_res[60:62])
                outputstr+='\nAttr 9: Configuration Consistency Value = '+str(configconsistency[0])

                global heartbeatint
                heartbeatint = struct.unpack("B",bytes([cip_res[62]]))
                outputstr+='\nAttr 10: Heartbeat Interval = '+str(heartbeatint[0])

                outputstr+='\n'
                t.insert(END,outputstr)


        insertstr=''
        found=0

        if comparefile_op.get() == '1':

            if vendorid_file != vendorid[0] and "15.1" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 1: Vendor ID = " + str(vendorid[0])
                insertstr+="\n+Attr 1: Vendor ID = " + str(vendorid_file)

            elif vendorid_file == vendorid[0] and "15.1" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 1: Vendor ID Passed"

            if devicetype_file != devicetype[0] and "15.2" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: Device Type = " + str(devicetype[0])
                insertstr+="\n+Attr 2: Device Type = " + str(devicetype_file)

            elif devicetype_file == devicetype[0] and "15.2" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: Device Type Passed"

            if productcode_file != productcode[0] and "15.3" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 3: Product Code = " + str(productcode[0])
                insertstr+="\n+Attr 3: Product Code = " + str(productcode_file)

            elif productcode_file == productcode[0] and "15.3" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 3: Product Code Passed"

            if revision_file1 != revision[0] and "15.4" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 4: Major Revision = " + str(revision[0])
                insertstr+="\n+Attr 4: Major Revision = " + str(revision_file1)

            elif revision_file1 == revision[0] and "15.4" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 4: Major Revision Passed"

            if revision_file2 != revision[1] and "15.4" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 4: Minor Revision = " + str(revision[1])
                insertstr+="\n+Attr 4: Minor Revision = " + str(revision_file2)

            elif revision_file2 == revision[1] and "15.4" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 4: Minor Revision Passed"

            if status2_file != status2[0] and "15.5" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 5: Status = " + str(status2[0])
                insertstr+="\n+Attr 5: Status = " + str(status2_file)

            elif status2_file == status2[0] and "15.5" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 5: Status Passed"

            if serialnum_file != serialnum[0] and "15.6" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 6: Serial Number = " + str(serialnum[0])
                insertstr+="\n+Attr 6: Serial Number = " + str(serialnum_file)

            elif serialnum_file == serialnum[0] and "15.6" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 6: Serial Number Passed"

            if productname_file != productname[0] and "15.7" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 7: Product Name = " + str(productname[0])
                insertstr+="\n+Attr 7: Product Name = " + str(productname_file)

            elif productname_file == productname[0] and "15.7" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 7: Product Name Passed"

            if state_file != state[0] and "15.8" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 8: State = " + str(state[0])
                insertstr+="\n+Attr 8: State = " + str(state_file)

            elif state_file == state[0] and "15.8" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 8: State Passed"

            if configconsistency_file != configconsistency[0] and "15.9" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 9: Configuration Consistency Value = " + str(configconsistency[0])
                insertstr+="\n+Attr 9: Configuration Consistency Value = " + str(configconsistency_file)

            elif configconsistency_file == configconsistency[0] and "15.9" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 9: Configuration Consistency Value Passed"

            if heartbeatint_file != heartbeatint[0] and "15.10" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 10: Heartbeat Interval = " + str(heartbeatint[0])
                insertstr+="\n+Attr 10: Heartbeat Interval = " + str(heartbeatint_file)

            elif heartbeatint_file == heartbeatint[0] and "15.10" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 10: Heartbeat Interval Passed"



        if found == 1:
            insertstr+="\n\nCompares = "+str(compares)+"\nPasses = "+str(passes)+"\nFails = "+str(fails)+"\n"
            insertstr= "\n(15) Identity object (0x01)\n"+insertstr
            t2.insert(END,insertstr)







    if cl.getstatus('CL16')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(16) Message Router object (0x02)\n"

        service_req = b'\x01'
        class_req = b'\x02'
        instance_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, b'\x00')
                
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
                
        if cip_res[42:44] == b'\x00\x00':
            test16=1
            outputstr+="\nTest Passed"
        else:
            test16=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test16)
        
        
    if cl.getstatus('CL17')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(17) Connection Manager object (0x06)\n"

        service_req = b'\x01'
        class_req = b'\x06'
        instance_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, b'\x00')
                
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
                
        if cip_res[42:44] == b'\x00\x00':
            test17=1
            outputstr+="\nTest Passed"
        else:
            test17=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test17)
        outputstr=''
        
        
        if checksize==1 and test17==1:
            
            getalllen=len(cip_res[44:])
            service_req = b'\x0e'
            
            
            attribute_req = b'\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen=len(cip_res[44:])

            attribute_req=b'\x02'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x03'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x04'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x05'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x06'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x07'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x08'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            if getalllen == getsinglelen:
                test17=1
                outputstr+="\nSizes Match"
            else:
                test17=2
                outputstr+="\nSizes Don't Match"
            
            t.insert(END,outputstr)
            color_test(test17)
        
        elif test17==1:
        
            openreqs = struct.unpack("<H",cip_res[44:46])
            outputstr+= "\nAttr 1: Open Requests = " + str(openreqs[0])
            
            openformatrejects = struct.unpack("<H",cip_res[46:48])
            outputstr+= "\nAttr 2: Open Format Rejects = " + str(openformatrejects[0])
            
            openresourcerejects = struct.unpack("<H",cip_res[48:50])
            outputstr+= "\nAttr 3: Open Resource Rejects = " + str(openresourcerejects[0])
            
            otheropenrejects = struct.unpack("<H",cip_res[50:52])
            outputstr+= "\nAttr 4: Other Open Rejects = " + str(otheropenrejects[0])
            
            closerejects = struct.unpack("<H",cip_res[52:54])
            outputstr+= "\nAttr 5: Close Requests = " + str(closerejects[0])
            
            closeformatreqs = struct.unpack("<H",cip_res[54:56])
            outputstr+= "\nAttr 6: Close Format Requests = " + str(closeformatreqs[0])
            
            closeotherreqs = struct.unpack("<H",cip_res[56:58])
            outputstr+= "\nAttr 7: Close Other Requests = " + str(closeotherreqs[0])
            
            conntimeouts = struct.unpack("<H",cip_res[58:60])
            outputstr+= "\nAttr 8: Connection Timeouts = " + str(conntimeouts[0])
            
            
            outputstr+='\n'
            t.insert(END,outputstr)
        
        insertstr=''
        found=0
        
        if comparefile_op.get() == '1':
        
            if openreqs_file != openreqs[0] and "17.1" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 1: Open Requests = " + str(openreqs[0])
                insertstr+="\n+Attr 1: Open Requests = " + str(openreqs_file)
                
            elif openreqs_file == openreqs[0] and "17.1" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 1: Open Requests Passed"
            

        if found == 1:
            insertstr+="\n\nCompares = "+str(compares)+"\nPasses = "+str(passes)+"\nFails = "+str(fails)+"\n"
            insertstr= "\n(17) Connection Manager object (0x06)\n"+insertstr
            t2.insert(END,insertstr)
        
        
    if cl.getstatus('CL18')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(18) QoS (Quality of Service) object (0x48)\n"

        service_req = b'\x0e'
        class_req = b'\x48'
        instance_req = b'\x01'
        attribute_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
                
        if cip_res[42] == 0:
            test18=1
            outputstr+="\nTest Passed"
        else:
            test18=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test18)
        outputstr=''
        outputstr2=''
        
        
        if test18==1:
        
            tagenable = struct.unpack('B',bytes([cip_res[44]]))
            outputstr+= "\nAttr 1: 802.1Q Tag Enable = " + str(tagenable[0])

            outputstr2,cip_res = requestsendreceive(outputstr2,sock,reg_sess, service_req, class_req, instance_req, b'\x02')
            dscpptpevent = struct.unpack('B',bytes([cip_res[44]]))
            outputstr+= "\nAttr 2: DSCP PTP Event = " + str(dscpptpevent[0])
            
            outputstr2,cip_res = requestsendreceive(outputstr2,sock,reg_sess, service_req, class_req, instance_req, b'\x03')
            dscpptpgeneral = struct.unpack('B',bytes([cip_res[44]]))
            outputstr+= "\nAttr 3: DSCP PTP General = " + str(dscpptpgeneral[0])
            
            outputstr2,cip_res = requestsendreceive(outputstr2,sock,reg_sess, service_req, class_req, instance_req, b'\x04')
            dscpurgent = struct.unpack('B',bytes([cip_res[44]]))
            outputstr+= "\nAttr 4: DSC Urgent = " + str(dscpurgent[0])
            
            outputstr2,cip_res = requestsendreceive(outputstr2,sock,reg_sess, service_req, class_req, instance_req, b'\x05')
            dscpscheduled = struct.unpack('B',bytes([cip_res[44]]))
            outputstr+= "\nAttr 5: DSCP Scheduled = " + str(dscpscheduled[0])
            
            outputstr2,cip_res = requestsendreceive(outputstr2,sock,reg_sess, service_req, class_req, instance_req, b'\x06')
            dscphigh = struct.unpack('B',bytes([cip_res[44]]))
            outputstr+= "\nAttr 6: DSCP High = " + str(dscphigh[0])
            
            outputstr2,cip_res = requestsendreceive(outputstr2,sock,reg_sess, service_req, class_req, instance_req, b'\x07')
            dscplow = struct.unpack('B',bytes([cip_res[44]]))
            outputstr+= "\nAttr 7: DSCP Low = " + str(dscplow[0])
            
            outputstr2,cip_res = requestsendreceive(outputstr2,sock,reg_sess, service_req, class_req, instance_req, b'\x08')
            dscpexplicit = struct.unpack('B',bytes([cip_res[44]]))
            outputstr+= "\nAttr 8: DSCP Explicit = " + str(dscpexplicit[0])
        
        
            outputstr+='\n'
            t.insert(END,outputstr)
        
    
        insertstr=''
        found=0
        
        if comparefile_op.get() == '1':
        
            if tagenable_file != tagenable[0] and "18.1" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 1: Tag Enable = " + str(tagenable[0])
                insertstr+="\n+Attr 1: Tag Enable = " + str(tagenable_file)
                
            elif tagenable_file == tagenable[0] and "18.1" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 1: Tag Enable Passed"
            

        if found == 1:
            insertstr+="\n\nCompares = "+str(compares)+"\nPasses = "+str(passes)+"\nFails = "+str(fails)+"\n"
            insertstr= "\n(18) QoS (Quality of Service) object (0x48)\n"+insertstr
            t2.insert(END,insertstr)
    
    
    
    
    
    if cl.getstatus('CL19')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(19) Port object (0xF4)\n"

        service_req = b'\x01'
        class_req = b'\xf4'
        instance_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, b'\x00')
                
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
                
        if cip_res[42:44] == b'\x00\x00':
            test19=1
            outputstr+="\nTest Passed"
        else:
            test19=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test19)
        outputstr=''
    
    
        if checksize==1 and test19==1:
            
            getalllen=len(cip_res[44:])
            service_req = b'\x0e'
            
            
            attribute_req = b'\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen=len(cip_res[44:])

            attribute_req=b'\x02'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x03'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x04'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x05'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x06'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x07'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])

            
            if getalllen == getsinglelen:
                test19=1
                outputstr+="\nSizes Match"
            else:
                test19=2
                outputstr+="\nSizes Don't Match"
            
            t.insert(END,outputstr)
            color_test(test19)
    
    
        elif test19==1:
    
            porttype = struct.unpack("<H",cip_res[44:46])
            outputstr+= "\nAttr 1: Port Type = " + str(porttype[0])
            
            portnumber = struct.unpack("<H",cip_res[46:48])
            outputstr+= "\nAttr 2: Port Number = " + str(portnumber[0])
            
            pathlength = struct.unpack("<H",cip_res[48:50])
            outputstr+= "\nAttr 3 (Link Object): Path Length (words) = " + str(pathlength[0])
            
            pathclass = struct.unpack("B",bytes([cip_res[51]]))
            outputstr+= "\nAttr 3: Class = " + str(pathclass[0])
            
            pathinstance = struct.unpack("B",bytes([cip_res[53]]))
            outputstr+= "\nAttr 3: Instance = " + str(pathinstance[0])
        
            portname = struct.unpack("<10s",cip_res[54:64])
            outputstr+= "\nAttr 4: Port Name = " + str(portname[0:10])
            
            port = struct.unpack("B",bytes([cip_res[65]]))
            outputstr+= "\nAttr 7: Port = " + str(port[0])
            
            address = struct.unpack("B",bytes([cip_res[66]]))
            outputstr+= "\nAttr 7: Node Address = " + str(address[0])
        
            outputstr+='\n'
            t.insert(END,outputstr)
    
    
        insertstr=''
        found=0
        
        if comparefile_op.get() == '1':
        
            if porttype_file != porttype[0] and "19.1" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 1: Port Type = " + str(porttype[0])
                insertstr+="\n+Attr 1: Port Type = " + str(porttype_file)
                
            elif porttype_file == porttype[0] and "19.1" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 1: Port Type Passed"
            

        if found == 1:
            insertstr+="\n\nCompares = "+str(compares)+"\nPasses = "+str(passes)+"\nFails = "+str(fails)+"\n"
            insertstr= "\n(19) Port object (0xF4)\n"+insertstr
            t2.insert(END,insertstr)
    
    
        
    if cl.getstatus('CL20')=='on':

        if z==0 or runAndCompare_var == 1:
    
            reqsRan+=1
        
            outputstr=""
            outputstr+="\n(20) TCP/IP object (0xF5)\n"

            service_req = b'\x01'
            class_req = b'\xf5'
            instance_req = b'\x01'
            
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, b'\x00')
                    
            t.insert(END,outputstr)
            bold_response()
            outputstr=''
                    
            if cip_res[42:44] == b'\x00\x00':
                test20=1
                outputstr+="\nTest Passed"
            else:
                test20=2
                outputstr+="\nTest Failed"
            
            t.insert(END,outputstr)
            color_test(test20)
            outputstr=""
            
            
            if checksize==1 and test20==1:
                
                getalllen=len(cip_res[44:])
                service_req = b'\x0e'
                
                
                attribute_req = b'\x01'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen=len(cip_res[44:])

                attribute_req=b'\x02'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x03'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x04'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x05'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x06'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x07'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x08'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x09'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x0a'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x0b'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x0c'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                attribute_req=b'\x0d'
                outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
                getsinglelen+=len(cip_res[44:])
                
                if getalllen == getsinglelen:
                    test20=1
                    outputstr+="\nSizes Match"
                else:
                    test20=2
                    outputstr+="\nSizes Don't Match"
                
                t.insert(END,outputstr)
                color_test(test20)
            
            
            
            
            
            elif test20==1:
            
                global status3
                status3 = struct.unpack("<I", cip_res[44:48])
                outputstr+= "\nAttr 1: Status = " + str(status3[0])
                
                configcapability = struct.unpack("<I", cip_res[48:52])
                outputstr+= "\nAttr 2: Configuration Capability = " + str(hex(configcapability[0]))
                
                configcontrol = struct.unpack("<I", cip_res[52:56])
                outputstr+= "\nAttr 3: Configuration Control = " + str(configcontrol[0])
                
                physlink = struct.unpack("<H", cip_res[56:58])
                outputstr+= "\nAttr 4: Physical Link = " + str(physlink[0])
                
                ipaddr = struct.unpack("<BBBB", cip_res[58:62])
                outputstr+= "\nAttr 5: IP Address = " + str(ipaddr[3]) + '.' + str(ipaddr[2]) + '.' + str(ipaddr[1]) + '.' + str(ipaddr[0])
                
                subnetmask = struct.unpack("<BBBB", cip_res[62:66])
                outputstr+= "\nAttr 5: Subnet mask = " + str(subnetmask[3])+'.'+str(subnetmask[2])+'.'+str(subnetmask[1])+'.'+str(subnetmask[0])
                
                gateway = struct.unpack("<BBBB", cip_res[66:70])
                outputstr+= "\nAttr 5: Gateway = " + str(gateway[3])+'.'+str(gateway[2])+'.'+str(gateway[1])+'.'+str(gateway[0])
                
                nameserver = struct.unpack("<BBBB", cip_res[70:74])
                outputstr+= "\nAttr 5: Name Server = "+str(nameserver[3])+'.' + str(nameserver[2])+'.' + str(nameserver[1])+'.' + str(nameserver[0])
                
                nameserver2 = struct.unpack("<BBBB",cip_res[74:78])
                outputstr+= "\nAttr 5: Name Server2 = "+str(nameserver2[3])+'.'+str(nameserver2[2])+'.'+str(nameserver2[1])+'.'+str(nameserver2[0])
                
                domain = struct.unpack("<H",cip_res[78:80])
                outputstr+= "\nAttr 5: Domain Name = "+str(domain[0])
                
                hostname = struct.unpack("<H",cip_res[80:82])
                outputstr+= "\nAttr 6: Host Name = "+str(hostname[0])
                
                safetynetnumdate = struct.unpack("<H",cip_res[82:84])
                outputstr+= "\nAttr 7: Safety Network Number (Manual) Date = " + str(hex(safetynetnumdate[0]))
                
                safetynetnumtime = struct.unpack("<I",cip_res[84:88])
                outputstr+= "\nAttr 7: Safety Network Number (Manual) Time = " + str(hex(safetynetnumtime[0]))
                
                ttlvalue = struct.unpack("B",bytes([cip_res[88]]))
                outputstr+= "\nAttr 8: TTL Value = " + str(ttlvalue[0])
                
                alloccontrol = struct.unpack("B",bytes([cip_res[89]]))
                outputstr+= "\nAttr 9: Alloc Control = " + str(alloccontrol[0])
                
                reserved = struct.unpack("B",bytes([cip_res[90]]))
                outputstr+= "\nAttr 9: Reserved = " + str(reserved[0])
                
                nummcast = struct.unpack("<H",cip_res[91:93])
                outputstr+= "\nAttr 9: Num MCast = " + str(nummcast[0])
                
                mcaststartaddr = struct.unpack("<BBBB",cip_res[93:97])
                outputstr+= "\nAttr 9: MCast Start Addr = " + str(mcaststartaddr[3]) + '.' + str(mcaststartaddr[2])+'.'+str(mcaststartaddr[1])+'.'+str(mcaststartaddr[0])
                
                selectacd = struct.unpack("B",bytes([cip_res[97]]))
                outputstr+= "\nAttr 10: Select ACD = " + str(selectacd[0])
                
                acdactivity = struct.unpack("B",bytes([cip_res[98]]))
                outputstr+= "\nAttr 11: ACD Activity = " + str(acdactivity[0])
                
                remotemac = struct.unpack("6B",cip_res[99:105])
                remotemacstr = str(remotemac[0])+':'+str(remotemac[1])+':'+str(remotemac[2])+':'+str(remotemac[3])+':'+str(remotemac[4])+':'+str(remotemac[5])
                outputstr+= "\nAttr 11: RemoteMAC = " + remotemacstr
                
                arppdu = struct.unpack("28B",cip_res[105:133])
                outputstr+= "\nAttr 11: Arp PDU = " + str(arppdu[:])
                
                eipquickconn = struct.unpack("B",bytes([cip_res[133]]))
                outputstr+= "\nAttr 12: EtherNet/IP Quick Connection = " + str(eipquickconn[0])
                
                encapinacttimeout = struct.unpack("<H",cip_res[134:136])
                outputstr+= "\nAttr 13: Encapsulation Inactivity Timeout = " + str(encapinacttimeout[0])
                
                outputstr+='\n'
                t.insert(END,outputstr)
        
        found=0
        insertstr=''
        
        if comparefile_op.get() == '1':
        
            if status3_file != status3[0] and "20.1" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 1: Status = " + str(status3[0])
                insertstr+="\n+Attr 1: Status = " + str(status3_file)
                
            elif status3_file == status3[0] and "20.1" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 1: Status Passed"
                
            if configcapability_file != configcapability[0] and "20.2" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 2: Configuration Capability = " + str(configcapability[0])
                insertstr+="\n+Attr 2: Configuration Capability = " + str(configcapability_file)
                
            elif configcapability_file == configcapability[0] and "20.2" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 2: Configuration Capability Passed"
                
            if configcontrol_file != configcontrol[0] and "20.3" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 3: Configuration Control = " + str(configcontrol[0])
                insertstr+="\n+Attr 3: Configuration Control = " + str(configcontrol_file)
                
            elif configcontrol_file == configcontrol[0] and "20.3" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 3: Configuration Control Passed"
                
            if physlink_file != physlink[0] and "20.4" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 4: Physical Link = " + str(physlink[0])
                insertstr+="\n+Attr 4: Physical Link = " + str(physlink_file)
                
            elif physlink_file == physlink[0] and "20.4" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 4: Physical Link Passed"
                
            if ipaddr_file != ipaddr[0] and "20.5" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 5: IP Address = " + str(ipaddr[0])
                insertstr+="\n+Attr 5: IP Address = " + str(ipaddr_file)
                
            elif ipaddr_file == ipaddr[0] and "20.5" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 5: IP Address Passed"
                
            if subnetmask_file != subnetmask[0] and "20.6" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 5: Subnet mask = " + str(subnetmask[0])
                insertstr+="\n+Attr 5: Subnet mask = " + str(subnetmask_file)
                
            elif subnetmask_file == subnetmask[0] and "20.6" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 5: Subnet mask Passed"
                
            if gateway_file != gateway[0] and "20.7" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 5: Gateway = " + str(gateway[0])
                insertstr+="\n+Attr 5: Gateway = " + str(gateway_file)
                
            elif gateway_file == gateway[0] and "20.7" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 5: Gateway Passed"
                
            if nameserver_file != nameserver[0] and "20.8" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 5: Name Server = " + str(nameserver[0])
                insertstr+="\n+Attr 5: Name Server = " + str(nameserver_file)
                
            elif nameserver_file == nameserver[0] and "20.8" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 5: Name Server Passed"
                
            if nameserver2_file != nameserver2[0] and "20.9" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 5: Name Server2 = " + str(nameserver2[0])
                insertstr+="\n+Attr 5: Name Server2 = " + str(nameserver2_file)
                
            elif nameserver2_file == nameserver2[0] and "20.9" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 5: Name Server2 Passed"
                
            if domain_file != domain[0] and "20.10" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 5: Domain Name = " + str(domain[0])
                insertstr+="\n+Attr 5: Domain Name = " + str(domain_file)
                
            elif domain_file == domain[0] and "20.10" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 5: Domain Name Passed"
                
            if hostname_file != hostname[0] and "20.11" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 6: Host Name = " + str(hostname[0])
                insertstr+="\n+Attr 6: Host Name = " + str(hostname_file)
                
            elif hostname_file == hostname[0] and "20.11" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 6: Host Name Passed"
                
            if safetynetnumdate_file != safetynetnumdate[0] and "20.12" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 7: Safety Network Number (Manual) Date = " + str(safetynetnumdate[0])
                insertstr+="\n+Attr 7: Safety Network Number (Manual) Date = " + str(safetynetnumdate_file)
                
            elif safetynetnumdate_file == safetynetnumdate[0] and "20.12" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 7: Safety Network Number (Manual) Date Passed"
                
            if safetynetnumtime_file != safetynetnumtime[0] and "20.13" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 7: Safety Network Number (Manual) Time = " + str(safetynetnumtime[0])
                insertstr+="\n+Attr 7: Safety Network Number (Manual) Time = " + str(safetynetnumtime_file)
                
            elif safetynetnumtime_file == safetynetnumtime[0] and "20.13" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 7: Safety Network Number (Manual) Time Passed"
                
            if ttlvalue_file != ttlvalue[0] and "20.14" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 8: TTL Value = " + str(ttlvalue[0])
                insertstr+="\n+Attr 8: TTL Value = " + str(ttlvalue_file)
                
            elif ttlvalue_file == ttlvalue[0] and "20.14" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 8: TTL Value Passed"
                
            if alloccontrol_file != alloccontrol[0] and "20.15" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 9: Alloc Control = " + str(alloccontrol[0])
                insertstr+="\n+Attr 9: Alloc Control = " + str(alloccontrol_file)
                
            elif alloccontrol_file == alloccontrol[0] and "20.15" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 9: Alloc Control Passed"
                
            if reserved_file != reserved[0] and "20.16" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 9: Reserved = " + str(reserved[0])
                insertstr+="\n+Attr 9: Reserved = " + str(reserved_file)
                
            elif reserved_file == reserved[0] and "20.16" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 9: Reserved Passed"
                
            if nummcast_file != nummcast[0] and "20.17" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 9: Num MCast = " + str(nummcast[0])
                insertstr+="\n+Attr 9: Num MCast = " + str(nummcast_file)
                
            elif nummcast_file == nummcast[0] and "20.17" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 9: Num MCast Passed"
                
            if mcaststartaddr_file != mcaststartaddr[0] and "20.18" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 9: MCast Start Addr = " + str(mcaststartaddr[0])
                insertstr+="\n+Attr 9: MCast Start Addr = " + str(mcaststartaddr_file)
                
            elif mcaststartaddr_file == mcaststartaddr[0] and "20.18" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 9: MCast Start Addr Passed"
                
            if selectacd_file != selectacd[0] and "20.19" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 10: Select ACD = " + str(selectacd[0])
                insertstr+="\n+Attr 10: Select ACD = " + str(selectacd_file)
                
            elif selectacd_file == selectacd[0] and "20.19" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 10: Select ACD Passed"
                
            if acdactivity_file != acdactivity[0] and "20.20" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 11: ACD Activity = " + str(acdactivity[0])
                insertstr+="\n+Attr 11: ACD Activity = " + str(acdactivity_file)
                
            elif acdactivity_file == acdactivity[0] and "20.20" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 11: ACD Activity Passed"
                
            if remotemac_file[:-2] != remotemacstr and "20.21" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 11: RemoteMAC = " + str(remotemacstr)
                insertstr+="\n+Attr 11: RemoteMAC = " + str(remotemac_file[:-2])
                
            elif remotemac_file[:-2] == remotemacstr and "20.21" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 11: RemoteMAC Passed"
                
            if arppdu_file != arppdu[0] and "20.22" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 11: Arp PDU = " + str(arppdu[0])
                insertstr+="\n+Attr 11: Arp PDU = " + str(arppdu_file)
                
            elif arppdu_file == arppdu[0] and "20.22" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 11: Arp PDU Passed"
                
            if eipquickconn_file != eipquickconn[0] and "20.23" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 12: EtherNet/IP Quick Connection = " + str(eipquickconn[0])
                insertstr+="\n+Attr 12: EtherNet/IP Quick Connection = " + str(eipquickconn_file)
                
            elif eipquickconn_file == eipquickconn[0] and "20.23" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 12: EtherNet/IP Quick Connection Passed"
                
            if encapinacttimeout_file != encapinacttimeout[0] and "20.24" in compare_sel:
                compares+=1
                fails+=1
                found=1
                insertstr+= "\n-Attr 13: Encapsulation Inactivity Timeout = " + str(encapinacttimeout[0])
                insertstr+="\n+Attr 13: Encapsulation Inactivity Timeout = " + str(encapinacttimeout_file)
                
            elif encapinacttimeout_file == encapinacttimeout[0] and "20.24" in compare_sel:
                compares+=1
                passes+=1
                found=1
                insertstr+="\nAttr 13: Encapsulation Inactivity Timeout Passed"
                

                
        
        
        if found == 1:
            insertstr+="\n\nCompares = "+str(compares)+"\nPasses = "+str(passes)+"\nFails = "+str(fails)+"\n"
            insertstr= "\n(20) TCP/IP object (0xF5)\n"+insertstr
            t2.insert(END,insertstr)
        
        
        
    if cl.getstatus('CL21')=='on':

        reqsRan+=1
    
        outputstr=""
        outputstr+="\n(21) Ethernet Link object (0xF6)\n"

        service_req = b'\x01'
        class_req = b'\xf6'
        instance_req = b'\x01'
        
        outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, b'\x00')
                
        t.insert(END,outputstr)
        bold_response()
        outputstr=''
                
        if cip_res[42:44] == b'\x00\x00':
            test21=1
            outputstr+="\nTest Passed"
        else:
            test21=2
            outputstr+="\nTest Failed"
        
        t.insert(END,outputstr)
        color_test(test21)
        outputstr=''
        

        
        if checksize==1 and test21==1:
            
            getalllen=len(cip_res[44:])
            service_req = b'\x0e'
            
            
            attribute_req = b'\x01'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen=len(cip_res[44:])

            attribute_req=b'\x02'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x03'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x04'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x05'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x06'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x07'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x08'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x09'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
            
            attribute_req=b'\x0a'
            outputstr,cip_res = requestsendreceive(outputstr,sock,reg_sess, service_req, class_req, instance_req, attribute_req)
            getsinglelen+=len(cip_res[44:])
        
            if getalllen == getsinglelen:
                test21=1
                outputstr+="\nSizes Match"
            else:
                test21=2
                outputstr+="\nSizes Don't Match"
            
            t.insert(END,outputstr)
            color_test(test21)
        
        
        
        elif test21==1:
        
            interfacespeed = struct.unpack("<I",cip_res[44:48])
            outputstr+= "\nAttr 1: Interface Speed = " + str(interfacespeed[0])
            
            interfaceflags = struct.unpack("<I",cip_res[48:52])
            outputstr+= "\nAttr 2: Interface Flags = " + str(hex(interfaceflags[0]))
            
            physaddr = struct.unpack("6B",cip_res[52:58])
            outputstr+= "\nAttr 3: Physical Address = " + str(physaddr[0])+':'+str(physaddr[1])+':'+str(physaddr[2])+':'+str(physaddr[3])+':'+str(physaddr[4])+':'+str(physaddr[5])
            
            inoctets = struct.unpack("<I",cip_res[58:62])
            outputstr+= "\nAttr 4 Interface Counters: In Octets = " + str(inoctets[0])
            
            inucastpackets = struct.unpack("<I",cip_res[62:66])
            outputstr+= "\nAttr 4: In Ucast Packets = " + str(inucastpackets[0])
            
            innucastpackets = struct.unpack("<I",cip_res[66:70])
            outputstr+= "\nAttr 4: In NUcast Packets = " + str(innucastpackets[0])
            
            indiscards = struct.unpack("<I",cip_res[70:74])
            outputstr+= "\nAttr 4: In Discards = " + str(indiscards[0])
            
            inerrors = struct.unpack("<I",cip_res[74:78])
            outputstr+= "\nAttr 4: In Errors = " + str(inerrors[0])
            
            inunknownprotos = struct.unpack("<I",cip_res[78:82])
            outputstr+= "\nAttr 4: In Unknown Protos = " + str(inunknownprotos[0])
            
            outoctets = struct.unpack("<I",cip_res[82:86])
            outputstr+= "\nAttr 4: Out Octets = " + str(outoctets[0])
            
            outucastpackets = struct.unpack("<I",cip_res[86:90])
            outputstr+= "\nAttr 4: Out Ucast Packets = " + str(outucastpackets[0])
            
            outnucastpackets = struct.unpack("<I",cip_res[90:94])
            outputstr+= "\nAttr 4: Out NUcast Packets = " + str(outnucastpackets[0])
            
            outdiscards = struct.unpack("<I",cip_res[94:98])
            outputstr+= "\nAttr 4: Out Discards = " + str(outdiscards[0])
            
            outerrors = struct.unpack("<I",cip_res[98:102])
            outputstr+= "\nAttr 4: Out Errors = " + str(outerrors[0])
            
            alignmenterrors = struct.unpack("<I",cip_res[102:106])
            outputstr+= "\nAttr 5 (Media Counters): Alignment Errors = " + str(alignmenterrors[0])
            
            fcserrors = struct.unpack("<I",cip_res[106:110])
            outputstr+= "\nAttr 5: FCS Errors = " + str(fcserrors[0])
            
            singlecollisions = struct.unpack("<I",cip_res[110:114])
            outputstr+= "\nAttr 5: Single Collisions = " + str(singlecollisions[0])
            
            multiplecollisions = struct.unpack("<I",cip_res[114:118])
            outputstr+= "\nAttr 5: Multiple Collisions = " + str(multiplecollisions[0])
            
            sqetesterrors = struct.unpack("<I",cip_res[118:122])
            outputstr+= "\nAttr 5: SQE Test Errors = " + str(sqetesterrors[0])
            
            deferredtransmission = struct.unpack("<I",cip_res[122:126])
            outputstr+= "\nAttr 5: Deferred Transmission = " + str(deferredtransmission[0])
            
            latecollisions = struct.unpack("<I",cip_res[126:130])
            outputstr+= "\nAttr 5: Late Collisions = " + str(latecollisions[0])
            
            excessivecollisions = struct.unpack("<I",cip_res[130:134])
            outputstr+= "\nAttr 5: Excessive Collisions = " + str(excessivecollisions[0])
            
            mactransmiterrors = struct.unpack("<I",cip_res[134:138])
            outputstr+= "\nAttr 5: MAC Transmit Errors = " + str(mactransmiterrors[0])
            
            carriersenseerrors = struct.unpack("<I",cip_res[138:142])
            outputstr+= "\nAttr 5: Carrier Sense Errors = " + str(carriersenseerrors[0])
            
            frametoolong = struct.unpack("<I",cip_res[142:146])
            outputstr+= "\nAttr 5: Frame Too Long = " + str(frametoolong[0])
            
            macreceiveerrors = struct.unpack("<I",cip_res[146:150])
            outputstr+= "\nAttr 5: MAC Receive Errors = " + str(macreceiveerrors[0])
            
            controlbits = struct.unpack("<H",cip_res[150:152])
            outputstr+= "\nAttr 6 (Interface Control): Control Bits = " + str(hex(controlbits[0]))
            
            forcedinterfacespeed = struct.unpack("<H",cip_res[152:154])
            outputstr+= "\nAttr 6: Forced Interface Speed = " + str(forcedinterfacespeed[0])
            
            interfacetype = struct.unpack("B",bytes([cip_res[154]]))
            outputstr+= "\nAttr 7: Interface Type = " + str(interfacetype[0])
            
            interfacestate = struct.unpack("B",bytes([cip_res[155]]))
            outputstr+= "\nAttr 8: Interface State = " + str(interfacestate[0])
            
            adminstate = struct.unpack("B",bytes([cip_res[156]]))
            outputstr+= "\nAttr 9: Admin State = " + str(adminstate[0])
            
            interfacelabel = struct.unpack("5B",cip_res[157:162])
            outputstr+= "\nAttr 10: Interface Label = " + str(interfacelabel[:])
            
            data = struct.unpack("5B",cip_res[162:167])
            outputstr+= "\nAttr 10: Data = " + str(data[:])
            
            
            outputstr+='\n'
            t.insert(END,outputstr)
        
        


    #Print the appropriate test results
    t.insert(END,"\n")
    if cl.getstatus('CL1')=='on':
        
        if test1==1:
            t.insert(END,"Test 1 Passed: Module Diagnostic object (0x300)")
            color_test2(1)
        elif test1==2:
            t.insert(END,"Test 1 Failed: Module Diagnostic object (0x300)")
            color_test2(2)
        elif test1==0:
            t.insert(END,"Test 1 didn't run: Module Diagnostic object (0x300)\n")
    if cl.getstatus('CL2')=='on':
        if test2==1:
            t.insert(END,"Test 2 Passed: Scanner Diagnostic object (0x301)")
            color_test2(1)
        elif test2==2:
            t.insert(END,"Test 2 Failed: Scanner Diagnostic object (0x301)")
            color_test2(2)
        elif test2==0:
            t.insert(END,"Test 2 didn't run: Scanner Diagnostic object (0x301)\n")
    if cl.getstatus('CL3')=='on':
        if test3==1:
            t.insert(END,"Test 3 Passed: Adapter Diagnostic object (0x302)")
            color_test2(1)
        elif test3==2:
            t.insert(END,"Test 3 Failed: Adapter Diagnostic object (0x302)")
            color_test2(2)
        elif test3==0:
            t.insert(END,"Test 3 didn't run: Adapter Diagnostic object (0x302)\n")
    if cl.getstatus('CL4')=='on':
        if test4==1:
            t.insert(END,"Test 4 Passed: Ethernet Interface Diagnostic object (0x350)")
            color_test2(1)
        elif test4==2:
            t.insert(END,"Test 4 Failed: Ethernet Interface Diagnostic object (0x350)")
            color_test2(2)
        elif test4==0:
            t.insert(END,"Test 4 didn't run: Ethernet Interface Diagnostic object (0x350)\n")
    if cl.getstatus('CL5')=='on':
        if test5==1:
            t.insert(END,"Test 5 Passed: IOScanner Diagnostic object (0x351)")
            color_test2(1)
        elif test5==2:
            t.insert(END,"Test 5 Failed: IOScanner Diagnostic object (0x351)")
            color_test2(2)
        elif test5==0:
            t.insert(END,"Test 5 didn't run: IOScanner Diagnostic object (0x351)\n")
    if cl.getstatus('CL6')=='on':
        if test6==1:
            t.insert(END,"Test 6 Passed: EIP I/O Connection Diagnostic object (0x352)")
            color_test2(1)
        elif test6==2:
            t.insert(END,"Test 6 Failed: EIP I/O Connection Diagnostic object (0x352)")
            color_test2(2)
        elif test6==0:
            t.insert(END,"Test 6 didn't run: EIP I/O Connection Diagnostic object (0x352)\n")
    if cl.getstatus('CL7')=='on':
        if test7==1:
            t.insert(END,"Test 7 Passed: EIP Explicit Connection Diagnostic object (0x353)")
            color_test2(1)
        elif test7==2:
            t.insert(END,"Test 7 Failed: EIP Explicit Connection Diagnostic object (0x353)")
            color_test2(2)
        elif test7==0:
            t.insert(END,"Test 7 didn't run: EIP Explicit Connection Diagnostic object (0x353)\n")
    if cl.getstatus('CL8')=='on':
        if test8==1:
            t.insert(END,"Test 8 Passed: EIP Explicit Connection List object (0x354)")
            color_test2(1)
        elif test8==2:
            t.insert(END,"Test 8 Failed: EIP Explicit Connection List object (0x354)")
            color_test2(2)
        elif test8==0:
            t.insert(END,"Test 8 didn't run: EIP Explicit Connection List object (0x354)\n")
    if cl.getstatus('CL9')=='on':
        if test9==1:
            t.insert(END,"Test 9 Passed: RSTP Diagnostic object (0x355)")
            color_test2(1)
        elif test9==2:
            t.insert(END,"Test 9 Failed: RSTP Diagnostic object (0x355)")
            color_test2(2)
        elif test9==0:
            t.insert(END,"Test 9 didn't run: RSTP Diagnostic object (0x355)\n")
    if cl.getstatus('CL10')=='on':
        if test10==1:
            t.insert(END,"Test 10 Passed: Service Port Control object (0x400)")
            color_test2(1)
        elif test10==2:
            t.insert(END,"Test 10 Failed: Service Port Control object (0x400)")
            color_test2(2)
        elif test10==0:
            t.insert(END,"Test 10 didn't run: Service Port Control object (0x400)\n")
    if cl.getstatus('CL11')=='on':
        if test11==1:
            t.insert(END,"Test 11 Passed: Router Diagnostic object (0x402)")
            color_test2(1)
        elif test11==2:
            t.insert(END,"Test 11 Failed: Router Diagnostic object (0x402)")
            color_test2(2)
        elif test11==0:
            t.insert(END,"Test 11 didn't run: Router Diagnostic object (0x402)\n")
    if cl.getstatus('CL12')=='on':
        if test12==1:
            t.insert(END,"Test 12 Passed: Routing Table Diagnostic object (0x403)")
            color_test2(1)
        elif test12==2:
            t.insert(END,"Test 12 Failed: Routing Table Diagnostic object (0x403)")
            color_test2(2)
        elif test12==0:
            t.insert(END,"Test 12 didn't run: Routing Table Diagnostic object (0x403)\n")
    if cl.getstatus('CL13')=='on':
        if test13==1:
            t.insert(END,"Test 13 Passed: SMTP object (0x404)")
            color_test2(1)
        elif test13==2:
            t.insert(END,"Test 13 Failed: SMTP object (0x404)")
            color_test2(2)
        elif test13==0:
            t.insert(END,"Test 13 didn't run: SMTP object (0x404)\n")
    if cl.getstatus('CL14')=='on':
        if test14==1:
            t.insert(END,"Test 14 Passed: SNTP object (0x405)")
            color_test2(1)
        elif test14==2:
            t.insert(END,"Test 14 Failed: SNTP object (0x405)")
            color_test2(2)
        elif test14==0:
            t.insert(END,"Test 14 didn't run: SNTP object (0x405)\n")
    if cl.getstatus('CL15')=='on':
        if test15==1:
            t.insert(END,"Test 15 Passed: Identity object (0x01)")
            color_test2(1)
        elif test15==2:
            t.insert(END,"Test 15 Failed: Identity object (0x01)")
            color_test2(2)
        elif test15==0:
            t.insert(END,"Test 15 didn't run: Identity object (0x01)\n")
    if cl.getstatus('CL16')=='on':
        if test16==1:
            t.insert(END,"Test 16 Passed: Message Router object (0x02)")
            color_test2(1)
        elif test16==2:
            t.insert(END,"Test 16 Failed: Message Router object (0x02)")
            color_test2(2)
        elif test16==0:
            t.insert(END,"Test 16 didn't run: Message Router object (0x02)\n")
    if cl.getstatus('CL17')=='on':
        if test17==1:
            t.insert(END,"Test 17 Passed: Connection Manager object (0x06)")
            color_test2(1)
        elif test17==2:
            t.insert(END,"Test 17 Failed: Connection Manager object (0x06)")
            color_test2(2)
        elif test17==0:
            t.insert(END,"Test 17 didn't run: Connection Manager object (0x06)\n")
    if cl.getstatus('CL18')=='on':
        if test18==1:
            t.insert(END,"Test 18 Passed: QoS object (0x48)")
            color_test2(1)
        elif test18==2:
            t.insert(END,"Test 18 Failed: QoS object (0x48)")
            color_test2(2)
        elif test18==0:
            t.insert(END,"Test 18 didn't run: QoS object (0x48)\n")
    if cl.getstatus('CL19')=='on':
        if test19==1:
            t.insert(END,"Test 19 Passed: Port object (0xF4)")
            color_test2(1)
        elif test19==2:
            t.insert(END,"Test 19 Failed: Port object (0xF4)")
            color_test2(2)
        elif test19==0:
            t.insert(END,"Test 19 didn't run: Port object (0xF4)\n")
    if cl.getstatus('CL20')=='on':
        if test20==1:
            t.insert(END,"Test 20 Passed: TCP/IP object (0xF5)")
            color_test2(1)
        elif test20==2:
            t.insert(END,"Test 20 Failed: TCP/IP object (0xF5)")
            color_test2(2)
        elif test20==0:
            t.insert(END,"Test 20 didn't run: TCP/IP object (0xF5)\n")
    if cl.getstatus('CL21')=='on':
        if test21==1:
            t.insert(END,"Test 21 Passed: Ethernet Link object (0xF6)")
            color_test2(1)
        elif test21==2:
            t.insert(END,"Test 21 Failed: Ethernet Link object (0xF6)")
            color_test2(2)
        elif test21==0:
            t.insert(END,"Test 21 didn't run: Ethernet Link object (0xF6)\n")

connections = []
#connections_listbox = []
#
# #Event handler for implicit connections
# class ExampleEventHandler(ScannerEventHandler):
#     def __init__(self, connection_event, invalid_event):
#         self.example_established_event = connection_event
#         self.example_invalid_event = invalid_event
#
#     def on_event(self, event, param1, param2):
#         print(event)
#
#     def on_implicit_connection(self, connection, address):
#         print('Implicit connection {} established to "{}".'.format(connection, address))
#         self.example_established_event.set()
#         global connections
#         #global connections_listbox
#         connections.append(connection)
#         l.insert(END, "Connection " + str(len(connections)))
#         #connections_listbox.append("Connection "+str(len(connections)))
#         #connections_listbox.set(connections_listbox.get()+"Connection "+str(len(connections_listbox)+1))
#
#
#     def on_implicit_timeout(self, connection, address):
#         print('Implicit connection {} timed out at "{}".'.format(connection,address))
#
#
#     def on_implicit_invalid_address(self, connection, address):
#         print('Implicit connection {} attempted to invalid address "{}".'.format(connection, address))
#         self.example_invalid_event.set()
#
#     def on_implicit_closed(self, connection, address):
#         print('Implicit connection {} to "{}" closed.'.format(connection, address))
#
#
# #Function to start a new thread and execute createClass1()
# def class1thread():
#
#     thread1 = threading.Thread(target=createClass1)
#     thread1.daemon = True
#     thread1.start()
#
#
#
# scanners = []
# handlers = []
#
# #Start a scanner and create a class 1 connection
# def createClass1():
#
#     producing_rpi_arg = producing_rpi_var.get()
#     if producing_rpi_arg == "":
#         producing_rpi_arg = 30
#     else:
#         producing_rpi_arg = int(producing_rpi_arg)
#     consuming_rpi_arg = producing_rpi_var.get()
#
#     if consuming_rpi_arg == "":
#         consuming_rpi_arg = 30
#     else:
#         consuming_rpi_arg = int(consuming_rpi_arg)
#
#     if runidle_op.get() == '1':
#         run_header_arg = True
#     else:
#         run_header_arg = False
#
#     if timeout_mult_var.get() == '':
#         timeout_mult_arg = 0
#     else:
#         timeout_mult_arg = int(timeout_mult_var.get())
#
#     if transporttype_var.get() == 'multicast':
#         transporttype_arg = ConnectionType.multicast
#     elif transporttype_var.get() == 'point_to_point':
#         transporttype_arg = ConnectionType.point_to_point
#
#
#
#     example_connection = Connection(
#         producing_config=ConnectionConfig(instance=int(producing_instance_var.get()), size=int(producing_size_var.get()), run_header=run_header_arg, rate=producing_rpi_arg, connection_type=transporttype_arg),
#         consuming_config=ConnectionConfig(instance=int(consuming_instance_var.get()), size=int(consuming_size_var.get()), rate=consuming_rpi_arg),
#         config_instance=int(config_instance_var.get()), timeout_multiplier=timeout_mult_arg
#     )
#     example_local_address = local_ip_var.get()
#     example_remote_address = remote_ip_var.get()
#     #example_invalid_address = '192.168.255.255'
#     example_handler = ExampleEventHandler(threading.Event(), threading.Event())
#
#     handlers.append(example_handler)
#
#     with Scanner(address=example_local_address, event_handler=example_handler) as example_scanner:
#         scanners.append(example_scanner)
#
#         example_scanner.open_connection(dest_addr=example_remote_address, connection=example_connection)
#
#         example_handler.example_established_event.wait()
#
#         example_scanner.wait_forever()
#
#         #example_scanner.open_connection(dest_addr=example_invalid_address, connection=example_connection)
#
#         #example_handler.example_invalid_event.wait()
#
#
# #Stop the class 3 scanner.
# def stopScanner3():
#
#     global scanners3
#     scanners3[0].stop()
#     scanners3 = []
#
# #Stop the class 1 scanner
# def stopScanner():
#
#     global scanners
#     scanners[0].stop()
#     scanners = []
#
#
# def createConnthread():
#
#     thread3 = threading.Thread(target=createConnOnly)
#     thread3.daemon = True
#     thread3.start()
#
#
# #Open class 1 connection with an existing scanner
# def createConnOnly():
#
#     global scanners
#     global handlers
#
#     producing_rpi_arg = producing_rpi_var.get()
#     if producing_rpi_arg == "":
#         producing_rpi_arg = 30
#     else:
#         producing_rpi_arg = int(producing_rpi_arg)
#     consuming_rpi_arg = producing_rpi_var.get()
#
#     if consuming_rpi_arg == "":
#         consuming_rpi_arg = 30
#     else:
#         consuming_rpi_arg = int(consuming_rpi_arg)
#
#     if runidle_op.get() == '1':
#         run_header_arg = True
#     else:
#         run_header_arg = False
#
#     if timeout_mult_var.get() == '':
#         timeout_mult_arg = 0
#     else:
#         timeout_mult_arg = int(timeout_mult_var.get())
#
#     if transporttype_var.get() == 'multicast':
#         transporttype_arg = ConnectionType.multicast
#     elif transporttype_var.get() == 'point_to_point':
#         transporttype_arg = ConnectionType.point_to_point
#
#     example_connection = Connection(
#         producing_config=ConnectionConfig(instance=int(producing_instance_var.get()), size=int(producing_size_var.get()),
#                                           run_header=run_header_arg, rate=producing_rpi_arg,
#                                           connection_type=transporttype_arg),
#         consuming_config=ConnectionConfig(instance=int(consuming_instance_var.get()), size=int(consuming_size_var.get()),
#                                           rate=consuming_rpi_arg),
#         config_instance=int(config_instance_var.get()), timeout_multiplier=timeout_mult_arg
#     )
#     example_local_address = local_ip_var.get()
#     example_remote_address = remote_ip_var.get()
#     # example_invalid_address = '192.168.255.255'
#     example_handler = handlers[0]
#
#     example_scanner = scanners[0]
#
#     example_scanner.open_connection(dest_addr=example_remote_address, connection=example_connection)
#
#     example_handler.example_established_event.wait()
#
#     example_scanner.wait_forever()
#
#
#
#
#
# #Assemblies event handler
# class ExampleEventHandler2(ScannerEventHandler):
#     def __init__(self, connection_event, data_event):
#         self.example_established_event = connection_event
#         self.example_data_event = data_event
#
#     def on_assembly_connection(self, assembly):
#         print('Assembly connection {} established.'.format(assembly))
#         self.example_established_event.set()
#
#     def on_assembly_data(self, assembly, data):
#         print('Assembly connection {} received data {}.'.format(assembly, data))
#         self.example_data_event.set()
#
#     def on_assembly_closed(self, assembly):
#         print('Assembly connection {} closed.'.format(assembly))
#
#
#
# def assemblythread():
#
#     thread2 = threading.Thread(target=createAssembly)
#     thread2.daemon = True
#     thread2.start()
#
# #Create an assembly
# def createAssembly():
#     example_producing_assembly = Assembly(instance=int(producing_assembly_var.get()),
#                                           length=int(producing_size_var2.get()), direction=Direction.producing)
#     example_consuming_assembly = Assembly(instance=int(consuming_assembly_var.get()),
#                                           length=int(consuming_size_var2.get()), direction=Direction.consuming)
#     example_local_address = local_ip_var2.get()
#     example_handler = ExampleEventHandler2(threading.Event(), threading.Event())
#
#     with Scanner(address=example_local_address, event_handler=example_handler) as example_scanner:
#         for assembly in (example_producing_assembly, example_consuming_assembly):
#             example_scanner.add_assembly(assembly)
#
#         example_handler.example_established_event.wait()
#
#         example_scanner.wait_forever()
#
#         # Change implicit connection output data of remote device for this event to trigger.
#         #example_handler.example_data_event.wait()
#
#
# #Get a hex value of a service and identify the correct object
# def getService(service):
#
#     if int(service,16) == 1:
#         ret = Service.get_attributes_all
#     elif int(service,16) == 14:
#         ret = Service.get_attribute_single
#
#     return ret
#
#
# #Explicit connection event handler
# class ExampleEventHandlerClass3(ScannerEventHandler):
#     def __init__(self, connection_event, invalid_event):
#         self.example_data_event = connection_event
#         self.example_invalid_event = invalid_event
#
#     def on_explicit_connection(self, connection, address, cip_object):
#         print('Explicit connection {} established to "{}".'.format(connection, address), end='\n\n')
#
#         global connections3
#         #global connections3_listbox
#         connections3.append(connection)
#         l2.insert(END, "Connection " + str(len(connections3)))
#
#
#     def on_explicit_timeout(self, connection, address):
#         print('Explicit connection {} timed out at "{}".'.format(connection, address), end='\n\n')
#
#
#     def on_explicit_data(self, connection, address, cip_object, data):
#         print('Explicit connection {} received data from "{}".\nCIP object {}:\n{}'.format(connection, address, cip_object, data), end='\n\n')
#
#         self.example_data_event.set()
#
#     def on_explicit_invalid_address(self, connection, address):
#         print('Explicit connection {} attempted to invalid address "{}".'.format(connection, address), end='\n\n')
#
#         self.example_invalid_event.set()
#
#     def on_explicit_closed(self, connection, address):
#         print('Explicit connection {} to "{}" closed.'.format(connection, address), end='\n\n')
#
#
#
# def class3thread():
#
#     thread4 = threading.Thread(target=createClass3)
#     thread4.daemon = True
#     thread4.start()
#
#
#
# connections3 = []
# handlers3 = []
# scanners3 = []
#
# #Create a class 3 connection
# def createClass3():
#
#     service = getService(service_ent2.get())
#     class_var = int(class_ent2.get(),16)
#
#     example_connection = Connection(cip_object=CipObject(service, class_var))
#     example_local_address = TCP_IP3.get()
#     example_remote_address = TCP_IP4.get()
#
#     example_handler = ExampleEventHandlerClass3(threading.Event(), threading.Event())
#
#     handlers3.append(example_handler)
#
#     with Scanner(address=example_local_address, event_handler=example_handler) as example_scanner:
#         scanners3.append(example_scanner)
#
#         example_scanner.open_connection(dest_addr=example_remote_address,
#                                         connection=example_connection)
#
#         example_handler.example_data_event.wait()
#
#         example_scanner.wait_forever()
#
#
#
#
# def createConn3thread():
#
#     thread5 = threading.Thread(target=createConn3Only)
#     thread5.daemon = True
#     thread5.start()
#
#
#
# #Create a class 3 connection with an existing scanner
# def createConn3Only():
#
#     service = getService(service_ent2.get())
#     class_var = int(class_ent2.get(), 16)
#
#     example_connection = Connection(cip_object=CipObject(service, class_var))
#     example_local_address = TCP_IP3.get()
#     example_remote_address = TCP_IP4.get()
#
#     example_handler = ExampleEventHandlerClass3(threading.Event(), threading.Event())
#
#     example_handler = handlers3[0]
#
#
#     example_scanner = scanners3[0]
#
#     example_scanner.open_connection(dest_addr=example_remote_address,
#                                     connection=example_connection)
#
#     example_handler.example_data_event.wait()
#
#     example_scanner.wait_forever()





        
#Initialize the GUI
root = tkinter.tix.Tk()
root.title("EIP Tests")

#Create a font with size 10
s = ttk.Style()

myFont = font.Font(size=10)

s.configure('Test.TCheckbutton',font=myFont)





n = ttk.Notebook(root)
n.pack(fill=BOTH,expand=True)
n.pressed_index = None


container = Frame(n)
container.pack(fill=BOTH,expand=True)
#container.grid(row=0,column=0,sticky=NW)

container2 = Frame(n)
container2.pack(fill=BOTH,expand=True)

container3 = Frame(n)
container3.pack(fill=BOTH,expand=True)

n.add(container,text='UCMM')
n.add(container2,text='Class 1')
n.add(container3,text='Class 3')


#Create the first canvas and configure it to use the scrollbar
canvas = Canvas(container,width=1100,height=700)

#Create the first scrollbar
yscrollbar = Scrollbar(container, command=canvas.yview)

canvas.config(yscrollcommand=yscrollbar.set)

canvas.pack(side=LEFT,fill=BOTH,expand=True)
yscrollbar.pack(side=RIGHT,fill=Y)

#canvas.grid(row=0, column=0,sticky=NW)
#yscrollbar.grid(row=0, column=1, sticky=N+S)

canvas2 = Canvas(container2,width=400,height=700)
scroll2 = Scrollbar(container2,command=canvas2.yview)
canvas2.config(yscrollcommand=scroll2.set)
canvas2.pack(side=LEFT,fill=BOTH,expand=True)
scroll2.pack(side=RIGHT,fill=Y)


canvas3 = Canvas(container3,width=400,height=700)
scroll3 = Scrollbar(container3,command=canvas3.yview)
canvas3.config(yscrollcommand=scroll3.set)
canvas3.pack(side=LEFT,fill=BOTH,expand=True)
scroll3.pack(side=RIGHT,fill=Y)




frame = Frame(canvas)
canvas.create_window(0,0, window=frame)

mainframe = Frame(canvas2)
canvas2.create_window(-100,0,window=mainframe)

frame3 = Frame(canvas3)
canvas3.create_window(370,350,window=frame3)



#Create a frame inside the canvas

#frame.rowconfigure(0, weight=1)
#frame.columnconfigure(0, weight=1)

#
# ttk.Label(mainframe, text="Local IP: ").grid(column=0, row=0)
#
# local_ip_var = StringVar()
# producing_instance = ttk.Entry(mainframe, width=15, textvariable=local_ip_var)
# producing_instance.grid(column=0,row=1)
#
#
# ttk.Label(mainframe, text="Remote IP: ").grid(column=0, row=2)
#
# remote_ip_var = StringVar()
# remote_ip = ttk.Entry(mainframe, width=15, textvariable=remote_ip_var)
# remote_ip.grid(column=0,row=3)
#
# ttk.Label(mainframe, text="Producing Instance: ").grid(column=0, row=4)
#
# producing_instance_var = StringVar()
# producing_instance = ttk.Entry(mainframe, width=15, textvariable=producing_instance_var)
# producing_instance.grid(column=0,row=5)
#
# ttk.Label(mainframe, text="Producing Size: ").grid(column=0, row=6)
#
# producing_size_var = StringVar()
# producing_size = ttk.Entry(mainframe, width=15, textvariable=producing_size_var)
# producing_size.grid(column=0,row=7)
#
#
# ttk.Label(mainframe, text="Consuming Instance: ").grid(column=0, row=8)
#
# consuming_instance_var = StringVar()
# consuming_instance = ttk.Entry(mainframe, width=15, textvariable=consuming_instance_var)
# consuming_instance.grid(column=0,row=9)
#
# ttk.Label(mainframe, text="Consuming Size: ").grid(column=0, row=10)
#
# consuming_size_var = StringVar()
# consuming_size = ttk.Entry(mainframe, width=15, textvariable=consuming_size_var)
# consuming_size.grid(column=0,row=11)
#
#
# ttk.Label(mainframe, text="Config Instance: ").grid(column=0, row=12)
#
# config_instance_var = StringVar()
# config_instance = ttk.Entry(mainframe, width=15, textvariable=config_instance_var)
# config_instance.grid(column=0,row=13)
#
#
# ttk.Label(mainframe, text="Producing RPI: ").grid(column=0, row=14)
#
# producing_rpi_var = StringVar()
# producing_rpi = ttk.Entry(mainframe, width=15, textvariable=producing_rpi_var)
# producing_rpi.grid(column=0,row=15)
#
#
# ttk.Label(mainframe, text="Consuming RPI: ").grid(column=0, row=16)
#
# consuming_rpi_var = StringVar()
# consuming_rpi = ttk.Entry(mainframe, width=15, textvariable=consuming_rpi_var)
# consuming_rpi.grid(column=0,row=17)
#
# runidle_op = StringVar()
# runidle_op.set('0')
# runidle = ttk.Checkbutton(mainframe, text='Run/Idle Header', style = 'Test.TCheckbutton', variable=runidle_op, onvalue='1', offvalue='0').grid(column=0, row=18)
#
# ttk.Label(mainframe, text="Transport Type T->O: ").grid(column=0, row=19)
#
# transporttype_var = StringVar()
# transporttype = ttk.Combobox(mainframe, textvariable=transporttype_var)
# transporttype.grid(column=0,row=20)
# transporttype['values'] = ('multicast','point_to_point')
# transporttype.set('multicast')
#
# ttk.Label(mainframe, text="Timeout multiplier \n(timeout = 2 ^ (2 + timeout multiplier)): ").grid(column=0, row=21)
# timeout_mult_var = StringVar()
# timeout_mult = ttk.Entry(mainframe, width=15, textvariable=timeout_mult_var)
# timeout_mult.grid(column=0,row=22)
#
#
# ttk.Button(mainframe, text="Create Scanner", command=class1thread).grid(column=0, row=23)
#
# ttk.Button(mainframe, text="Create Connection", command=createConnthread).grid(column=0, row=24)
#
#
#
# ttk.Label(mainframe, text="Local IP: ").grid(column=1, row=0)
#
# local_ip_var2 = StringVar()
# local_ip2 = ttk.Entry(mainframe, width=15, textvariable=local_ip_var2)
# local_ip2.grid(column=1,row=1)
#
# ttk.Label(mainframe, text="Producing Assembly: ").grid(column=1, row=2)
#
# producing_assembly_var = StringVar()
# producing_assembly = ttk.Entry(mainframe, width=15, textvariable=producing_assembly_var)
# producing_assembly.grid(column=1,row=3)
#
# ttk.Label(mainframe, text="Producing Size: ").grid(column=1, row=4)
#
# producing_size_var2 = StringVar()
# producing_size2 = ttk.Entry(mainframe, width=15, textvariable=producing_size_var2)
# producing_size2.grid(column=1,row=5)
#
# ttk.Label(mainframe, text="Consuming Assembly: ").grid(column=1, row=6)
#
# consuming_assembly_var = StringVar()
# consuming_assembly = ttk.Entry(mainframe, width=15, textvariable=consuming_assembly_var)
# consuming_assembly.grid(column=1,row=7)
#
# ttk.Label(mainframe, text="Consuming Size: ").grid(column=1, row=8)
#
# consuming_size_var2 = StringVar()
# consuming_size2 = ttk.Entry(mainframe, width=15, textvariable=consuming_size_var2)
# consuming_size2.grid(column=1,row=9)
#
#
# ttk.Button(mainframe, text="Create Assembly", command=assemblythread).grid(column=1, row=10)
#
#
#
# #Close the currently selected connection
# def closeConn():
#
#     global connections
#     currSel = l.curselection()
#
#     for x in range(0,len(currSel)):
#         currSel2 = l.curselection()
#         l.delete(currSel2[0])
#         connections[currSel2[0]].close()
#         del connections[currSel2[0]]
#
#
#
# l = Listbox(mainframe, height=10, selectmode='extended')
# l.grid(column=2,row=5)
#
# b = Button(mainframe, text="Close", command=closeConn)
# b.grid(column=2,row=6)
#
#
# b4 = Button(mainframe, text="Stop Scanner", command=stopScanner)
# b4.grid(column=2,row=7)
#
#
# s3 = ttk.Scrollbar( mainframe, orient=VERTICAL, command=l.yview)
# l.configure(yscrollcommand=s3.set)
# s3.grid(column=3,row=5,sticky=NS)


#
# ttk.Button(frame3, text="Toggle All", command=toggleAll).grid(column=0, row=0, sticky=NW)
#
#
# cl2 = tkinter.tix.CheckList(frame3, width=400,height=400)
#
#
# cl2.grid(column=0, row=1, sticky=NW)
#
# cl2.hlist.add("CL0", text="(0) Check/Uncheck All")
# #cl.hlist.add("CL0.Item1", text="subitem1")
# cl2.hlist.add("CL1", text="(1) Module Diagnostic object (0x300)")
# cl2.hlist.add("CL2", text="(2) Scanner Diagnostic object (0x301)")
# cl2.hlist.add("CL3", text="(3) Adapter Diagnostic object (0x302)")
# cl2.hlist.add("CL4", text="(4) Ethernet Interface Diagnostic object (0x350)")
# cl2.hlist.add("CL4.1",text="1 Protocols supported")
# cl2.hlist.add("CL4.2",text="2.1 Max CIP IO Connection opened")
# cl2.hlist.add("CL4.3",text="2.2 Current CIP IO Connections")
# cl2.hlist.add("CL4.4",text="2.3 Max CIP Explicit Connections")
# cl2.hlist.add("CL4.5",text="2.4 Current CIP Explicit Connections")
# cl2.hlist.add("CL4.6",text="2.5 CIP Connections Opening Errors")
# cl2.hlist.add("CL4.7",text="2.6 CIP Connections Timeout Errors")
# cl2.hlist.add("CL4.8",text="2.7 Max EIP TCP Connections opened")
# cl2.hlist.add("CL4.9",text="2.8 Current EIP TCP Connections")
# cl2.hlist.add("CL4.10",text="3.1 IO Production Counter")
# cl2.hlist.add("CL4.11",text="3.2 IO Consumtion Counter")
# cl2.hlist.add("CL4.12",text="3.3 IO Production Send Errors Counter")
# cl2.hlist.add("CL4.13",text="3.4 IO Consumption Receive Errors Counter")
# cl2.hlist.add("CL4.14",text="4.1 Class 3 Msg Send Counter")
# cl2.hlist.add("CL4.15",text="4.2 Class 3 Msg Receive Counter")
# cl2.hlist.add("CL4.16",text="4.3 UCMM Msg Send Counter")
# cl2.hlist.add("CL4.17",text="4.4 UCMM Msg Receive Counter")
# cl2.hlist.add("CL5", text="(5) IOScanner Diagnostic object (0x351)")
# cl2.hlist.add("CL6", text="(6) EIP I/O Connection Diagnostic object (0x352)")
# cl2.hlist.add("CL7", text="(7) EIP Explicit Connection Diagnostic object (0x353)")
# cl2.hlist.add("CL8", text="(8) EIP Explicit Connection List object (0x354)")
# cl2.hlist.add("CL9", text="(9) RSTP Diagnostic object (0x355)")
# cl2.hlist.add("CL9.1", text="1.1 Protocol Spec")
# cl2.hlist.add("CL9.2", text="1.2 Bridge Priority")
# cl2.hlist.add("CL9.3", text="1.3 Time Since Topology Change")
# cl2.hlist.add("CL9.4", text="1.4 Topology Change Count")
# cl2.hlist.add("CL9.5", text="1.5 Designated Root")
# cl2.hlist.add("CL9.6", text="1.6 Root Cost")
# cl2.hlist.add("CL9.7", text="1.7 Root Port")
# cl2.hlist.add("CL9.8", text="1.8 Max Age")
# cl2.hlist.add("CL9.9", text="1.9 Hello Time")
# cl2.hlist.add("CL9.10", text="1.10 Hold Time")
# cl2.hlist.add("CL9.11", text="1.11 Forward Delay")
# cl2.hlist.add("CL9.12", text="1.12 Bridge Max Age")
# cl2.hlist.add("CL9.13", text="1.13 Bridge Hello Time")
# cl2.hlist.add("CL9.14", text="1.14 Bridge Forward Delay")
# cl2.hlist.add("CL9.15", text="2.1 Port")
# cl2.hlist.add("CL9.16", text="2.2 Priority")
# cl2.hlist.add("CL9.17", text="2.3 State")
# cl2.hlist.add("CL9.18", text="2.4 Enable")
# cl2.hlist.add("CL9.19", text="2.5 Path Cost")
# cl2.hlist.add("CL9.20", text="2.6 Designated Root")
# cl2.hlist.add("CL9.21", text="2.7 Designated Cost")
# cl2.hlist.add("CL9.22", text="2.8 Designated Bridge")
# cl2.hlist.add("CL9.23", text="2.9 Designated Port")
# cl2.hlist.add("CL9.24", text="2.10 Forward Transitions Count")
# cl2.hlist.add("CL9.25", text="3.1 Port Number")
# cl2.hlist.add("CL9.26", text="3.2 Admin Edge Port")
# cl2.hlist.add("CL9.27", text="3.3 Oper Edge Port")
# cl2.hlist.add("CL9.28", text="3.4 Auto Edge Port")
# cl2.hlist.add("CL10", text="(10) Service Port Control object (0x400)")
# cl2.hlist.add("CL11", text="(11) Router Diagnostic object (0x402)")
# cl2.hlist.add("CL12", text="(12) Routing Table Diagnostic object (0x403)")
# cl2.hlist.add("CL13", text="(13) SMTP object (0x404)")
# cl2.hlist.add("CL14", text="(14) SNTP object (0x405)")
# cl2.hlist.add("CL15", text="(15) Identity object (0x01)")
# cl2.hlist.add("CL15.1", text="1 Vendor ID")
# cl2.hlist.add("CL15.2", text="2 Device Type")
# cl2.hlist.add("CL15.3", text="3 Product Code")
# cl2.hlist.add("CL15.4", text="4 Revision")
# cl2.hlist.add("CL15.5", text="5 Status")
# cl2.hlist.add("CL15.6", text="6 Serial Number")
# cl2.hlist.add("CL15.7", text="7 Product Name")
# cl2.hlist.add("CL15.8", text="8 State")
# cl2.hlist.add("CL15.9", text="9 Configuration Consistency Value")
# cl2.hlist.add("CL15.10", text="10 Heartbeat Interval")
# cl2.hlist.add("CL16", text="(16) Message router object (0x02)")
# cl2.hlist.add("CL17", text="(17) Connection Manager object (0x06)")
# cl2.hlist.add("CL17.1", text="Open Requests")
# cl2.hlist.add("CL18", text="(18) QoS (Quality of Service) object (0x48)")
# cl2.hlist.add("CL18.1", text="Tag Enable")
# cl2.hlist.add("CL19", text="(19) Port object (0xF4)")
# cl2.hlist.add("CL19.1", text="Port Type")
# cl2.hlist.add("CL20", text="(20) TCP/IP object (0xF5)")
# cl2.hlist.add("CL20.1", text="1 Status")
# cl2.hlist.add("CL20.2", text="2 Configuration Capability")
# cl2.hlist.add("CL20.3", text="3 Configuration Control")
# cl2.hlist.add("CL20.4", text="4 Physical Link")
# cl2.hlist.add("CL20.5", text="5.1 IP Address")
# cl2.hlist.add("CL20.6", text="5.2 Subnet mask")
# cl2.hlist.add("CL20.7", text="5.3 Gateway")
# cl2.hlist.add("CL20.8", text="5.4 Name Server")
# cl2.hlist.add("CL20.9", text="5.5 Name Server2")
# cl2.hlist.add("CL20.10", text="5.6 Domain Name")
# cl2.hlist.add("CL20.11", text="6 Host Name")
# cl2.hlist.add("CL20.12", text="7.1 Safety Network Number (Manual) Date")
# cl2.hlist.add("CL20.13", text="7.2 Safety Network Number (Manual) Time")
# cl2.hlist.add("CL20.14", text="8 TTL Value")
# cl2.hlist.add("CL20.15", text="9.1 Alloc Control")
# cl2.hlist.add("CL20.16", text="9.2 Reserved")
# cl2.hlist.add("CL20.17", text="9.3 Num MCast")
# cl2.hlist.add("CL20.18", text="9.4 MCast Start Addr")
# cl2.hlist.add("CL20.19", text="10 Select ACD")
# cl2.hlist.add("CL20.20", text="11.1 ACD Activity")
# cl2.hlist.add("CL20.21", text="11.2 RemoteMAC")
# cl2.hlist.add("CL20.22", text="11.3 Arp PDU")
# cl2.hlist.add("CL20.23", text="12 EtherNet/IP Quick Connection")
# cl2.hlist.add("CL20.24", text="13 Encapsulation Inactivity Timeout")
# cl2.hlist.add("CL21", text="(21) Ethernet Link object (0xF6)")
# cl2.hlist.add("CL22", text="(22) Custom request")
#
# cl2.setstatus("CL0","off")
# cl2.setstatus("CL1","off")
# cl2.setstatus("CL2","off")
# cl2.setstatus("CL3","off")
# cl2.setstatus("CL4","off")
# cl2.setstatus("CL4.1","off")
# cl2.setstatus("CL4.2","off")
# cl2.setstatus("CL4.3","off")
# cl2.setstatus("CL4.4","off")
# cl2.setstatus("CL4.5","off")
# cl2.setstatus("CL4.6","off")
# cl2.setstatus("CL4.7","off")
# cl2.setstatus("CL4.8","off")
# cl2.setstatus("CL4.9","off")
# cl2.setstatus("CL4.10","off")
# cl2.setstatus("CL4.11","off")
# cl2.setstatus("CL4.12","off")
# cl2.setstatus("CL4.13","off")
# cl2.setstatus("CL4.14","off")
# cl2.setstatus("CL4.15","off")
# cl2.setstatus("CL4.16","off")
# cl2.setstatus("CL4.17","off")
# cl2.setstatus("CL5","off")
# cl2.setstatus("CL6","off")
# cl2.setstatus("CL7","off")
# cl2.setstatus("CL8","off")
# cl2.setstatus("CL9","off")
# cl2.setstatus("CL9.1","off")
# cl2.setstatus("CL9.2","off")
# cl2.setstatus("CL9.3","off")
# cl2.setstatus("CL9.4","off")
# cl2.setstatus("CL9.5","off")
# cl2.setstatus("CL9.6","off")
# cl2.setstatus("CL9.7","off")
# cl2.setstatus("CL9.8","off")
# cl2.setstatus("CL9.9","off")
# cl2.setstatus("CL9.10","off")
# cl2.setstatus("CL9.11","off")
# cl2.setstatus("CL9.12","off")
# cl2.setstatus("CL9.13","off")
# cl2.setstatus("CL9.14","off")
# cl2.setstatus("CL9.15","off")
# cl2.setstatus("CL9.16","off")
# cl2.setstatus("CL9.17","off")
# cl2.setstatus("CL9.18","off")
# cl2.setstatus("CL9.19","off")
# cl2.setstatus("CL9.20","off")
# cl2.setstatus("CL9.21","off")
# cl2.setstatus("CL9.22","off")
# cl2.setstatus("CL9.23","off")
# cl2.setstatus("CL9.24","off")
# cl2.setstatus("CL9.25","off")
# cl2.setstatus("CL9.26","off")
# cl2.setstatus("CL9.27","off")
# cl2.setstatus("CL9.28","off")
# cl2.setstatus("CL10","off")
# cl2.setstatus("CL11","off")
# cl2.setstatus("CL12","off")
# cl2.setstatus("CL13","off")
# cl2.setstatus("CL14","off")
# cl2.setstatus("CL15","off")
# cl2.setstatus("CL15.1","off")
# cl2.setstatus("CL15.2","off")
# cl2.setstatus("CL15.3","off")
# cl2.setstatus("CL15.4","off")
# cl2.setstatus("CL15.5","off")
# cl2.setstatus("CL15.6","off")
# cl2.setstatus("CL15.7","off")
# cl2.setstatus("CL15.8","off")
# cl2.setstatus("CL15.9","off")
# cl2.setstatus("CL15.10","off")
# cl2.setstatus("CL16","off")
# cl2.setstatus("CL17","off")
# cl2.setstatus("CL17.1","off")
# cl2.setstatus("CL18","off")
# cl2.setstatus("CL18.1","off")
# cl2.setstatus("CL19","off")
# cl2.setstatus("CL19.1","off")
# cl2.setstatus("CL20","off")
# cl2.setstatus("CL20.1","off")
# cl2.setstatus("CL20.2","off")
# cl2.setstatus("CL20.3","off")
# cl2.setstatus("CL20.4","off")
# cl2.setstatus("CL20.5","off")
# cl2.setstatus("CL20.6","off")
# cl2.setstatus("CL20.7","off")
# cl2.setstatus("CL20.8","off")
# cl2.setstatus("CL20.9","off")
# cl2.setstatus("CL20.10","off")
# cl2.setstatus("CL20.11","off")
# cl2.setstatus("CL20.12","off")
# cl2.setstatus("CL20.13","off")
# cl2.setstatus("CL20.14","off")
# cl2.setstatus("CL20.15","off")
# cl2.setstatus("CL20.16","off")
# cl2.setstatus("CL20.17","off")
# cl2.setstatus("CL20.18","off")
# cl2.setstatus("CL20.19","off")
# cl2.setstatus("CL20.20","off")
# cl2.setstatus("CL20.21","off")
# cl2.setstatus("CL20.22","off")
# cl2.setstatus("CL20.23","off")
# cl2.setstatus("CL20.24","off")
# cl2.setstatus("CL21","off")
# cl2.setstatus("CL22","off")
# #cl.setstatus("CL0.Item1", "off")
#
# #cl.setmode("CL0",mode="open")
#
# cl2.autosetmode()
#
#
#
# ttk.Label(frame3, text="Local IP: ").grid(column=1, row=0, sticky=N)
#
# TCP_IP3 = StringVar()
# ip_entry2 = ttk.Entry(frame3, width=15, textvariable=TCP_IP3)
# ip_entry2.grid(column=1, row=1, sticky=N, pady=0)
#
# ttk.Label(frame3, text="Remote IP: ").grid(column=1, row=1, sticky=NE, pady=25)
#
# TCP_IP4 = StringVar()
# ip_entry = ttk.Entry(frame3, width=15, textvariable=TCP_IP4)
# ip_entry.grid(column=1, row=1, sticky=NE, pady=50)
#
# ttk.Label(frame3, text="Service (hex): ").grid(column=1, row=1, sticky=NE, pady=75)
#
# service_ent2 = StringVar()
# service_entry2 = ttk.Entry(frame3, width=15, textvariable=service_ent2)
# service_entry2.grid(column=1, row=1, sticky=NE, pady=100)
#
# ttk.Label(frame3, text="Class (hex): ").grid(column=1, row=1, sticky=NE, pady=125)
#
# class_ent2 = StringVar()
# class_entry2 = ttk.Entry(frame3, width=15, textvariable=class_ent2)
# class_entry2.grid(column=1, row=1, sticky=NE, pady=150)
#
# ttk.Label(frame3, text="Instance (hex): ").grid(column=1, row=1, sticky=NE, pady=175)
#
# instance_ent2 = StringVar()
# instance_entry2 = ttk.Entry(frame3, width=15, textvariable=instance_ent2)
# instance_entry2.grid(column=1, row=1, sticky=NE, pady=200)
#
# ttk.Label(frame3, text="Attribute (hex): ").grid(column=1, row=1, sticky=NE, pady=225)
#
# attribute_ent2 = StringVar()
# attribute_entry2 = ttk.Entry(frame3, width=15, textvariable=attribute_ent2)
# attribute_entry2.grid(column=1, row=1, sticky=NE, pady=250)
#
# ttk.Button(frame3, text="Create Scanner", command=class3thread).grid(column=1, row=1, pady=280, sticky=NE)
#
# ttk.Button(frame3, text="Create Connection", command=createConn3thread).grid(column=1, row=1, pady=310, sticky=NE)
#
# l2 = Listbox(frame3, height=10, selectmode='extended')
# l2.grid(column=2,row=1,sticky=N)
#
#
# def closeConn3():
#
#     global connections3
#     currSel = l2.curselection()
#
#     for x in range(0,len(currSel)):
#         currSel2 = l2.curselection()
#         l2.delete(currSel2[0])
#         connections3[currSel2[0]].close()
#         del connections3[currSel2[0]]
#
#
#
# b2 = Button(frame3, text="Close", command=closeConn3)
# b2.grid(column=2,row=1,pady=(0,180))
#
# b3 = Button(frame3, text="Stop Scanner", command=stopScanner3)
# b3.grid(column=2,row=1,pady=(0,120))
#
#
# s4 = ttk.Scrollbar( frame3, orient=VERTICAL, command=l2.yview)
# l2.configure(yscrollcommand=s4.set)
# s4.grid(column=3,row=1,sticky=NS,pady=(0,435))
#
#



ttk.Button(frame, text="Toggle All", command=toggleAll).grid(column=0, row=0, sticky=NW)


cl = tkinter.tix.CheckList(frame, width=400,height=400)


cl.grid(column=0, row=1, sticky=NW)

cl.hlist.add("CL0", text="(0) Check/Uncheck All")
#cl.hlist.add("CL0.Item1", text="subitem1")
cl.hlist.add("CL1", text="(1) Module Diagnostic object (0x300)")
cl.hlist.add("CL2", text="(2) Scanner Diagnostic object (0x301)")
cl.hlist.add("CL3", text="(3) Adapter Diagnostic object (0x302)")
cl.hlist.add("CL4", text="(4) Ethernet Interface Diagnostic object (0x350)")
cl.hlist.add("CL4.1",text="1 Protocols supported")
cl.hlist.add("CL4.2",text="2.1 Max CIP IO Connection opened")
cl.hlist.add("CL4.3",text="2.2 Current CIP IO Connections")
cl.hlist.add("CL4.4",text="2.3 Max CIP Explicit Connections")
cl.hlist.add("CL4.5",text="2.4 Current CIP Explicit Connections")
cl.hlist.add("CL4.6",text="2.5 CIP Connections Opening Errors")
cl.hlist.add("CL4.7",text="2.6 CIP Connections Timeout Errors")
cl.hlist.add("CL4.8",text="2.7 Max EIP TCP Connections opened")
cl.hlist.add("CL4.9",text="2.8 Current EIP TCP Connections")
cl.hlist.add("CL4.10",text="3.1 IO Production Counter")
cl.hlist.add("CL4.11",text="3.2 IO Consumtion Counter")
cl.hlist.add("CL4.12",text="3.3 IO Production Send Errors Counter")
cl.hlist.add("CL4.13",text="3.4 IO Consumption Receive Errors Counter")
cl.hlist.add("CL4.14",text="4.1 Class 3 Msg Send Counter")
cl.hlist.add("CL4.15",text="4.2 Class 3 Msg Receive Counter")
cl.hlist.add("CL4.16",text="4.3 UCMM Msg Send Counter")
cl.hlist.add("CL4.17",text="4.4 UCMM Msg Receive Counter")
cl.hlist.add("CL5", text="(5) IOScanner Diagnostic object (0x351)")
cl.hlist.add("CL6", text="(6) EIP I/O Connection Diagnostic object (0x352)")
cl.hlist.add("CL7", text="(7) EIP Explicit Connection Diagnostic object (0x353)")
cl.hlist.add("CL8", text="(8) EIP Explicit Connection List object (0x354)")
cl.hlist.add("CL9", text="(9) RSTP Diagnostic object (0x355)")
cl.hlist.add("CL9.1", text="1.1 Protocol Spec")
cl.hlist.add("CL9.2", text="1.2 Bridge Priority")
cl.hlist.add("CL9.3", text="1.3 Time Since Topology Change")
cl.hlist.add("CL9.4", text="1.4 Topology Change Count")
cl.hlist.add("CL9.5", text="1.5 Designated Root")
cl.hlist.add("CL9.6", text="1.6 Root Cost")
cl.hlist.add("CL9.7", text="1.7 Root Port")
cl.hlist.add("CL9.8", text="1.8 Max Age")
cl.hlist.add("CL9.9", text="1.9 Hello Time")
cl.hlist.add("CL9.10", text="1.10 Hold Time")
cl.hlist.add("CL9.11", text="1.11 Forward Delay")
cl.hlist.add("CL9.12", text="1.12 Bridge Max Age")
cl.hlist.add("CL9.13", text="1.13 Bridge Hello Time")
cl.hlist.add("CL9.14", text="1.14 Bridge Forward Delay")
cl.hlist.add("CL9.15", text="2.1 Port")
cl.hlist.add("CL9.16", text="2.2 Priority")
cl.hlist.add("CL9.17", text="2.3 State")
cl.hlist.add("CL9.18", text="2.4 Enable")
cl.hlist.add("CL9.19", text="2.5 Path Cost")
cl.hlist.add("CL9.20", text="2.6 Designated Root")
cl.hlist.add("CL9.21", text="2.7 Designated Cost")
cl.hlist.add("CL9.22", text="2.8 Designated Bridge")
cl.hlist.add("CL9.23", text="2.9 Designated Port")
cl.hlist.add("CL9.24", text="2.10 Forward Transitions Count")
cl.hlist.add("CL9.25", text="3.1 Port Number")
cl.hlist.add("CL9.26", text="3.2 Admin Edge Port")
cl.hlist.add("CL9.27", text="3.3 Oper Edge Port")
cl.hlist.add("CL9.28", text="3.4 Auto Edge Port")
cl.hlist.add("CL10", text="(10) Service Port Control object (0x400)")
cl.hlist.add("CL11", text="(11) Router Diagnostic object (0x402)")
cl.hlist.add("CL12", text="(12) Routing Table Diagnostic object (0x403)")
cl.hlist.add("CL13", text="(13) SMTP object (0x404)")
cl.hlist.add("CL14", text="(14) SNTP object (0x405)")
cl.hlist.add("CL15", text="(15) Identity object (0x01)")
cl.hlist.add("CL15.1", text="1 Vendor ID")
cl.hlist.add("CL15.2", text="2 Device Type")
cl.hlist.add("CL15.3", text="3 Product Code")
cl.hlist.add("CL15.4", text="4 Revision")
cl.hlist.add("CL15.5", text="5 Status")
cl.hlist.add("CL15.6", text="6 Serial Number")
cl.hlist.add("CL15.7", text="7 Product Name")
cl.hlist.add("CL15.8", text="8 State")
cl.hlist.add("CL15.9", text="9 Configuration Consistency Value")
cl.hlist.add("CL15.10", text="10 Heartbeat Interval")
cl.hlist.add("CL16", text="(16) Message router object (0x02)")
cl.hlist.add("CL17", text="(17) Connection Manager object (0x06)")
cl.hlist.add("CL17.1", text="Open Requests")
cl.hlist.add("CL18", text="(18) QoS (Quality of Service) object (0x48)")
cl.hlist.add("CL18.1", text="Tag Enable")
cl.hlist.add("CL19", text="(19) Port object (0xF4)")
cl.hlist.add("CL19.1", text="Port Type")
cl.hlist.add("CL20", text="(20) TCP/IP object (0xF5)")
cl.hlist.add("CL20.1", text="1 Status")
cl.hlist.add("CL20.2", text="2 Configuration Capability")
cl.hlist.add("CL20.3", text="3 Configuration Control")
cl.hlist.add("CL20.4", text="4 Physical Link")
cl.hlist.add("CL20.5", text="5.1 IP Address")
cl.hlist.add("CL20.6", text="5.2 Subnet mask")
cl.hlist.add("CL20.7", text="5.3 Gateway")
cl.hlist.add("CL20.8", text="5.4 Name Server")
cl.hlist.add("CL20.9", text="5.5 Name Server2")
cl.hlist.add("CL20.10", text="5.6 Domain Name")
cl.hlist.add("CL20.11", text="6 Host Name")
cl.hlist.add("CL20.12", text="7.1 Safety Network Number (Manual) Date")
cl.hlist.add("CL20.13", text="7.2 Safety Network Number (Manual) Time")
cl.hlist.add("CL20.14", text="8 TTL Value")
cl.hlist.add("CL20.15", text="9.1 Alloc Control")
cl.hlist.add("CL20.16", text="9.2 Reserved")
cl.hlist.add("CL20.17", text="9.3 Num MCast")
cl.hlist.add("CL20.18", text="9.4 MCast Start Addr")
cl.hlist.add("CL20.19", text="10 Select ACD")
cl.hlist.add("CL20.20", text="11.1 ACD Activity")
cl.hlist.add("CL20.21", text="11.2 RemoteMAC")
cl.hlist.add("CL20.22", text="11.3 Arp PDU")
cl.hlist.add("CL20.23", text="12 EtherNet/IP Quick Connection")
cl.hlist.add("CL20.24", text="13 Encapsulation Inactivity Timeout")
cl.hlist.add("CL21", text="(21) Ethernet Link object (0xF6)")
cl.hlist.add("CL22", text="(22) Custom request")
cl.hlist.add("CL23", text="(23) From file")

cl.setstatus("CL0","off")
cl.setstatus("CL1","off")
cl.setstatus("CL2","off")
cl.setstatus("CL3","off")
cl.setstatus("CL4","off")
cl.setstatus("CL4.1","off")
cl.setstatus("CL4.2","off")
cl.setstatus("CL4.3","off")
cl.setstatus("CL4.4","off")
cl.setstatus("CL4.5","off")
cl.setstatus("CL4.6","off")
cl.setstatus("CL4.7","off")
cl.setstatus("CL4.8","off")
cl.setstatus("CL4.9","off")
cl.setstatus("CL4.10","off")
cl.setstatus("CL4.11","off")
cl.setstatus("CL4.12","off")
cl.setstatus("CL4.13","off")
cl.setstatus("CL4.14","off")
cl.setstatus("CL4.15","off")
cl.setstatus("CL4.16","off")
cl.setstatus("CL4.17","off")
cl.setstatus("CL5","off")
cl.setstatus("CL6","off")
cl.setstatus("CL7","off")
cl.setstatus("CL8","off")
cl.setstatus("CL9","off")
cl.setstatus("CL9.1","off")
cl.setstatus("CL9.2","off")
cl.setstatus("CL9.3","off")
cl.setstatus("CL9.4","off")
cl.setstatus("CL9.5","off")
cl.setstatus("CL9.6","off")
cl.setstatus("CL9.7","off")
cl.setstatus("CL9.8","off")
cl.setstatus("CL9.9","off")
cl.setstatus("CL9.10","off")
cl.setstatus("CL9.11","off")
cl.setstatus("CL9.12","off")
cl.setstatus("CL9.13","off")
cl.setstatus("CL9.14","off")
cl.setstatus("CL9.15","off")
cl.setstatus("CL9.16","off")
cl.setstatus("CL9.17","off")
cl.setstatus("CL9.18","off")
cl.setstatus("CL9.19","off")
cl.setstatus("CL9.20","off")
cl.setstatus("CL9.21","off")
cl.setstatus("CL9.22","off")
cl.setstatus("CL9.23","off")
cl.setstatus("CL9.24","off")
cl.setstatus("CL9.25","off")
cl.setstatus("CL9.26","off")
cl.setstatus("CL9.27","off")
cl.setstatus("CL9.28","off")
cl.setstatus("CL10","off")
cl.setstatus("CL11","off")
cl.setstatus("CL12","off")
cl.setstatus("CL13","off")
cl.setstatus("CL14","off")
cl.setstatus("CL15","off")
cl.setstatus("CL15.1","off")
cl.setstatus("CL15.2","off")
cl.setstatus("CL15.3","off")
cl.setstatus("CL15.4","off")
cl.setstatus("CL15.5","off")
cl.setstatus("CL15.6","off")
cl.setstatus("CL15.7","off")
cl.setstatus("CL15.8","off")
cl.setstatus("CL15.9","off")
cl.setstatus("CL15.10","off")
cl.setstatus("CL16","off")
cl.setstatus("CL17","off")
cl.setstatus("CL17.1","off")
cl.setstatus("CL18","off")
cl.setstatus("CL18.1","off")
cl.setstatus("CL19","off")
cl.setstatus("CL19.1","off")
cl.setstatus("CL20","off")
cl.setstatus("CL20.1","off")
cl.setstatus("CL20.2","off")
cl.setstatus("CL20.3","off")
cl.setstatus("CL20.4","off")
cl.setstatus("CL20.5","off")
cl.setstatus("CL20.6","off")
cl.setstatus("CL20.7","off")
cl.setstatus("CL20.8","off")
cl.setstatus("CL20.9","off")
cl.setstatus("CL20.10","off")
cl.setstatus("CL20.11","off")
cl.setstatus("CL20.12","off")
cl.setstatus("CL20.13","off")
cl.setstatus("CL20.14","off")
cl.setstatus("CL20.15","off")
cl.setstatus("CL20.16","off")
cl.setstatus("CL20.17","off")
cl.setstatus("CL20.18","off")
cl.setstatus("CL20.19","off")
cl.setstatus("CL20.20","off")
cl.setstatus("CL20.21","off")
cl.setstatus("CL20.22","off")
cl.setstatus("CL20.23","off")
cl.setstatus("CL20.24","off")
cl.setstatus("CL21","off")
cl.setstatus("CL22","off")
cl.setstatus("CL23","off")
#cl.setstatus("CL0.Item1", "off")

#cl.setmode("CL0",mode="open")

cl.autosetmode()


#def test(cl):

#    print cl.getstatus("CL1")


#ttk.Button(frame, text="Test", command=test(cl)).grid(column=0, row=1, sticky=NW)
    
#Create the checkboxes
# check05 = ttk.Checkbutton(frame, text='(0) Check/Uncheck All', style = 'Test.TCheckbutton', variable=half_op, onvalue='1', offvalue='0', command=toggleAll).grid(column=0, row=0, sticky=NW)
# check = ttk.Checkbutton(frame, text='(1) Module Diagnostic object (0x300)', style = 'Test.TCheckbutton', variable=first_op, onvalue='1', offvalue='0').grid(column=0, row=1, sticky=(N, W))
# check2 = ttk.Checkbutton(frame, text='(2) Scanner Diagnostic object (0x301)', style = 'Test.TCheckbutton', variable=second_op, onvalue='1', offvalue='0').grid(column=0, row=2, sticky=NW)
# check3 = ttk.Checkbutton(frame, text='(3) Adapter Diagnostic object (0x302)', style = 'Test.TCheckbutton', variable=third_op, onvalue='1', offvalue='0').grid(column=0, row=3, sticky=NW)
# check4 = ttk.Checkbutton(frame, text='(4) Ethernet Interface Diagnostic object (0x350)', style = 'Test.TCheckbutton', variable=fourth_op, onvalue='1', offvalue='0').grid(column=0, row=4, sticky=NW)
# check5 = ttk.Checkbutton(frame, text='(5) IOScanner Diagnostic object (0x351)', style = 'Test.TCheckbutton', variable=fifth_op, onvalue='1', offvalue='0').grid(column=0, row=5, sticky=NW)
# check6 = ttk.Checkbutton(frame, text='(6) EIP I/O Connection Diagnostic object (0x352)', style = 'Test.TCheckbutton', variable=sixth_op, onvalue='1', offvalue='0').grid(column=0, row=6, sticky=NW)
# check7 = ttk.Checkbutton(frame, text='(7) EIP Explicit Connection Diagnostic object (0x353)', style = 'Test.TCheckbutton', variable=seventh_op, onvalue='1', offvalue='0').grid(column=0, row=7, sticky=NW)
# check8 = ttk.Checkbutton(frame, text='(8) EIP Explicit Connection List object (0x354)', style = 'Test.TCheckbutton', variable=eighth_op, onvalue='1', offvalue='0').grid(column=0, row=8, sticky=NW)
# check9 = ttk.Checkbutton(frame, text='(9) RSTP Diagnostic object (0x355)', style = 'Test.TCheckbutton', variable=ninth_op, onvalue='1', offvalue='0').grid(column=0, row=9, sticky=NW)
# check10 = ttk.Checkbutton(frame, text='(10) Service Port Control object (0x400)', style = 'Test.TCheckbutton', variable=tenth_op, onvalue='1', offvalue='0').grid(column=0, row=10, sticky=NW)
# check11 = ttk.Checkbutton(frame, text='(11) Router Diagnostic object (0x402)', style = 'Test.TCheckbutton', variable=eleventh_op, onvalue='1', offvalue='0').grid(column=0, row=11, sticky=NW)
# check12 = ttk.Checkbutton(frame, text='(12) Routing Table Diagnostic object (0x403)', style = 'Test.TCheckbutton', variable=twelvth_op, onvalue='1', offvalue='0').grid(column=0, row=12, sticky=NW)
# check13 = ttk.Checkbutton(frame, text='(13) SMTP object (0x404)', style = 'Test.TCheckbutton', variable=thirteenth_op, onvalue='1', offvalue='0').grid(column=0, row=13, sticky=NW)
# check14 = ttk.Checkbutton(frame, text='(14) SNTP object (0x405)', style = 'Test.TCheckbutton', variable=fourteenth_op, onvalue='1', offvalue='0').grid(column=0, row=14, sticky=NW)
# check15 = ttk.Checkbutton(frame, text='(15) Identity object (0x01)', style = 'Test.TCheckbutton', variable=fifteenth_op, onvalue='1', offvalue='0').grid(column=0, row=15, sticky=NW)
# check16 = ttk.Checkbutton(frame, text='(16) Message router object (0x02)', style = 'Test.TCheckbutton', variable=sixteenth_op, onvalue='1', offvalue='0').grid(column=0, row=16, sticky=NW)
# check17 = ttk.Checkbutton(frame, text='(17) Connection Manager object (0x06)', style = 'Test.TCheckbutton', variable=seventeenth_op, onvalue='1', offvalue='0').grid(column=0, row=17, sticky=NW)
# check17 = ttk.Checkbutton(frame, text='(18) QoS (Quality of Service) object (0x48)', style = 'Test.TCheckbutton', variable=eighteenth_op, onvalue='1', offvalue='0').grid(column=0, row=18, sticky=NW)
# check19 = ttk.Checkbutton(frame, text='(19) Port object (0xF4)', style = 'Test.TCheckbutton', variable=nineteenth_op, onvalue='1', offvalue='0').grid(column=0, row=19, sticky=NW)
# check18 = ttk.Checkbutton(frame, text='(20) TCP/IP object (0xF5)', style = 'Test.TCheckbutton', variable=twentieth_op, onvalue='1', offvalue='0').grid(column=0, row=20, sticky=NW)
# check19 = ttk.Checkbutton(frame, text='(21) Ethernet Link object (0xF6)', style = 'Test.TCheckbutton', variable=twentyfirst_op, onvalue='1', offvalue='0').grid(column=0, row=21, sticky=NW)
# check20 = ttk.Checkbutton(frame, text='(22) Custom request', style = 'Test.TCheckbutton', variable=twentysecond_op, onvalue='1', offvalue='0').grid(column=0, row=22, sticky=NW)
    
t_status = Text(frame,width=7,height=1,wrap=WORD,font=myFont)
t_status.grid(column=0,row=1,sticky=N,pady=420)
ttk.Label(frame, text="1-16").grid(column=0, row=1,pady=420,sticky=N, padx=(120,1))

t_status2 = Text(frame,width=7,height=1,wrap=WORD,font=myFont)
t_status2.grid(column=0,row=1,sticky=N,pady=440)
ttk.Label(frame, text="17-32").grid(column=0, row=1,pady=440,sticky=N, padx=(125,1))

t_status3 = Text(frame,width=11,height=1,wrap=WORD,font=myFont)
t_status3.grid(column=0,row=1,sticky=N,pady=460)
ttk.Label(frame, text="33-64").grid(column=0, row=1,pady=460,sticky=N, padx=(135,1))

t_status4 = Text(frame,width=20,height=1,wrap=WORD,font=myFont)
t_status4.grid(column=0,row=1,pady=480,sticky=N)
ttk.Label(frame, text="65-128").grid(column=0, row=1,pady=480,sticky=N, padx=(200,1))

ttk.Button(frame, text="Use Message Router", command=MR).grid(column=0, row=1,pady=400, sticky=NW)

#Initialize the entry variables
TCP_IP = StringVar()

filename_ent=StringVar()


# container2 = Frame(n)
# container2.grid(row=0,column=0)
# n.add(container2,text='Two')

# #Create the second canvas and configure it to use the scrollbar
# canvas2 = Canvas(container2, width=400,height=700)

# #Create the second scrollbar
# yscrollbar2 = Scrollbar(container2, command=canvas2.yview)
# yscrollbar2.grid(row=0, column=1, sticky=N+S)

# canvas2.config(yscrollcommand=yscrollbar2.set)

# canvas2.grid(row=0, column=0, sticky=NE)


# #Create a frame inside the canvas
# mainframe = Frame(canvas2, width=400,height=700)
# mainframe.grid(column=0,row=0, sticky=NE)

# canvas2.create_window(400,700,window=mainframe)


#mainframe.rowconfigure(0, weight=1)
#mainframe.columnconfigure(0, weight=1)
    
#Initialize entry variables
service_ent=StringVar()
class_ent=StringVar()
instance_ent=StringVar()
attribute_ent=StringVar()

#Create the labels, entries, buttons, and textbox


# ttk.Label(frame, text="Local IP: ").grid(column=1, row=0, sticky=N)
#
# TCP_IP2 = StringVar()
# ip_entry2 = ttk.Entry(frame, width=15, textvariable=TCP_IP2)
# ip_entry2.grid(column=1, row=1, sticky=N)


ttk.Label(frame, text="Remote IP: ").grid(column=1, row=0, sticky=NE)

TCP_IP = StringVar()
ip_entry = ttk.Entry(frame, width=15, textvariable=TCP_IP)
ip_entry.grid(column=1, row=1, sticky=NE)
    
ttk.Label(frame, text="Service (hex): ").grid(column=1, row=1, sticky=NE,pady=25)



service_entry = ttk.Entry(frame, width=15, textvariable=service_ent)
service_entry.grid(column=1, row=1, sticky=NE,pady=50)

ttk.Label(frame, text="Class (hex): ").grid(column=1, row=1, sticky=NE,pady=75)

class_entry = ttk.Entry(frame, width=15, textvariable=class_ent)
class_entry.grid(column=1, row=1, sticky=NE,pady=100)

ttk.Label(frame, text="Instance (hex): ").grid(column=1, row=1, sticky=NE,pady=125)

instance_entry = ttk.Entry(frame, width=15, textvariable=instance_ent)
instance_entry.grid(column=1, row=1, sticky=NE,pady=150)

ttk.Label(frame, text="Attribute (hex): ").grid(column=1, row=1, sticky=NE,pady=175)

attribute_entry = ttk.Entry(frame, width=15, textvariable=attribute_ent)
attribute_entry.grid(column=1, row=1, sticky=NE,pady=200)
    
#Create a scrollbar for the textbox



yscrollbar3=Scrollbar(frame)

t = Text(frame,width=40,height=20,yscrollcommand=yscrollbar3.set,wrap=WORD,font=myFont)
t.grid(column=1,row=1,pady=260,sticky=NE)

yscrollbar3.grid(column=2,row=1,pady=(260,1105),sticky=NS)

yscrollbar3.config(command=t.yview)

ttk.Button(frame, text="Send CIP Request", command=sendCIPReq).grid(column=1, row=1,pady=230, sticky=NE)

ttk.Label(frame, text="# of sessions").grid(column=1, row=0, sticky=NW)

sessions_ent = StringVar()
sessions_entry = ttk.Entry(frame, width=10, textvariable=sessions_ent)
sessions_entry.grid(column=1, row=1, sticky=NW)

ttk.Button(frame, text="Run sessions", command=mult_sessions).grid(column=1, row=1,pady=30, sticky=NW)

closeopen_op = StringVar()
closeopen_op.set('0')
check_closeopen = ttk.Checkbutton(frame, text='Close/Open', style = 'Test.TCheckbutton', variable=closeopen_op, onvalue='1', offvalue='0').grid(column=1, row=1,pady=60, sticky=(N, W))

ttk.Label(frame, text="Loop count").grid(column=1, row=1,pady=85, sticky=NW)

loop_count_ent = StringVar()
loop_count_entry = ttk.Entry(frame, width=10, textvariable=loop_count_ent)
loop_count_entry.grid(column=1, row=1,pady=110, sticky=NW)

ttk.Label(frame, text="Loop delay (ms): ").grid(column=1, row=1,pady=135, sticky=NW)

loop_ent = StringVar()
loopStop = StringVar()
loop_entry = ttk.Entry(frame, width=10, textvariable=loop_ent)
loop_entry.grid(column=1, row=1,pady=160, sticky=NW)

ttk.Button(frame, text="Run in loop", command=runLoop).grid(column=1, row=1,pady=195, sticky=NW)

ttk.Button(frame, text="Stop loop", command=stopLoop).grid(column=1, row=1,pady=225, sticky=NW)


ttk.Label(frame, text="Certificate path: ").grid(column=1, row=1,pady=110, sticky=N)

cert_ent = StringVar()
cert_entry = ttk.Entry(frame, width=10, textvariable=cert_ent)
cert_entry.grid(column=1, row=1,pady=135, sticky=N)


ttk.Label(frame, text="Host name: ").grid(column=1, row=1,pady=160, sticky=N)

host_ent = StringVar()
host_entry = ttk.Entry(frame, width=10, textvariable=host_ent)
host_entry.grid(column=1, row=1,pady=195, sticky=N)


ssl_op = StringVar()
ssl_op.set('0')
check_ssl = ttk.Checkbutton(frame, text='SSL', style = 'Test.TCheckbutton', variable=ssl_op, onvalue='1', offvalue='0').grid(column=1, row=1,pady=85, sticky=(N))

ttk.Button(frame, text="Add Compares", command=addCompares).grid(column=1, row=1,pady=225, sticky=N)


ttk.Label(frame, text="Timeout: ").grid(column=1, row=1,pady=645, sticky=N)

timeout_ent = StringVar()
timeout_entry = ttk.Entry(frame, width=10, textvariable=timeout_ent)
timeout_entry.grid(column=1, row=1,pady=670, sticky=N)

ttk.Button(frame, text="Clear", command=clearText).grid(column=1, row=1,pady=645, sticky=NW)

ttk.Button(frame, text="Check sizes", command=checkSizes).grid(column=1, row=1,pady=675, sticky=NW)

comparefile_op = StringVar()
comparefile_op.set('0')
check_compare = ttk.Checkbutton(frame, text='Compare to file(s)', style = 'Test.TCheckbutton', variable=comparefile_op, onvalue='1', offvalue='0').grid(column=1, row=1,pady=705, sticky=(N, W))

compare_ent = StringVar()
compare_entry = ttk.Entry(frame, width=15, textvariable=compare_ent)
compare_entry.grid(column=1, row=1,pady=730, sticky=NW)
compare_ent2 = StringVar()
compare_ent3 = StringVar()
compare_ent4 = StringVar()
compare_ent5 = StringVar()
compare_entry2 = ttk.Entry(frame, width=15, textvariable=compare_ent2)
compare_entry2.grid(column=1, row=1,pady=755, sticky=NW)
compare_entry3 = ttk.Entry(frame, width=15, textvariable=compare_ent3)
compare_entry3.grid(column=1, row=1,pady=780, sticky=NW)
compare_entry4 = ttk.Entry(frame, width=15, textvariable=compare_ent4)
compare_entry4.grid(column=1, row=1,pady=805, sticky=NW)
compare_entry5 = ttk.Entry(frame, width=15, textvariable=compare_ent5)
compare_entry5.grid(column=1, row=1,pady=830, sticky=NW)

ttk.Button(frame, text="Run and compare", command=runAndCompare).grid(column=1, row=1,pady=860, sticky=NW)

ttk.Label(frame, text="Filename: ").grid(column=1, row=1,pady=645, sticky=NE)

filename_entry = ttk.Entry(frame, width=15, textvariable=filename_ent)
filename_entry.grid(column=1, row=1,pady=670, sticky=NE)

ttk.Button(frame, text="Save output to file", command=saveToFile).grid(column=1, row=1,pady=695, sticky=NE)
    
filename2_entry=StringVar()

ttk.Label(frame, text="Filename: ").grid(column=1, row=1,pady=725, sticky=NE)

filename2_entry_obj = ttk.Entry(frame, width=15, textvariable=filename2_entry)
filename2_entry_obj.grid(column=1, row=1,pady=750, sticky=NE)

ttk.Button(frame, text="Run test from file", command=runFromFile).grid(column=1, row=1,pady=775, sticky=NE)
    
ttk.Button(frame, text="Run in loop", command=runFileLoop).grid(column=1, row=1,pady=(805,0), sticky=NE)

#frame3 = Frame(n)
#frame3.grid(row=0,column=0)
#n.add(frame3,text='Three')

ttk.Label(frame, text="Filename: ").grid(column=3, row=0, sticky=NE)

filename3_entry = StringVar()

filename3_entry_obj = ttk.Entry(frame, width=15, textvariable=filename3_entry)
filename3_entry_obj.grid(column=3, row=1, sticky=NE)

ttk.Button(frame, text="Diff output with file", command=diff_outputs).grid(column=3, row=1,pady=30, sticky=NE)

yscrollbar4=Scrollbar(frame)
yscrollbar4.grid(column=4,row=1,pady=(75,1290),sticky=NS)


t2 = Text(frame,width=30,height=20,yscrollcommand=yscrollbar4.set,wrap=WORD,font=myFont)
t2.grid(column=3,row=1,pady=75,sticky=NE)

yscrollbar4.config(command=t2.yview)
    
ttk.Button(frame, text="Clear", command=clearText2).grid(column=3, row=1,pady=470, sticky=NW)
    
    
ttk.Label(frame, text="Filename: ").grid(column=3, row=1,pady=470, sticky=NE)

filenamediff_ent = StringVar()

filenamediff_entry = ttk.Entry(frame, width=15, textvariable=filenamediff_ent)
filenamediff_entry.grid(column=3, row=1,pady=500, sticky=NE)

ttk.Button(frame, text="Save diff to file", command=saveToFile2).grid(column=3, row=1,pady=530, sticky=NE)
    
    
#Create windows with the frames inside the canvases
#canvas.create_window(0,0,anchor=NW,window=frame)

frame.update_idletasks()

canvas.config(scrollregion=canvas.bbox("all"))

#canvas2.create_window(0,0,anchor=NE,window=frame)
frame.update_idletasks()

canvas2.config(scrollregion=canvas2.bbox("all"))

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)





#Run the GUI
root.mainloop()
    
    
    

    
    

#root2 = Tix.Tk()



#root2.update()
#root2.mainloop()
    
    
    
    
    
    
    
    
    
    
