import os
from os import path
import sys
import argparse
from argparse import RawTextHelpFormatter
import traceback

from PIL import Image

from enum import IntEnum

class ProcessingMode(IntEnum):
    Cli = 1
    Gui = 2

FILE_EXTENSIONS = ('.jpg', '.bmp', '.png', '.gif')

class CliProcessing:
    def __init__(self):
        appArgs = argparse.ArgumentParser(description='Reduce size of pictures for publishing them to web', 
                                          epilog="Exit codes: 0 - successful completion, 1 - completion with any error",
                                          formatter_class=RawTextHelpFormatter)
        
        appArgs.add_argument("--sourcefolder", nargs=1, required=True, help="Input folder with pictures", metavar='"source folder"')
        appArgs.add_argument("--desiredsize", nargs=1, required=True, help="Output image size", metavar='"desired size"')
        
        args = appArgs.parse_args()
        
        self.sourceFolder = args.sourcefolder[0]
        self.desiredSize = int(args.desiredsize[0])
        
        self.errorDesc = ''
        
    def run(self):
        
        returnCode = 1
        
        try:
        
            originalFiles = os.listdir(self.sourceFolder)
            originalFilesCount = 0 
            for sourceFile in originalFiles:
                if sourceFile.lower().endswith(FILE_EXTENSIONS):
                    originalFilesCount +=1
                    
            fileIndex = 1
            
            for sourceFile in originalFiles:
                if sourceFile.lower().endswith(FILE_EXTENSIONS):
                    sourceFilePath = path.join(self.sourceFolder, sourceFile)
                    sourceBareFileName = path.splitext(sourceFile)[0]
                    outputFileFolder = path.join(self.sourceFolder, 'Ready')
                    outputFilePath = path.join(outputFileFolder, sourceBareFileName + '.jpg')
                    
                    if not path.exists(outputFileFolder):
                        os.mkdir(outputFileFolder)
                    
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
                    print('Processed {} out of {}: {}. Size: {:.2f} KB.'.format(fileIndex, originalFilesCount, sourceFile, outputFileSize))
                    
                    fileIndex +=1
            
            print()
            print('Processing has completed successfully.')
            
            returnCode = 0
        
        except IOError:
            print("Output file can't be created for ".format(sourceFile))
            
        except:
            print(traceback.format_exc())
            
        return returnCode

class GuiProcessing:
    def __init__(self):
        pass
    
    def run(self):
        print('GUI functionality is still in progress')

if __name__=="__main__":
    
    returnCode = 1
    
    try:
        
        processingMode = ProcessingMode.Gui
        
        if len(sys.argv)>1:
            # if any parameters, command line mode
            processing = CliProcessing()
            processingMode = ProcessingMode.Cli
        else:
            # if no parameters, show GUI
            processing = GuiProcessing()
        
        returnCode = processing.run()
        
    except:
        print(traceback.format_exc())
    
    finally:    
        sys.exit(returnCode)
