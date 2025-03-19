import xmlrpc.client

# Connecting to the XML-RPC servers
serverHandlingNotes = xmlrpc.client.ServerProxy("http://127.0.0.1:8000")
serverHandlingWiki = xmlrpc.client.ServerProxy("http://127.0.0.1:8001")


#Main menu
if __name__ == "__main__":
    print("\nGreetings! Welcome to the notebook app!\n")

    while True:
        print("\nSelect an option to proceed:")

        print("1. Make Note")
        print("2. Fetch Notes")
        print("3. Search in Wikipedia")

        print("4. Exit the application")

        userChoice = input("\nEnter choice: ")

        if userChoice == "1":

            topic = input("Enter topic: ")

            name = input("Enter note name: ")

            text = input("Enter note text: ")
            try:
                print(serverHandlingNotes.editNote(topic, name, text))
            except Exception as e:
                print("\nServer responsible for Note operations is offline.")

        elif userChoice == "2":

            topic = input("\nEnter topic: ")

            try:
                print("\nNotes:\n" + serverHandlingNotes.getNotes(topic))
            except Exception as e:
                print("\nServer responsible for Note operations is offline.")

        elif userChoice == "3":

            topic = input("Enter search term for Wikipedia: ")
            
            try:
                fetchedData = serverHandlingWiki.restApiWiki(topic)
                print("\nWikipedia Summary:\n" + fetchedData)
            except Exception as e:
                print("\nResponsible server for Wikipedia operations is offline.")
                continue

            #y/n handling looke up here: https://stackabuse.com/bytes/handling-yes-no-user-input-in-python/#
            addingDataOption = input("Add this data to a topic in the notebook? (Y/n): ")

            if addingDataOption.strip().lower() in ["y", "yes"]:
                topic2 = input("Enter topic name in the notebook: ")
                nameOfNote = input("Enter note name where Wiki data will be appended: ")

                print(serverHandlingNotes.editNote(topic2, nameOfNote, fetchedData))
            
            else:
                print("\nFetched data was not added to the notebook.\n")

        elif userChoice == "4":

            print("Application closed. Thanks for using the notebook!")

            break


#Main menu error handling
        else:
            print("Invalid choice, try again.")
