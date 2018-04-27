run-jenkins-lts:
	docker run --rm -p 8080:8080 -v `pwd`/jenkins_home:/var/jenkins_home jenkins/jenkins:lts

test:
	venv-jenkins/bin/pytest -vvv tests/