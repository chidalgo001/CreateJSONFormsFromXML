# -*- coding: utf-8 -*-
# Use this script in order to get the XML form from v4 to convert it a form for v5
# in json format


clr.AddReference("MySql.Data")
from MySql.Data import *
import System;
import System.Reflection;
import xml.etree.ElementTree as ET 
import json
from System.Collections.Generic import Dictionary
from System import String
import threading

myConnectionString = """server=127.0.0.1;
            uid=root;
            pwd=******;
            database=studiocgbis;
            connection timeout=600"""
 
Globals["Skip"] = []

"""
Globals["Skip"] = ["98701","98702",
"98704","98705","98711","98610","98611","98612", "98614","98615","98616","98617",
"96710","96720","96711","96810", "96820","96210","96211","96220","986260","96810","98621","98114","98711",
"95700","98102","98040","98401","98400","96210","95612","96211","98060","96711","95800","95190","98150","96720",
"96820","96710","95610","98061","98041","98181","98183"]
"""

Globals["typeDictionary"] = {
		"ImageField":"grid-file",
		"OptionField":"grid-combo",
		"TextField":"grid-input",
		"Section":"grid-label",
		"NumericField":"grid-input",
		"CheckBoxField":"grid-checkbox",
		"LabelField":"grid-label",
		"TimeField":"grid-input",
		"MultiLine":"grid-datalist",
		
		}
		
Globals["keyTypeDictionary"] = {
		"ImageField":"Image",
		"OptionField":"Text",
		"TextField":"Text",
		"Section":"Text",
		"NumericField":"Int",
		"CheckBoxField":"Bool",
		"LabelField":"Text",
		"TimeField":"Text",
		"MultiLine":"Text",
		}

global number
number = 0

SQL = "'%Studio/8001_Resized'"
LABELNUM = 2.0

def getGraphicBySceneName(SceneName):
	bin = GraphicTemplatesManager.GetAllGraphics()
	
	for g in bin:
		if g.SceneFullName == SceneName:
			return g

def Execute():
	global number
	
	conn = MySqlClient.MySqlConnection();
	try:
		conn.ConnectionString = myConnectionString;
		conn.Open();
		cmd = MySqlClient.MySqlCommand();
		#cmd.CommandText = "SELECT * FROM studiocgbis.templates;";
		#cmd.CommandText = "SELECT * FROM studiocgbis.templates where sceneName like '%/LaLiga%' or sceneName like '%/La_Liga%'";
		cmd.CommandText = "SELECT * FROM studiocgbis.templates where  sceneName like %s;"%SQL; # where ScriptId = '006d6474-68e9-48d9-ac0b-95cdb6cc2399'
		cmd.Connection = conn;
		reader = cmd.ExecuteReader();
	except MySqlClient.MySqlException as ex: 
	    print ex.Message	
	    
	IdsPath = "D:\Todo.txt"
	
	try:
		fileIDs = open(IdsPath, "w")
		pass
	except Exception as e:
		print "ERROR - OpenFiles : %s"%(e)

	total = 0
	try:
		while (reader.Read()):

			print reader[0]
			total = total+1
			fileIDs.write("%s\n"%(reader[0]) )
		print total			
	except Exception as e:
		print "here: " +str(e)
		
	finally:
	
		conn.Close()
		fileIDs.close()
		print "==== Connection and file closed ====\n"
		
#-------------- Iteration of all fiels found end. Closed conn of first MySQL connection ----------				

	errorPath = "D:\Error.txt"
	successPath = "D:\Succes.txt"

	try:
		Globals['fileError'] = open(errorPath, "a")
		Globals['fileSucc'] = open(successPath, "a")
		
	except Exception as e:
		print "ERROR - OpenFiles : %s"%(e)


	fileIDs = open(IdsPath).readlines()
	count = 0
	for line in fileIDs[::1]: 
		ProcessGraphic(line)
		#thread = threading.Thread( target=ProcessGraphic , args=(line,) )
		#thread.start()
		#thread.join()
		print"Thread finished"
		del fileIDs[0]
		
		count = count + 1
		if count >= total:
			break

	fopen = open(IdsPath, 'w')
	fopen.writelines(fileIDs)
	fopen.close()
	Globals['fileError'].close()
	Globals['fileSucc'].close()

	print "DONE"
	
	
