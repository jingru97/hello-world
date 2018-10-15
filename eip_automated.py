
import socket, time, struct, ssl

TCP_IP = input("IP? ")


TCP_PORT = 44818

# Change options to equal 1 to enable them
#
# i.e. option1 = 1
#
# (1) Module Diagnostic object (0x300)
# (2) Scanner Diagnostic object (0x301)
# (3) Adapter Diagnostic object (0x302)
# (4) Ethernet Interface Diagnostic object (0x350)
# (5) IOScanner Diagnostic object (0x351)
# (6) EIP I/O Connection Diagnostic object (0x352)
# (7) EIP Explicit Connection Diagnostic object (0x353)
# (8) EIP Explicit Connection List object (0x354)
# (9) RSTP Diagnostic object (0x355)
# (10) Service Port Control object (0x400)
# (11) Router Diagnostic object (0x402)
# (12) Routing Table Diagnostic object (0x403)
# (13) SMTP object (0x404)
# (14) SNTP object (0x405)
# (15) Identity object (0x01)
# (16) Message router object (0x02)
# (17) Connection Manager object (0x06)
# (18) QoS (Quality of Service) object (0x48)
# (19) Port object (0xF4)
# (20) TCP/IP object (0xF5)
# (21) Ethernet Link object (0xF6)

option1 = 1
option2 = 1
option3 = 1
option4 = 1
option5 = 1
option6 = 1
option7 = 1
option8 = 1
option9 = 1
option10 = 1
option11 = 1
option12 = 1
option13 = 1
option14 = 1
option15 = 1
option16 = 1
option17 = 1
option18 = 1
option19 = 1
option20 = 1
option21 = 1

option22 = 0

file = open("eip_results.txt","w")

# Instance variable for classes 301 and 352
# It is little-endian
# So for example, for 111, make it b'\x11\x01'

instance_manual = input("Instance? (press enter for default of 273) ")

if instance_manual == '':
    instance_manual = b'\x11\x01'
else:
    instance_manual = struct.pack("<H",int(instance_manual))





answered = 0
while 1:

    if answered == 1:
        print("Wrong choice, must be y, n, or blank")

    ssl_choice = input("SSL (y/n)? ")

    if ssl_choice == 'y' or ssl_choice == 'n' or ssl_choice == '':
        break
    else:
        answered = 1


if ssl_choice == 'y':
    cert = input("Certificate path (leave blank for default)? ")
    host = input("Host name (leave blank for default)? ")




#Open a socket, send a register session, and send the CIP requests
def sendCIP():

    global TCP_IP
    global TCP_PORT

    example_handler = ''
    scanner = ''
    compare_sel = '1'
    z=0

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.settimeout(2.0)

    if ssl_choice == 'y':

        if cert == '':
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.verify_mode = ssl.CERT_REQUIRED

            if host != '':
                context.check_hostname = True

            context.load_verify_locations(cert)

        if host != '':
            sock = context.wrap_socket(sock, server_hostname=host)
        else:
            sock = context.wrap_socket(sock)

        sock.connect((TCP_IP, 2221))
    else:
        sock.connect((TCP_IP, TCP_PORT))

    outputstr=''
    sess_hand= b'\x00\x00\x00\x00'
    send_con = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    reg_session,outputstr = EIP_Reg_Session(sock,outputstr, sess_hand, send_con)

    execute_eip(sock,reg_session, compare_sel,z ,scanner, example_handler)

    sock.close()


# Function to send an EIP Register Session packet
def EIP_Reg_Session(s ,outputstr ,sess_hand ,send_con):


    # ENIP Register Session Packet

    # Encapsulation Header
    EIP_COMMAND_REG_SESSION = b'\x65\x00'
    EIP_LENGTH_1 = b'\x04\x00'
    EIP_SESSION_HANDLE_1 =  sess_hand  # b'\x00\x00\x00\x00'
    EIP_SUCCESS_1 = b'\x00\x00\x00\x00'
    EIP_SENDER_CONTEXT_1 = send_con  # b'\x00\x00\x00\x00\x00\x00\x00\x00'
    EIP_OPTIONS_1 = b'\x00\x00\x00\x00'
    EIP_ENCAP_HEADER_1 = EIP_COMMAND_REG_SESSION + EIP_LENGTH_1 + EIP_SESSION_HANDLE_1 + EIP_SUCCESS_1 + EIP_SENDER_CONTEXT_1 + EIP_OPTIONS_1

    # Command Specific Data
    EIP_PROTOCOL_VER = b'\x01\x00'
    EIP_OPTION_FLAGS = b'\x00\x00'
    EIP_COMMAND_SPEC_DATA_1 = EIP_PROTOCOL_VER + EIP_OPTION_FLAGS

    REG_SESSION_FRAME = EIP_ENCAP_HEADER_1 + EIP_COMMAND_SPEC_DATA_1

    outputstr += "\nRegister EIP Session Frame Request\n"

    # Print the request
    reg_session_send = ""
    for b in REG_SESSION_FRAME:
        reg_session_send += hex(b) + " "
    outputstr += reg_session_send + "\n"

    BUFFER_SIZE_REG_SESSION = 82

    # Send the request
    s.send(REG_SESSION_FRAME)

    # Receive the response
    reg_session_rec = s.recv(BUFFER_SIZE_REG_SESSION)

    outputstr += "\nRegister EIP Session Response\n"

    # Print the response
    reg_session_rec_str = ""
    for a in reg_session_rec:
        reg_session_rec_str += hex(a) + " "
    outputstr += reg_session_rec_str + "\n"

    # s.close()

    return reg_session_rec, outputstr


# Function to send a CIP packet given the EIP Session data from the above function, the service, class, instance, and attribute
def EIP_CIP(sock, outputstr, reg_session_data, service, class_var, instance_var, attribute_var):
    global responsetimes
    global responsefile
    # EtherNet/IP send data
    # Encapsulation Header

    EIP_COMMAND = b'\x6f\x00'
    if service == b'\x0e' and (
        (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1)):
        EIP_LENGTH = b'\x1a\x00'
    elif service == b'\x0e' and len(class_var) == 1 and len(instance_var) == 1:
        EIP_LENGTH = b'\x18\x00'
    elif service == b'\x0e' and len(class_var) == 2 and len(instance_var) == 2:
        EIP_LENGTH = b'\x1c\x00'
    elif service == b'\x01' and len(class_var) == 1 and len(instance_var) == 1:
        EIP_LENGTH = b'\x16\x00'
    elif service == b'\x01' and (
        (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1)):
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
    EIP_INTHAND = b'\x00\x00\x00\x00'  # CIP
    EIP_TIMEOUT = b'\x00\x04'
    EIP_ITEM_COUNT = b'\x02\x00'
    EIP_TYPE_ITEM1_ID = b'\x00\x00'
    EIP_TYPE_ITEM1_LEN = b'\x00\x00'
    EIP_TYPE_ITEM2_ID = b'\xb2\x00'
    if service == b'\x0e' and (
        (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1)):
        EIP_TYPE_ITEM2_LEN = b'\x0a\x00'
    elif service == b'\x0e' and len(class_var) == 1 and len(instance_var) == 1:
        EIP_TYPE_ITEM2_LEN = b'\x08\x00'
    elif service == b'\x0e' and len(class_var) == 2 and len(instance_var) == 2:
        EIP_TYPE_ITEM2_LEN = b'\x0c\x00'
    elif service == b'\x01' and len(class_var) == 1 and len(instance_var) == 1:
        EIP_TYPE_ITEM2_LEN = b'\x06\x00'
    elif service == b'\x01' and (
        (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1)):
        EIP_TYPE_ITEM2_LEN = b'\x08\x00'
    elif service == b'\x01' and len(class_var) == 2 and len(instance_var) == 2:
        EIP_TYPE_ITEM2_LEN = b'\x0a\x00'
    else:
        EIP_TYPE_ITEM2_LEN = b'\x0a\x00'

    EIP_COMMAND_SPEC_DATA = EIP_INTHAND + EIP_TIMEOUT + EIP_ITEM_COUNT + EIP_TYPE_ITEM1_ID + EIP_TYPE_ITEM1_LEN + EIP_TYPE_ITEM2_ID + EIP_TYPE_ITEM2_LEN

    # CIP
    CIP_SERVICE = service

    if service == b'\x0e' and (
        (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1)):
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
    elif service == b'\x01' and (
        (len(class_var) == 1 and len(instance_var) == 2) or (len(class_var) == 2 and len(instance_var) == 1)):
        CIP_REQ_SIZE = b'\x03'
        CIP_REQ_PATH = b'\x21\x00' + class_var + b'\x24' + instance_var
    elif service == b'\x01' and len(class_var) == 2 and len(instance_var) == 2:
        CIP_REQ_SIZE = b'\x04'
        CIP_REQ_PATH = b'\x21\x00' + class_var + b'\x25\x00' + instance_var
    else:
        CIP_REQ_SIZE = b'\x04'
        CIP_REQ_PATH = b'\x21\x00' + class_var + b'\x24' + instance_var + b'\x30' + attribute_var  # Param 1 Run Forward

    CIP = CIP_SERVICE + CIP_REQ_SIZE + CIP_REQ_PATH

    # glue all together
    CIP_FRAME = EIP_ENCAP_HEADER + EIP_COMMAND_SPEC_DATA + CIP

    outputstr += "\nCIP Frame Request\n"

    # Print the request
    cip_frame_send = ""
    for b in CIP_FRAME:
        cip_frame_send += hex(b) + " "
    outputstr += cip_frame_send + "\n"

    BUFFER_SIZE_CIP = 400

    try:

        sock.settimeout(2.0)

        starttime = time.clock()

        # Send the request
        sock.send(CIP_FRAME)

        # Receive the response
        cip_rec = sock.recv(BUFFER_SIZE_CIP)

        timetaken = time.clock() - starttime


    except socket.timeout:
        outputstr = "Timed out"
        return -1, outputstr

    outputstr += "\nCIP Frame Response\n"

    # Print the response
    cip_rec_str = ""
    for b in cip_rec:
        cip_rec_str += hex(b) + " "
    outputstr += cip_rec_str + "\n"

    # outputstr+="\nResponse time = %.5f\n" % timetaken

    timetaken = "%.5f" % timetaken

    #responsetimes.append(timetaken)

    try:
        if 'responsefile' in globals():
            responsefile.write(timetaken + "\n")
    except ValueError:
        pass

    outputstr += "\nResponse time = " + timetaken + "\n"

    # s.close()

    return cip_rec, outputstr


