# spec file for php-kolab-net-ldap3
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

Name:           php-kolab-net-ldap3
Version:        1.0.2
Release:        2%{?dist}
Summary:        Advanced functionality for accessing LDAP directories

Group:          Development/Libraries
License:        GPLv3+
URL:            http://git.kolab.org/pear/Net_LDAP3/
Source0:        http://git.kolab.org/pear/Net_LDAP3/snapshot/pear-Net-LDAP3-%{version}.tar.gz

# Upstream patch for license clarification
# https://issues.kolab.org/show_bug.cgi?id=4695
Patch0:         php-kolab-net-ldap3-license.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# From composer.json
#               "php": ">=5.3.3",
#               "pear-pear/Net_LDAP2": ">=2.0.12"
Requires:       php(language) >= 5.3.3
Requires:       php-pear-Net-LDAP2 >= 2.0.12
# From phpcompatinfo report for version 1.0.2
Requires:       php-json
Requires:       php-ldap
Requires:       php-pcre

Provides:       php-composer(kolab/Net_LDAP3) = %{version}


%description
A successor of the PEAR:Net_LDAP2 module providing advanced functionality
for accessing LDAP directories.


%prep
%setup -q -n pear-Net-LDAP3-%{version}

%patch0 -p1


%build
# Nothing to build


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{_datadir}/php
cp -pr lib/* %{buildroot}%{_datadir}/php


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc composer.json
%{_datadir}/php/Net


%changelog
* Tue Feb 24 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- add upstream patch for License clarification

* Sun Feb 22 2015 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- initial package, version 1.0.2