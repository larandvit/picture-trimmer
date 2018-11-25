import os
import sys
import argparse
from argparse import RawTextHelpFormatter
import traceback

from PIL import Image

fileExtensions = ('.jpg', '.bmp', '.png')

returnCode = 1

try:
    
    appArgs = argparse.ArgumentParser(description='Reduce size of pictures for publishing them to web', 
                                      epilog="Exit codes: 0 - successful completion, 1 - completion with any error",
                                      formatter_class=RawTextHelpFormatter)
    
    appArgs.add_argument("--sourcefolder", nargs=1, required=True, help="Input folder with pictures", metavar='"source folder"')
    appArgs.add_argument("--desiredsize", nargs=1, required=True, help="Output image size", metavar='"desired size"')
    
    args = appArgs.parse_args()
    
    sourceFolder = args.sourcefolder[0]
    desiredSize = int(args.desiredsize[0])
    
    originalFiles = os.listdir(sourceFolder)
    originalFilesCount = 0 
    for sourceFile in originalFiles:
        if sourceFile.lower().endswith(fileExtensions):
            originalFilesCount +=1
            
    fileIndex = 1
    
    for sourceFile in originalFiles:
        if sourceFile.lower().endswith(fileExtensions):
            sourceFilePath = os.path.join(sourceFolder, sourceFile)
            sourceBareFileName, sourceFileExtension = os.path.splitext(sourceFile)
            outputFileFolder = outputFilePath = os.path.join(sourceFolder, 'Ready')
            outputFilePath = os.path.join(outputFileFolder, sourceBareFileName + '.jpg')
            
            if not os.path.exists(outputFileFolder):
                os.mkdir(outputFileFolder)
            
            im = Image.open(sourceFilePath)
     
            old_size = im.size
            ratio = float(desiredSize)/max(old_size)
            new_size = tuple([int(x*ratio) for x in old_size])
            im = im.resize(new_size, Image.ANTIALIAS)
            new_im = Image.new("RGB", (desiredSize, desiredSize), (255,255,255))
            new_im.paste(im, ((desiredSize - new_size[0])//2, (desiredSize  -new_size[1])//2))
            new_im.save(outputFilePath)
            
            outputFileSize = os.path.getsize(outputFilePath)/1024
            print('Processed {} out of {}: {}. Size: {:.2f} KB.'.format(fileIndex, originalFilesCount, sourceFile, outputFileSize))
            
            fileIndex +=1
    
    print()
    print('Processing has completed successfully.')
    
    returnCode = 0
    
except IOError:
    print("Output file can't be created for ".format(sourceFile))
    
except Exception as err:
    print(traceback.format_exc())

finally:    
    sys.exit(returnCode)