def getXML():
	global number
	path = "D:\info.xml" 
	conn = MySqlClient.MySqlConnection();
	try:
		conn.ConnectionString = myConnectionString;
		conn.Open();
		cmd = MySqlClient.MySqlCommand();
		#cmd.CommandText = "SELECT * FROM studiocgbis.templates;";
		#cmd.CommandText = "SELECT * FROM studiocgbis.templates where sceneName like '%/LaLiga%' or sceneName like '%/La_Liga%'";
		cmd.CommandText = "SELECT * FROM studiocgbis.templates where  sceneName like %s;"%SQL; # where ScriptId = '006d6474-68e9-48d9-ac0b-95cdb6cc2399'
		cmd.Connection = conn;
		reader = cmd.ExecuteReader();
	except MySqlClient.MySqlException as ex: 
	    print ex.Message	
	

	total = 0
	file = open(path, "w")				#-- HERE IS WHERE THE XML IS STORED
	try:
		while (reader.Read()):

			print reader[0]
			total = total+1

			#file.write(reader[2].replace("/>","/>\n"))
			file.write(reader[2])

		print total			
	except Exception as e:
		print "Error Getting XML: " +str(e)
		
	finally:
		file.close()
		conn.Close()
		print "==== Connection and file closed ====\n"
	
def ProcessGraphic(id):
	
	myConnectionString = """server=127.0.0.1;
            uid=root;
            pwd=myeZqie1;
            database=studiocgbis;
            connection timeout=600"""
            
	conn = MySqlClient.MySqlConnection();
	path = "D:\info.xml" 
	
	try:
		conn.ConnectionString = myConnectionString;
		conn.Open();
		cmd = MySqlClient.MySqlCommand();
		cmd.CommandText = "SELECT formText, SceneName FROM studiocgbis.templates WHERE ScriptId = '%s';"%(id[:-1]); # WHERE ScriptRef = '97710' where SceneName = 'beIN/Scenes/concept=English/Studio/News/8907_Resized' 'beIN/Scenes/concept=English/Studio/98621'
		cmd.Connection = conn;
		reader = cmd.ExecuteReader();
		
	except MySqlClient.MySqlException as ex:
		print "MySQL error"
		print ex.Message	
	
	while (reader.Read()):
		print reader[1]
		for template in Globals["Skip"]:
			try:
				if reader[1].Contains(template):
					print "GRAPHIC -%s- SKIPPED"%template
					conn.Close()
					print "** CONNECT CLOSE ***"
					return 
			except Exception as E:
				print E
				print "error in skip"
				conn.Close()
				print "** CONNECT CLOSE ***"
				return 
		
		template = "beIN/Scenes/concept=English/Studio/8001_Resized_R2"
		graphic = getGraphicBySceneName(template)
		
		#graphic = getGraphicBySceneName(reader[1])
		
		if graphic:
			try:
				StudioCore.CreateForm(graphic, graphic.Id)
				print "Form for %s was created" %(reader[1])
			except Exception as e:
				print "ERROR - CreateForm : %s"%(e)

			#file = open(path, "w")				#-- HERE IS WHERE THE XML IS STORED
			#file.write(reader[0].replace("/>","/>\n"))
			
			#file.close()
					   	
			dic = []
			item = {}	
			
			try:				
				xmlFile = ET.parse(path)
			
				root = xmlFile.getroot()
			except Exception as e:
				print "ERROR - ParsingXML : %s"%(e)
			
			for child in root:						
				item = __EvaluateChild(child)
				
				if item:
					dic.append( item )
				
			try:
				with open("D:\data_file.json", "w") as write_file:
	   				json.dump(dic, write_file, indent = 3, ensure_ascii=False, encoding='utf8')#--- this file is to view the json output
	   		except:
	   			pass
				
			write_file.close()
			
			try:
				StudioCore.UpdateForm(graphic.Id, json.dumps(dic,ensure_ascii=False,encoding="utf-8") ) #This is supposed to fill in form
				print "Form for %s was updated" %(reader[1])
				Globals['fileSucc'].write("%s\n"%(reader[1]) )
			
			except Exception as e:
				Globals['fileError'].write("%s - %s\n"%(reader[1] , e) )
				print "ERROR: %s"%e
					
		else:
			print "No template found for %s"%reader[1]
			Globals['fileError'].write("%s (%s) - Not Found in Graphics Template Manager\n"%(reader[1],id[:-1] ))
		
	try:
		conn.Close()
		print "** CONNECT CLOSED ***"
	except:
		print "problem closing"
		
	print "finished with %s"%(id)
	


#------- Helper Functions ------------

#-- reads the child and determines to make the section or not. (it wont make a section for childs with empty atributes i.e. <Section title="" /> )
def __EvaluateChild(child):

	#print child.tag
	jsonSection = {}

	if child.tag == "HorizontalStack" and child.getchildren().Count == 0:
		return False
		
	if child.tag == "Section" and child.attrib["title"] != "":
		jsonSection =  __CreateSection(child)
		
	elif child.tag != "Section":
		jsonSection =  __CreateSection(child)
		
	return jsonSection

