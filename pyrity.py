# -*- coding: utf-8 -*-

import logging
from suds import WebFault
from suds.xsd.doctor import Import,  ImportDoctor
from suds.client import Client
from suds.sax.attribute import Attribute
from suds.plugin import MessagePlugin
from suds.sax.text import Raw
from xml.dom.minidom import *

class XML:
    
    def __init__(self):
        self.doc = Document()
        
        
    def createHeader(self,noNameSpaceSchemaLocation,action,objectType,externalSource):
        niku_root = self.doc.createElement("NikuDataBus")   
        niku_root.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
        niku_root.setAttribute('xsi:noNamespaceSchemaLocation',noNameSpaceSchemaLocation)
        niku_header = self.doc.createElement("Header")
        niku_header.setAttribute('version','6.0.11')
        niku_header.setAttribute('action', action)
        niku_header.setAttribute('objectType',objectType)
        niku_header.setAttribute('externalSource',externalSource)
        niku_root.appendChild(niku_header)
        self.doc.appendChild(niku_root)
    
    def __str__(self):
        return self.doc.toxml().replace('<?xml version="1.0" ?>','')
        #return self.doc.toprettyxml().replace('<?xml version="1.0" ?>','')

    def createElement (self,parent,element,arg = []):
        el = self.doc.createElement(element)
        for x in arg:
            el.setAttribute(x[0],x[1])
        pa = self.doc.getElementsByTagName(parent)        
        pa[0].appendChild(el)
    
    def createContent(self,parent,content):
        ct = self.doc.createTextNode(content)
        pa = self.doc.getElementsByTagName(parent)        
        pa[0].appendChild(ct)

class Project():
    
    def __init__(self,projectName):
        self.projectName = projectName
    
    def generateXML(self):
        xml = XML()
        xml.createHeader("../xsd/nikuxog_read.xsd","read","project","NIKU")
        xml.createElement("NikuDataBus","Query")
        xml.createElement("Header","args",[("name","order_by_1"),("value","name")])
        xml.createElement("Header","args",[("name","order_by_2"),("value","projectID")])
        xml.createElement("Header","args",[("name","include_tasks"),("value","true")])
        xml.createElement("Query","Filter",[("name","projectID"),("criteria","EQUALS")])
        xml.createContent("Filter", self.projectName)
        return xml.__str__()
    
    def readProject(self):
        niku = NikuDataBus("http://www-dprojetos/niku/wsdl/Object/Projects","d339954","foobar","Auth") 
        ser = niku.webServiceAuth()
        rp = ser.service.ReadProject(Raw(self.generateXML()))
        tasks = rp.Projects.Project.Tasks.Task
        return tasks
        ser.service.Logout(id)

class NikuDataBus():
    
    def __init__(self,url,login,password,path):
        self.url = url
        self.login = login
        self.password = password
        self.path = path
        
    def webServiceAuth(self):
        client = Client(self.url)

        try:
            id = client.service.Login(self.login, self.password)
            auth = client.factory.create(self.path)
            auth.SessionID = id
            client.set_options(soapheaders=auth)
            return client
        except WebFault, e:
            print e 
      



