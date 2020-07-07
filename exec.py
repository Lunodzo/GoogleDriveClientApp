from __future__ import print_function #Necessary if you are working in Python2 or older
import pickle
import os.path 
#import io
import gi

gi.require_version('Pango', '1.0')
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib import flow
from google.protobuf import service

#GTK import
gi.require_version('Gtk', '3.0')
from gi.repository import GObject
from gi.repository import Pango
from gi.repository import Gtk

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

# We import the Gtk module. The require_version() method ensures the namespace 
# gets loaded with the given version. 
# 
# The gi.repository is the Python module 
# for PyGObject. PyGObject (Python GObject introspection) contains Python bindings 
# and support for gobject, glib, gtk and other Gnome libraries.

#To succesful run your program, install pyGobject package using any package installer.
#Have you tried jhbuild

class main():
    def __init__(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the files the user has access to.
        The Upload, download and create files on the drive
        """

        self.builder = Gtk.Builder()
        self.builder.add_from_file("google_client.glade")
        self.builder.connect_signals(self)
        window = self.builder.get_object("global_window")

        #self.bashrcpath = os.path.expanduser('~') + "/" + ".bashrc"
        cwd_dir = os.getcwd()
        self.filepath = os.listdir(path='.')
        self.treeview = self.builder.get_object("treeview")
        self.store = Gtk.ListStore(str, str)

        #self.loadPaths()
        
        window.connect("destroy", Gtk.main_quit)
        
        window.show_all()
        Gtk.main()


        #Drive API AUTHENTICATION
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        #To clear login cache, just delete the file, and on the next execution you will
        #be required to authenticate again (Allow access to Google Drive)

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, require the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds) #We are using V3 API

        # the label we use to show the selection
        label = Gtk.Label()
        label.set_text("")

        #Trying handlers approach
        handlers = {
            "on_list_clicked": listFiles(10),
            "on_men_destroy": Gtk.main_quit
        }

        
        #Listing files
        def listFiles(size):
            results = service.files().list(
                pageSize= size, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            #Check if there exists files to be loaded
            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print(u'{0} ({1})'.format(item['name'], item['id'])) #List the files
        #listFiles(10)

        #Uploading files (from local directory)
        def uploadFile(filename,filepath,mimetype):
            file_metadata = {'name': filename}
            media = MediaFileUpload(filepath,
                                    mimetype=mimetype)
            file = service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields='id').execute()
            print('File ID: %s' % file.get('id'))
            
        uploadFile('google.jpg', 'google.jpg', 'image/jpeg')


        #Downloading files (We dont do this now)
        def downloadFile(file_id,filepath):
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))
            with io.open(filepath,'wb') as f:
                fh.seek(0)
                f.write(fh.read())

        #Creating a folder
        def createFolder(name):
            file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
            }
            file = service.files().create(body=file_metadata,
        fields='id').execute()
            print ('Folder ID: %s' % file.get('id'))
        #createFolder("Lunodzo")

        #Search query (Within directory)
        def searchFile(size,query):
            results = service.files().list(
            pageSize=size,fields="nextPageToken, files(id, name, kind, mimeType)",q=query).execute()
            items = results.get('files', [])
            if not items:
                print('No files found.')
            else:
                print('Files:')
                for item in items:
                    print(item)
                    print('{0} ({1})'.format(item['name'], item['id']))
        #searchFile(10,"name contains 'Getting'")


if __name__ == '__main__':
    main()   
      
    def loadPaths(self):
        pathsStr = os.getenv("PATH")   
        paths = pathsStr.split(":")     

        for path in paths:
            self.store.append([path])

        renderer = Gtk.CellRendererText()
        pathColumn = Gtk.TreeViewColumn(title="Paths", cell_renderer = renderer, text = 0)
        self.treeview.append_column(pathColumn)
        self.treeview.set_model(self.store)
    
    #Function calling
    #uploadFile('icon.png','icon.png','image/png')
    #downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')
    #createFolder('Google')
    #searchFile(10,"name contains 'Getting'")
    #listFiles(100)


        # def on_upload_clicked(self, button):
        #     print("Uploading files")
        #     #uploadFile('icon.png','icon.png','image/png')

        # def on_download_clicked(self, button):
        #     print("Downloading files")
        #     #downloadFile('1Knxs5kRAMnoH5fivGeNsdrj_SIgLiqzV','google.jpg')

        # def on_list_clicked(self, button):
        #     label = Gtk.Label(label="Hello World", angle=25, halign=Gtk.Align.END)
        #     print("List files")
        #     listFiles(100)
        #uploadFile('icon.png','icon.png','image/png')    
main()


    



