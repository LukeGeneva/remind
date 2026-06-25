BINARY  = remind
DIST    = dist/$(BINARY)
VERSION ?= $(error VERSION is not set — usage: make release VERSION=x.y.z)

.PHONY: build install release clean

build:
	python -m PyInstaller --onefile --name $(BINARY) remind.py

install: build
	cp $(DIST) /usr/local/bin/$(BINARY)

release: build
	gh release create v$(VERSION) "$(DIST)#remind-$(shell uname -m)" \
		--title "v$(VERSION)"

clean:
	rm -rf build dist $(BINARY).spec
