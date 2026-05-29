### How to work in local debug session with docker ###

* add the submodule from bitbucket
  *  git submodule add https://bitbucket.org/wemblee/shared-lambda shared
  *  git submodule init
  *  git submodule update --remote
  *  git add .\.gitmodules shared
  *  git commit -am "ajout du code partagé"
  *  git push
  
* in the IDE edit a new configuration "Python server debug" and edit it
  * in the "IDE host name" write "host.docker.internal"
  * in the "Port" write "5681"
  * in the "Path mappings" clic on the folder
  * write in the "local path" the origin of the local folder in my case "G:/Wemblee/projet"
  * in "Remote path" write "/"
  * run the debug server

* run docker with "docker-compose up --build"
* when the docker is started you will be redirect on the app press F9 to start the debug
* put an endpoint in the code
* run a test in postman with the classic port in the app.py at app.listen in this case "6604"


### What to do before commit the code ###

* 1st you have to play the collection "lambda-extract-acte-TNR" in Postman
    * all the test have to be good
* If is any changes in the TRN tests or variables you need to change the files in TNR_test folder

### Before starting test ###

make sure you have install in your machin AWS cli and Docker

### How to test the lambda ###


**1 - login to AWS**

`aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 416920486107.dkr.ecr.eu-west-3.amazonaws.com`

**2 - build the image**

`docker build --build-arg extract-acte -f shared/Docker/Dockerfile -t lambda-extract-acte .`

**3 - create a tag of the image**

`docker tag lambda-extract-acte:latest 416920486107.dkr.ecr.eu-west-3.amazonaws.com/lambda-extract-acte:latest`

**4 - push the image to Amazon elastic container register**

`docker push 416920486107.dkr.ecr.eu-west-3.amazonaws.com/lambda-extract-acte:latest`

**5 - update pre-prod the lambda**

`aws lambda update-function-code --function-name lambda-extract-acte-recette --image-uri 416920486107.dkr.ecr.eu-west-3.amazonaws.com/lambda-extract-acte:latest`
