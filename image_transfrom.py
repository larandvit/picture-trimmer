"""
    Description: The tool can be used to reduce image size for publishing them to Web. 
                 It's useful to create galleries of pictures when there are square 
                 pictures of smaller sizes.
"""

__author__ = "Vitaly Saversky"
__date__ = "2018-11-24"
__credits__ = ["Vitaly Saversky"]
__version__ = "2.0.0"
__maintainer__ = "Vitaly Saversky"
__email__ = "larandvit@hotmail.com"
__status__ = "Production"

import os
from os import path
import sys
import argparse
from argparse import RawTextHelpFormatter
import traceback

from PIL import Image

from enum import IntEnum

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class ProcessingMode(IntEnum):
    Cli = 1
    Gui = 2

FILE_EXTENSIONS = ('.jpg', '.bmp', '.png', '.gif')
PICTURE_SIZE_MIN = 2
PICTURE_SIZE_MAX = 12000

class ReturnCode(IntEnum):
    Success = 0
    SourceFolderNotExist = 1
    NoPictureFiles = 2
    DesiredSizeOutOfBound = 3
    SourceFolderEmpty = 4
    ReadyFolderEmpty = 5
    Unexpected = 255

RETURNCODES = {"Success" : ReturnCode.Success.value,
               "Source folder not exist" :ReturnCode.SourceFolderNotExist.value,
               "No picture files found" : ReturnCode.NoPictureFiles.value,
               "Desired size out of bound"  : ReturnCode.DesiredSizeOutOfBound.value,
               "Source folder empty"  : ReturnCode.SourceFolderEmpty.value,
               "Ready folder empty" : ReturnCode.ReadyFolderEmpty.value,
               "Unexpected" : ReturnCode.Unexpected.value
    }

