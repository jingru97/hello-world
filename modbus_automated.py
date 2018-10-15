import socket, time, struct, ssl


TCP_IP = input("IP? ")

unitid_manual = input("Unit ID? ")
unitid_manual = int(unitid_manual)

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



# (1) FC 8/21
# (1_1) Modbus Messaging Statistics (0x65)
# (1_2) Modbus Messaging Statistics Connections (0x66)
# (1_3) Reset Messaging Counters (0x67)
# (1_4) DHCP Statistics (0x6D)
# (1_5) SMTP Statistics (0x6E)
# (1_6) NTP Statistics (0x6F)
# (1_7) Firmware Version (0x70)
# (1_8) Get Basic Switch Info (0x71)
# (1_9) Get RSTP Port of Switch Info (0x72)
# (2) FC 8/22
# (2_1) Read Basic Network Diagnostics (1/0x100)
# (2_2) Read Port Diagnostic Data (1/0x200)
# (2_3) Read Modbus TCP/Port 502 Diag Data (1/0x300)
# (2_4) Read Modbus TCP/Port Connection Data (1/0x400)
# (2_5) Read Data Structures Offsets (1/0x7F00)
# (2_6) Clear Diag data for Network (2/0x100)
# (2_7) Clear Diag data for Ethernet Port (2/0x200)
# (2_8) Clear Diag data for MB Port 502 (2/0x300)
# (2_9)Clear Diag data for Connection table (2/0x400)
# (2_10) Clear All Diagnostic Data (3/0)
# (2_11) List Ports (4/0)
# (3) FC 2B
# (3_1) Read Basic Object Device ID (0E/1/0)
# (3_2) Read Regular Object Device ID (0E/2/0)
# (3_3) Read Extended Object Device ID (0E/3/0)
# (3_4) Read Individual Object of Device ID (0E/4/0)
# (4) Modbus Read Register Command FC 3 Unit Id 255
# (5) Read Coils (FC 1)
# (6) Read Inputs (FC 2)
# (7) Read Holding Registers (FC 3)
# (8) Read Input Registers (FC 4)
# (9) Write Single Coil (FC 5)
# (10) Write Single Register (FC 6)
# (11) Write Multiple Coils (FC 15)
# (12) Write Multiple Registers (FC 16)
# (13) Read/Write Multiple Registers (FC 23)
# (14) Custom request

option1_1 = 1
option1_2 = 1
option1_3 = 1
option1_4 = 1
option1_5 = 1
option1_6 = 1
option1_7 = 1
option1_8 = 1
option1_9 = 1
option2_1 = 1
option2_2 = 1
option2_3 = 1
option2_4 = 1
option2_5 = 1
option2_6 = 1
option2_7 = 1
option2_8 = 1
option2_9 = 1
option2_10 = 1
option2_11 = 1
option3_1 = 1
option3_2 = 1
option3_3 = 1
option3_4 = 1
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

option14 = 0

mfile = open("modbus_results.txt","w")

# Function that takes in a request and returns the response
def modbusReq(func_req, sock):
    sock.send(func_req)

    rec = sock.recv(300)
    s = struct.Struct(str(len(rec)) + 'B')
    data = s.unpack(rec)

    dataStr = ""

    for z in range(0, len(data)):
        dataStr += str(hex(data[z])) + " "

    return (rec, dataStr)


#Open a socket and then send the modbus requests
def sendModbus():
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

        sock.connect((TCP_IP, 802))

    else:

        sock.connect((TCP_IP, 502))


    execute_modbus(sock)

    sock.close()





