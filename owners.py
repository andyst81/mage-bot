from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json


def get_owners(address):
  scopes = [
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/drive'
  ]
  address = address.lower()
  credentials = ServiceAccountCredentials.from_json_keyfile_name("topm-scholar-tracking.json", scopes) #access the json key you downloaded earlier 
  file = gspread.authorize(credentials) # authenticate the JSON key with gspread
  sheet = file.open("The Order of the Portal Mages Managers (Responses)") #open sheet
  sheet = sheet.sheet1

  cells = sheet.range('C2:C100')
  
  for c in cells:
    if c.value !='':  
      lower_address = c.value.lower()
      if address == lower_address:
        owner = sheet.cell(c.row, c.col -1).value
        break
      else:
        owner = 'Unknown'
  
  print(owner)
  return owner