class Processing:
    def __init__(self, sourceFolder, readyFolder, desiredSize):
        self.sourceFolder = sourceFolder
        self.readyFolder = readyFolder
        self.desiredSize = desiredSize
        
        self.errorMessage = ''
        self.errorCode = ReturnCode.Success
        
    def buildPictureList(self):
        
        self.errorCode = ReturnCode.Success
        
        if self.sourceFolder=='':
            self.errorCode = ReturnCode.SourceFolderEmpty
            self.errorMessage = 'Source folder is empty'
        else:
            if self.readyFolder=='':
                self.errorCode = ReturnCode.ReadyFolderEmpty
                self.errorMessage = 'Ready folder is empty'
            else:
                if path.exists(self.sourceFolder):
        
                    if self.desiredSize<PICTURE_SIZE_MIN or self.desiredSize>PICTURE_SIZE_MAX:
                        self.errorCode = ReturnCode.DesiredSizeOutOfBound
                        self.errorMessage = 'Desired picture size has to be between {} and {}'.format(PICTURE_SIZE_MIN, PICTURE_SIZE_MAX)
                    else:
                        self.originalFiles =  []
                        for sourceFile in os.listdir(self.sourceFolder):
                            if sourceFile.lower().endswith(FILE_EXTENSIONS):
                                self.originalFiles.append(sourceFile)
                        
                        if len(self.originalFiles)<1:
                            self.errorMessage = 'No picture files have been found in "{}" folder'.format(self.sourceFolder)
                            self.errorCode = ReturnCode.NoPictureFiles
                else:
                    self.errorMessage = '"{}" folder does not exist'.format(self.sourceFolder)
                    self.errorCode = ReturnCode.SourceFolderNotExist
                
        return (self.errorCode, self.errorMessage)
                
    def run(self):
        
        self.errorCode = ReturnCode.Success
        
        fileIndex = 0
        filesCount = len(self.originalFiles)
        
        for sourceFile in self.originalFiles:
            fileIndex +=1
            
            sourceFilePath = path.join(self.sourceFolder, sourceFile)
            sourceBareFileName = path.splitext(sourceFile)[0]
            
            outputFilePath = path.join(self.readyFolder, sourceBareFileName + '.jpg')
            
            if not path.exists(self.readyFolder):
                os.mkdir(self.readyFolder)
            
            im = Image.open(sourceFilePath)
     
            old_size = im.size
            ratio = float(self.desiredSize)/max(old_size)
            new_size = tuple([int(x*ratio) for x in old_size])
            im = im.resize(new_size, Image.ANTIALIAS)
            new_im = Image.new("RGB", (self.desiredSize, self.desiredSize), (255,255,255))
            new_im.paste(im, ((self.desiredSize - new_size[0])//2, (self.desiredSize  -new_size[1])//2))
            
            if path.exists(outputFilePath):
                os.remove(outputFilePath)
            
            new_im.save(outputFilePath)
            
            outputFileSize = path.getsize(outputFilePath)/1024
            
            message = 'Processed {} out of {}: {}. Size: {:.2f} KB'.format(fileIndex, filesCount, sourceFile, outputFileSize)
             
            yield (sourceFile, message)
            

class CliProcessing:
    def __init__(self):

        exitCodesText = ''
        for text, code in zip(RETURNCODES,RETURNCODES.values()):
            exitCodesText += "\n" + str(code) + " - " + text
        
        appArgs = argparse.ArgumentParser(description='Reduce size of pictures for publishing them to web', 
                                          epilog=exitCodesText,
                                          formatter_class=RawTextHelpFormatter)
        
        appArgs.add_argument("--sourcefolder", nargs=1, required=True, help="Input folder with pictures", metavar='"source folder"')
        appArgs.add_argument("--desiredsize", nargs=1, required=True, help="Output image size", metavar='"desired size"')

        args = appArgs.parse_args()

        self.sourceFolder = args.sourcefolder[0]
        self.desiredSize = int(args.desiredsize[0])
        
        self.errorMessage = ''
        self.errorCode = ReturnCode.Success
        
    def run(self):
        
        returnCode = 1
        
        try:
            self.errorCode = ReturnCode.Success
            
            self.readyFolder = path.join(self.sourceFolder, 'Ready')
            processing = Processing(self.sourceFolder, self.readyFolder, self.desiredSize)
            
            self.errorCode, self.errorMessage = processing.buildPictureList()
            
            if self.errorCode==ReturnCode.Success:
                for _, message in processing.run():
                    print(message)

        except Exception as err:
            self.errorMessage = 'Unexpected error: {}'.format(err)
            self.errorCode = ReturnCode.Unexpected
        
        finally:
            if self.errorCode==ReturnCode.Success:
                print("Pictures have been processed successfully")
            else:
                print(self.errorMessage)
                print('Picture processing has failed')
                
        return returnCode

class GuiProcessing(ttk.Frame):
    def __init__(self, master=None):
        
        self.sourceFolderValue = tk.StringVar()
        self.readyFolderValue = tk.StringVar()
        self.desiredSizeValue = tk.StringVar()
        
        self.processValue = tk.StringVar()
        
        super().__init__(master)
        master.title('Picture Trimmer v.{}'.format(__version__))
        # master.iconbitmap(path.join(appFolder(),"images","app.ico"))
        master.minsize(width=500, height=170)
        
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        
        # position app window in center of screen
        windowWidth = root.winfo_reqwidth()
        windowHeight = root.winfo_reqheight()
         
        positionRight = int(root.winfo_screenwidth()/2.5 - windowWidth/2)
        positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
         
        master.geometry("+{}+{}".format(positionRight, positionDown))
        
        self.createWidgets()
        
        self.desiredSizeValue.set(640)
        
        self.processValue.set('Ready')
        
        self.errorMessage = ''
        self.errorCode = ReturnCode.Success
        
    def createWidgets(self):
        
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        self.frameMain = ttk.Frame(self)
        self.frameMain.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.frameMain.columnconfigure(0, weight=1)
        self.frameMain.rowconfigure(0, weight=1)
        self.frameMain.rowconfigure(1, pad=15)
        
        self.frameTop = ttk.Frame(self.frameMain, padding=5)
        self.frameTop.grid(column=0, row=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.frameTop.columnconfigure(1, weight=1)
        self.frameTop.rowconfigure(3, weight=1)
        
        self.labelSourceFolder = ttk.Label(self.frameTop, text="Source Folder:")
        self.labelSourceFolder.grid(column=0, row=0, sticky=tk.W, pady=2)
        self.entrySourceFolder = ttk.Entry(self.frameTop, textvariable=self.sourceFolderValue)
        self.entrySourceFolder.grid(column=1, row=0, sticky=tk.E+tk.W, pady=2)
        self.buttonSourceFolder = ttk.Button(self.frameTop, text="...",  width="3", command=self.eventSourceFolderClicked)
        self.buttonSourceFolder.grid(column=2, row=0, pady=2)
        
        self.labelReadyFolder = ttk.Label(self.frameTop, text="Ready Folder:")
        self.labelReadyFolder.grid(column=0, row=1, sticky=tk.W, pady=2)
        self.entryReadyFolder = ttk.Entry(self.frameTop, textvariable=self.readyFolderValue)
        self.entryReadyFolder.grid(column=1, row=1, sticky=tk.E+tk.W, pady=2)
        self.buttonReadyFolder = ttk.Button(self.frameTop, text="...",  width="3", command=self.eventReadyFolderClicked)
        self.buttonReadyFolder.grid(column=2, row=1, pady=2)
        
        self.labelDesiredSize = ttk.Label(self.frameTop, text="Desired Size:")
        self.labelDesiredSize.grid(column=0, row=2, sticky=tk.W, pady=2)
        self.spinboxDesiredSize = tk.Spinbox(self.frameTop, textvariable=self.desiredSizeValue, from_=PICTURE_SIZE_MIN, to=PICTURE_SIZE_MAX, width=6)
        self.spinboxDesiredSize.grid(column=1, row=2, sticky=tk.W, pady=2)
        
        self.frameSeparator = ttk.Frame(self.frameMain, padding=5)
        self.frameSeparator.grid(column=0, row=2, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.frameSeparator.columnconfigure(0, weight=1)
        
        self.separatorBottom = ttk.Separator(self.frameSeparator, orient=tk.HORIZONTAL)
        self.separatorBottom.grid(column=0, row=0, sticky=tk.W+tk.E)
        
        self.frameBotom = ttk.Frame(self.frameMain, padding=5)
        self.frameBotom.grid(column=0, row=3, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.frameBotom.columnconfigure(0, weight=1)
        
        self.buttonProceed = ttk.Button(self.frameBotom, text='Proceed', command=self.eventProceedClicked)
        self.buttonProceed.grid(column=0, row=0, sticky=tk.E)
        self.buttonClose = ttk.Button(self.frameBotom, text='Close', command=self.quit)
        self.buttonClose.grid(column=1, row=0, sticky=tk.E)
        
        self.frameProgress = ttk.Frame(self.frameMain, padding=3)
        self.frameProgress.grid(column=0, row=4, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.frameProgress.columnconfigure(0, weight=1)
        
        self.labelProgress = ttk.Label(self.frameProgress, borderwidth=1, relief=tk.SUNKEN, textvariable=self.processValue)
        self.labelProgress.grid(column=0, row=0, sticky=tk.E+tk.W)
        
        self.update()
        
    def eventSourceFolderClicked(self):
        folderName = filedialog.askdirectory(title="Select source folder", parent=self.winfo_toplevel())
        folderName = os.path.normpath(folderName)
        self.sourceFolderValue.set(folderName)
        
        if self.readyFolderValue.get()=='':
            readyFolder = path.join(folderName, 'Ready')
            self.readyFolderValue.set(readyFolder)
            
    def eventReadyFolderClicked(self):
        folderName = filedialog.askdirectory(title="Select ready folder", parent=self.winfo_toplevel())
        folderName = os.path.normpath(folderName)
        self.readyFolderValue.set(folderName)
        
    def eventProceedClicked(self):
        
        try:
            self.errorCode = ReturnCode.Success
            
            self.processValue.set('Processing..')
            self.update()
            
            self.buttonProceed.config(state="disabled")
        
            processing = Processing(self.sourceFolderValue.get(), self.readyFolderValue.get(), int(self.desiredSizeValue.get()))
            
            self.errorCode, self.errorMessage = processing.buildPictureList()
            
            if self.errorCode==ReturnCode.Success:
                for _, message in processing.run():
                    self.printProgress(message)
            
        except Exception as err:
            self.errorMessage = 'Unexpected error: {}'.format(err)
            self.errorCode = ReturnCode.Unexpected
            
        finally:
            self.buttonProceed.config(state="normal")
            
            if self.errorCode==ReturnCode.Success:
                message = "Pictures have been processed successfully"
                messagebox.showinfo("Info", message)
            else:
                message = 'Picture processing has failed'
                messagebox.showerror('Error', self.errorMessage)
                
            self.printProgress(message)
    
    def printProgress(self, message):
        self.processValue.set(message)
        self.update()
                    
if __name__=="__main__":
    
    returnCode = ReturnCode.Success
    
    try:
        
        processingMode = ProcessingMode.Cli
        
        if len(sys.argv)<=1:
            # if no parameters, show GUI
            processingMode = ProcessingMode.Gui
            root = tk.Tk()
            app = GuiProcessing(master=root)
            app.mainloop()
            returnCode = app.errorCode
        else:
            # if any parameters, command line mode
            processing = CliProcessing()
            returnCode = processing.run()
    
    #ignore exception when call with help parameeter -h or --help 
    except ArgumentError:
        pass
     
    except:
        print('Unexpected error in main: {}'.format(traceback.format_exc()))
    
    finally:    
        sys.exit(returnCode)
