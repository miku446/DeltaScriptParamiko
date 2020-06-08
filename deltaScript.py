#!/usr/bin/python
'''
Created on 02-May-2020

@author: mmahapat
'''

import getopt
import getpass
import sys
import time
import paramiko
from paramiko_expect import SSHClientInteraction

from delta import delta
from parse import parse


def login(argv):
    cmds = ''
    hostname = ''
    interval = 1
    out1 = []
    out2 = []
    res_1 = []
    res_2 = []
    prompt =''
    try:
        opts, args = getopt.getopt(argv, "hc:i:n:", ["command=", "interval=", "node="])
    except getopt.GetoptError:
        print('deltaScript.py -n <node> -i <interval in secs> -c <command>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('deltaScript.py -n <node> -i <interval in secs> -c <command>')
            sys.exit()
        elif opt in ("-i", "--interval"):
            interval = int(arg)
        elif opt in ("-c", "--command"):
            cmds = arg
        elif opt in ("-n", "--node"):
            hostname = arg
    #s = pxssh.pxssh()
    # hostname = raw_input('hostname: ')
    username = input('username: ')
    password = getpass.getpass('password: ')
    if username == "":
        username = "mike"
    if password == "":
        password = "test123"
    # if not s.login(hostname, username, password, auto_prompt_reset=False):
    remote_conn_pre = paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    remote_conn_pre.connect(hostname, username, password, allow_agent=False, look_for_keys=False)
    if remote_conn_pre.get_transport() is None or not remote_conn_pre.get_transport().is_active():
        print("SSH session failed on login.")
    else:
        # s.sync_original_prompt()
        print("SSH session login successful")
        remote_conn = remote_conn_pre.invoke_shell()
        #interact = SSHClientInteraction(remote_conn_pre, timeout=20, display=False)
        time.sleep(5)
        output = remote_conn.recv(9999).decode("utf-8")
        #print(output)
        node_str = output.strip().split("\n")[-1]
        remote_conn.close()
        #s.PROMPT = "#"
        #s.sendline()
        #s.prompt()
        #print(s.before.split("\n")[1])
        #node_str = s.before.split("\n")[1]
        if len(node_str.split("*")) == 2:
            #s.PROMPT = node_str.split("*")[1] + "#"
            prompt = node_str.split("*")[1]+" "
        else:
            #s.PROMPT = node_str.split("*")[0] + "#"
            prompt = node_str.split("*")[0]+" "
        print("The prompt is :" + prompt+"\"")
        remote_conn_pre.connect(hostname, username, password, allow_agent=False, look_for_keys=False)
        interact = SSHClientInteraction(remote_conn_pre, timeout=20, display=False)
        #time.sleep(5)
        #interact.send('\n')
        interact.expect(prompt)
        interact.send('environment time-stamp')
        interact.expect(prompt)
        interact.send('environment no more')
        interact.expect(prompt)
        cmd_output = interact.current_output_clean
        #interact.send(cmd_output)
        #print(cmd_output)
        #s.sendline('environment time-stamp')
        #s.prompt()
        #s.sendline('environment no more')
        #s.prompt()
        for cmd in cmds.split(";"):
            #s.sendline(cmd)
            interact.send(cmd)
            #s.prompt()  # match the prompt
            interact.expect(prompt)
            #out1.append(s.before)
            out1.append(interact.current_output)
            #print(out1[-1])
        # print(s.before)    # print everything before the prompt.
        # s.prompt ()
        # s.sendline ('sleep ' + str(interval))
        time.sleep(interval)
        # s.prompt ()         # match the prompt
        for cmd in cmds.split(";"):
            #s.sendline(cmd)
            interact.send(cmd)
            #s.prompt()  # match the prompt
            interact.expect(prompt)
            #out2.append(s.before)
            out2.append(interact.current_output)
            # print len(out2)
        # print(s.before)    # print everything before the prompt.
        print("The prompt is " + prompt)
        #s.sendline('logout')
        #s.close()
        #print (out1)
        #print (out2)
        for (aOut1, aOut2) in zip(out1, out2):
            #print(aOut1.decode('utf-8').split("\r")[-2])
            #print(aOut2.decode('utf-8').split("\r")[-2])
            #res_1.append(parse(aOut1.decode('utf-8').split("\r")))
            #res_2.append(parse(aOut2.decode('utf-8').split("\r")))
            #print(aOut1)
            #print(aOut2)
            print(aOut1.split("\n")[-2])
            print(aOut2.split("\n")[-2])
            res_1.append(parse(aOut1.split("\n")))
            res_2.append(parse(aOut2.split("\n")))
        # print (res_1)
        # print (res_2)
        for (aRes_1, aRes_2) in zip(res_1, res_2):
            delta(aRes_1, aRes_2, interval)


if __name__ == "__main__":
    login(sys.argv[1:])