#----------------------------------------------------------------------------------------------------
#-- this method creates the json section and also adds the items if any
def __CreateSection(child):

	#print "-Created"
	true = True
	false = False
	null = None				
	
	if child.tag == "Multiplier":
		multiplier = child.attrib["range"]
	else:
		multiplier = ""
	
	item =  {
		"gridColumns": 12,
		"tableMode": false,
		"selected": true,
		"items":__CreateItems(child),
	    "multiplier": multiplier,
	    "visibility": true,
	    "label": null
	 }
	
	return item

#----------------------------------------------------------------------------------------------------
#-- this function creates the items according to the section. "Horizontal" child will have 1 or more items, where section will only have 1.
#-- this is also where we map the properties from v4 to v5
def __CreateItems(child):
	
	global number
	
	true = True
	false = False
	null = None		
	lst = []
	x = 0
	
	#-- START OF MULTIPLIER CHILD NODE -- 
	if child.tag == "Multiplier":
	
		y = 0 
		for grand in child:

			if grand.tag == "HorizontalStack":	
				
				x = 0
				
				if grand.getchildren().Count > 0:
					size = 12.0 / float(grand.getchildren().Count - grand.findall("Section").Count ) 
				else:
					size = 12
				
				for greatgrand in grand:
				
					#print "	|-- %s"%greatgrand.tag
					
					options = ''
					
					#-- This is the only one that has options
					if greatgrand.tag == "OptionField": 
						provider = CreateProvider(greatgrand.attrib["options"] , greatgrand.attrib["label"])#-- params: the option string, and the name. In this case the labe (for now)
					else:
						provider = ""
					
					if "basePath" in greatgrand.attrib:
						path = greatgrand.attrib["basePath"][15:]
					else:
						path =""
					
					if "fileExtensions" in greatgrand.attrib:
						fileExt = greatgrand.attrib["fileExtensions"]
						fileExt = fileExt.replace(".","*.")
					else:
						fileExt = ""

					if "defaultValue" in greatgrand.attrib:
						try:
							default = greatgrand.attrib["defaultValue"] 
						except:
							default = ""
					else:
						default =""
						
					#print path
					if greatgrand.tag != "Section":
					
						item = {
								"extensions": fileExt,
							    "moved": false,
							    "labelOnTop": false,
							    "lockControl": false,
							    "parameterControl": false,
							    "visibilityControl": true,
							    "autoTemplate": false,
							    "templateRunner": "Server",
							    "dataTemplate": "" ,
							    "path": path,
							    "provider": provider,
							    "options": [],
							    "type": Globals["typeDictionary"][greatgrand.tag],
							    "h": 1,
							    "w": size,
							    "y": y,
							    "x": x,
							    "keyType":Globals["keyTypeDictionary"][greatgrand.tag],
							    "key": greatgrand.attrib["tag"].replace("#","{{id}}"),
							    "label": greatgrand.attrib["label"].replace("#","{{id}}").strip(),
							    "labelWidth": "155",
							    "widget":  Globals["typeDictionary"][greatgrand.tag],
							    "selected": true,
							    "i": "item_%s"%( str(number).zfill(4) ),
							    "default": default
							 }
					
				
						lst.append( item )
						number = number + 1	
						x = x + size #-- Will keep the spaces according to the size ( size = 12 / child.getchildren().Count )
					
				y = y + 1
				
			else:
				options = ''
				
				#print "|--xx %s"%grand.tag
				#-- This is the only one that has options
				if grand.tag == "OptionField": 
					provider = CreateProvider(grand.attrib["options"] , grand.attrib["label"])#-- params: the option string, and the name. In this case the labe (for now)
				else:
					provider = ""
				
				if "basePath" in grand.attrib:
					path = grand.attrib["basePath"][15:]
				else:
					path =""
				#print path[15:]
				if "fileExtensions" in grand.attrib:
					fileExt = grand.attrib["fileExtensions"]
					fileExt = fileExt.replace(".","*.")
				else:
					fileExt = ""


				if "defaultValue" in grand.attrib:
					try:
						default = grand.attrib["defaultValue"] 
					except:
						default = ""
				else:
					default =""
				
				if grand.tag != "Section":
					item = {
							"extensions": fileExt,
						    "moved": false,
						    "labelOnTop": false,
						    "lockControl": false,
						    "parameterControl": false,
						    "visibilityControl": true,
						    "autoTemplate": false,
						    "templateRunner": "Server",
						    "dataTemplate": "",
						    "path": path,
						    "provider": provider,
						    "options": [],
						    "type": Globals["typeDictionary"][grand.tag],
						    "h": 1,
						    "w": 12,
						    "y": 0,
						    "x": 0,
						    "keyType": Globals["keyTypeDictionary"][grand.tag],
						    "key": grand.attrib["tag"].replace("#","{{id}}"),
						    "label": grand.attrib["label"].replace("#","{{id}}").strip(),
						    "labelWidth": "155",
						    "widget":  Globals["typeDictionary"][grand.tag],
						    "selected": true,
						    "i": "item_%s"%( str(number).zfill(4) ),
						    "default": default
						 }
						 
					
					lst.append( item )
					number = number + 1	
					
	#-- START OF HORIZONTALSTACK CHILD NODE --
	elif child.tag == "HorizontalStack": 
		y = 0
		x = 0
	 	childCount = child.getchildren().Count - child.findall("Section").Count
	 	
	 	if childCount > 0:
	 		if childCount > ( int(LABELNUM) - 1 ):
	 			size = 12.0 / LABELNUM
	 			
	 		else:
				size = 12.0 / float(childCount) 
		else:
			size = 12
			
		for grand in child:
		
			#print "|-- %s"%grand.tag

			if grand.tag == "LabelField":
				try:
					key= grand.attrib["label"].strip()
					label = grand.attrib["label"].strip()
				except:
					key= ""
					label = ""			
			else:
			
				try:
					key = grand.attrib["title"]
					label = grand.attrib["title"].strip()
				except:
					key = grand.attrib["tag"]
					label = grand.attrib["label"].strip()

			
			#-- This is the only one that has options
			if grand.tag == "OptionField": 
				provider = CreateProvider(grand.attrib["options"] , grand.attrib["label"])#-- params: the option string, and the name. In this case the labe (for now)
				#print provider	
			else:
				provider = ""
			
			if "basePath" in grand.attrib:
				path = grand.attrib["basePath"][15:]
			else:
				path =""
		#	print path[15:]	
			if "defaultValue" in grand.attrib:
				try:
					default = grand.attrib["defaultValue"]
				except:
					default = ""
				
			else:
				default =""
			#print default	
			if "fileExtensions" in grand.attrib:
				fileExt = grand.attrib["fileExtensions"]
				fileExt = fileExt.replace(".","*.")
			else:
				fileExt = ""
			
			if grand.tag != "Section":
				
				item = {
						"extensions": fileExt,
					    "moved": false,
					    "labelOnTop": false,
					    "lockControl": false,
					    "parameterControl": false,
					    "visibilityControl": true,
					    "autoTemplate": true,
					    "templateRunner": "Server",
					    "dataTemplate": "",
					    "path": path,
					    "provider": provider,
					    "options": [],
					    "type": Globals["typeDictionary"][grand.tag],
					    "h": 1,
					    "w": size,
					    "y": y,
					    "x": x,
					    "keyType":Globals["keyTypeDictionary"][grand.tag],
					    "key": key,
					    "label": label,
					    "labelWidth": "155",
					    "widget":  Globals["typeDictionary"][grand.tag],
					    "selected": true,
					    "i": "item_%s"%( str(number).zfill(4) ),
					    "default": default
					 }
		
				lst.append( item )
				#print "%s - %s : %s"%(x,y,label)
				number = number + 1	
				x = x + size #-- Will keep the spaces according to the size ( size = 12 / child.getchildren().Count )
				if x >= 12:
					y = y + 1
					x = 0
				
	#-- START THE REMAINING CHILD NODE --		
	else:
		
		if child.tag == "LabelField":
			try:
				key= child.attrib["label"].strip()
				label = child.attrib["label"].strip()
			except:
				key= ""
				label = ""			
		else:
			try:
				key = child.attrib["title"]
				label = child.attrib["title"].strip()
			except:
				key = child.attrib["tag"]
				label = child.attrib["label"].strip()
		
		
		if child.tag == "OptionField": 
			provider = CreateProvider(child.attrib["options"] , child.attrib["label"])
		else:
			provider = ""
			
		if "basePath" in child.attrib:
			path = child.attrib["basePath"][15:]
		else:
			path =""
		#print path[15:]
		if "defaultValue" in child.attrib:
			try:
				default = child.attrib["defaultValue"] 
			except:
				default = ""
		else:
			default =""

		if "fileExtensions" in child.attrib:
			fileExt = child.attrib["fileExtensions"]
			fileExt = fileExt.replace(".","*.")
		else:
			fileExt = ""
		
		
		item = {
				"extensions": fileExt,
			    "moved": false,
			    "labelOnTop": false,
			    "lockControl": false,
			    "parameterControl": false,
			    "visibilityControl": true,
			    "autoTemplate": false,
			    "templateRunner": "Server",
			    "dataTemplate": "",
			    "path": path,
			    "provider": provider,
			    "options": [],
			    "type": Globals["typeDictionary"][child.tag],
			    "h": 1,
			    "w": 12,
			    "y": 0,
			    "x": 0,
			    "keyType": Globals["keyTypeDictionary"][child.tag],
			    "key": key,
			    "label": label,
			    "labelWidth": "155",
			    "widget": Globals["typeDictionary"][child.tag],
			    "selected": true,
			    "i": "item_%s"%( str(number).zfill(4) ),
			    "default": default
			 }
			 
		lst.append( item )
			
		number = number + 1	
	
	return lst

