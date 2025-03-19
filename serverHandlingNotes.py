#Necessary imports (For conveinience I used same variable names and "as" shortages in imports as in the library documentations).
import xml.etree.ElementTree as ET
import datetime

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler



import requests
import os
import time

#Threading
from socketserver import ThreadingMixIn
import threading
xml_lock = threading.Lock()


# Globally declared XML Database File
xmlDATABASE = "notes.xml"



#Database initialization
def databaseINITIALIZATION():

    #Building XML documents learned here: https://docs.python.org/3/library/xml.etree.elementtree.html

    if not os.path.exists(xmlDATABASE):
        root = ET.Element("data")

        tree = ET.ElementTree(root)
        tree.write(xmlDATABASE)



# Saving note to XML (Includes Name Attribute)
def editNote(topic, name, text):

    #Basic datetime limbrary usage and implementation
    timestamp = datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S")


    with xml_lock:

        #Parsing XML, this step explained in a very similar way here: https://docs.python.org/3/library/xml.etree.elementtree.html
        tree = ET.parse(xmlDATABASE)
        root = tree.getroot()


        # After getting topic name from user, wither finding existing topic with given name or making a new one.
        topicVerification = root.find(f"./topic[@name='{topic}']")


        if topicVerification is None:
            topicVerification = ET.SubElement(root, "topic", name=topic)

        # Create note with name attribute
        noteSubelement = ET.SubElement(topicVerification, "note", name=name)
        ET.SubElement(noteSubelement, "text").text = text
        ET.SubElement(noteSubelement, "timestamp").text = timestamp


        tree.write(xmlDATABASE)

    #Sending success message to client
    return f"\nNote '{name}' saved under topic '{topic}' at {timestamp}."



#Printing out notes by the given note topic attribute
def getNotes(topic):
    with xml_lock:
        tree = ET.parse(xmlDATABASE)
        root = tree.getroot()


        topicSubelement = root.find(f"./topic[@name='{topic}']")

        #Handling the case of user inputting a topic that doesn't exist.
        if topicSubelement is None:

            return "Oups! No notes found for this topic."
        


        notesTemporaryVar = []

        for i in topicSubelement.findall("note"): 

            if "name" in i.attrib:  
                nameTemp = i.get("name") 


            else:  
                nameTemp = "Note with no name"


            text = i.find("text").text
            timestamp = i.find("timestamp").text

            notesTemporaryVar.append(f"{nameTemp} [{timestamp}]: {text}")


    return "\n".join(notesTemporaryVar)




class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass





# Start XML-RPC Server
def launchServer():
    server = ThreadedXMLRPCServer(("127.0.0.1", 8000), requestHandler=SimpleXMLRPCRequestHandler, allow_none=True)


    server.register_function(editNote, "editNote")
    server.register_function(getNotes, "getNotes")

    print("Server started on 127.0.0.1:8000")
    server.serve_forever()


# Initialize XML storage
databaseINITIALIZATION()



# Run the server
if __name__ == "__main__":
    launchServer()
