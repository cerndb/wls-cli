#*******************************************************************************
# Copyright (C) 2015, CERN
# # This software is distributed under the terms of the GNU General Public
# # License version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# # In applying this license, CERN does not waive the privileges and immunities
# # granted to it by virtue of its status as Intergovernmental Organization
# # or submit itself to any jurisdiction.
# #
# #
# #*******************************************************************************
SPECFILE=$(shell find -maxdepth 1 -name \*.spec -exec basename {} \; )
REPOURL=git+ssh://git@gitlab.cern.ch:7999
# DB gitlab group
REPOPREFIX=/db

# Get all the package infos from the spec file
PKGVERSION=$(shell awk '/Version:/ { print $$2 }' ${SPECFILE})
PKGRELEASE=$(shell awk '/Release:/ { print $$2 }' ${SPECFILE})
PKGNAME=$(shell awk '/Name:/ { print $$2 }' ${SPECFILE})
PKGID=$(PKGNAME)-$(PKGVERSION)
TARFILE=$(PKGID).tar.gz

sources:
	#tar cvzf $(TARFILE) --exclude-vcs --transform 's,^,$(PKGID)/,' *
	rm -rf /tmp/$(PKGID)
	mkdir /tmp/$(PKGID)
	cp -rv * /tmp/$(PKGID)/
	pwd ; ls -l
	cd /tmp ; tar --exclude .svn --exclude .git --exclude .gitkeep -czf $(TARFILE) $(PKGID)
	mv /tmp/$(TARFILE) .
	rm -rf /tmp/$(PKGID)

all:    sources

clean:
	rm $(TARFILE)

srpm:   all
	rpmbuild -bs --define '_sourcedir $(PWD)' ${SPECFILE}

rpm:    all
	rpmbuild -ba --define '_sourcedir $(PWD)' ${SPECFILE}

scratch:
	koji build db6 --nowait --scratch  ${REPOURL}${REPOPREFIX}/${PKGNAME}.git#master

build:
	koji build db6 --nowait ${REPOURL}${REPOPREFIX}/${PKGNAME}.git#master
