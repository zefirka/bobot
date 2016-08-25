PYLINTRC='./.pylintrc'
VERSION=$(shell python lib.py version)

# developer
DEFAULT_CALL_URL="http://127.0.0.1:8000/bot"
DEFAULT_CALL_ID="172862922"
DEFAULT_CALL_TEXT="test"

ifeq ('$(DEV_CALL_ID)','')
	DEV_CALL_ID=$(DEFAULT_CALL_ID)
endif

ifeq ('$(DEV_CALL_URL)','')
	DEV_CALL_URL=$(DEFAULT_CALL_URL)
endif

ifeq ('$(CALL_TEXT)','')
	CALL_TEXT=$(DEFAULT_CALL_TEXT)
endif

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
	echo 'Publishing into PYPI $(SEMVER) release with version: $(VERSION)'
	./tasks/publish.sh pypi $(VERSION) $(PUSH)

release-test:
	echo 'Publishing into PYPITEST $(SEMVER) release with version: $(NEXT) (Update from: $(VERSION))'
	./tasks/publish.sh pypitest $(NEXT) $(PUSH)

release:
	echo 'Publishing into PYPI $(SEMVER) release with version: $(NEXT) (Update from: $(VERSION))'
	./tasks/publish.sh pypi $(NEXT) $(PUSH)

register-test:
	python setup.py register -r pypitest

register:
	python setup.py register -r pypi

call:
	./tasks/call.sh $(DEV_CALL_URL) $(DEV_CALL_ID) "$(CALL_TEXT)"