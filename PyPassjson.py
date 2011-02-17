#!/usr/bin/python 
# -*- coding: utf-8 -*-

import json

class JsonClass(object):
    """
    """
    
    def generatePasswordList(self):
        jsonstring = {}
        websites = []
        websites.append({
            "name":"sourceforge",
            "user":"sfuser",
            "pass":"sfpass"
        })
        websites.append({
            "name":"fedora",
            "user":"feduser",
            "pass":"fedpass"
        })
        jsonstring['websites'] = websites
        perso = []
        perso.append({
            "name":"server1",
            "user":"sv1user",
            "pass":"sv1pass"
        })
        perso.append({
            "name":"server2",
            "user":"sv2user",
            "pass":"sv2pass"
        })
        jsonstring['pers'] = perso
        print json.dumps(jsonstring,  sort_keys=True, indent=2)
        return jsonstring
    
if __name__ == "__main__":
   jsono = JsonClass()
   jsono.generatePasswordList()
