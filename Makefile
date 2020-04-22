IP=$(shell hostname -I | awk '{print $$1}')
# run process
pull:
	docker pull chengyehwang/android
	docker tag chengyehwang/android android
stop:
	-docker stop $(shell docker ps -a -q)
	-docker rm $(shell docker ps -a -q)
# build process
build:
	docker build -t android:latest .
shell:
	docker run -i --mount src=`pwd`,target=/android,type=bind -w /android -t android
push:
	docker login
	docker tag android chengyehwang/android
	docker push chengyehwang/android
clean:
	docker system prune -a
image:
	docker image ls -a

