CURRENT_PATH  := $(notdir $(patsubst %/,%,$(CURDIR)))
REPO_URI      := jaspajjr
NAME          := ${CURRENT_PATH}
TAG           := $(shell git rev-parse --short HEAD)
IMG_BUILD     := ${NAME}:tmp
IMG           := ${REPO_URI}/${NAME}:${TAG}
LATEST        := ${REPO_URI}/${NAME}:latest

all: pull build tag push

pull:
	-@docker pull ${LATEST} && (echo "docker tag already exists"; exit 1)
	-@docker pull ${IMG}

build:
	@docker build -t ${IMG_BUILD} .

test:
	@docker run --name ${NAME}_${TAG} ${IMG_BUILD} -t
	@docker rm ${NAME}_${TAG}

tag:
	@docker tag ${IMG_BUILD} ${IMG}
	@docker tag ${IMG_BUILD} ${LATEST}

push:
	@docker push ${IMG}
	@docker push ${LATEST}
	@echo Pushed to ${IMG}

login:
	@docker log -u ${DOCKER_USER} -p ${DOCKER_PASS}

clean:
	-@docker images -q "*/${NAME}" | xargs docker image rm
	-@docker rmi ${IMG_BUILD}
	-@docker rm ${NAME}_${TAG}