import http.client
import json 
import pandas as pd

connection = http.client.HTTPSConnection("api.qmk.fm")

keyboardBaseLocation="https://github.com/qmk/qmk_firmware/tree/master/keyboards/"

connection.request("GET", "/v1/keyboards/all")
response = connection.getresponse()
print("Status: {} and reason: {}".format(response.status, response.reason))
data=json.loads(response.read().decode())

connection.close()
indexList=[]
listOfKeys=data["keyboards"].keys()
for key in listOfKeys:
    keebName=""
    keebDescription=""
    keebFolder=""
    if "/" in data["keyboards"][key]["keyboard_name"]:
        keebName="{} for {}".format(data["keyboards"][key]["keyboard_name"].split("/")[0],data["keyboards"][key]["keyboard_name"].split("/")[1])
    else:
        keebName=data["keyboards"][key]["keyboard_name"]
    if keebName=="":
        keebName=key
    if data["keyboards"][key]["keyboard_folder"]!="":
        keebFolder=data["keyboards"][key]["keyboard_folder"]
    else:
        keebFolder=key
    
    keebDescription=data["keyboards"][key].get("description","") 
    indexList.append([key,keebName,keebFolder,keebDescription])
   
#print (indexList)

f = open("index.md", "w", encoding="utf-8")
f.write("### Index for all the keyboards that can run QMK\n")
#f.write("======================================================================================\n")
f.write("| Keyboard | Description |\n")
f.write("|----------|-------------|\n")

dfForIndex=pd.DataFrame(indexList)
dfForIndex.columns = ["KeebId", "BoardName","ParentFolder","KeyboardDescription"]
dfForIndex=dfForIndex.sort_values("BoardName")
print(dfForIndex)
for index, row in dfForIndex.iterrows():
    #print("trying to enter \n")
    #print("|[{}]({}{})|{}|\n".format(row["BoardName"],keyboardBaseLocation,row["ParentFolder"],row["KeyboardDescription"]))
    f.write("|[{}]({}{})|{}|\n".format(row["BoardName"],keyboardBaseLocation,row["ParentFolder"],row["KeyboardDescription"]))

f.close()