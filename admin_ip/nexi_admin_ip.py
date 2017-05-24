#!/usr/bin/env python3
# coding=utf-8

import tkinter as tk
import subprocess

# some const
DEF_IP_STR = '163.111.168.150'
DEF_MASK_STR = '255.255.255.0'
DEF_GW_STR = '163.111.168.1'
RED = '#bc3f3c'
GREEN = '#51c178'


def set_ip_address(ip, mask, gateway):
    subprocess.Popen('set_ip.bat %s %s %s' % (ip, mask, gateway),
                     shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)


def set_dhcp():
    subprocess.Popen('dhcp.bat',
                     shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)


def get_ip_config():
    try:
        cmd = subprocess.check_output('netsh interface ip show address "Ethernet"', shell=True)
        return cmd.decode('cp850')
    except:
        return 'impossible de lire la configuration'


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # configure main window
        self.wm_title('Nexi admin IP')
        self.resizable(width=False, height=False)
        # build interface
        self.ip_str_var = tk.StringVar()
        self.ip_str_var.set(DEF_IP_STR)
        self.mk_str_var = tk.StringVar()
        self.mk_str_var.set(DEF_MASK_STR)
        self.gw_str_var = tk.StringVar()
        self.gw_str_var.set(DEF_GW_STR)
        self.cnf_str_var = tk.StringVar()
        # frame 1
        self.frm_1 = tk.LabelFrame(self, text='IP config. type', padx=5, pady=5)
        self.frm_1.pack(padx=5, pady=5, fill=tk.BOTH)
        # send DHCP
        tk.Button(self.frm_1, text='T-Box (Pour envoi tws/tpg mise en service ITC)', command=self.send_tbox_ip).pack(fill=tk.BOTH)
        tk.Button(self.frm_1, text='DHCP (IP dynamique pour LAN maintenance)', command=self.send_dhcp).pack(fill=tk.BOTH)
        # frame 2
        self.frm_2 = tk.LabelFrame(self, text='IP personnalisée', padx=5, pady=5)
        self.frm_2.pack(padx=5, pady=5, fill=tk.BOTH)
        # set column size
        self.frm_2.grid_columnconfigure(0, minsize=150)
        self.frm_2.grid_columnconfigure(1, minsize=150)
        self.frm_2.grid_columnconfigure(2, minsize=80)
        self.frm_2.grid_rowconfigure(0, minsize=40)
        self.frm_2.grid_rowconfigure(1, minsize=40)
        self.frm_2.grid_rowconfigure(2, minsize=40)
        # ip
        tk.Label(self.frm_2, text='Adresse IP').grid(row=0, column=0)
        self.ent_ip = tk.Entry(self.frm_2, textvariable=self.ip_str_var, width=15)
        self.ent_ip.bind('<Return>', lambda evt: self.rtu_connect())
        self.ent_ip.grid(row=0, column=1)
        # mask
        tk.Label(self.frm_2, text='Masque').grid(row=1, column=0)
        self.ent_mk = tk.Entry(self.frm_2, textvariable=self.mk_str_var, width=15)
        self.ent_mk.grid(row=1, column=1)
        # gateway
        tk.Label(self.frm_2, text='Routeur').grid(row=2, column=0)
        self.ent_gw = tk.Entry(self.frm_2, textvariable=self.gw_str_var, width=15)
        self.ent_gw.grid(row=2, column=1)
        # send button
        tk.Button(self.frm_2, text='Envoi', command=self.send_custom_ip).grid(row=2, column=2, sticky=tk.EW)
        # frame 3
        self.frm_3 = tk.LabelFrame(self, text='Lecture config. Ethernet', padx=5, pady=5)
        self.frm_3.pack(padx=5, pady=5, fill=tk.BOTH)
        tk.Label(self.frm_3, textvariable=self.cnf_str_var).grid(row=0, column=0)
        # frame 4
        self.frm_4 = tk.Frame(self, padx=5, pady=5)
        self.frm_4.pack(padx=5, pady=5, fill=tk.BOTH)

        # exit button
        tk.Button(self.frm_4, text='Exit', command=self.destroy).pack()

        # periodic tags update
        self.do_every(self.update_status, every_ms=2000)

    def do_every(self, do_cmd, every_ms=1000):
        do_cmd()
        self.after(every_ms, lambda: self.do_every(do_cmd, every_ms=every_ms))

    def update_status(self):
        self.cnf_str_var.set(get_ip_config())

    def send_dhcp(self):
        set_dhcp()

    def send_tbox_ip(self):
        set_ip_address('192.168.1.100', '255.255.255.0', '192.168.1.1')

    def send_custom_ip(self):
        set_ip_address(self.ip_str_var.get(), self.mk_str_var.get(), self.gw_str_var.get())


if __name__ == '__main__':
    # main Tk App
    app = App()
    app.mainloop()
