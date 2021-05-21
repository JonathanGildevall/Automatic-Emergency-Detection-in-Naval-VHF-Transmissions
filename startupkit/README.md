# Startupkit

Startup kit for the data factory. We are providing a simplified cookbook to get you started as soon as possible.
Forked from [AI-sweden](https://github.com/aidotse/startupkit-DF)

## Creating a docker image and it's docker container

### Dockerfile Method:

#### Building/Creating a docker image

> cd Docker  
> sh build.sh 

This will create a docker image called custom\_docker\_image. You can change the name of the docker image in build.sh. It has been already installed with the packages you mentioned in the dockerfile and misc/requirements.txt. The container has been preconfigured with all the necessary requirements and packages to run wav2vec 2.0.

#### Starting a container from the docker image

> cd Docker  
> sh run.sh

This will start an instance of the docker image(which means a docker container)

#### Attach to a started container

> docker attach container_id