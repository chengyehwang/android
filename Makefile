IP=$(shell hostname -I | awk '{print $$1}')
# docker run process
pull:
	docker pull chengyehwang/android
	docker tag chengyehwang/android android
shell:
	docker run -i --mount src=`pwd`,target=/android,type=bind -w /android -t android
stop:
	-docker stop $(shell docker ps -a -q)
	-docker rm $(shell docker ps -a -q)

# android process
TAG=android-10.0.0_r33
repo:
	mkdir -p $(TAG)
	export TAG=$(TAG) ; cd $(TAG); ../run_repo.sh

# docker build process
build:
	docker build --build-arg userid=1001 --build-arg groupid=1001 --build-arg username=android -t android:latest .
push:
	docker login
	docker tag android chengyehwang/android
	docker push chengyehwang/android
clean:
	docker system prune -a
image:
	docker image ls -a
