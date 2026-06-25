BINARY            = remind
DIST              = dist/$(BINARY)
APPLE_ID         ?= $(error APPLE_ID is not set)
APPLE_TEAM_ID    ?= $(error APPLE_TEAM_ID is not set)
APPLE_SIGNING_IDENTITY ?= $(error APPLE_SIGNING_IDENTITY is not set)
APP_PASS         ?= $(shell security find-generic-password -a "$(APPLE_ID)" -s "notarytool" -w)
VERSION          ?= $(error VERSION is not set — usage: make release VERSION=x.y.z)

.PHONY: build sign notarize install release clean

build:
	python -m PyInstaller --onefile --name $(BINARY) remind.py

sign: build
	codesign --deep --force --sign "$(APPLE_SIGNING_IDENTITY)" $(DIST)

notarize: sign
	xcrun notarytool submit $(DIST) \
		--apple-id $(APPLE_ID) \
		--team-id $(APPLE_TEAM_ID) \
		--password $(APP_PASS) \
		--wait
	xcrun stapler staple $(DIST)

install: notarize
	cp $(DIST) /usr/local/bin/$(BINARY)

release:
	gh release create v$(VERSION) "$(DIST)#remind-$(shell uname -m)" \
		--title "v$(VERSION)"

clean:
	rm -rf build dist $(BINARY).spec
