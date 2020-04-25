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
init:
	mkdir -p $(TAG)
	export TAG=$(TAG) ; cd $(TAG); ../run_repo_init.sh
sync:
	cd $(TAG) ; ../run_repo_sync.sh

simpleperf: sync
	cd $(TAG); ../run_simpleperf.sh

android_deps: repo
	cd $(TAG) ; ../soong_project -o ../android_bp.json
	cd $(TAG) ; ../repo list > ../repo_list
	python3 android_deps.py

repo:
	curl -o ./repo https://storage.googleapis.com/git-repo-downloads/repo && chmod a+x ./repo

du:
	cd $(TAG) ; du -k --max-depth=1

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

