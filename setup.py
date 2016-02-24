#*******************************************************************************
# Copyright (C) 2015, CERN
# This software is distributed under the terms of the GNU General Public
# License version 3 (GPL Version 3), copied verbatim in the file "LICENSE".
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as Intergovernmental Organization
# or submit itself to any jurisdiction.
#
#
#*******************************************************************************
from distutils.core import setup

setup(name='cerndb-infra-wls_rest',
		version='0.7',
		description='WLS Rest scripts',
		author='IT-DB-IMS',
		author_email='it-dep-db-ims@cern.ch',
		url='http://www.cern.ch/',
		package_dir= {'': 'wls_rest/src'},
		packages=['wlscli','wlscli.common','wlscli.controller', 'wlscli.controller.console', 'wlscli.model', 'wlscli.view',
			'wlscli.model.business_logic','wlscli.model.application_logic','wlscli.service', 'wlscli.service.curl', 
                        'wlscli.service.weblogic', 'wlscli.service.node_manager', 'wlscli.service.security', 
                        'wlscli.service.security.data', 'wlscli.service.security.data.data_access', 'wlscli.view.console_ui'],
		scripts=['wls_rest/bin/wls-cli'],
		)
