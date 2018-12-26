pyinstaller --onefile --windowed --icon="images/app.ico" --add-data="images/app.ico:images" --hidden-import='PIL._tkinter_finder' image_transfrom.py

read -p "Press enter to continue"
