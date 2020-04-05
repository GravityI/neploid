#The purpose of this program is to fetch ygoprodeck's database and store it into a JSON file.
#import needed libraries
import urllib.request, json 

#fp represents the target file path on which the data will be stored.
def fetchData(fp):
    #Define headers used to simulate access as a user. I got these specific settings from a solution at StackOverflow.
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    #Make a Request at ygoprodeck as an user, then open it, then convert it to a bytes object.
    data = urllib.request.urlopen(urllib.request.Request("https://db.ygoprodeck.com/api/v4/cardinfo.php", headers = headers)).read()
    #Serialize data.
    jsonData = json.loads(data)
    #Open file and store the serialized data.
    with open(fp, "w") as file:
        json.dump(jsonData, file)
    print("Database successfully fetched")