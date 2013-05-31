%global gh_commit  ee5073f6a04b77ad3f06061af8990221303d6e07
%global gh_short   %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner   sabberworm
%global gh_project PHP-CSS-Parser

Name:           php-%{gh_project}
Summary:        A Parser for CSS Files
Version:        5.0.5
Release:        1%{?dist}

URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz
License:        MIT
Group:          Development/Libraries

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
# For tests
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)

Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl


%description
PHP CSS Parser: a Parser for CSS Files written in PHP.
Allows extraction of CSS files into a data structure, manipulation
of said structure and output as (optimized) CSS.


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
# nothing to build


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -pr lib/Sabberworm %{buildroot}%{_datadir}/php/Sabberworm


%check
cd tests
# https://github.com/sabberworm/PHP-CSS-Parser/issues/64
sed -e 's/testEndToken/SKIP_testEndToken/'  \
    -i Sabberworm/CSS/RuleSet/LenientParsingTest.php

phpunit --bootstrap bootstrap.php .



%files
%defattr(-,root,root,-)
# LICENSE is in the README.md file
%doc *md
%{_datadir}/php/Sabberworm


%changelog
* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 5.0.5-1
- Initial packaging
