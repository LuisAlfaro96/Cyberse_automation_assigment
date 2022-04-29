# Cyberse_automation_assigment
This repo explain the solution for the Pfizer assigment to the Cyberse
The objective was to develop a script that captures the data using a DomainTool API tool, domain names will be passed through a yaml file, 
the information will be saved and compared with the previous day's data to see if any of its data changed, if so, 
the changes will be saved in a json file (name of the) which at the time of its creation will be sent by mail. 
For this exercise we are going to analyse the CRETED EXPIRES and UPDATED attributes of the domains described in the file.

## Structure of the project
The project consists of a few files and folders for the following purpose
![image](https://user-images.githubusercontent.com/8351858/165890299-23852d24-6cb9-4f9e-a17e-1864f38e230a.png)

* **domain_data** : Folder where the data related to the domains's results will be stored.

* **Dockerfile** : Dockerfile used to create the image of the project.

* **crontab**: Contrab file used to configured the scheduling of the  data.py script.

* **data.py** : Python file develop to interact with the Domaintool API and the files within the Domain_Data folder.

* **domains.yml** : Store all the domains which their data will be requested.

* **project_env.sh** : Bash script used in order to Crontab understand the enviroment variables we will use in the docker run command.

## Gmail feature configuration
Depending on your email provider(tested on Gmail) and configuration, we would need to turn off some security aspects (MF2 and Access to Less secure Apps), this could be done following the documentation presented
* **TURN OFF MF2** : Check the following [documentation](https://support.google.com/accounts/answer/1064203?hl=es-419&co=GENIE.Platform%3DDesktop&oco=0) to complete this.

* **Less Secure Apps** : You would need to activate the [Less Secure Apps](https://www.google.com/settings/security/lesssecureapps) for your gmail account, in order to comunicate with the script

or you can use a test Email provider.

## Building the Image
You can clone the repo and check for your Docker engine versione, the project was develop using Docker version 20.10.14, you can check that using
```bash
docker --version
```

Once you have the repo cloned you can start building the Docker image with the command

```bash
docker build -t project .
```

## Running the Container

Once you have the image already created you can proceed to run the container with the following command.
```bash
docker container run --env SENDER_EMAIL=your@email.com --env RECEIVER_EMAIL=your@email.com  --env SENDER_PASSWORD=yourpassoword project:latest 
```


# Application Output 
What you would see in your terminal is the logs resistred by the script, the crontab configuration is develop to execute the script every minute (for testing purpose)
so every minute we will see the script doing the GET request to the [Domain Tool API](https://www.domaintools.com/resources/api-documentation) in order to extract the information of every Domain listed in domains.yml file.

To possible scenarios could appear
* **Domain's info has changed**: The script will compare the new data requested(CREATED,EXPIRES and UPDATED ) with the same values previously collected, if the new values has changed, it will triger the ALERT sending an email(updated_info.json) with the values thas been modified (the new value and the old value) and the output of the script should be like this(testing with only 2 Domains).

```
    +++ Starting the script +++


+ Getting info for Domain: DailyChanges.com
+ Executing Get request: https://api.domaintools.com/v1/DailyChanges.com/whois/
+ Comparing the new data with yersterday data...
+ Checing value: created
+ New server info has been found for the Domain: DailyChanges.com on value: created


- Data to be send: {'Domain': 'DailyChanges.com', 'created_New_entry_': '2002-02-17', 'created_Old_data_': '2002-02-19'}


+ Creating file/domain_data/updated_info.json
+ Writting the data into: /domain_data/updated_info.json
+ Checing value: expires
+ Same value, nothings has changed
+ Checing value: updated
+ Same value, nothings has changed
+ Getting info for Domain: DomainTools.com
+ Executing Get request: https://api.domaintools.com/v1/DomainTools.com/whois/
+ Comparing the new data with yersterday data...
+ Nothing has changed in the domain, moving to the next one...




+ Sending Alert via EMAIL
- Removing temporary files
```
  as you can see the value CREATED in the DailyChanges.com Domain has been modified and the 'Data to be send' would be what you can expect in the email.

* **Domain's info has NOT changed** If nothing has changed and the new and old data is the same, nothing will trigger and the output should be like this.
```
  +++ Starting the script +++


+ Getting info for Domain: DailyChanges.com
+ Executing Get request: https://api.domaintools.com/v1/DailyChanges.com/whois/
+ Comparing the new data with yersterday data...
+ Nothing has changed in the domain, moving to the next one...


+ Getting info for Domain: DomainTools.com
+ Executing Get request: https://api.domaintools.com/v1/DomainTools.com/whois/
+ Comparing the new data with yersterday data...
+ Nothing has changed in the domain, moving to the next one...




   +++ Ending the script +++
```


# Crontab interaction
For the automation part, since the script should be executed programatically every 24 hours, i used crontab to achieve that, /enviroment are the enviroment variables that you enter once the docker container is deployed, those are the credentials for your email that then the script will use to send the email, and the /var/log/cron.log will send the output of the script to the crontab log environment.
```crontab
* * * * * . /environment; /usr/bin/python3 /data.py >> /var/log/cron.log
```
