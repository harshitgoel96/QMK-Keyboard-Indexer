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
    if "/" in data["keyboards"][key]["keyboard_name"]:
        keebName="{} for {}".format(data["keyboards"][key]["keyboard_name"].split("/")[0],data["keyboards"][key]["keyboard_name"].split("/")[1])
    else:
        keebName=data["keyboards"][key]["keyboard_name"]
    indexList.append([key,keebName])
#print (indexList)

f = open("index.md", "w")
f.write("Index for all the keyboards, search keyboard name here to go to the keyboard directory\n")
f.write("======================================================================================\n")
f.write("| Keyboard | Location |\n")
f.write("|----------|----------|\n")

dfForIndex=pd.DataFrame(indexList)
dfForIndex.columns = ["ParentFolder", "BoardName"]
dfForIndex=dfForIndex.sort_values("BoardName")
print(dfForIndex)
for index, row in dfForIndex.iterrows():
    f.write("|{}|{}{}|\n".format(row["BoardName"],keyboardBaseLocation,row["ParentFolder"]))

f.close()