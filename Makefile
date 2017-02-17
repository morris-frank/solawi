
PYTHON35 := $(shell which python3.5 2> /dev/null)

all:
	ifnndef PYTHON35
		$(error "Python 3.5 is not installed on the system. Please do this.")
	endif


install:
	( \
	[ ! -d venv ] && virtualenv --system-site-packages --python=python3.5 --prompt=SoLaWi venv; \
	source ./venv/bin/activate; \
	pip install -r requirements.txt; \
	)


clean:
	rm -fr venv; \
