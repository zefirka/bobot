PYLINTRC='./.pylintrc'
VERSION=$(shell python lib.py version)

ifeq ('$(SEMVER)','')
	SEMVER='patch'
endif

ifeq ('$(PUSH)','')
	PUSH='false'
endif

NEXT='$(shell python lib.py $(SEMVER) next-version)'

lint:
	pylint --rcfile=$(PYLINTRC) bobot

publish-test:
	echo 'Publishing into PYPITEST $(SEMVER) release with version: $(VERSION)'
	./tasks/publish.sh pypitest $(VERSION) $(PUSH)

publish:
	echo 'Publishing $(SEMVER) release with version: $(VERSION)'
	./tasks/publish.sh pypi $(VERSION) $(PUSH)

release-test:
	echo 'Publishing into PYPITEST $(SEMVER) release with version: $(NEXT) (Update from: $(VERSION))'
	./tasks/publish.sh pypitest $(NEXT) $(PUSH)

release:
	echo 'Publishing $(SEMVER) release with version: $(NEXT) (Update from: $(VERSION))'
	./tasks/publish.sh pypi $(NEXT) $(PUSH)

register-test:
	python setup.py register -r pypitest

register:
	python setup.py register -r pypi

