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
if your email account has MFA activated could be better to disable it just for the matter of testing.

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