#----------------------------------------------------------------------------------------------------	
#-- Here, a provider is created if there is an "OptionField" on the xml. For now, we are using the label as a name for the provider until a better approach is found.
def CreateProvider(options , name):
	
	from System.Collections.Generic import Dictionary
	#print options # in essence it will be the key
	
	providerName = filter(str.isalnum, name)#-- this will remove all spaces and special chars
	#print providerName[:-1]
	
	if options not in Globals["Providers"]:
		
		if providerName in StudioCore.GetProviders(Project.Name):
			repeated = True
			count = 00
			while repeated:
				print "the name is repeated"
				providerName = providerName[:-1] + str(count)
				
				count = count + 1
				repeated = providerName in StudioCore.GetProviders(Project.Name)			
		
		Globals["Providers"][options] = providerName #-- name is the value, that will be the provider name
		print "Not in Dic, provider created.\n Name: %s -- Options: %s"%(providerName, options)
	
	Globals["PS"] = Globals["Providers"]
	
	providerName = Globals["Providers"][options]
		
	total = options.split(",")#--stores that many options separate
	
	dict = Dictionary[str, str]()
	
	for option in total:
		
		tokens = option.split(":")
		key = tokens[1]
		value = tokens[0]	
		
		try:
			if key not in dict:
				dict.Add(key,value) 
		except Excepton as e:			
			print "Error in prov: %s"%e
			
	try:

		StudioCore.InsertOrUpdateProvider(Project.Name, providerName, dict)
		print providerName + " Added to item as provider\n"
	except Exception as e:
		pass
		#print "error in insert prov: %s"%e
	
	return 	providerName		
	
