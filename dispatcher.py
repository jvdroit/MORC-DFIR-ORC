#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil


class Dispatcher:

    def __init__ (self,q_dis,q_extrac,q_extrad,q_av,q_hsh,q_hsd,i_dir,w_dir,o_dir,dir_o):
        self.q_dis = q_dis
        self.q_extrac = q_extrac
        self.q_extrad = q_extrad
        self.q_av = q_av
        self.q_hash = q_hsh
        self.q_hashed = q_hsd
        self.in_dir = i_dir
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.dir_ou = dir_o
        self.end = False
        print("== INIT Dispatcher ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP Dispacher ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_dis.qsize() > 0:
                fic_dis = self.q_dis.get()
                _thread.start_new_thread(self.run2,(fic_dis,))
            if self.q_hashed.qsize() > 0:
                fic_hsd = self.q_hashed.get()
                _thread.start_new_thread(self.run3,(fic_hsd,))
            if self.q_extrad.qsize() > 0:
                dir_ext = self.q_extrad.get()
                _thread.start_new_thread(self.run4,(dir_ext,))


    def run2 (self,f):
        # seeker send a file to be hashed
        print("Dispatcher on : " + f)
        self.q_hash.put(f)

    def run3 (self,f):
        # hasher send a file to be extracted
        # MD5 calculated and f.md5 generated at least
        print("Dispatch after hash on : " + f)
        self.q_extrac.put(f)
        # make the directory OUTPUT
        md5f = self.md5_recup(f)
        if not os.path.isdir(self.ou_dir+md5f):
            print("=== Directory OUTPUT ... ===")
            os.mkdir(self.ou_dir+md5f)
            os.mkdir(self.ou_dir+md5f+"/"+f+".dir")
            for d in self.dir_ou:
                os.mkdir(self.ou_dir+md5f+"/"+f+".dir/"+d)
        else:
            print("=== Directory OUTPUT exist ===")

    def run4 (self,d):
        # extractor send the extracting directory to be exploited
        # MD5 calculated and f.md5 generated at least
        # 1st extract done in WORK_DIR/MD5(f)
        print("Dispatch after extract on : " + d)
        # Check AV?
        # Create AV arch
        # Check CSV?
        # Copy and move CSV
        # Check timeline
        # Create timeline

    def md5_recup (self,f):
        # Method to not calculate but extract from the
        # f.md5 in the IN_DIR
        with open(self.in_dir+f+".md5") as hfile:
            f_line = hfile.readline()
            f_other = hfile.read()
            hfile.close()
        return str(f_line.split()[0]).upper()
