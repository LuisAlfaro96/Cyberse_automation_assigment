import io
import os
import json
import requests
import re
import time
import smtplib
from email.message import EmailMessage
#docker container run --env SENDER_EMAIL=test1 --env RECEIVER_EMAIL=test2  --env SENDER_PASSWORD=test3 test11:latest 
#docker container exec -it c2aa2299cc3c /bin/bash
import sys

import yaml
from yaml.loader import SafeLoader

import logging


#sender_email = os.environ['SENDER_EMAIL']
#receiver_email = os.environ['RECEIVER_EMAIL']
#sender_password = os.environ['SENDER_PASSWORD']
print ("    +++ Starting the script +++")
print("\n")
name_file2 = 'domain_data/updated_info.json' #care with the path
send_alert_flag = 0


# Open the file and load the file
with open('domains.yml') as f: #care with the path
    data = yaml.load(f, Loader=SafeLoader)
    #print(len(data['domains']))
    all_domains = data['domains']
#    print(sender_email)


    for domain in all_domains: # getting all the domains in a loop to scan
        print("+ Getting info for Domain: " + domain)
        api_call = "https://api.domaintools.com/v1/" + str(domain) + "/whois/"
        print("+ Executing Get request: " + api_call)
        response = requests.get(api_call)
        result = json.loads(response.text)
    #print(result)
            
        todays_data = result['response']['registration']
        todays_data.pop('registrar')
        todays_data.pop('statuses')

        
        #print(todays_data)
      
        name_file = 'domain_data/' + domain + "_data.json" #care with the path
        
        if os.path.isfile(name_file): #compare if the file already exist, this if because could be the posibility that the script its running for its first time
            print("+ Comparing the new data with yersterday data...")
    
            listObj = []
            with open(name_file) as fp: #charging the data that exist into the python enviroment to compare with the new entry data (today's data)
                listObj = json.load(fp)
                
                yesterday_data= listObj[-1] #where we will be storing yesterday's data.
                #print (yesterday_data)
                if  yesterday_data == todays_data: #since we are dealing with dic we can make this type of validation
                    print("+ Nothing has changed in the domain, moving to the next one...")
                    print("\n")
                else:
                    send_alert_flag=1
                    for key in todays_data: #if something has changed in the new data entrance, we will capture the old and new value
                         
                        #print(todays_data[key])
            
                        #print(yesterday_data[key])
                        
                        print("+ Checing value: "+key)
                        if todays_data[key] != yesterday_data[key]: #we are capturing the value that has been modified
                            print("+ New server info has been found for the Domain: " +domain+ " on value: "+ key)
                            
                            
                            print("\n")  
                            new_dic = {}
                            new_dic["Domain"] = domain
                            new_dic[key+"_New_entry_"] = todays_data[key] 
                            new_dic[key+"_Old_data_"] = yesterday_data[key]
                            data_updated = new_dic
                            
                            print("- Data to be send: "+str(data_updated))
                            print("\n")

                            if os.path.isfile(name_file2): #this is to divide if its the firs time the script its executed or if the files has been deleted, depends on that could append the data or create a new file.
                                print("+ Writting the data into: "+name_file2)
                                listObj2 = []
                                with open(name_file2) as fp:
                                    listObj2 = json.load(fp)
                                    listObj2.append(data_updated)
                                    with open(name_file2, 'w') as json_file:
                                        json.dump(listObj2, json_file,indent=4,separators=(',',': '))
                            else:

                                with open(name_file2,'w') as outfile:
                                    print("+ Creating file"+name_file2)
                                    print("+ Writting the data into: "+name_file2)
                                    #data_updated['Domain'] = domain
                                    array = []
                                    array.append(data_updated)
                                    array.append({'Domain': domain})
                                    json.dump(array, outfile)
                        else:
                            print("+ Same value, nothings has changed")  
                                    
                listObj.append(todays_data)

            
            with open(name_file, 'w') as json_file:
                json.dump(listObj, json_file,indent=4,separators=(',',': '))





        else:
            with open(name_file,'w') as outfile:
                array = []
                array.append(todays_data)
                json.dump(array, outfile)

if send_alert_flag == 1:
###sending the email
    print("\n")
    print("+ Sending Alert via EMAIL")
    contacts = ['alfaro.13.luis@gmail.com']

    msg = EmailMessage()
    msg['Subject'] = 'ALERT! - NEW SERVER INFO HAS APPEARED'
    msg['From'] = 'alfaro.13.luis@gmail.com'
    msg['To'] = 'alfaro.13.luis@gmail.com'

    msg.set_content('You can find more information about the domain info that has been updated in the file attached')
    files = [name_file2]
    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data,maintype='application', subtype ='octet-stream', filename=file_name)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('alfaro.13.luis@gmail.com', 'madestiktrolo1')
        smtp.send_message(msg)

    if os.path.exists(name_file2): #
        time.sleep(2)
        os.remove(name_file2)
        print("- Removing temporary files")
    else:
        print("Can not delete the file as it doesn't exists")
else:
    print("\n")
    print("   +++ Ending the script +++")

        