#==================== TESTS ====================	
	
#==============================================================================================================================	
def test():
	dict = Dictionary[str, str]()
	
	
	for key in Globals["Providers"]:
		print "%s - %s"%(Globals["Providers"][key] , key) 
	print "executed"
	return


#from System.Collections.Generic import Dictionary as Dict

def count():
	count = 0
	total = 0
	for folder in GraphicTemplatesManager.Folders:
		
		for i in folder.Graphics:
			count = count+1
		print "%s - %s"%(folder.Name, count)
		
		if not folder.Name == "Orphans": 
			total = total + count
			
		count = 0
	
	print "Total - " + str(total) + " (Not counting Orphans)"


def GlobalsDic():
	for a in Globals["Providers"]:
		print a

def Compare():
	for provider in StudioCore.GetProviders(Project.Name):
		
		if not provider in Globals["Providers"].values():
			print provider
			print "NOT FOUND!!!"
			
	print "THESE ARE THE PROVIDERS NOT ADDDED TO THE DICT"



def DeleteProvidersGlobal():
	Globals["Providers"] = {}
	
	
	
def RestoreDictionary():

	for provider in StudioCore.GetProviders(Project.Name):
	
		string = StudioCore.GetProvider(Project.Name, provider)
	
		s = string.replace("{" ,"").replace("\n","").replace("\r","")
		finalstring = s.replace("}" , "")
		
		list = finalstring.split(",")
	
		line=""
		
		for i in list:
		    #Get Key Value pairs separately to store in dictionary
		    keyvalue = i.split(":")
			
		    #Replacing the single quotes in the leading.
		    m= keyvalue[0].strip('\'')
		    m = m.replace("\"", "")
		    line = keyvalue[1][1:].strip('"\'') + ":" +m[2:].strip('"\'')+ "," + line 
		 
		try:
			Globals["Providers"][line.replace('"','')[:-1]] = provider
		except:
			print "Failed!!"
			
			
		print line.replace('"','')[:-1] + " - "+ provider
	
	return


	
	
