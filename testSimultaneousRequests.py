#Copilot was a huge help in writing this code

import xmlrpc.client
import threading
import time



def addNote(topic, name, text):
    serverNotes = xmlrpc.client.ServerProxy("http://127.0.0.1:8000")

    result = serverNotes.editNote(topic, name, text)


    print(result)



def getNotes(topic):
    serverNotes2 = xmlrpc.client.ServerProxy("http://127.0.0.1:8000")
    result = serverNotes2.getNotes(topic)

    print(result)


def searchWiki(term):
    serverWiki = xmlrpc.client.ServerProxy("http://127.0.0.1:8001")
    result = serverWiki.restApiWiki(term)
    
    print(result)





#All threads
threads = []


#This page basically taught me threading and was a huge help: https://pymotw.com/2/threading/
#creating threads to add notes simulatanously
for i in range(3):
    t = threading.Thread(target=addNote, args=("TestTopic", f"Note{i}", f"Content {i}"))
    threads.append(t)


#threads for fetching notes
for i in range(3):
    t = threading.Thread(target=getNotes, args=("TestTopic",))
    threads.append(t)


#threads for wikipedia api search
for term in ["Blockchain", "RPC", "Concurrency"]:
    t = threading.Thread(target=searchWiki, args=(term,))
    threads.append(t)






#had a lot of errors with this, the following page helped: https://stackoverflow.com/questions/75568608/threads-arent-joined-in-multithreading-python
#Launch threads
for t in threads:
    t.start()

for t in threads:
    t.join()




print("\nConcurrency tested!!!!\n")