#Redundant function to send a CIP request
def requestsendreceive(outputstr, s, reg_sess, service_req, class_req, instance_req, attribute_req):
    # t = Timer("cip_res,outputstr = EIP_CIP(s,outputstr, reg_sess, service_req, class_req, instance_req, attribute_req)", "from __main__ import EIP_CIP")

    # print t.timeit(number=1)
    cip_res, outputstr = EIP_CIP(s, outputstr, reg_sess, service_req, class_req, instance_req, attribute_req)

    return outputstr, cip_res


#Send all the CIP requests that are selected
def execute_eip(sock, reg_sess, compare_sel, z, scanner, example_handler):

    global instance_manual

    global file

    global reqsRan
    global checksize
    global runAndCompare

    global compares
    global passes
    global fails

    global status

    global option1
    global option2
    global option3
    global option4
    global option5
    global option6
    global option7
    global option8
    global option9
    global option10
    global option11
    global option12
    global option13
    global option14
    global option15
    global option16
    global option17
    global option18
    global option19
    global option20
    global option21
    global option22



    # Initialize the flags that indicate the result of a test
    test1 = 0
    test2 = 0
    test3 = 0
    test4 = 0
    test5 = 0
    test6 = 0
    test7 = 0
    test8 = 0
    test9 = 0
    test10 = 0
    test11 = 0
    test12 = 0
    test13 = 0
    test14 = 0
    test15 = 0
    test16 = 0
    test17 = 0
    test18 = 0
    test19 = 0
    test20 = 0
    test21 = 0

   # insertstr = "\nExecuting cases "

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

    #insertstr += "\n"

    #t.insert(END, insertstr)

    # Custom CIP request
    if option22 == 1:

        reqsRan += 1

        # Ask the user for the service, class, instance, and attribute to build the request packet
        service_req = service_ent.get()
        class_req = class_ent.get()
        instance_req = instance_ent.get()
        attribute_req = attribute_ent.get()

        # Convert the input into byte strings
        service_req = struct.pack('B', int(service_req, 16))
        if len(class_req) > 2:
            class_req = struct.pack('<H', int(class_req, 16))
        else:
            instance_req = struct.pack('B', int(instance_req, 16))
        if len(instance_req) > 2:
            instance_req = struct.pack('<H', int(instance_req, 16))
        else:
            instance_req = struct.pack('B', int(instance_req, 16))
        attribute_req = struct.pack('B', int(attribute_req, 16))

        caseFound = 0
        if service_req == b'\x0e' and class_req == b'\x00\x03' and instance_req == b'\x01' and attribute_req == b'\x01':
            cl.setstatus("CL1", "on")
            caseFound = 1
            t.insert(END, "Custom is case 1")
        elif service_req == b'\x01' and class_req == b'\x01\x03':
            cl.setstatus("CL2", "on")
            caseFound = 1
            t.insert(END, "Custom is case 2")
        elif service_req == b'\x01' and class_req == b'\x02\x03' and instance_req == b'\x01' and attribute_req == b'\x01':
            cl.setstatus("CL3", "on")
            caseFound = 1
            t.insert(END, "Custom is case 3")
        elif service_req == b'\x01' and class_req == b'\x50\x03' and instance_req == b'\x01' and attribute_req == b'\x01':
            cl.setstatus("CL4", "on")
            caseFound = 1
            t.insert(END, "Custom is case 4")

        if caseFound == 0:
            outputstr = ""

            outputstr += "\n(22) Custom request\n"
            outputstr += "Service = " + service_ent.get() + ",Class = " + class_ent.get() + ",Instance = " + instance_ent.get() + ",Attribute = " + attribute_ent.get() + "\n"

            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    attribute_req)

            t.insert(END, outputstr)
            bold_response()
            outputstr = ''

    # Run the tests depending on which checkboxes are checked

    if option1 == 1:

        #reqsRan += 1

        # if runall==1:
        #     selection='2'
        outputstr = ""
        outputstr += "\n(1) Module Diagnostic object (0x300)\n"

        # Initialize service, class, instance, and attribute for the request
        service_req = b'\x0e'
        class_req = b'\x00\x03'
        instance_req = b'\x01'
        attribute_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

     #   t.insert(END, outputstr)
     #   bold_response()
     #   outputstr = ''

        # Check if byte 43 is 00 to indicate success
        if cip_res[42] == 0:
            test1 = 1
            outputstr += "\nTest Passed"
        else:
            test1 = 2
            outputstr += "\nTest Failed"

        getalllen = len(cip_res[44:])

        # Insert the string we created into the end of the textbox
        #t.insert(END, outputstr)
        #color_test(test1)

    if option2 == 1:

        #reqsRan += 1

        outputstr = ""
        outputstr += "\n(2) Scanner Diagnostic object (0x301)\n"

        service_req = b'\x01'
        class_req = b'\x01\x03'
       # if instance_ent.get() == "":
       #     instance_req = b'\x11\x01'
       # else:
       #     instance_req = instance_ent.get()
       #     if len(instance_req) > 2:
       #         instance_req = struct.pack('<H', int(instance_req, 16))
       #     else:
       #         instance_req = struct.pack('B', int(instance_req, 16))
        instance_req = instance_manual
        attribute_req = ''

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

     #   t.insert(END, outputstr)
     #   bold_response()
     #   outputstr = ''

        if cip_res[42] == 5:
            instance_req = b'\x01\x01'
            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    attribute_req)

        if cip_res[42] == 0:
            test2 = 1
            outputstr += "\nTest Passed"
        else:
            test2 = 2
            outputstr += "\nTest Failed"

     #   t.insert(END, outputstr)
     #   color_test(test2)

    if option3 == 1:

        #reqsRan += 1

        outputstr = ""
        outputstr += "\n(3) Adapter Diagnostic object (0x302)\n"

        service_req = b'\x01'
        class_req = b'\x02\x03'
        instance_req = b'\x01'
        attribute_req = b'\x01'

        # example_cip_object = CipObject(Service.get_attributes_all, class_=0x302)


        # scanner.send_unconnected(dest_addr=TCP_IP.get(), cip_object=example_cip_object)


        # example_handler.example_response_event.wait()



        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

        #t.insert(END, outputstr)
        #bold_response()
        #outputstr = ''

        if cip_res[42] == 0:
            test3 = 1
            outputstr += "\nTest Passed"
        else:
            test3 = 2
            outputstr += "\nTest Failed"

        #t.insert(END, outputstr)
        #color_test(test3)

    if option4 == 1:

        if z == 0 or runAndCompare_var == 1:

           # reqsRan += 1

            outputstr = ""
            outputstr += "\n(4) Ethernet Interface Diagnostic object (0x350)\n"

            service_req = b'\x01'
            class_req = b'\x50\x03'
            instance_req = b'\x01'
            attribute_req = b'\x01'

            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    attribute_req)

          #  t.insert(END, outputstr)
          #  bold_response()
          #  outputstr = ''

            if cip_res[42] == 0:
                test4 = 1
                outputstr += "\nTest Passed"
            else:
                test4 = 2
                outputstr += "\nTest Failed"

          #  t.insert(END, outputstr)
          #  color_test(test4)
          #  outputstr = ''



            # if test4 == 1:
            #
            #     global protocolssupported
            #     protocolssupported = struct.unpack("<H", cip_res[44:46])
            #     outputstr += "\nAttr 1: Protocols supported = " + str(protocolssupported[0])
            #
            #     global maxcipioconnsopened
            #     maxcipioconnsopened = struct.unpack("<H", cip_res[46:48])
            #     outputstr += "\nAttr 2 (Connection Diag): Max CIP IO Connection opened = " + str(maxcipioconnsopened[0])
            #
            #     global currentcipioconns
            #     currentcipioconns = struct.unpack("<H", cip_res[48:50])
            #     outputstr += "\nAttr 2: Current CIP IO Connections = " + str(currentcipioconns[0])
            #
            #     global maxcipexpconnsopened
            #     maxcipexpconnsopened = struct.unpack("<H", cip_res[50:52])
            #     outputstr += "\nAttr 2: Max CIP Explicit Connections = " + str(maxcipexpconnsopened[0])
            #
            #     global currentcipexpconns
            #     currentcipexpconns = struct.unpack("<H", cip_res[52:54])
            #     outputstr += "\nAttr 2: Current CIP Explicit Connections = " + str(currentcipexpconns[0])
            #
            #     global cipconnsopeningerrors
            #     cipconnsopeningerrors = struct.unpack("<H", cip_res[54:56])
            #     outputstr += "\nAttr 2: CIP Connections Opening Errors = " + str(cipconnsopeningerrors[0])
            #
            #     global cipconnstimeouterrors
            #     cipconnstimeouterrors = struct.unpack("<H", cip_res[56:58])
            #     outputstr += "\nAttr 2: CIP Connections Timeout Errors = " + str(cipconnstimeouterrors[0])
            #
            #     global maxeiptcpconnsopened
            #     maxeiptcpconnsopened = struct.unpack("<H", cip_res[58:60])
            #     outputstr += "\nAttr 2: Max EIP TCP Connections opened = " + str(maxeiptcpconnsopened[0])
            #
            #     global currenteiptcpconns
            #     currenteiptcpconns = struct.unpack("<H", cip_res[60:62])
            #     outputstr += "\nAttr 2: Current EIP TCP Connections = " + str(currenteiptcpconns[0])
            #
            #     global ioproductionctr
            #     ioproductionctr = struct.unpack("<I", cip_res[62:66])
            #     outputstr += "\nAttr 3 (IO Messaging Diag): IO Production Counter = " + str(ioproductionctr[0])
            #
            #     global ioconsumptionctr
            #     ioconsumptionctr = struct.unpack("<I", cip_res[66:70])
            #     outputstr += "\nAttr 3: IO Consumption Counter = " + str(ioconsumptionctr[0])
            #
            #     global ioproductionsenderrorsctr
            #     ioproductionsenderrorsctr = struct.unpack("<H", cip_res[70:72])
            #     outputstr += "\nAttr 3: IO Production Send Errors Counter = " + str(ioproductionsenderrorsctr[0])
            #
            #     global ioconsumptionrecverrorsctr
            #     ioconsumptionrecverrorsctr = struct.unpack("<H", cip_res[72:74])
            #     outputstr += "\nAttr 3: IO Consumption Receive Errors Counter = " + str(ioconsumptionrecverrorsctr[0])
            #
            #     global class3msgsendctr
            #     class3msgsendctr = struct.unpack("<I", cip_res[74:78])
            #     outputstr += "\nAttr 4 (Explicit Messaging Diag): Class 3 Msg Send Counter = " + str(
            #         class3msgsendctr[0])
            #
            #     global class3msgrecvctr
            #     class3msgrecvctr = struct.unpack("<I", cip_res[78:82])
            #     outputstr += "\nAttr 4: Class 3 Msg Receive Counter = " + str(class3msgrecvctr[0])
            #
            #     global ucmmmsgsendctr
            #     ucmmmsgsendctr = struct.unpack("<I", cip_res[82:86])
            #     outputstr += "\nAttr 4: UCMM Msg Send Counter = " + str(ucmmmsgsendctr[0])
            #
            #     global ucmmmsgrecvctr
            #     ucmmmsgrecvctr = struct.unpack("<I", cip_res[86:90])
            #     outputstr += "\nAttr 4: UCMM Msg Receive Counter = " + str(ucmmmsgrecvctr[0])

                outputstr += '\n'
            #    t.insert(END, outputstr)


    if option5 == 1:

       # reqsRan += 1

        outputstr = ""
        outputstr += "\n(5) IOScanner Diagnostic object (0x351)\n"

        service_req = b'\x0e'
        class_req = b'\x51\x03'
        instance_req = b'\x01'
        attribute_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

       # t.insert(END, outputstr)
       # bold_response()
       # outputstr = ''

        if cip_res[42] == 0:
            test5 = 1
            outputstr += "\nTest Passed"
        else:
            test5 = 2
            outputstr += "\nTest Failed"

       # t.insert(END, outputstr)
      #  color_test(test5)
       # outputstr = ''




        if test5 == 1:

            size = struct.unpack("<H", cip_res[44:46])
            outputstr += "\nAttr 1: IO Status Table: Size = " + str(size[0])

            global status1
            status1 = struct.unpack("<" + str(int(size[0] / 2)) + "H", cip_res[46:(size[0] + 46)])
            outputstr += "\nAttr 1: Status = " + str(status1)

            #outputstr += '\n'
            #t.insert(END, outputstr)

    if option6 == 1:

      #  reqsRan += 1

        outputstr = ""
        outputstr += "\n(6) EIP I/O Connection Diagnostic object (0x352)\n"

        service_req = b'\x01'
        class_req = b'\x52\x03'
    #    if instance_ent.get() == "":
    #        instance_req = b'\x11\x01'
     #   else:
     #       instance_req = instance_ent.get()
     #       if len(instance_req) > 2:
     #           instance_req = struct.pack('<H', int(instance_req, 16))
     #       else:
     #           instance_req = struct.pack('B', int(instance_req, 16))
        instance_req = instance_manual
        attribute_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

        if cip_res[42] == 5:
            instance_req = b'\x01\x01'
            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    attribute_req)

      #  t.insert(END, outputstr)
      #  bold_response()
       # outputstr = ''

        if cip_res[42] == 0:
            test6 = 1
            outputstr += "\nTest Passed"
        else:
            test6 = 2
            outputstr += "\nTest Failed"

       # t.insert(END, outputstr)
       # color_test(test6)
       # outputstr = ''


        # if test6 == 1:
        #
        #     ioprodctr = struct.unpack("<I", cip_res[44:48])
        #     outputstr += "\nAttr 1 (IO Com Diag): IO Production Counter = " + str(ioprodctr[0])
        #
        #     ioconsctr = struct.unpack("<I", cip_res[48:52])
        #     outputstr += "\nAttr 1: IO Consumption Counter = " + str(ioconsctr[0])
        #
        #     ioprodsenderrsctr = struct.unpack("<H", cip_res[52:54])
        #     outputstr += "\nAttr 1: IO Production Send Errors Counter = " + str(ioprodsenderrsctr[0])
        #
        #     ioconsrecverrsctr = struct.unpack("<H", cip_res[54:56])
        #     outputstr += "\nAttr 1: IO Consumption Receive Errors Counter = " + str(ioconsrecverrsctr[0])
        #
        #     cipconntimeouterrs = struct.unpack("<H", cip_res[56:58])
        #     outputstr += "\nAttr 1: CIP Connection TimeOut Errors = " + str(cipconntimeouterrs[0])
        #
        #     cipconnopeningerrs = struct.unpack("<H", cip_res[58:60])
        #     outputstr += "\nAttr 1: CIP Connection Opening Errors = " + str(cipconnopeningerrs[0])
        #
        #     cipconnstate = struct.unpack("<H", cip_res[60:62])
        #     outputstr += "\nAttr 1: CIP Connection State = " + str(cipconnstate[0])
        #
        #     ciplasterrgenstatus = struct.unpack("<H", cip_res[62:64])
        #     outputstr += "\nAttr 1: CIP Last Error General Status = " + str(ciplasterrgenstatus[0])
        #
        #     ciplasterrextstatus = struct.unpack("<H", cip_res[64:66])
        #     outputstr += "\nAttr 1: CIP Last Error Extended Status = " + str(ciplasterrextstatus[0])
        #
        #     inputcomstatus = struct.unpack("<H", cip_res[66:68])
        #     outputstr += "\nAttr 1: Input Com Status = " + str(inputcomstatus[0])
        #
        #     outputcomstatus = struct.unpack("<H", cip_res[68:70])
        #     outputstr += "\nAttr 1: Output Com Status = " + str(outputcomstatus[0])
        #
        #     prodconnid = struct.unpack("<I", cip_res[70:74])
        #     outputstr += "\nAttr 2 (Connection Diag): Production Connection ID = " + str(prodconnid[0])
        #
        #     consconnid = struct.unpack("<I", cip_res[74:78])
        #     outputstr += "\nAttr 2: Consumption Connection ID = " + str(consconnid[0])
        #
        #     prodrpi = struct.unpack("<I", cip_res[78:82])
        #     outputstr += "\nAttr 2: Production RPI = " + str(prodrpi[0])
        #
        #     prodapi = struct.unpack("<I", cip_res[82:86])
        #     outputstr += "\nAttr 2: Production API = " + str(prodapi[0])
        #
        #     consrpi = struct.unpack("<I", cip_res[86:90])
        #     outputstr += "\nAttr 2: Consumption RPI = " + str(consrpi[0])
        #
        #     consapi = struct.unpack("<I", cip_res[90:94])
        #     outputstr += "\nAttr 2: Consumption API = " + str(consapi[0])
        #
        #     prodconnpara = struct.unpack("<I", cip_res[94:98])
        #     outputstr += "\nAttr 2: Production Connection Parameters = " + str(prodconnpara[0])
        #
        #     consconnpara = struct.unpack("<I", cip_res[98:102])
        #     outputstr += "\nAttr 2: Consumption Connection Parameters = " + str(consconnpara[0])
        #
        #     localip = struct.unpack("<I", cip_res[102:106])
        #     outputstr += "\nAttr 2: Local IP = " + str(localip[0])
        #
        #     localudpport = struct.unpack("<H", cip_res[106:108])
        #     outputstr += "\nAttr 2: Local UDP Port = " + str(localudpport[0])
        #
        #     remoteip = struct.unpack("<I", cip_res[108:112])
        #     outputstr += "\nAttr 2: Remote IP = " + str(remoteip[0])
        #
        #     remoteudpport = struct.unpack("<H", cip_res[112:114])
        #     outputstr += "\nAttr 2: Remote UDP Port = " + str(remoteudpport[0])
        #
        #     prodmulticastip = struct.unpack("<I", cip_res[114:118])
        #     outputstr += "\nAttr 2: Production Multicast IP = " + str(prodmulticastip[0])
        #
        #     consmulticastip = struct.unpack("<I", cip_res[118:122])
        #     outputstr += "\nAttr 2: Consumption Multicast IP = " + str(consmulticastip[0])
        #
        #     protocolssupported = struct.unpack("<H", cip_res[122:124])
        #     outputstr += "\nAttr 2: Protocols supported = " + str(protocolssupported[0])

          #  outputstr += '\n'
         #   t.insert(END, outputstr)

    if option7 == 1:

      #  reqsRan += 1

        outputstr = ""
        outputstr += "\n(7) EIP Explicit Connection Diagnostic object (0x353)\n"

        service_req = b'\x01'
        class_req = b'\x53\x03'
        instance_req = b'\x01'
        attribute_req = ''

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

    #    t.insert(END, outputstr)
    #    bold_response()
    #    outputstr = ''

        if cip_res[42] == 0:
            test7 = 1
            outputstr += "\nTest Passed"
        else:
            test7 = 2
            outputstr += "\nTest Failed"

    #    t.insert(END, outputstr)
    #    color_test(test7)
    #    outputstr = ''



        if test7 == 1:

            origconnid = struct.unpack("<I", cip_res[44:48])
            outputstr += "\nAttr 1: Originator Connection ID = " + str(origconnid[0])

            origip = struct.unpack("<I", cip_res[48:52])
            outputstr += "\nAttr 2: Originator IP = " + str(origip[0])

            origtcpport = struct.unpack("<H", cip_res[52:54])
            outputstr += "\nAttr 3: Originator TCP Port = " + str(origtcpport[0])

            targetconnid = struct.unpack("<I", cip_res[54:58])
            outputstr += "\nAttr 4: Target Connection ID = " + str(targetconnid[0])

            targetip = struct.unpack("<I", cip_res[58:62])
            outputstr += "\nAttr 5: Target IP = " + str(targetip[0])

            targettcpport = struct.unpack("<H", cip_res[62:64])
            outputstr += "\nAttr 6: Target TCP Port = " + str(targettcpport[0])

            msgsendctr = struct.unpack("<I", cip_res[64:68])
            outputstr += "\nAttr 7: Msg Send Counter = " + str(msgsendctr[0])

            msgrecvctr = struct.unpack("<I", cip_res[68:72])
            outputstr += "\nAttr 8: Msg Receive Counter = " + str(msgrecvctr[0])

         #   outputstr += '\n'
         #   t.insert(END, outputstr)

    if option8 == 1:

     #   reqsRan += 1

        outputstr = ""
        outputstr += "\n(8) EIP Explicit Connection List object (0x354)\n"

        service_req = b'\x0e'
        class_req = b'\x54\x03'
        instance_req = b'\x01'
        attribute_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

     #   t.insert(END, outputstr)
     #   bold_response()
     #   outputstr = ''

        if cip_res[42] == 0:
            test8 = 1
            outputstr += "\nTest Passed"
        else:
            test8 = 2
            outputstr += "\nTest Failed"

     #   t.insert(END, outputstr)
     #   color_test(test8)

    if option9 == 1:

        if z == 0 or runAndCompare_var == 1:

          #  reqsRan += 1

            outputstr = ""
            outputstr += "\n(9) RSTP Diagnostic object (0x355)\n"

            service_req = b'\x01'
            class_req = b'\x55\x03'
            instance_req = b'\x01'
            attribute_req = ''

            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    attribute_req)

        #    t.insert(END, outputstr)
        #    bold_response()
        #    outputstr = ''

            if cip_res[42] == 0:
                test9 = 1
                outputstr += "\nTest Passed"
            else:
                test9 = 2
                outputstr += "\nTest Failed"

        #    t.insert(END, outputstr)
        #    color_test(test9)
        #    outputstr = ''

            if test9 == 1:

                protocolspec = struct.unpack("<H", cip_res[44:46])
                outputstr += "\nAttr 1 (Switch Status): Protocol Specification = " + str(protocolspec[0])

                bridgepriority = struct.unpack("<I", cip_res[46:50])
                outputstr += "\nAttr 1: Bridge Priority = " + str(bridgepriority[0])

                timesincetopchange = struct.unpack("<I", cip_res[50:54])
                outputstr += "\nAttr 1: Time Since Topology Change = " + str(timesincetopchange[0])

                topchangecount = struct.unpack("<I", cip_res[54:58])
                outputstr += "\nAttr 1: Topology Change Count = " + str(topchangecount[0])

                desrootsize = struct.unpack("<H", cip_res[58:60])
                desroot = struct.unpack(str(desrootsize[0]) + "B", cip_res[60:60 + desrootsize[0]])
                outputstr += "\nAttr 1: Designated Root = "

                for x in range(0, len(desroot)):
                    outputstr += str(hex(desroot[x])[2:]) + " "

                newstart = 60 + desrootsize[0]
                rootcost = struct.unpack("<I", cip_res[newstart:newstart + 4])
                outputstr += "\nAttr 1: Root Cost = " + str(rootcost[0])

                rootport = struct.unpack("<I", cip_res[newstart + 4:newstart + 8])
                outputstr += "\nAttr 1: Root Port = " + str(rootport[0])

                maxage = struct.unpack("<H", cip_res[newstart + 8:newstart + 10])
                outputstr += "\nAttr 1: Max Age = " + str(maxage[0])

                hellotime = struct.unpack("<H", cip_res[newstart + 10:newstart + 12])
                outputstr += "\nAttr 1: Hello Time = " + str(hellotime[0])

                holdtime = struct.unpack("<I", cip_res[newstart + 12:newstart + 16])
                outputstr += "\nAttr 1: Hold Time = " + str(holdtime[0])

                forwarddelay = struct.unpack("<H", cip_res[newstart + 16:newstart + 18])
                outputstr += "\nAttr 1: Forward Delay = " + str(forwarddelay[0])

                bridgemaxage = struct.unpack("<H", cip_res[newstart + 18:newstart + 20])
                outputstr += "\nAttr 1: Bridge Max Age = " + str(bridgemaxage[0])

                bridgehellotime = struct.unpack("<H", cip_res[newstart + 20:newstart + 22])
                outputstr += "\nAttr 1: Bridge Hello Time = " + str(bridgehellotime[0])

                bridgeforwarddelay = struct.unpack("<H", cip_res[newstart + 22:newstart + 24])
                outputstr += "\nAttr 1: Bridge Forward Delay = " + str(bridgeforwarddelay[0])

                rstpport = struct.unpack("<I", cip_res[newstart + 24:newstart + 28])
                outputstr += "\nAttr 2 (Port Status): Port = " + str(rstpport[0])

                rstppriority = struct.unpack("<I", cip_res[newstart + 28:newstart + 32])
                outputstr += "\nAttr 2: Priority = " + str(rstppriority[0])

                rstpstate = struct.unpack("<H", cip_res[newstart + 32:newstart + 34])
                outputstr += "\nAttr 2: State = " + str(rstpstate[0])

                rstpenable = struct.unpack("<H", cip_res[newstart + 34:newstart + 36])
                outputstr += "\nAttr 2: Enable = " + str(rstpenable[0])

                pathcost = struct.unpack("<I", cip_res[newstart + 36:newstart + 40])
                outputstr += "\nAttr 2: Path Cost = " + str(pathcost[0])

                desrootsize2 = struct.unpack("<H", cip_res[newstart + 40:newstart + 42])
                desroot2 = struct.unpack(str(desrootsize2[0]) + "B",
                                         cip_res[newstart + 42:newstart + 42 + desrootsize2[0]])
                outputstr += "\nAttr 2: Designated Root = "

                for x in range(0, len(desroot2)):
                    outputstr += str(hex(desroot2[x])[2:]) + " "

                newstart = newstart + 42 + desrootsize2[0]

                descost = struct.unpack("<I", cip_res[newstart:newstart + 4])
                outputstr += "\nAttr 2: Designated Cost = " + str(descost[0])

                desbridgesize = struct.unpack("<H", cip_res[newstart + 4:newstart + 6])
                desbridge = struct.unpack(str(desbridgesize[0]) + "B",
                                          cip_res[newstart + 6:newstart + 6 + desbridgesize[0]])
                outputstr += "\nAttr 2: Designated Bridge = "

                for x in range(0, len(desbridge)):
                    outputstr += str(hex(desbridge[x])[2:]) + " "

                newstart = newstart + 6 + desbridgesize[0]

                desportsize = struct.unpack("<H", cip_res[newstart:newstart + 2])
                desport = struct.unpack(str(desportsize[0]) + "B", cip_res[newstart + 2:newstart + 2 + desportsize[0]])
                outputstr += "\nAttr 2: Designated Port = "

                desportstr = ""
                for x in range(0, len(desport)):
                    desportstr += str('{:02x}'.format(desport[x])) + " "
                    outputstr += str('{:02x}'.format(desport[x])) + " "

                newstart = newstart + 2 + desportsize[0]

                forwardtranscount = struct.unpack("<I", cip_res[newstart:newstart + 4])
                outputstr += "\nAttr 2: Forward Transitions Count = " + str(forwardtranscount[0])

                portnum = struct.unpack("<H", cip_res[newstart + 4:newstart + 6])
                outputstr += "\nAttr 3 (Port Mode): Port Number = " + str(portnum[0])

                adminedgeport = struct.unpack("<H", cip_res[newstart + 6:newstart + 8])
                outputstr += "\nAttr 3: Admin Edge Port = " + str(adminedgeport[0])

                operedgeport = struct.unpack("<H", cip_res[newstart + 8:newstart + 10])
                outputstr += "\nAttr 3: Oper Edge Port = " + str(operedgeport[0])

                autoedgeport = struct.unpack("<H", cip_res[newstart + 10:newstart + 12])
                outputstr += "\nAttr 3: Auto Edge Port = " + str(autoedgeport[0])

                outputstr += '\n'
           #     t.insert(END, outputstr)

        insertstr = ''
        found = 0



    if option10 == 1:

     #   reqsRan += 1

        outputstr = ""
        outputstr += "\n(10) Service Port Control object (0x400)\n"

        service_req = b'\x01'
        class_req = b'\x00\x04'
        instance_req = b'\x01'
        attribute_req = ''

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

      #  t.insert(END, outputstr)
      #  bold_response()
      #  outputstr = ''

        if cip_res[42] == 0:
            test10 = 1
            outputstr += "\nTest Passed"
        else:
            test10 = 2
            outputstr += "\nTest Failed"

      #  t.insert(END, outputstr)
      #  color_test(test10)
      #  outputstr = ''



        if test10 == 1:

            portcontrol = struct.unpack("<H", cip_res[44:46])
            outputstr += "\nAttr 1: Port Control = " + str(portcontrol[0])

            mirror = struct.unpack("<H", cip_res[46:48])
            outputstr += "\nAttr 2: Mirror = " + str(mirror[0])

           # outputstr += '\n'
           # t.insert(END, outputstr)

    if option11 == 1:

      #  reqsRan += 1

        outputstr = ""
        outputstr += "\n(11) Router Diagnostic object (0x402)\n"

        service_req = b'\x0e'
        class_req = b'\x02\x04'
        instance_req = b'\x01'
        attribute_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

     #   t.insert(END, outputstr)
      #  bold_response()
      #  outputstr = ''

        if cip_res[42] == 0:
            test11 = 1
            outputstr += "\nTest Passed"
        else:
            test11 = 2
            outputstr += "\nTest Failed"

    #    t.insert(END, outputstr)
     #   color_test(test11)

    if option12 == 1:

     #   reqsRan += 1

        outputstr = ""
        outputstr += "\n(12) Routing Table Diagnostic object (0x403)\n"

        service_req = b'\x0e'
        class_req = b'\x03\x04'
        instance_req = b'\x01'
        attribute_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

     #   t.insert(END, outputstr)
     #   bold_response()
     #   outputstr = ''

        if cip_res[42] == 0:
            test12 = 1
            outputstr += "\nTest Passed"
        else:
            test12 = 2
            outputstr += "\nTest Failed"

      #  t.insert(END, outputstr)
      #  color_test(test12)

    if option13 == 1:

     #   reqsRan += 1

        outputstr = ""
        outputstr += "\n(13) SMTP object (0x404)\n"

        service_req = b'\x01'
        class_req = b'\x04\x04'
        instance_req = b'\x01'
        attribute_req = ''

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

     #   t.insert(END, outputstr)
     #   bold_response()
     #   outputstr = ''

        if cip_res[42] == 0:
            test13 = 1
            outputstr += "\nTest Passed"
        else:
            test13 = 2
            outputstr += "\nTest Failed"

     #   t.insert(END, outputstr)
     #   color_test(test13)

    if option14 == 1:

    #    reqsRan += 1

        outputstr = ""
        outputstr += "\n(14) SNTP object (0x405)\n"

        service_req = b'\x01'
        class_req = b'\x05\x04'
        instance_req = b'\x01'
        attribute_req = ''

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

    #    t.insert(END, outputstr)
    #    bold_response()
     #   outputstr = ''

        if cip_res[42] == 0:
            test14 = 1
            outputstr += "\nTest Passed"
        else:
            test14 = 2
            outputstr += "\nTest Failed"

     #   t.insert(END, outputstr)
    #    color_test(test14)

        # if test14 == 1:
        #     primaryntpserver = struct.unpack("<I", cip_res[44:48])
        #     outputstr += "\nAttr 1 (Network Time Service Configuration): Primary NTP Server IP Address = " + str(
        #         primaryntpserver[0])
        #
        #     secondaryntpserver = struct.unpack("<I", cip_res[48:52])
        #     outputstr += "\nAttr 1: Secondary NTP Server IP Address = " + str(secondaryntpserver[0])
        #
        #     pollingperiod = struct.unpack("B", bytes([cip_res[52]]))
        #     outputstr += "\nAttr 1: Polling Period = " + str(pollingperiod[0])
        #
        #     updatecpumodtime = struct.unpack("B", bytes([cip_res[53]]))
        #     outputstr += "\nAttr 1: Update CPU with Module Time = " + str(updatecpumodtime[0])
        #
        #     timezone = struct.unpack("<I", cip_res[54:58])
        #     outputstr += "\nAttr 1: Time Zone = " + str(timezone[0])
        #
        #     timezoneoffset = struct.unpack("<H", cip_res[58:60])
        #     outputstr += "\nAttr 1: Time Zone Offset = " + str(timezoneoffset[0])
        #
        #     daylightsavingtimebias = struct.unpack("B", bytes([cip_res[60]]))
        #     outputstr += "\nAttr 1: Daylight saving time bias = " + str(daylightsavingtimebias[0])
        #
        #     daylightsavingstartdatemonth = struct.unpack("B", bytes([cip_res[61]]))
        #     outputstr += "\nAttr 1: Daylight Saving Start Date - Month = " + str(daylightsavingstartdatemonth[0])
        #
        #     daylightsavingstartdateweek = struct.unpack("B", bytes([cip_res[62]]))
        #     outputstr += "\nAttr 1: Daylight Saving Start Date - week #, day of week = " + str(
        #         daylightsavingstartdateweek[0])
        #
        #     daylightsavingstarttime = struct.unpack("<I", cip_res[63:67])
        #     outputstr += "\nAttr 1: Daylight Saving Start Time = " + str(daylightsavingstarttime[0])
        #
        #     daylightsavingenddatemonth = struct.unpack("B", bytes([cip_res[67]]))
        #     outputstr += "\nAttr 1: Daylight Saving End Date - Month = " + str(daylightsavingenddatemonth[0])
        #
        #     daylightsavingenddateweek = struct.unpack("B", bytes([cip_res[68]]))
        #     outputstr += "\nAttr 1: Daylight Saving End Date - week #, day of week = " + str(
        #         daylightsavingenddateweek[0])
        #
        #     daylightsavingendtime = struct.unpack("<I", cip_res[69:73])
        #     outputstr += "\nAttr 1: Daylight Saving End Time = " + str(daylightsavingendtime[0])
        #
        #     reserved = struct.unpack("15B", cip_res[73:88])
        #     outputstr += "\nAttr 1: Reserved = " + str(reserved[0])
        #
        #     nettimeservstat = struct.unpack("<I", cip_res[88:92])
        #     outputstr += "\nAttr 2: Network Time Service Status = " + str(nettimeservstat[0])
        #
        #     linktontpservstat = struct.unpack("<I", cip_res[92:96])
        #     outputstr += "\nAttr 3: Link to NTP Server Status = " + str(linktontpservstat[0])
        #
        #     currentntpserveripaddress = struct.unpack("<I", cip_res[96:100])
        #     outputstr += "\nAttr 4: Current NTP Server IP Address = " + str(currentntpserveripaddress[0])
        #
        #     ntpservertype = struct.unpack("<I", cip_res[100:104])
        #     outputstr += "\nAttr 5: NTP Server Type = " + str(ntpservertype[0])
        #
        #     ntpservertimequality = struct.unpack("<I", cip_res[104:108])
        #     outputstr += "\nAttr 6: NTP Server Time Quality = " + str(ntpservertimequality[0])
        #
        #     numofntpreqsent = struct.unpack("<I", cip_res[108:112])
        #     outputstr += "\nAttr 7: Number of NTP Requests Sent = " + str(numofntpreqsent[0])
        #
        #     numofcommerrors = struct.unpack("<I", cip_res[112:116])
        #     outputstr += "\nAttr 8: Number of Communication Errors = " + str(numofcommerrors[0])
        #
        #     numofntpresprecv = struct.unpack("<I", cip_res[116:120])
        #     outputstr += "\nAttr 9: Number of NTP Responses Received = " + str(numofntpresprecv[0])
        #
        #     lasterror = struct.unpack("<H", cip_res[120:122])
        #     outputstr += "\nAttr 10: Last Error = " + str(lasterror[0])
        #
        #     currentdateandtime = struct.unpack("<IH", cip_res[122:128])
        #     outputstr += "\nAttr 11: Current Date and Time = " + str(currentdateandtime[0])
        #
        #     daylightsavingsstatus = struct.unpack("<I", cip_res[128:132])
        #     outputstr += "\nAttr 12: Daylight Savings Status = " + str(daylightsavingsstatus[0])
        #
        #     timesincelastupdate = struct.unpack("<I", cip_res[132:136])
        #     outputstr += "\nAttr 13: Time Since Last Update = " + str(timesincelastupdate[0])
        #
        #     outputstr += '\n'

     #       t.insert(END, outputstr)

    if option15 == 1:

        if z == 0 or runAndCompare_var == 1:

       #     reqsRan += 1

            outputstr = ""
            outputstr += "\n(15) Identity object (0x01)\n"

            service_req = b'\x01'
            class_req = b'\x01'
            instance_req = b'\x01'

            # example_cip_object = CipObject(Service.get_attributes_all, class_=0x01)


            # scanner.send_unconnected(dest_addr=TCP_IP.get(), cip_object=example_cip_object)


            # example_handler.example_response_event.wait()


            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    b'\x00')

       #     t.insert(END, outputstr)
        #    bold_response()
       #     outputstr = ''

            if cip_res[42] == 0:
                test15 = 1
                outputstr += "\nTest Passed"
            else:
                test15 = 2
                outputstr += "\nTest Failed"

       #     t.insert(END, outputstr)
       #     color_test(test15)
       #     outputstr = ""




            if test15 == 1:

                global vendorid
                vendorid = struct.unpack('<H', cip_res[44:46])
                outputstr += '\nAttr 1: Vendor ID = ' + str(vendorid[0])

                global devicetype
                devicetype = struct.unpack('<H', cip_res[46:48])
                outputstr += '\nAttr 2: Device Type = ' + str(devicetype[0])

                global productcode
                productcode = struct.unpack('<H', cip_res[48:50])
                outputstr += '\nAttr 3: Product Code = ' + str(productcode[0])

                global revision
                revision = struct.unpack('2B', cip_res[50:52])
                outputstr += '\nAttr 4: Major Revision = ' + str(revision[0])
                outputstr += '\nAttr 4: Minor Revision = ' + str(revision[1])

                global status2
                status2 = struct.unpack('<H', cip_res[52:54])
                outputstr += '\nAttr 5: Status = ' + str(hex(status2[0]))

                global serialnum
                serialnum = struct.unpack("<I", cip_res[54:58])
                outputstr += '\nAttr 6: Serial Number = ' + str(hex(serialnum[0]))

                global productname
                productname = struct.unpack("B", bytes([cip_res[58]]))
                if productname[0] == 0:
                    outputstr += '\nAttr 7: Product Name = NULL'
                else:
                    outputstr += '\nAttr 7: Product Name = ' + str(chr(productname[0]))

                global state
                state = struct.unpack("B", bytes([cip_res[59]]))
                outputstr += '\nAttr 8: State = ' + str(hex(state[0]))

                global configconsistency
                configconsistency = struct.unpack("<H", cip_res[60:62])
                outputstr += '\nAttr 9: Configuration Consistency Value = ' + str(configconsistency[0])

                global heartbeatint
                heartbeatint = struct.unpack("B", bytes([cip_res[62]]))
                outputstr += '\nAttr 10: Heartbeat Interval = ' + str(heartbeatint[0])

             #   outputstr += '\n'
              #  t.insert(END, outputstr)


    if option16 == 1:

      #  reqsRan += 1

        outputstr = ""
        outputstr += "\n(16) Message Router object (0x02)\n"

        service_req = b'\x01'
        class_req = b'\x02'
        instance_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                b'\x00')

     #   t.insert(END, outputstr)
     #   bold_response()
     #   outputstr = ''

        if cip_res[42:44] == b'\x00\x00':
            test16 = 1
            outputstr += "\nTest Passed"
        else:
            test16 = 2
            outputstr += "\nTest Failed"

     #   t.insert(END, outputstr)
     #   color_test(test16)

    if option17 == 1:

     #   reqsRan += 1

        outputstr = ""
        outputstr += "\n(17) Connection Manager object (0x06)\n"

        service_req = b'\x01'
        class_req = b'\x06'
        instance_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                b'\x00')

      #  t.insert(END, outputstr)
      #  bold_response()
      #  outputstr = ''

        if cip_res[42:44] == b'\x00\x00':
            test17 = 1
            outputstr += "\nTest Passed"
        else:
            test17 = 2
            outputstr += "\nTest Failed"

      #  t.insert(END, outputstr)
      #  color_test(test17)
      #  outputstr = ''


        if test17 == 1:

            openreqs = struct.unpack("<H", cip_res[44:46])
            outputstr += "\nAttr 1: Open Requests = " + str(openreqs[0])

            openformatrejects = struct.unpack("<H", cip_res[46:48])
            outputstr += "\nAttr 2: Open Format Rejects = " + str(openformatrejects[0])

            openresourcerejects = struct.unpack("<H", cip_res[48:50])
            outputstr += "\nAttr 3: Open Resource Rejects = " + str(openresourcerejects[0])

            otheropenrejects = struct.unpack("<H", cip_res[50:52])
            outputstr += "\nAttr 4: Other Open Rejects = " + str(otheropenrejects[0])

            closerejects = struct.unpack("<H", cip_res[52:54])
            outputstr += "\nAttr 5: Close Requests = " + str(closerejects[0])

            closeformatreqs = struct.unpack("<H", cip_res[54:56])
            outputstr += "\nAttr 6: Close Format Requests = " + str(closeformatreqs[0])

            closeotherreqs = struct.unpack("<H", cip_res[56:58])
            outputstr += "\nAttr 7: Close Other Requests = " + str(closeotherreqs[0])

            conntimeouts = struct.unpack("<H", cip_res[58:60])
            outputstr += "\nAttr 8: Connection Timeouts = " + str(conntimeouts[0])

            outputstr += '\n'
        #    t.insert(END, outputstr)

        insertstr = ''
        found = 0


    if option18 == 1:

      ##  reqsRan += 1

        outputstr = ""
        outputstr += "\n(18) QoS (Quality of Service) object (0x48)\n"

        service_req = b'\x0e'
        class_req = b'\x48'
        instance_req = b'\x01'
        attribute_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                attribute_req)

    #    t.insert(END, outputstr)
     #   bold_response()
     #   outputstr = ''

        if cip_res[42] == 0:
            test18 = 1
            outputstr += "\nTest Passed"
        else:
            test18 = 2
            outputstr += "\nTest Failed"

      #  t.insert(END, outputstr)
    #    color_test(test18)
     #   outputstr = ''
        outputstr2 = ''

        if test18 == 1:
            tagenable = struct.unpack('B', bytes([cip_res[44]]))
            outputstr += "\nAttr 1: 802.1Q Tag Enable = " + str(tagenable[0])

            outputstr2, cip_res = requestsendreceive(outputstr2, sock, reg_sess, service_req, class_req, instance_req,
                                                     b'\x02')
            dscpptpevent = struct.unpack('B', bytes([cip_res[44]]))
            outputstr += "\nAttr 2: DSCP PTP Event = " + str(dscpptpevent[0])

            outputstr2, cip_res = requestsendreceive(outputstr2, sock, reg_sess, service_req, class_req, instance_req,
                                                     b'\x03')
            dscpptpgeneral = struct.unpack('B', bytes([cip_res[44]]))
            outputstr += "\nAttr 3: DSCP PTP General = " + str(dscpptpgeneral[0])

            outputstr2, cip_res = requestsendreceive(outputstr2, sock, reg_sess, service_req, class_req, instance_req,
                                                     b'\x04')
            dscpurgent = struct.unpack('B', bytes([cip_res[44]]))
            outputstr += "\nAttr 4: DSC Urgent = " + str(dscpurgent[0])

            outputstr2, cip_res = requestsendreceive(outputstr2, sock, reg_sess, service_req, class_req, instance_req,
                                                     b'\x05')
            dscpscheduled = struct.unpack('B', bytes([cip_res[44]]))
            outputstr += "\nAttr 5: DSCP Scheduled = " + str(dscpscheduled[0])

            outputstr2, cip_res = requestsendreceive(outputstr2, sock, reg_sess, service_req, class_req, instance_req,
                                                     b'\x06')
            dscphigh = struct.unpack('B', bytes([cip_res[44]]))
            outputstr += "\nAttr 6: DSCP High = " + str(dscphigh[0])

            outputstr2, cip_res = requestsendreceive(outputstr2, sock, reg_sess, service_req, class_req, instance_req,
                                                     b'\x07')
            dscplow = struct.unpack('B', bytes([cip_res[44]]))
            outputstr += "\nAttr 7: DSCP Low = " + str(dscplow[0])

            outputstr2, cip_res = requestsendreceive(outputstr2, sock, reg_sess, service_req, class_req, instance_req,
                                                     b'\x08')
            dscpexplicit = struct.unpack('B', bytes([cip_res[44]]))
            outputstr += "\nAttr 8: DSCP Explicit = " + str(dscpexplicit[0])

            outputstr += '\n'
          #  t.insert(END, outputstr)

        insertstr = ''
        found = 0

    if option19 == 1:

     #   reqsRan += 1

        outputstr = ""
        outputstr += "\n(19) Port object (0xF4)\n"

        service_req = b'\x01'
        class_req = b'\xf4'
        instance_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                b'\x00')

      #  t.insert(END, outputstr)
       # bold_response()
        outputstr = ''

        if cip_res[42:44] == b'\x00\x00':
            test19 = 1
            outputstr += "\nTest Passed"
        else:
            test19 = 2
            outputstr += "\nTest Failed"

      #  t.insert(END, outputstr)
       # color_test(test19)
        outputstr = ''


        if test19 == 1:

            porttype = struct.unpack("<H", cip_res[44:46])
        #     outputstr += "\nAttr 1: Port Type = " + str(porttype[0])
        #
        #     portnumber = struct.unpack("<H", cip_res[46:48])
        #     outputstr += "\nAttr 2: Port Number = " + str(portnumber[0])
        #
        #     pathlength = struct.unpack("<H", cip_res[48:50])
        #     outputstr += "\nAttr 3 (Link Object): Path Length (words) = " + str(pathlength[0])
        #
        #     pathclass = struct.unpack("B", bytes([cip_res[51]]))
        #     outputstr += "\nAttr 3: Class = " + str(pathclass[0])
        #
        #     pathinstance = struct.unpack("B", bytes([cip_res[53]]))
        #     outputstr += "\nAttr 3: Instance = " + str(pathinstance[0])
        #
        #     portname = struct.unpack("<10s", cip_res[54:64])
        #     outputstr += "\nAttr 4: Port Name = " + str(portname[0:10])
        #
        #     port = struct.unpack("B", bytes([cip_res[65]]))
        #     outputstr += "\nAttr 7: Port = " + str(port[0])
        #
        #     address = struct.unpack("B", bytes([cip_res[66]]))
        #     outputstr += "\nAttr 7: Node Address = " + str(address[0])
        #
        #     outputstr += '\n'
          #  t.insert(END, outputstr)

        insertstr = ''
        found = 0

    if option20 == 1:

        if z == 0 or runAndCompare_var == 1:

        #    reqsRan += 1

            outputstr = ""
            outputstr += "\n(20) TCP/IP object (0xF5)\n"

            service_req = b'\x01'
            class_req = b'\xf5'
            instance_req = b'\x01'

            outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                    b'\x00')

          #  t.insert(END, outputstr)
       #     bold_response()
            outputstr = ''

            if cip_res[42:44] == b'\x00\x00':
                test20 = 1
                outputstr += "\nTest Passed"
            else:
                test20 = 2
                outputstr += "\nTest Failed"

          #  t.insert(END, outputstr)
         #   color_test(test20)
            outputstr = ""



            if test20 == 1:

                global status3
                status3 = struct.unpack("<I", cip_res[44:48])
                outputstr += "\nAttr 1: Status = " + str(status3[0])

                configcapability = struct.unpack("<I", cip_res[48:52])
                outputstr += "\nAttr 2: Configuration Capability = " + str(hex(configcapability[0]))

                configcontrol = struct.unpack("<I", cip_res[52:56])
                outputstr += "\nAttr 3: Configuration Control = " + str(configcontrol[0])

                physlink = struct.unpack("<H", cip_res[56:58])
                outputstr += "\nAttr 4: Physical Link = " + str(physlink[0])

                ipaddr = struct.unpack("<BBBB", cip_res[58:62])
                outputstr += "\nAttr 5: IP Address = " + str(ipaddr[3]) + '.' + str(ipaddr[2]) + '.' + str(
                    ipaddr[1]) + '.' + str(ipaddr[0])

                subnetmask = struct.unpack("<BBBB", cip_res[62:66])
                outputstr += "\nAttr 5: Subnet mask = " + str(subnetmask[3]) + '.' + str(subnetmask[2]) + '.' + str(
                    subnetmask[1]) + '.' + str(subnetmask[0])

                gateway = struct.unpack("<BBBB", cip_res[66:70])
                outputstr += "\nAttr 5: Gateway = " + str(gateway[3]) + '.' + str(gateway[2]) + '.' + str(
                    gateway[1]) + '.' + str(gateway[0])

                nameserver = struct.unpack("<BBBB", cip_res[70:74])
                outputstr += "\nAttr 5: Name Server = " + str(nameserver[3]) + '.' + str(nameserver[2]) + '.' + str(
                    nameserver[1]) + '.' + str(nameserver[0])

                nameserver2 = struct.unpack("<BBBB", cip_res[74:78])
                outputstr += "\nAttr 5: Name Server2 = " + str(nameserver2[3]) + '.' + str(nameserver2[2]) + '.' + str(
                    nameserver2[1]) + '.' + str(nameserver2[0])

                domain = struct.unpack("<H", cip_res[78:80])
                outputstr += "\nAttr 5: Domain Name = " + str(domain[0])

                hostname = struct.unpack("<H", cip_res[80:82])
                outputstr += "\nAttr 6: Host Name = " + str(hostname[0])

                safetynetnumdate = struct.unpack("<H", cip_res[82:84])
                outputstr += "\nAttr 7: Safety Network Number (Manual) Date = " + str(hex(safetynetnumdate[0]))

                safetynetnumtime = struct.unpack("<I", cip_res[84:88])
                outputstr += "\nAttr 7: Safety Network Number (Manual) Time = " + str(hex(safetynetnumtime[0]))

                ttlvalue = struct.unpack("B", bytes([cip_res[88]]))
                outputstr += "\nAttr 8: TTL Value = " + str(ttlvalue[0])

                alloccontrol = struct.unpack("B", bytes([cip_res[89]]))
                outputstr += "\nAttr 9: Alloc Control = " + str(alloccontrol[0])

                reserved = struct.unpack("B", bytes([cip_res[90]]))
                outputstr += "\nAttr 9: Reserved = " + str(reserved[0])

                nummcast = struct.unpack("<H", cip_res[91:93])
                outputstr += "\nAttr 9: Num MCast = " + str(nummcast[0])

                mcaststartaddr = struct.unpack("<BBBB", cip_res[93:97])
                outputstr += "\nAttr 9: MCast Start Addr = " + str(mcaststartaddr[3]) + '.' + str(
                    mcaststartaddr[2]) + '.' + str(mcaststartaddr[1]) + '.' + str(mcaststartaddr[0])

                selectacd = struct.unpack("B", bytes([cip_res[97]]))
                outputstr += "\nAttr 10: Select ACD = " + str(selectacd[0])

                acdactivity = struct.unpack("B", bytes([cip_res[98]]))
                outputstr += "\nAttr 11: ACD Activity = " + str(acdactivity[0])
                # 
                # remotemac = struct.unpack("6B", cip_res[99:105])
                # remotemacstr = str(remotemac[0]) + ':' + str(remotemac[1]) + ':' + str(remotemac[2]) + ':' + str(
                #     remotemac[3]) + ':' + str(remotemac[4]) + ':' + str(remotemac[5])
                # outputstr += "\nAttr 11: RemoteMAC = " + remotemacstr
                #
                # arppdu = struct.unpack("28B", cip_res[105:133])
                # outputstr += "\nAttr 11: Arp PDU = " + str(arppdu[:])
                #
                # eipquickconn = struct.unpack("B", bytes([cip_res[133]]))
                # outputstr += "\nAttr 12: EtherNet/IP Quick Connection = " + str(eipquickconn[0])
                #
                # encapinacttimeout = struct.unpack("<H", cip_res[134:136])
                # outputstr += "\nAttr 13: Encapsulation Inactivity Timeout = " + str(encapinacttimeout[0])
                #
                # outputstr += '\n'
             #   t.insert(END, outputstr)

        found = 0
        insertstr = ''

    if option21 == 1:

   #     reqsRan += 1

        outputstr = ""
        outputstr += "\n(21) Ethernet Link object (0xF6)\n"

        service_req = b'\x01'
        class_req = b'\xf6'
        instance_req = b'\x01'

        outputstr, cip_res = requestsendreceive(outputstr, sock, reg_sess, service_req, class_req, instance_req,
                                                b'\x00')

      #  t.insert(END, outputstr)
      #  bold_response()
        outputstr = ''

        if cip_res[42:44] == b'\x00\x00':
            test21 = 1
            outputstr += "\nTest Passed"
        else:
            test21 = 2
            outputstr += "\nTest Failed"

       # t.insert(END, outputstr)
       # color_test(test21)
        outputstr = ''



        #
        # if test21 == 1:
        #
        #     interfacespeed = struct.unpack("<I", cip_res[44:48])
        #     outputstr += "\nAttr 1: Interface Speed = " + str(interfacespeed[0])
        #
        #     interfaceflags = struct.unpack("<I", cip_res[48:52])
        #     outputstr += "\nAttr 2: Interface Flags = " + str(hex(interfaceflags[0]))
        #
        #     physaddr = struct.unpack("6B", cip_res[52:58])
        #     outputstr += "\nAttr 3: Physical Address = " + str(physaddr[0]) + ':' + str(physaddr[1]) + ':' + str(
        #         physaddr[2]) + ':' + str(physaddr[3]) + ':' + str(physaddr[4]) + ':' + str(physaddr[5])
        #
        #     inoctets = struct.unpack("<I", cip_res[58:62])
        #     outputstr += "\nAttr 4 Interface Counters: In Octets = " + str(inoctets[0])
        #
        #     inucastpackets = struct.unpack("<I", cip_res[62:66])
        #     outputstr += "\nAttr 4: In Ucast Packets = " + str(inucastpackets[0])
        #
        #     innucastpackets = struct.unpack("<I", cip_res[66:70])
        #     outputstr += "\nAttr 4: In NUcast Packets = " + str(innucastpackets[0])
        #
        #     indiscards = struct.unpack("<I", cip_res[70:74])
        #     outputstr += "\nAttr 4: In Discards = " + str(indiscards[0])
        #
        #     inerrors = struct.unpack("<I", cip_res[74:78])
        #     outputstr += "\nAttr 4: In Errors = " + str(inerrors[0])
        #
        #     inunknownprotos = struct.unpack("<I", cip_res[78:82])
        #     outputstr += "\nAttr 4: In Unknown Protos = " + str(inunknownprotos[0])
        #
        #     outoctets = struct.unpack("<I", cip_res[82:86])
        #     outputstr += "\nAttr 4: Out Octets = " + str(outoctets[0])
        #
        #     outucastpackets = struct.unpack("<I", cip_res[86:90])
        #     outputstr += "\nAttr 4: Out Ucast Packets = " + str(outucastpackets[0])
        #
        #     outnucastpackets = struct.unpack("<I", cip_res[90:94])
        #     outputstr += "\nAttr 4: Out NUcast Packets = " + str(outnucastpackets[0])
        #
        #     outdiscards = struct.unpack("<I", cip_res[94:98])
        #     outputstr += "\nAttr 4: Out Discards = " + str(outdiscards[0])
        #
        #     outerrors = struct.unpack("<I", cip_res[98:102])
        #     outputstr += "\nAttr 4: Out Errors = " + str(outerrors[0])
        #
        #     alignmenterrors = struct.unpack("<I", cip_res[102:106])
        #     outputstr += "\nAttr 5 (Media Counters): Alignment Errors = " + str(alignmenterrors[0])
        #
        #     fcserrors = struct.unpack("<I", cip_res[106:110])
        #     outputstr += "\nAttr 5: FCS Errors = " + str(fcserrors[0])
        #
        #     singlecollisions = struct.unpack("<I", cip_res[110:114])
        #     outputstr += "\nAttr 5: Single Collisions = " + str(singlecollisions[0])
        #
        #     multiplecollisions = struct.unpack("<I", cip_res[114:118])
        #     outputstr += "\nAttr 5: Multiple Collisions = " + str(multiplecollisions[0])
        #
        #     sqetesterrors = struct.unpack("<I", cip_res[118:122])
        #     outputstr += "\nAttr 5: SQE Test Errors = " + str(sqetesterrors[0])
        #
        #     deferredtransmission = struct.unpack("<I", cip_res[122:126])
        #     outputstr += "\nAttr 5: Deferred Transmission = " + str(deferredtransmission[0])
        #
        #     latecollisions = struct.unpack("<I", cip_res[126:130])
        #     outputstr += "\nAttr 5: Late Collisions = " + str(latecollisions[0])
        #
        #     excessivecollisions = struct.unpack("<I", cip_res[130:134])
        #     outputstr += "\nAttr 5: Excessive Collisions = " + str(excessivecollisions[0])
        #
        #     mactransmiterrors = struct.unpack("<I", cip_res[134:138])
        #     outputstr += "\nAttr 5: MAC Transmit Errors = " + str(mactransmiterrors[0])
        #
        #     carriersenseerrors = struct.unpack("<I", cip_res[138:142])
        #     outputstr += "\nAttr 5: Carrier Sense Errors = " + str(carriersenseerrors[0])
        #
        #     frametoolong = struct.unpack("<I", cip_res[142:146])
        #     outputstr += "\nAttr 5: Frame Too Long = " + str(frametoolong[0])
        #
        #     macreceiveerrors = struct.unpack("<I", cip_res[146:150])
        #     outputstr += "\nAttr 5: MAC Receive Errors = " + str(macreceiveerrors[0])
        #
        #     controlbits = struct.unpack("<H", cip_res[150:152])
        #     outputstr += "\nAttr 6 (Interface Control): Control Bits = " + str(hex(controlbits[0]))
        #
        #     forcedinterfacespeed = struct.unpack("<H", cip_res[152:154])
        #     outputstr += "\nAttr 6: Forced Interface Speed = " + str(forcedinterfacespeed[0])
        #
        #     interfacetype = struct.unpack("B", bytes([cip_res[154]]))
        #     outputstr += "\nAttr 7: Interface Type = " + str(interfacetype[0])
        #
        #     interfacestate = struct.unpack("B", bytes([cip_res[155]]))
        #     outputstr += "\nAttr 8: Interface State = " + str(interfacestate[0])
        #
        #     adminstate = struct.unpack("B", bytes([cip_res[156]]))
        #     outputstr += "\nAttr 9: Admin State = " + str(adminstate[0])
        #
        #     interfacelabel = struct.unpack("5B", cip_res[157:162])
        #     outputstr += "\nAttr 10: Interface Label = " + str(interfacelabel[:])
        #
        #     data = struct.unpack("5B", cip_res[162:167])
        #     outputstr += "\nAttr 10: Data = " + str(data[:])
        #
        #     outputstr += '\n'
            #t.insert(END, outputstr)

    # Print the appropriate test results
    #t.insert(END, "\n")
    if option1 == 1:

        if test1 == 1:
            print("Test 1 Passed: Module Diagnostic object (0x300)")
            file.write("Test 1 Passed: Module Diagnostic object (0x300)\n")
            #color_test2(1)
        elif test1 == 2:
            print("Test 1 Failed: Module Diagnostic object (0x300)")
            file.write("Test 1 Failed: Module Diagnostic object (0x300)\n")
            #color_test2(2)
        elif test1 == 0:
            print("Test 1 didn't run: Module Diagnostic object (0x300)\n")
            file.write("Test 1 didn't run: Module Diagnostic object (0x300)\n")
    if option2 == 1:
        if test2 == 1:
            print("Test 2 Passed: Scanner Diagnostic object (0x301)")
            file.write("Test 2 Passed: Scanner Diagnostic object (0x301)\n")
            #color_test2(1)
        elif test2 == 2:
            print("Test 2 Failed: Scanner Diagnostic object (0x301)")
            file.write("Test 2 Failed: Scanner Diagnostic object (0x301)\n")
            #color_test2(2)
        elif test2 == 0:
            print("Test 2 didn't run: Scanner Diagnostic object (0x301)\n")
            file.write("Test 2 didn't run: Scanner Diagnostic object (0x301)\n")
    if option3 == 1:
        if test3 == 1:
            print("Test 3 Passed: Adapter Diagnostic object (0x302)")
            file.write("Test 3 Passed: Adapter Diagnostic object (0x302)\n")
            #color_test2(1)
        elif test3 == 2:
            print("Test 3 Failed: Adapter Diagnostic object (0x302)")
            file.write("Test 3 Failed: Adapter Diagnostic object (0x302)\n")
            #color_test2(2)
        elif test3 == 0:
            print("Test 3 didn't run: Adapter Diagnostic object (0x302)\n")
            file.write("Test 3 didn't run: Adapter Diagnostic object (0x302)\n")
    if option4 == 1:
        if test4 == 1:
            print("Test 4 Passed: Ethernet Interface Diagnostic object (0x350)")
            file.write("Test 4 Passed: Ethernet Interface Diagnostic object (0x350)\n")
            #color_test2(1)
        elif test4 == 2:
            print("Test 4 Failed: Ethernet Interface Diagnostic object (0x350)")
            file.write("Test 4 Failed: Ethernet Interface Diagnostic object (0x350)\n")
            #color_test2(2)
        elif test4 == 0:
            print("Test 4 didn't run: Ethernet Interface Diagnostic object (0x350)\n")
            file.write("Test 4 didn't run: Ethernet Interface Diagnostic object (0x350)\n")
    if option5 == 1:
        if test5 == 1:
            print("Test 5 Passed: IOScanner Diagnostic object (0x351)")
            file.write("Test 5 Passed: IOScanner Diagnostic object (0x351)\n")
            #color_test2(1)
        elif test5 == 2:
            print("Test 5 Failed: IOScanner Diagnostic object (0x351)")
            file.write("Test 5 Failed: IOScanner Diagnostic object (0x351)\n")
            #color_test2(2)
        elif test5 == 0:
            print("Test 5 didn't run: IOScanner Diagnostic object (0x351)\n")
            file.write("Test 5 didn't run: IOScanner Diagnostic object (0x351)\n")
    if option6 == 1:
        if test6 == 1:
            print("Test 6 Passed: EIP I/O Connection Diagnostic object (0x352)")
            file.write("Test 6 Passed: EIP I/O Connection Diagnostic object (0x352)\n")
            #color_test2(1)
        elif test6 == 2:
            print("Test 6 Failed: EIP I/O Connection Diagnostic object (0x352)")
            file.write("Test 6 Failed: EIP I/O Connection Diagnostic object (0x352)\n")
            #color_test2(2)
        elif test6 == 0:
            print("Test 6 didn't run: EIP I/O Connection Diagnostic object (0x352)\n")
            file.write("Test 6 didn't run: EIP I/O Connection Diagnostic object (0x352)\n")
    if option7 == 1:
        if test7 == 1:
            print("Test 7 Passed: EIP Explicit Connection Diagnostic object (0x353)")
            file.write("Test 7 Passed: EIP Explicit Connection Diagnostic object (0x353)\n")
            #color_test2(1)
        elif test7 == 2:
            print("Test 7 Failed: EIP Explicit Connection Diagnostic object (0x353)")
            file.write("Test 7 Failed: EIP Explicit Connection Diagnostic object (0x353)\n")
            #color_test2(2)
        elif test7 == 0:
            print("Test 7 didn't run: EIP Explicit Connection Diagnostic object (0x353)\n")
            file.write("Test 7 didn't run: EIP Explicit Connection Diagnostic object (0x353)\n")
    if option8 == 1:
        if test8 == 1:
            print("Test 8 Passed: EIP Explicit Connection List object (0x354)")
            file.write("Test 8 Passed: EIP Explicit Connection List object (0x354)\n")
            #color_test2(1)
        elif test8 == 2:
            print("Test 8 Failed: EIP Explicit Connection List object (0x354)")
            file.write("Test 8 Failed: EIP Explicit Connection List object (0x354)\n")
            #color_test2(2)
        elif test8 == 0:
            print("Test 8 didn't run: EIP Explicit Connection List object (0x354)\n")
            file.write("Test 8 didn't run: EIP Explicit Connection List object (0x354)\n")
    if option9 == 1:
        if test9 == 1:
            print("Test 9 Passed: RSTP Diagnostic object (0x355)")
            file.write("Test 9 Passed: RSTP Diagnostic object (0x355)\n")
            #color_test2(1)
        elif test9 == 2:
            print("Test 9 Failed: RSTP Diagnostic object (0x355)")
            file.write("Test 9 Failed: RSTP Diagnostic object (0x355)\n")
            #color_test2(2)
        elif test9 == 0:
            print("Test 9 didn't run: RSTP Diagnostic object (0x355)\n")
            file.write("Test 9 didn't run: RSTP Diagnostic object (0x355)\n")
    if option10 == 1:
        if test10 == 1:
            print("Test 10 Passed: Service Port Control object (0x400)")
            file.write("Test 10 Passed: Service Port Control object (0x400)\n")
            #color_test2(1)
        elif test10 == 2:
            print("Test 10 Failed: Service Port Control object (0x400)")
            file.write("Test 10 Failed: Service Port Control object (0x400)\n")
            #color_test2(2)
        elif test10 == 0:
            print("Test 10 didn't run: Service Port Control object (0x400)\n")
            file.write("Test 10 didn't run: Service Port Control object (0x400)\n")
    if option11 == 1:
        if test11 == 1:
            print("Test 11 Passed: Router Diagnostic object (0x402)")
            file.write("Test 11 Passed: Router Diagnostic object (0x402)\n")
            #color_test2(1)
        elif test11 == 2:
            print("Test 11 Failed: Router Diagnostic object (0x402)")
            file.write("Test 11 Failed: Router Diagnostic object (0x402)\n")
            #color_test2(2)
        elif test11 == 0:
            print("Test 11 didn't run: Router Diagnostic object (0x402)\n")
            file.write("Test 11 didn't run: Router Diagnostic object (0x402)\n")
    if option12 == 1:
        if test12 == 1:
            print("Test 12 Passed: Routing Table Diagnostic object (0x403)")
            file.write("Test 12 Passed: Routing Table Diagnostic object (0x403)\n")
            #color_test2(1)
        elif test12 == 2:
            print("Test 12 Failed: Routing Table Diagnostic object (0x403)")
            file.write("Test 12 Failed: Routing Table Diagnostic object (0x403)\n")
            #color_test2(2)
        elif test12 == 0:
            print("Test 12 didn't run: Routing Table Diagnostic object (0x403)\n")
            file.write("Test 12 didn't run: Routing Table Diagnostic object (0x403)\n")
    if option13 == 1:
        if test13 == 1:
            print("Test 13 Passed: SMTP object (0x404)")
            file.write("Test 13 Passed: SMTP object (0x404)\n")
            #color_test2(1)
        elif test13 == 2:
            print("Test 13 Failed: SMTP object (0x404)")
            file.write("Test 13 Failed: SMTP object (0x404)\n")
            #color_test2(2)
        elif test13 == 0:
            print("Test 13 didn't run: SMTP object (0x404)\n")
            file.write("Test 13 didn't run: SMTP object (0x404)\n")
    if option14 == 1:
        if test14 == 1:
            print("Test 14 Passed: SNTP object (0x405)")
            file.write("Test 14 Passed: SNTP object (0x405)\n")
            #color_test2(1)
        elif test14 == 2:
            print("Test 14 Failed: SNTP object (0x405)")
            file.write("Test 14 Failed: SNTP object (0x405)\n")
            #color_test2(2)
        elif test14 == 0:
            print("Test 14 didn't run: SNTP object (0x405)\n")
            file.write("Test 14 didn't run: SNTP object (0x405)\n")
    if option15 == 1:
        if test15 == 1:
            print("Test 15 Passed: Identity object (0x01)")
            file.write("Test 15 Passed: Identity object (0x01)\n")
            #color_test2(1)
        elif test15 == 2:
            print("Test 15 Failed: Identity object (0x01)")
            file.write("Test 15 Failed: Identity object (0x01)\n")
            #color_test2(2)
        elif test15 == 0:
            print("Test 15 didn't run: Identity object (0x01)\n")
            file.write("Test 15 didn't run: Identity object (0x01)\n")
    if option16 == 1:
        if test16 == 1:
            print("Test 16 Passed: Message Router object (0x02)")
            file.write("Test 16 Passed: Message Router object (0x02)\n")
            #color_test2(1)
        elif test16 == 2:
            print("Test 16 Failed: Message Router object (0x02)")
            file.write("Test 16 Failed: Message Router object (0x02)\n")
            #color_test2(2)
        elif test16 == 0:
            print("Test 16 didn't run: Message Router object (0x02)\n")
            file.write("Test 16 didn't run: Message Router object (0x02)\n")
    if option17 == 1:
        if test17 == 1:
            print("Test 17 Passed: Connection Manager object (0x06)")
            file.write("Test 17 Passed: Connection Manager object (0x06)\n")
            #color_test2(1)
        elif test17 == 2:
            print("Test 17 Failed: Connection Manager object (0x06)")
            file.write("Test 17 Failed: Connection Manager object (0x06)\n")
            #color_test2(2)
        elif test17 == 0:
            print("Test 17 didn't run: Connection Manager object (0x06)\n")
            file.write("Test 17 didn't run: Connection Manager object (0x06)\n")
    if option18 == 1:
        if test18 == 1:
            print("Test 18 Passed: QoS object (0x48)")
            file.write("Test 18 Passed: QoS object (0x48)\n")
            #color_test2(1)
        elif test18 == 2:
            print("Test 18 Failed: QoS object (0x48)")
            file.write("Test 18 Failed: QoS object (0x48)\n")
            #color_test2(2)
        elif test18 == 0:
            print("Test 18 didn't run: QoS object (0x48)\n")
            file.write("Test 18 didn't run: QoS object (0x48)\n")
    if option19 == 1:
        if test19 == 1:
            print("Test 19 Passed: Port object (0xF4)")
            file.write("Test 19 Passed: Port object (0xF4)\n")
            #color_test2(1)
        elif test19 == 2:
            print("Test 19 Failed: Port object (0xF4)")
            file.write("Test 19 Failed: Port object (0xF4)\n")
            #color_test2(2)
        elif test19 == 0:
            print("Test 19 didn't run: Port object (0xF4)\n")
            file.write("Test 19 didn't run: Port object (0xF4)\n")
    if option20 == 1:
        if test20 == 1:
            print("Test 20 Passed: TCP/IP object (0xF5)")
            file.write("Test 20 Passed: TCP/IP object (0xF5)\n")
            #color_test2(1)
        elif test20 == 2:
            print("Test 20 Failed: TCP/IP object (0xF5)")
            file.write("Test 20 Failed: TCP/IP object (0xF5)\n")
            #color_test2(2)
        elif test20 == 0:
            print("Test 20 didn't run: TCP/IP object (0xF5)\n")
            file.write("Test 20 didn't run: TCP/IP object (0xF5)\n")
    if option21 == 1:
        if test21 == 1:
            print("Test 21 Passed: Ethernet Link object (0xF6)")
            file.write("Test 21 Passed: Ethernet Link object (0xF6)\n")
            #color_test2(1)
        elif test21 == 2:
            print("Test 21 Failed: Ethernet Link object (0xF6)")
            file.write("Test 21 Failed: Ethernet Link object (0xF6)\n")
            #color_test2(2)
        elif test21 == 0:
            print("Test 21 didn't run: Ethernet Link object (0xF6)\n")
            file.write("Test 21 didn't run: Ethernet Link object (0xF6)\n")


#Run the main function
sendCIP()