#Send the selected modbus requests
def execute_modbus(sock):
    global reqsRan
    global unitid_manual

    global option1_1
    global option1_2
    global option1_3
    global option1_4
    global option1_5
    global option1_6
    global option1_7
    global option1_8
    global option1_9
    global option2_1
    global option2_2
    global option2_3
    global option2_4
    global option2_5
    global option2_6
    global option2_7
    global option2_8
    global option2_9
    global option2_10
    global option2_11
    global option3_1
    global option3_2
    global option3_3
    global option3_4
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



    # Initialize the flags that indicate if a test passed or failed
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
    test22 = 0
    test23 = 0
    test24 = 0
    test25 = 0
    test26 = 0
    test27 = 0
    test28 = 0
    test29 = 0
    test30 = 0
    test31 = 0
    test32 = 0
    test33 = 0
    test34 = 0

    # Pack the input we get for unit id into a byte string
    unitId = struct.pack("B", int(unitid_manual))

    #resp.set("")

    # Check if the first checkbox is checked, and if it is then send the request, get the response, and run the test
    if option1_1 == 1:

       # reqsRan += 1

        # Modbus request
        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x65"

        # Send the request and get the response
        output, dataStr = modbusReq(req, sock)

        outputstr = ""
        # Print the name of the test, the request, and the response

        outputstr += "\n(1) Modbus Messaging Statistics (0x65)\n\n" + " ".join(hex(n) for n in req) + "\n\n" + dataStr

        passfail = 0

        if output[7:13] == b"\x08\x00\x15\x00\x65\x1e" and (
                (output[15:19] == b"\x00\x00\x00\x01") or (output[15:19] == b"\x00\x00\x00\x02") or (
            output[15:19] == b"\x00\x00\x00\x03")):
            # print ("\nTest Passed\n")
            outputstr += "\n\nTest Passed"
            test1 = 1
            passfail = 1
        else:
            # print ("\n\nTest Failed")
            outputstr += "\n\nTest Failed"
            test1 = 2
            passfail = 2


        #43 = pass
        test1len = len(output)


        # Insert the string we created into the textbox
        # resp.set(outputstr)

      #  t.insert(END, outputstr)

      #  color_test(passfail)

    if option1_2 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x15\x00\x66\x01\x01"

        outputstr = ""

        output, dataStr = modbusReq(req, sock)
        outputstr += "\n(2) Modbus Messaging Statistics Connections (0x66)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        passfail = 0
        if (output[7:12] == b"\x08\x00\x15\x00\x66") and (
                    (output[23:27] == b"\x00\x00\x00\x00") or (output[23:27] == b"\x00\x00\x00\x01") or (
                output[23:27] == b"\x00\x00\x00\x02") or (output[23:27] == b"\x00\x00\x00\x03")):
            outputstr += "\n\nTest Passed"
            test2 = 1
            passfail = 1
        else:
            outputstr += "\n\nTest Failed"
            test2 = 2
            passfail = 2

        test2len = len(output)

        # resp.set(resp.get() + outputstr)
     #   t.insert(END, outputstr)

     #   color_test(passfail)

    if option1_3 == 1:

      #  reqsRan += 1

        outputstr = ""

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x67"

        output, dataStr = modbusReq(req, sock)
        outputstr += "\n(3) Reset Messaging Counters (0x67)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        passfail = 0
        if output[7:12] == b"\x08\x00\x15\x00\x67":
            outputstr += "\n\nTest Passed"
            test3 = 1
            passfail = 1
        else:
            outputstr += "\n\nTest Failed"
            test3 = 2
            passfail = 2

        #12 = pass
        test3len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(passfail)

    if option1_4 == 1:

      #  reqsRan += 1

        outputstr = ""

        req = b"\x00\x00\x00\x00\x00\x07" + unitId + b"\x08\x00\x15\x00\x6D\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr += "\n(4) DHCP Statistics (0x6D)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        passfail = 0
        if (output[7:12] == b"\x08\x00\x15\x00\x6d") and (
            (output[13:15] == b"\x00\x01") or (output[13:15] == b"\x00\x02")):
            outputstr += "\n\nTest Passed"
            test4 = 1
            passfail = 1
        else:
            outputstr += "\n\nTest Failed"
            test4 = 2
            passfail = 2

        test4len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(passfail)

    if option1_5 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x6E"

        output, dataStr = modbusReq(req, sock)

        outputstr = ""

        outputstr += "\n(5) SMTP Statistics (0x6E)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        passfail = 0
        if output[7:13] == b"\x08\x00\x15\x00\x6e\x2a":
            outputstr += "\n\nTest Passed"
            test5 = 1
            passfail = 1
        else:
            outputstr += "\n\nTest Failed (might not be implemented)"
            test5 = 2
            passfail = 2

        test5len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(passfail)

    if option1_6 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x6F"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(6) NTP Statistics (0x6F)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        passfail = 0
        if output[7:13] == b"\x08\x00\x15\x00\x6f\x46":
            outputstr += "\n\nTest Passed"
            test6 = 1
            passfail = 1
        else:
            outputstr += "\n\nTest Failed"
            test6 = 2
            passfail = 2

        test6len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(passfail)

    if option1_7 == 1:

       # reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x70"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(7) Firmware Version (0x70)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        passfail = 0
        if output[7:13] == b"\x08\x00\x15\x00\x70\x06":
            outputstr += "\n\nTest Passed"
            test7 = 1
            passfail = 1
        else:
            outputstr += "\n\nTest Failed"
            test7 = 2
            passfail = 2

        test7len = len(output)

      # t.insert(END, outputstr)
      #  color_test(passfail)

    if option1_8 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x08\x00\x15\x00\x71"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(8) Get Basic Switch Info (0x71)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:13] == b"\x08\x00\x15\x00\x71\x27":
            outputstr += "\n\nTest Passed"
            test8 = 1

        else:
            outputstr += "\n\nTest Failed"
            test8 = 2

        test8len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test8)

    if option1_9 == 1:

       # reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x07" + unitId + b"\x08\x00\x15\x00\x72\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(9) Get RSTP Port of Switch Info (0x72)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:13] == b"\x08\x00\x15\x00\x72\x2f":
            outputstr += "\n\nTest Passed"
            test9 = 1
        else:
            outputstr += "\n\nTest Failed"
            test9 = 2

        test9len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test9)

    if option2_1 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x09" + unitId + b"\x08\x00\x16\x00\x01\x01\x00\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(10) Read Basic Network Diagnostics (1/0x100)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x01\x01\x00":
            outputstr += "\n\nTest Passed"
            test10 = 1
        else:
            outputstr += "\n\nTest Failed"
            test10 = 2

        test10len = len(output)

       # t.insert(END, outputstr)
       # color_test(test10)

    if option2_2 == 1:

    #    reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x09" + unitId + b"\x08\x00\x16\x00\x01\x02\x00\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(11) Read Port Diagnostic Data (1/0x200)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:13] == b"\x08\x00\x16\x00\x01\x02":
            outputstr += "\n\nTest Passed"
            test11 = 1
        else:
            outputstr += "\n\nTest Failed"
            test11 = 2

        test11len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test11)

    if option2_3 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x09" + unitId + b"\x08\x00\x16\x00\x01\x03\x00\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(12) Read Modbus TCP/Port 502 Diag Data (1/0x300)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x01\x03\x00":
            outputstr += "\n\nTest Passed"
            test12 = 1
        else:
            outputstr += "\n\nTest Failed"
            test12 = 2

        test12len = len(output)

      #  t.insert(END, outputstr)
     #   color_test(test12)

    if option2_4 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x09" + unitId + b"\x08\x00\x16\x00\x01\x04\x00\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(13) Read Modbus TCP/Port Connection Data (1/0x400)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x01\x04\x00":
            outputstr += "\n\nTest Passed"
            test13 = 1
        else:
            outputstr += "\n\nTest Failed"
            test13 = 2

        test13len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test13)

    if option2_5 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x01\x7F\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(14) Read Data Structures Offsets (1/0x7F00)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x01\x7f\x00":
            outputstr += "\n\nTest Passed"
            test14 = 1
        else:
            outputstr += "\n\nTest Failed"
            test14 = 2

        test14len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test14)

    if option2_6 == 1:

    #    reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x02\x01\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ''
        outputstr += "\n(15) Clear Diag data for Network (2/0x100)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x02\x01\x00":
            outputstr += "\n\nTest Passed"
            test15 = 1
        else:
            outputstr += "\n\nTest Failed"
            test15 = 2

        test15len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test15)

    if option2_7 == 1:

       # reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x02\x02\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(16) Clear Diag data for Ethernet Port (2/0x200)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x02\x02\x00":
            outputstr += "\n\nTest Passed"
            test16 = 1
        else:
            outputstr += "\n\nTest Failed"
            test16 = 2

        test16len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test16)

    if option2_8 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x02\x03\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(17) Clear Diag data for MB Port 502 (2/0x300)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x02\x03\x00":
            outputstr += "\n\nTest Passed"
            test17 = 1
        else:
            outputstr += "\n\nTest Failed"
            test17 = 2

        test17len = len(output)

       # t.insert(END, outputstr)
      #  color_test(test17)

    if option2_9 == 1:

     #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x02\x04\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(18) Clear Diag data for Connection table (2/0x400)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x02\x04\x00":
            outputstr += "\n\nTest Passed"
            test18 = 1
        else:
            outputstr += "\n\nTest Failed"
            test18 = 2

        test18len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test18)

    if option2_10 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x03\x00\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(19) Clear All Diagnostic Data (3/0)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x03\x00\x00":
            outputstr += "\n\nTest Passed"
            test19 = 1
        else:
            outputstr += "\n\nTest Failed"
            test19 = 2

        test19len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test19)

    if option2_11 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x08\x00\x16\x00\x04\x00\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(20) List Ports (4/0)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:14] == b"\x08\x00\x16\x00\x04\x00\x00":
            outputstr += "\n\nTest Passed"
            test20 = 1
        else:
            outputstr += "\n\nTest Failed"
            test20 = 2

        test20len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test20)

    if option3_1 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x2B\x0E\x01\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(21) Read Basic Object Device ID (0E/1/0)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        isFile=0
        if isFile:

            if output[7:10] == b"\x2b\x0e\x01" and output[16:36].decode("utf-8") + "\n" == content[0] and output[
                                                                                                          38:50].decode(
                    "utf-8") + "\n" == content[1] and output[52:58].decode("utf-8") + "\n" == content[2]:
                outputstr += "\n\nTest Passed"
                test21 = 1
            else:
                outputstr += "\n\nTest Failed"
                test21 = 2
        else:
            if output[7:10] == b"\x2b\x0e\x01":
                outputstr += "\n\nTest Passed"
                test21 = 1
            else:
                outputstr += "\n\nTest Failed"
                test21 = 2

        test21len = len(output)

      #  t.insert(END, outputstr)
     #   color_test(test21)

    if option3_2 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x2B\x0E\x02\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(22) Read Regular Object Device ID (0E/2/0)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:10] == b"\x2b\x0e\x02":
            outputstr += "\n\nTest Passed"
            test22 = 1
        else:
            outputstr += "\n\nTest Failed"
            test22 = 2

        test22len = len(output)

     #   t.insert(END, outputstr)
      #  color_test(test22)

    if option3_3 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x2B\x0E\x03\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(23) Read Extended Object Device ID (0E/3/0)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:10] == b"\x2b\x0e\x03":
            outputstr += "\n\nTest Passed"
            test23 = 1
        else:
            outputstr += "\n\nTest Failed"
            test23 = 2

        test23len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test23)

    if option3_4 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x2B\x0E\x04\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(24) Read Individual Object of Device ID (0E/4/0)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:10] == b"\x2b\x0e\x04":
            outputstr += "\n\nTest Passed"
            test24 = 1
        else:
            outputstr += "\n\nTest Failed"
            test24 = 2

        test24len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test24)

    if option4 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06\xFF\x03\x00\x63\x00\x05"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(25) Modbus Read Register Command FC 3 Unit Id 255\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[5:9] == b"\x0d\xff\x03\x0a":
            outputstr += "\n\nTest Passed"
            test25 = 1
        else:
            outputstr += "\n\nTest Failed"
            test25 = 2

        test25len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test25)

    if option5 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x01\x00\x00\x00\x05"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(26) Read Coils (FC 1)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[0:9] == (b"\x00\x00\x00\x00\x00\x04" + unitId + b"\x01\x01"):
            outputstr += "\n\nTest Passed"
            test26 = 1
        else:
            outputstr += "\n\nTest Failed"
            test26 = 2

        test26len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test26)

    if option6 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x02\x00\x00\x00\x05"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(27) Read Inputs (FC 2)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[0:9] == (b"\x00\x00\x00\x00\x00\x04" + unitId + b"\x02\x01"):
            outputstr += "\n\nTest Passed"
            test27 = 1
        else:
            outputstr += "\n\nTest Failed"
            test27 = 2

        test27len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test27)

    if option7 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x03\x00\x64\x00\x01"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(28) Read Holding Registers (FC 3)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[0:9] == (b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x03\x02"):
            outputstr += "\n\nTest Passed"
            test28 = 1
        else:
            outputstr += "\n\nTest Failed"
            test28 = 2

        test28len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test28)

    if option8 == 1:

       # reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x04\x00\x64\x00\x01"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(29) Read Input Registers (FC 4)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[0:9] == (b"\x00\x00\x00\x00\x00\x05" + unitId + b"\x04\x02"):
            outputstr += "\n\nTest Passed"
            test29 = 1
        else:
            outputstr += "\n\nTest Failed"
            test29 = 2

        test29len = len(output)

      #  t.insert(END, outputstr)
     #   color_test(test29)

    if option9 == 1:

       # reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x05\x01\x00\xff\x00"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(30) Write Single Coil (FC 5)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:] == b"\x05\x01\x00\xff\x00":
            outputstr += "\n\nTest Passed"
            test30 = 1
        else:
            outputstr += "\n\nTest Failed"
            test30 = 2

        test30len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test30)

    if option10 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x06" + unitId + b"\x06\x01\x00\x00\x01"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(31) Write Single Register (FC 6)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:] == b"\x06\x01\x00\x00\x01":
            outputstr += "\n\nTest Passed"
            test31 = 1
        else:
            outputstr += "\n\nTest Failed"
            test31 = 2

        test31len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test31)

    if option11 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x08" + unitId + b"\x0f\x00\x64\x00\x02\x01\x66"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(32) Write Multiple Coils (FC 15)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:] == b"\x0f\x00\x64\x00\x02":
            outputstr += "\n\nTest Passed"
            test32 = 1
        else:
            outputstr += "\n\nTest Failed"
            test32 = 2

        test32len = len(output)

     #   t.insert(END, outputstr)
      #  color_test(test32)

    if option12 == 1:

      #  reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x0b" + unitId + b"\x10\x00\x64\x00\x02\x04\x3a\xbe\x5f\xc6"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(33) Write Multiple Registers (FC 16)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:] == b"\x10\x00\x64\x00\x02":
            outputstr += "\n\nTest Passed"
            test33 = 1
        else:
            outputstr += "\n\nTest Failed"
            test33 = 2

        test33len = len(output)

     #   t.insert(END, outputstr)
     #   color_test(test33)

    if option13 == 1:

     #   reqsRan += 1

        req = b"\x00\x00\x00\x00\x00\x0d" + unitId + b"\x17\x00\x64\x00\x01\x00\x64\x00\x01\x02\x2d\xd6"

        output, dataStr = modbusReq(req, sock)
        outputstr = ""
        outputstr += "\n(34) Read/Write Multiple Registers (FC 23)\n\n"
        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        outputstr += dataStr

        if output[7:] == b"\x17\x02\x2d\xd6":
            outputstr += "\n\nTest Passed"
            test34 = 1
        else:
            outputstr += "\n\nTest Failed"
            test34 = 2

        test34len = len(output)

      #  t.insert(END, outputstr)
      #  color_test(test34)

    # Send a custom modbus request and get the response
    if option14 == 1:

      #  reqsRan += 1

        # Prompt user for the frame starting with the function code, i.e. 0800150003 would be function code 8 (diagnostic), sub function code 21, and operation code 3
        frame = custom_ent.get()

        # Get the length of the frame string
        frameLen = int(len(frame))

        # Calculate the number of bytes in the frame
        lengthField = frameLen // 2

        # Initialize the argument list
        argsList = []

        # The transaction id and protocol id are 0, length is the number of bytes in the inputted frame plus 1 for the unit id
        # and get the unit id that was given by user input at the beginning
        argsList.append("0, 0, " + str(lengthField + 1) + ", " + unitId_input.get() + ", ")

        # Loop through the frame, grabbing two characters at a time, convert them from hex to decimal, and add them to the argument list
        for x in range(0, int(frameLen) // 2):

            if x == ((frameLen // 2) - 1):
                argsList.append("int('0x' + frame[" + str(x * 2) + ":" + str(x * 2 + 2) + "], 16))")
            else:
                argsList.append("int('0x' + frame[" + str(x * 2) + ":" + str(x * 2 + 2) + "], 16), ")

        # > means big endian. H means word (two bytes), for the transaction id, protocol id, and length
        # B means bytes, and we take the length plus one for the unit id
        # The result is the 3H corresponds to the first three arguments, and the _B corresponds to the rest of the frame
        # to pack into a byte string
        packStr = '>3H ' + str(frameLen // 2 + 1) + 'B'

        # Create the string to execute with argsList
        evalStr = "struct.pack(packStr, "

        for y in range(0, len(argsList)):
            evalStr = evalStr + argsList[y]

        # Execute the command struct.pack.... with all the arguments to create the request
        outputstr = ""

        outputstr += "\n(35) Custom request\n\n"

        try:
            req = eval(evalStr)
        except SyntaxError:
            outputstr += "Invalid frame\n\n"

        outputstr += " ".join(hex(n) for n in req) + "\n\n"

        # Send the request and get the response
        output, dataStr = modbusReq(req, sock)

        outputstr += dataStr + "\n\n"

     #   t.insert(END, outputstr)

  #  t.insert(END, "\n")

    # Print the appropriate test results

    if option1_1 == 1:
        if test1 == 1:
            print("\nTest 1 Passed: Modbus Messaging Statistics (0x65)")
            mfile.write("Test 1 Passed: Modbus Messaging Statistics (0x65)\n")
        elif test1 == 2:
            print("\nTest 1 Failed: Modbus Messaging Statistics (0x65)")
            mfile.write("Test 1 Failed: Modbus Messaging Statistics (0x65)\n")
        elif test1 == 0:
            print("\nTest 1 didn't run: Modbus Messaging Statistics (0x65)")
            mfile.write("Test 1 didn't run: Modbus Messaging Statistics (0x65)\n")

        #43 = pass
        if test1len == 43:
            print("Test 1 length = "+str(test1len) + " (pass)")
            mfile.write("Test 1 length = "+str(test1len) + " (pass)\n")
        else:
            print("Test 1 length = "+str(test1len) + " (fail)")
            mfile.write("Test 1 length = "+str(test1len) + " (fail)\n")



    if option1_2 == 1:
        if test2 == 1:
            print("Test 2 Passed: Modbus Messaging Statistics Connections (0x66)")
            mfile.write("Test 2 Passed: Modbus Messaging Statistics Connections (0x66)\n")
        elif test2 == 2:
            print("Test 2 Failed: Modbus Messaging Statistics Connections (0x66)")
            mfile.write("Test 2 Failed: Modbus Messaging Statistics Connections (0x66)\n")
        # color_test2(2)
        elif test2 == 0:
            print("Test 2 didn't run: Modbus Messaging Statistics Connections (0x66)\n")
            mfile.write("Test 2 didn't run: Modbus Messaging Statistics Connections (0x66)\n")

        print("Test 2 length = " + str(test2len))
        mfile.write("Test 2 length = " + str(test2len) + "\n")

    if option1_3 == 1:
        if test3 == 1:
            print("Test 3 Passed: Reset Messaging Counters (0x67)")
            mfile.write("Test 3 Passed: Reset Messaging Counters (0x67)\n")
        #    color_test2(1)
        elif test3 == 2:
            print("Test 3 Failed: Reset Messaging Counters (0x67)")
            mfile.write("Test 3 Failed: Reset Messaging Counters (0x67)\n")
        #    color_test2(2)
        elif test3 == 0:
            print("Test 3 didn't run: Reset Messaging Counters (0x67)\n")
            mfile.write("Test 3 didn't run: Reset Messaging Counters (0x67)\n")

        #12 = pass
        if test3len == 12:
            print("Test 3 length = "+str(test3len) + " (pass)")
            mfile.write("Test 3 length = "+str(test3len) + " (pass)\n")
        else:
            print("Test 3 length = "+str(test3len) + " (fail)")
            mfile.write("Test 3 length = "+str(test3len) + " (fail)\n")

    if option1_4 == 1:
        if test4 == 1:
            print("Test 4 Passed: DHCP Statistics (0x6D)")
            mfile.write("Test 4 Passed: DHCP Statistics (0x6D)\n")
            #     color_test2(1)
        elif test4 == 2:
            print("Test 4 Failed: DHCP Statistics (0x6D)")
            mfile.write("Test 4 Failed: DHCP Statistics (0x6D)\n")
            #     color_test2(2)
        elif test4 == 0:
            print("Test 4 didn't run: DHCP Statistics (0x6D)\n")
            mfile.write("Test 4 didn't run: DHCP Statistics (0x6D)\n")

        print("Test 4 length = " + str(test4len))
        mfile.write("Test 4 length = " + str(test4len) + "\n")

    if option1_5 == 1:
        if test5 == 1:
            print("Test 5 Passed: SMTP Statistics (0x6E)")
            mfile.write("Test 5 Passed: SMTP Statistics (0x6E)\n")
        # color_test2(1)
        elif test5 == 2:
            print("Test 5 Failed: SMTP Statistics (0x6E) (might not be implemented)")
            mfile.write("Test 5 Failed: SMTP Statistics (0x6E) (might not be implemented)\n")
        # color_test2(2)
        elif test5 == 0:
            print("Test 5 didn't run: SMTP Statistics (0x6E)\n")
            mfile.write("Test 5 didn't run: SMTP Statistics (0x6E)\n")

        #55 = pass
        # if test5len == 55:
        #     print("Test 5 length = "+str(test5len) + " (pass)")
        #     mfile.write("Test 5 length = "+str(test5len) + " (pass)\n")
        # else:
        #     print("Test 5 length = "+str(test5len) + " (fail)")
        #     mfile.write("Test 5 length = "+str(test5len) + " (fail)\n")

    if option1_6 == 1:
        if test6 == 1:
            print("Test 6 Passed: NTP Statistics (0x6F)")
            mfile.write("Test 6 Passed: NTP Statistics (0x6F)\n")
            #      color_test2(1)
        elif test6 == 2:
            print("Test 6 Failed: NTP Statistics (0x6F)")
            mfile.write("Test 6 Failed: NTP Statistics (0x6F)\n")
        # color_test2(2)
        elif test6 == 0:
            print("Test 6 didn't run: NTP Statistics (0x6F)\n")
            mfile.write("Test 6 didn't run: NTP Statistics (0x6F)\n")

        print("Test 6 length = " + str(test6len))
        mfile.write("Test 6 length = " + str(test6len) + "\n")

    if option1_7 == 1:
        if test7 == 1:
            print("Test 7 Passed: Firmware Version (0x70)")
            mfile.write("Test 7 Passed: Firmware Version (0x70)\n")
        # color_test2(1)
        elif test7 == 2:
            print("Test 7 Failed: Firmware Version (0x70)")
            mfile.write("Test 7 Failed: Firmware Version (0x70)\n")
            #     color_test2(2)
        elif test7 == 0:
            print("Test 7 didn't run: Firmware Version (0x70)\n")
            mfile.write("Test 7 didn't run: Firmware Version (0x70)\n")

        #19 = pass
        if test7len == 19:
            print("Test 7 length = "+str(test7len) + " (pass)")
            mfile.write("Test 7 length = "+str(test7len) + " (pass)\n")
        else:
            print("Test 7 length = "+str(test7len) + " (fail)")
            mfile.write("Test 7 length = "+str(test7len) + " (fail)\n")

    if option1_8 == 1:
        if test8 == 1:
            print("Test 8 Passed: Get Basic Switch Info (0x71)")
            mfile.write("Test 8 Passed: Get Basic Switch Info (0x71)\n")
            #     color_test2(1)
        elif test8 == 2:
            print("Test 8 Failed: Get Basic Switch Info (0x71)")
            mfile.write("Test 8 Failed: Get Basic Switch Info (0x71)\n")
        # color_test2(2)
        elif test8 == 0:
            print("Test 8 didn't run: Get Basic Switch Info (0x71)\n")
            mfile.write("Test 8 didn't run: Get Basic Switch Info (0x71)\n")

        #52 = pass
        if test8len == 52:
            print("Test 8 length = "+str(test8len) + " (pass)")
            mfile.write("Test 8 length = "+str(test8len) + " (pass)\n")
        else:
            print("Test 8 length = "+str(test8len) + " (fail)")
            mfile.write("Test 8 length = "+str(test8len) + " (fail)\n")

    if option1_9 == 1:
        if test9 == 1:
            print("Test 9 Passed: Get RSTP Port of Switch Info (0x72)")
            mfile.write("Test 9 Passed: Get RSTP Port of Switch Info (0x72)\n")
            #     color_test2(1)
        elif test9 == 2:
            print("Test 9 Failed: Get RSTP Port of Switch Info (0x72)")
            mfile.write("Test 9 Failed: Get RSTP Port of Switch Info (0x72)\n")
            #      color_test2(2)
        elif test9 == 0:
            print("Test 9 didn't run: Get RSTP Port of Switch Info (0x72)\n")
            mfile.write("Test 9 didn't run: Get RSTP Port of Switch Info (0x72)\n")

        print("Test 9 length = " + str(test9len))
        mfile.write("Test 9 length = " + str(test9len) + "\n")

    if option2_1 == 1:
        if test10 == 1:
            print("Test 10 Passed: Read Basic Network Diagnostics (1/0x100)")
            mfile.write("Test 10 Passed: Read Basic Network Diagnostics (1/0x100)\n")
            #      color_test2(1)
        elif test10 == 2:
            print("Test 10 Failed: Read Basic Network Diagnostics (1/0x100)")
            mfile.write("Test 10 Failed: Read Basic Network Diagnostics (1/0x100)\n")
            #     color_test2(2)
        elif test10 == 0:
            print("Test 10 didn't run: Read Basic Network Diagnostics (1/0x100)\n")
            mfile.write("Test 10 didn't run: Read Basic Network Diagnostics (1/0x100)\n")

        #95 = pass
        if test10len == 95:
            print("Test 10 length = "+str(test10len) + " (pass)")
            mfile.write("Test 10 length = "+str(test10len) + " (pass)\n")
        else:
            print("Test 10 length = "+str(test10len) + " (fail)")
            mfile.write("Test 10 length = "+str(test10len) + " (fail)\n")

    if option2_2 == 1:
        if test11 == 1:
            print("Test 11 Passed: Read Port Diagnostic Data (1/0x200)")
            mfile.write("Test 11 Passed: Read Port Diagnostic Data (1/0x200)\n")
            #     color_test2(1)
        elif test11 == 2:
            print("Test 11 Failed: Read Port Diagnostic Data (1/0x200)")
            mfile.write("Test 11 Failed: Read Port Diagnostic Data (1/0x200)\n")
            #      color_test2(2)
        elif test11 == 0:
            print("Test 11 didn't run: Read Port Diagnostic Data (1/0x200)\n")
            mfile.write("Test 11 didn't run: Read Port Diagnostic Data (1/0x200)\n")

        print("Test 11 length = " + str(test11len))
        mfile.write("Test 11 length = " + str(test11len) + "\n")

    if option2_3 == 1:
        if test12 == 1:
            print("Test 12 Passed: Read Modbus TCP/Port 502 Diag Data (1/0x300)")
            mfile.write("Test 12 Passed: Read Modbus TCP/Port 502 Diag Data (1/0x300)\n")
            #      color_test2(1)
        elif test12 == 2:
            print("Test 12 Failed: Read Modbus TCP/Port 502 Diag Data (1/0x300)")
            mfile.write("Test 12 Failed: Read Modbus TCP/Port 502 Diag Data (1/0x300)\n")
        # color_test2(2)
        elif test12 == 0:
            print("Test 12 didn't run: Read Modbus TCP/Port 502 Diag Data (1/0x300)\n")
            mfile.write("Test 12 didn't run: Read Modbus TCP/Port 502 Diag Data (1/0x300)\n")

        #53 = pass
        if test12len == 53:
            print("Test 12 length = "+str(test12len) + " (pass)")
            mfile.write("Test 12 length = "+str(test12len) + " (pass)\n")
        else:
            print("Test 12 length = "+str(test12len) + " (fail)")
            mfile.write("Test 12 length = "+str(test12len) + " (fail)\n")

    if option2_4 == 1:
        if test13 == 1:
            print("Test 13 Passed: Read Modbus TCP/Port Connection Data (1/0x400)")
            mfile.write("Test 13 Passed: Read Modbus TCP/Port Connection Data (1/0x400)\n")
            #     color_test2(1)
        elif test13 == 2:
            print("Test 13 Failed: Read Modbus TCP/Port Connection Data (1/0x400)")
            mfile.write("Test 13 Failed: Read Modbus TCP/Port Connection Data (1/0x400)\n")
            #     color_test2(2)
        elif test13 == 0:
            print("Test 13 didn't run: Read Modbus TCP/Port Connection Data (1/0x400)\n")
            mfile.write("Test 13 didn't run: Read Modbus TCP/Port Connection Data (1/0x400)\n")

        print("Test 13 length = " + str(test13len))
        mfile.write("Test 13 length = " + str(test13len) + "\n")

    if option2_5 == 1:
        if test14 == 1:
            print("Test 14 Passed: Read Data Structures Offsets (1/0x7F00)")
            mfile.write("Test 14 Passed: Read Data Structures Offsets (1/0x7F00)\n")
        # color_test2(1)
        elif test14 == 2:
            print("Test 14 Failed: Read Data Structures Offsets (1/0x7F00)")
            mfile.write("Test 14 Failed: Read Data Structures Offsets (1/0x7F00)\n")
            #     color_test2(2)
        elif test14 == 0:
            print("Test 14 didn't run: Read Data Structures Offsets (1/0x7F00)\n")
            mfile.write("Test 14 didn't run: Read Data Structures Offsets (1/0x7F00)\n")

        #35 = pass
        if test14len == 35:
            print("Test 14 length = "+str(test14len) + " (pass)")
            mfile.write("Test 14 length = "+str(test14len) + " (pass)\n")
        else:
            print("Test 14 length = "+str(test14len) + " (fail)")
            mfile.write("Test 14 length = "+str(test14len) + " (fail)\n")

    if option2_6 == 1:
        if test15 == 1:
            print("Test 15 Passed: Clear Diag data for Network (2/0x100)")
            mfile.write("Test 15 Passed: Clear Diag data for Network (2/0x100)\n")
            #     color_test2(1)
        elif test15 == 2:
            print("Test 15 Failed: Clear Diag data for Network (2/0x100)")
            mfile.write("Test 15 Failed: Clear Diag data for Network (2/0x100)\n")
            #     color_test2(2)
        elif test15 == 0:
            print("Test 15 didn't run: Clear Diag data for Network (2/0x100)")
            mfile.write("Test 15 didn't run: Clear Diag data for Network (2/0x100)\n")

        #14 = pass
        if test15len == 14:
            print("Test 15 length = "+str(test15len) + " (pass)")
            mfile.write("Test 15 length = "+str(test15len) + " (pass)\n")
        else:
            print("Test 15 length = "+str(test15len) + " (fail)")
            mfile.write("Test 15 length = "+str(test15len) + " (fail)\n")

    if option2_7 == 1:
        if test16 == 1:
            print("Test 16 Passed: Clear Diag data for Ethernet Port (2/0x200)")
            mfile.write("Test 16 Passed: Clear Diag data for Ethernet Port (2/0x200)\n")
            #   color_test2(1)
        elif test16 == 2:
            print("Test 16 Failed: Clear Diag data for Ethernet Port (2/0x200)")
            mfile.write("Test 16 Failed: Clear Diag data for Ethernet Port (2/0x200)\n")
            #   color_test2(2)
        elif test16 == 0:
            print("Test 16 didn't run: Clear Diag data for Ethernet Port (2/0x200)")
            mfile.write("Test 16 didn't run: Clear Diag data for Ethernet Port (2/0x200)\n")

        #14 = pass
        if test16len == 14:
            print("Test 16 length = "+str(test16len) + " (pass)")
            mfile.write("Test 16 length = "+str(test16len) + " (pass)\n")
        else:
            print("Test 16 length = "+str(test16len) + " (fail)")
            mfile.write("Test 16 length = "+str(test16len) + " (fail)\n")

    if option2_8 == 1:
        if test17 == 1:
            print("Test 17 Passed: Clear Diag data for MB Port 502 (2/0x300)")
            mfile.write("Test 17 Passed: Clear Diag data for MB Port 502 (2/0x300)\n")
        # color_test2(1)
        elif test17 == 2:
            print("Test 17 Failed: Clear Diag data for MB Port 502 (2/0x300)")
            mfile.write("Test 17 Failed: Clear Diag data for MB Port 502 (2/0x300)\n")
        # color_test2(2)
        elif test17 == 0:
            print("Test 17 didn't run: Clear Diag data for MB Port 502 (2/0x300)")
            mfile.write("Test 17 didn't run: Clear Diag data for MB Port 502 (2/0x300)\n")

        #14 = pass
        if test17len == 14:
            print("Test 17 length = "+str(test17len) + " (pass)")
            mfile.write("Test 17 length = "+str(test17len) + " (pass)\n")
        else:
            print("Test 17 length = "+str(test17len) + " (fail)")
            mfile.write("Test 17 length = "+str(test17len) + " (fail)\n")

    if option2_9 == 1:
        if test18 == 1:
            print("Test 18 Passed: Clear Diag data for Connection table (2/0x400)")
            mfile.write("Test 18 Passed: Clear Diag data for Connection table (2/0x400)\n")
            #      color_test2(1)
        elif test18 == 2:
            print("Test 18 Failed: Clear Diag data for Connection table (2/0x400)")
            mfile.write("Test 18 Failed: Clear Diag data for Connection table (2/0x400)\n")
            #      color_test2(2)
        elif test18 == 0:
            print("Test 18 didn't run: Clear Diag data for Connection table (2/0x400)")
            mfile.write("Test 18 didn't run: Clear Diag data for Connection table (2/0x400)\n")

        #14 = pass
        if test18len == 14:
            print("Test 18 length = "+str(test18len) + " (pass)")
            mfile.write("Test 18 length = "+str(test18len) + " (pass)\n")
        else:
            print("Test 18 length = "+str(test18len) + " (fail)")
            mfile.write("Test 18 length = "+str(test18len) + " (fail)\n")

    if option2_10 == 1:
        if test19 == 1:
            print("Test 19 Passed: Clear All Diagnostic Data (3/0)")
            mfile.write("Test 19 Passed: Clear All Diagnostic Data (3/0)\n")
            #     color_test2(1)
        elif test19 == 2:
            print("Test 19 Failed: Clear All Diagnostic Data (3/0)")
            mfile.write("Test 19 Failed: Clear All Diagnostic Data (3/0)\n")
            #      color_test2(2)
        elif test19 == 0:
            print("Test 19 didn't run: Clear All Diagnostic Data (3/0)")
            mfile.write("Test 19 didn't run: Clear All Diagnostic Data (3/0)\n")

        #14 = pass
        if test19len == 14:
            print("Test 19 length = "+str(test19len) + " (pass)")
            mfile.write("Test 19 length = "+str(test19len) + " (pass)\n")
        else:
            print("Test 19 length = "+str(test19len) + " (fail)")
            mfile.write("Test 19 length = "+str(test19len) + " (fail)\n")

    if option2_11 == 1:
        if test20 == 1:
            print("Test 20 Passed: List Ports (4/0)")
            mfile.write("Test 20 Passed: List Ports (4/0)\n")
            #       color_test2(1)
        elif test20 == 2:
            print("Test 20 Failed: List Ports (4/0)")
            mfile.write("Test 20 Failed: List Ports (4/0)\n")
            #      color_test2(2)
        elif test20 == 0:
            print("Test 20 didn't run: List Ports (4/0)\n")
            mfile.write("Test 20 didn't run: List Ports (4/0)\n")

        print("Test 20 length = " + str(test20len))
        mfile.write("Test 20 length = " + str(test20len) + "\n")

    if option3_1 == 1:
        if test21 == 1:
            print("Test 21 Passed: Read Basic Object Device ID (0E/1/0)")
            mfile.write("Test 21 Passed: Read Basic Object Device ID (0E/1/0)\n")
            #      color_test2(1)
        elif test21 == 2:
            print("Test 21 Failed: Read Basic Object Device ID (0E/1/0)")
            mfile.write("Test 21 Failed: Read Basic Object Device ID (0E/1/0)\n")
            #     color_test2(2)
        elif test21 == 0:
            print("Test 21 didn't run: Read Basic Object Device ID (0E/1/0)\n")
            mfile.write("Test 21 didn't run: Read Basic Object Device ID (0E/1/0)\n")

        print("Test 21 length = " + str(test21len))
        mfile.write("Test 21 length = " + str(test21len) + "\n")

    if option3_2 == 1:
        if test22 == 1:
            print("Test 22 Passed: Read Regular Object Device ID (0E/2/0)")
            mfile.write("Test 22 Passed: Read Regular Object Device ID (0E/2/0)\n")
            #      color_test2(1)
        elif test22 == 2:
            print("Test 22 Failed: Read Regular Object Device ID (0E/2/0)")
            mfile.write("Test 22 Failed: Read Regular Object Device ID (0E/2/0)\n")
            #      color_test2(2)
        elif test22 == 0:
            print("Test 22 didn't run: Read Regular Object Device ID (0E/2/0)\n")
            mfile.write("Test 22 didn't run: Read Regular Object Device ID (0E/2/0)\n")

        print("Test 22 length = " + str(test22len))
        mfile.write("Test 22 length = " + str(test22len) + "\n")

    if option3_3 == 1:
        if test23 == 1:
            print("Test 23 Passed: Read Extended Object Device ID (0E/3/0)")
            mfile.write("Test 23 Passed: Read Extended Object Device ID (0E/3/0)\n")
            #     color_test2(1)
        elif test23 == 2:
            print("Test 23 Failed: Read Extended Object Device ID (0E/3/0)")
            mfile.write("Test 23 Failed: Read Extended Object Device ID (0E/3/0)\n")
            #      color_test2(2)
        elif test23 == 0:
            print("Test 23 didn't run: Read Extended Object Device ID (0E/3/0)\n")
            mfile.write("Test 23 didn't run: Read Extended Object Device ID (0E/3/0)\n")

        print("Test 23 length = " + str(test23len))
        mfile.write("Test 23 length = " + str(test23len) + "\n")

    if option3_4 == 1:
        if test24 == 1:
            print("Test 24 Passed: Read Individual Object of Device ID (0E/4/0)")
            mfile.write("Test 24 Passed: Read Individual Object of Device ID (0E/4/0)\n")
            #     color_test2(1)
        elif test24 == 2:
            print("Test 24 Failed: Read Individual Object of Device ID (0E/4/0)")
            mfile.write("Test 24 Failed: Read Individual Object of Device ID (0E/4/0)\n")
            #      color_test2(2)
        elif test24 == 0:
            print("Test 24 didn't run: Read Individual Object of Device ID (0E/4/0)\n")
            mfile.write("Test 24 didn't run: Read Individual Object of Device ID (0E/4/0)\n")

        print("Test 24 length = " + str(test24len))
        mfile.write("Test 24 length = " + str(test24len) + "\n")

    if option4 == 1:
        if test25 == 1:
            print("Test 25 Passed: Modbus Read Register Command FC 3 Unit Id 255")
            mfile.write("Test 25 Passed: Modbus Read Register Command FC 3 Unit Id 255\n")
            #     color_test2(1)
        elif test25 == 2:
            print("Test 25 Failed: Modbus Read Register Command FC 3 Unit Id 255")
            mfile.write("Test 25 Failed: Modbus Read Register Command FC 3 Unit Id 255\n")
            #     color_test2(2)
        elif test25 == 0:
            print("Test 25 didn't run: Modbus Read Register Command FC 3 Unit Id 255\n")
            mfile.write("Test 25 didn't run: Modbus Read Register Command FC 3 Unit Id 255\n")

        print("Test 25 length = " + str(test25len))
        mfile.write("Test 25 length = " + str(test25len) + "\n")

    if option5 == 1:
        if test26 == 1:
            print("Test 26 Passed: Read Coils (FC 1)")
            mfile.write("Test 26 Passed: Read Coils (FC 1)\n")
            #      color_test2(1)
        elif test26 == 2:
            print("Test 26 Failed: Read Coils (FC 1)")
            mfile.write("Test 26 Failed: Read Coils (FC 1)\n")
            #      color_test2(2)
        elif test26 == 0:
            print("Test 26 didn't run: Read Coils (FC 1)\n")
            mfile.write("Test 26 didn't run: Read Coils (FC 1)\n")

        print("Test 26 length = " + str(test26len))
        mfile.write("Test 26 length = " + str(test26len) + "\n")

    if option6 == 1:
        if test27 == 1:
            print("Test 27 Passed: Read Inputs (FC 2)")
            mfile.write("Test 27 Passed: Read Inputs (FC 2)\n")
            #     color_test2(1)
        elif test27 == 2:
            print("Test 27 Failed: Read Inputs (FC 2)")
            mfile.write("Test 27 Failed: Read Inputs (FC 2)\n")
            #     color_test2(2)
        elif test27 == 0:
            print("Test 27 didn't run: Read Inputs (FC 2)\n")
            mfile.write("Test 27 didn't run: Read Inputs (FC 2)\n")

        print("Test 27 length = " + str(test27len))
        mfile.write("Test 27 length = " + str(test27len) + "\n")

    if option7 == 1:
        if test28 == 1:
            print("Test 28 Passed: Read Holding Registers (FC 3)")
            mfile.write("Test 28 Passed: Read Holding Registers (FC 3)\n")
            #       color_test2(1)
        elif test28 == 2:
            print("Test 28 Failed: Read Holding Registers (FC 3)")
            mfile.write("Test 28 Failed: Read Holding Registers (FC 3)\n")
            #      color_test2(2)
        elif test28 == 0:
            print("Test 28 didn't run: Read Holding Registers (FC 3)\n")
            mfile.write("Test 28 didn't run: Read Holding Registers (FC 3)\n")

        print("Test 28 length = " + str(test28len))
        mfile.write("Test 28 length = " + str(test28len) + "\n")

    if option8 == 1:
        if test29 == 1:
            print("Test 29 Passed: Read Input Registers (FC 4)")
            mfile.write("Test 29 Passed: Read Input Registers (FC 4)\n")
            #      color_test2(1)
        elif test29 == 2:
            print("Test 29 Failed: Read Input Registers (FC 4)")
            mfile.write("Test 29 Failed: Read Input Registers (FC 4)\n")
            #      color_test2(2)
        elif test29 == 0:
            print("Test 29 didn't run: Read Input Registers (FC 4)\n")
            mfile.write("Test 29 didn't run: Read Input Registers (FC 4)\n")

        print("Test 29 length = " + str(test29len))
        mfile.write("Test 29 length = " + str(test29len) + "\n")

    if option9 == 1:
        if test30 == 1:
            print("Test 30 Passed: Write Single Coil (FC 5)")
            mfile.write("Test 30 Passed: Write Single Coil (FC 5)\n")
            #      color_test2(1)
        elif test30 == 2:
            print("Test 30 Failed: Write Single Coil (FC 5)")
            mfile.write("Test 30 Failed: Write Single Coil (FC 5)\n")
            #      color_test2(2)
        elif test30 == 0:
            print("Test 30 didn't run: Write Single Coil (FC 5)")
            mfile.write("Test 30 didn't run: Write Single Coil (FC 5)\n")

        print("Test 30 length = " + str(test30len))
        mfile.write("Test 30 length = " + str(test30len) + "\n")

    if option10 == 1:
        if test31 == 1:
            print("Test 31 Passed: Write Single Register (FC 6)")
            mfile.write("Test 31 Passed: Write Single Register (FC 6)\n")
            #      color_test2(1)
        elif test31 == 2:
            print("Test 31 Failed: Write Single Register (FC 6)")
            mfile.write("Test 31 Failed: Write Single Register (FC 6)\n")
            #     color_test2(2)
        elif test31 == 0:
            print("Test 31 didn't run: Write Single Register (FC 6)")
            mfile.write("Test 31 didn't run: Write Single Register (FC 6)\n")

        print("Test 31 length = " + str(test31len))
        mfile.write("Test 31 length = " + str(test31len) + "\n")

    if option11 == 1:
        if test32 == 1:
            print("Test 32 Passed: Write Multiple Coils (FC 15)")
            mfile.write("Test 32 Passed: Write Multiple Coils (FC 15)\n")
            #      color_test2(1)
        elif test32 == 2:
            print("Test 32 Failed: Write Multiple Coils (FC 15)")
            mfile.write("Test 32 Failed: Write Multiple Coils (FC 15)\n")
            #     color_test2(2)
        elif test32 == 0:
            print("Test 32 didn't run: Write Multiple Coils (FC 15)")
            mfile.write("Test 32 didn't run: Write Multiple Coils (FC 15)")

        print("Test 32 length = " + str(test32len))
        mfile.write("Test 32 length = " + str(test32len) + "\n")

    if option12 == 1:
        if test33 == 1:
            print("Test 33 Passed: Write Multiple Registers (FC 16)")
            mfile.write("Test 33 Passed: Write Multiple Registers (FC 16)\n")
            #      color_test2(1)
        elif test33 == 2:
            print("Test 33 Failed: Write Multiple Registers (FC 16)")
            mfile.write("Test 33 Failed: Write Multiple Registers (FC 16)\n")
            #     color_test2(2)
        elif test33 == 0:
            print("Test 33 didn't run: Write Multiple Registers (FC 16)")
            mfile.write("Test 33 didn't run: Write Multiple Registers (FC 16)\n")

        print("Test 33 length = " + str(test33len))
        mfile.write("Test 33 length = " + str(test33len) + "\n")

    if option13 == 1:
        if test34 == 1:
            print("Test 34 Passed: Read/Write Multiple Registers (FC 23)")
            mfile.write("Test 34 Passed: Read/Write Multiple Registers (FC 23)\n")
            #     color_test2(1)
        elif test34 == 2:
            print("Test 34 Failed: Read/Write Multiple Registers (FC 23)")
            mfile.write("Test 34 Failed: Read/Write Multiple Registers (FC 23)\n")
            #     color_test2(2)
        elif test34 == 0:
            print("Test 34 didn't run: Read/Write Multiple Registers (FC 23)")
            mfile.write("Test 34 didn't run: Read/Write Multiple Registers (FC 23)\n")

        print("Test 34 length = " + str(test34len))
        mfile.write("Test 34 length = " + str(test34len) + "\n")

#Run the main function
sendModbus()
















