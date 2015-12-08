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
# Standard install path for infra stuff
%define install_path /ORA/dbs01/syscontrol/projects
%define debug_package %{nil}
%define __jar_repack %{nil}
%define __arch_install_post %{nil}
%define __os_install_post %{nil}


# Begin customised part
Summary:	Weblogic REST
Name:		cerndb-infra-wls_rest
Version:	0.9
Release:	2%{?dist}
License:	GPL
BuildArch:	noarch
Group:		Development/Tools
Source:		%{name}-%{version}.tar.gz
BuildRoot:	%{_builddir}/%{name}-root
AutoReqProv:	no

%description
The package cerndb-infra-wls_rest contains the tools for weblogic REST API.

# End customised part

%prep
%setup -q

%build
#CFLAGS="%{optflags}" %{__python} wls_rest/setup.py build

%install
%{__rm} -rf %{buildroot}

mkdir -p $RPM_BUILD_ROOT/bin/
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1

%{__python} setup.py install --root %{buildroot}
install -m 644 wls_rest/man/wls-cli.1 $RPM_BUILD_ROOT/%{_mandir}/man1/
#mkdir -p $RPM_BUILD_ROOT/%{install_path}
#find . -maxdepth 1 -type d -not -name '\.*' -exec cp -a {} $RPM_BUILD_ROOT/%{install_path} \;

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*
%{_bindir}/wls-cli
%{_mandir}/man1/wls-cli.1

# Please keep a meaningful changelog
%changelog
* Mon Nov 30 2015 Konrad Kaczkowski <konrad.kaczkowski@cern.ch> - 0.8-2
- New Tool version
* Mon Oct 28 2015 Damian Moskalik <damian.moskalik@cern.ch> - 0.1-1
- Initial creation of the RPM
