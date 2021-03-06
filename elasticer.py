#!/usr/bin/python3.5
# coding=utf-8

import os
import magic
import subprocess
import queue
import time
import _thread
import shutil
from evtx2es import evtx2es
from evtx2es import evtx2json


class Elasticer:

    def __init__ (self,q_in,w_dir,o_dir):
        self.q_inp = q_in
        self.wk_dir = w_dir
        self.ou_dir = o_dir
        self.end = False
        print("== INIT Elasticer ==")

    def start (self):
        _thread.start_new_thread(self.run,())

    def stop (self):
        print("## STOP Elasticer ##")
        self.end = True

    def run (self):
        while not self.end:
            if self.q_inp.qsize() > 0:
                pfic_es = self.q_inp.get()
                _thread.start_new_thread(self.run2,(pfic_es,))

    def run2 (self,pf):
        # Copy from WORKSPACE to OUTPUT/AVCheck
        print("Elasticer on : " + pf)
        
        md5dfir = self.get_md5(pf)
        filename = pf.split("/")[-1]
        
        newfilename = filename + ".json"
 
        with open(self.ou_dir+md5dfir+"/CSV_Splunk/"+newfilename, "w", encoding='utf-8') as outjson:
           result: List[dict] = evtx2json(pf)
           outjson.write(result)
        outjson.close() 
        
        evtx2es(pf, host="192.168.1.12", port=9200, index="MORC_evtx")


    def get_filename (self,pf):
        # Method to get the filename from a pathfile
        return pf.split("/")[-1]

    def get_md5 (self,pf):
        # Method to get the DFIR MD5 from a pathfile
        tpath = pf.split("/")
        for d in tpath:
            if len(d) == 32:
                return d
        return ""
