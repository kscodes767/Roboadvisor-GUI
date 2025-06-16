import pandas as pd
import os



def saveCSV(data):
    fileName =  input("Please enter filename: ").strip()
    fullFileName = f"{fileName}.csv"
    write_header = not os.path.exists(fullFileName)
    data.to_csv(fullFileName, mode = 'a', header =write_header, index = False)
    print(f"Data saved to {fullFileName}")

def saveExcel(data):
    fileName = input("Please enter filename: ").strip()
    fullFileName = f"{fileName}.xlsx"
    userSheetName = input("What would you like to call this sheet: ")
    if not os.path.exists(fullFileName):
        with pd.ExcelWriter(fullFileName, engine ='openpyxl', mode='w') as writer:
            data.to_excel(writer, sheet_name = userSheetName, index = False)   
        print(f"Data saved to {fullFileName}")
    else:
         with pd.ExcelWriter(fullFileName, engine ='openpyxl', mode = 'a', if_sheet_exists= 'replace') as writer:
            data.to_excel(writer, sheet_name = userSheetName, index = False) 


def saveData(data):
    saveChoice = input("Press 'y' to save data or 'n' for do NOT save\nEnter Choice: ").strip().lower()
    if saveChoice == "y":
        typeFile = input("If you want to save as 'csv file' press 'c' if you want to save as excel file press 'e' \nEnter Choice: ").strip().lower()
        if typeFile == 'c':
            saveCSV(data)
        elif typeFile == 'e':
            saveExcel(data)
        else:
            print("Invalid choice")
            return saveData(data)
    else:
        print("Data not saved")
