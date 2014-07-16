#
# RPM spec file for php-doctrine-annotations
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     doctrine
%global github_name      annotations
%global github_version   1.2.0
%global github_commit    d9b1a37e9351ddde1f19f09a02e3d6ee92e82efd

%global composer_vendor  doctrine
%global composer_project annotations

# "php": ">=5.3.2"
%global php_min_ver      5.3.2
# "doctrine/cache": "1.*"
%global cache_min_ver    1.0
%global cache_max_ver    2.0
# "doctrine/lexer": "1.*"
%global lexer_min_ver    1.0
%global lexer_max_ver    2.0

# Build using "--without tests" to disable tests
%global with_tests       %{?_without_tests:0}%{!?_without_tests:1}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       PHP docblock annotations parser library

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
%if %{with_tests}
# For tests
BuildRequires: php(language)                >= %{php_min_ver}
BuildRequires: php-composer(doctrine/cache) >= %{cache_min_ver}
BuildRequires: php-composer(doctrine/cache) <  %{cache_max_ver}
BuildRequires: php-composer(doctrine/lexer) >= %{lexer_min_ver}
BuildRequires: php-composer(doctrine/lexer) <  %{lexer_max_ver}
BuildRequires: php-phpunit-PHPUnit
# For tests: phpcompatinfo (computed from version 1.2.0)
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
BuildRequires: php-tokenizer
%endif

Requires:      php(language)                >= %{php_min_ver}
Requires:      php-composer(doctrine/lexer) >= %{lexer_min_ver}
Requires:      php-composer(doctrine/lexer) <  %{lexer_max_ver}
# phpcompatinfo (computed from version 1.2.0)
Requires:      php-ctype
Requires:      php-date
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
Requires:      php-tokenizer

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Extracted from Doctrine Common as of version 2.4
Conflicts:     php-pear(pear.doctrine-project.org/DoctrineCommon) < 2.4

%description
%{summary} (extracted from Doctrine Common).


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit --include-path ./lib -d date.timezone="UTC"
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE *.md composer.json
%{_datadir}/php/Doctrine/Common/Annotations


%changelog
* Tue Jul 15 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0 (BZ #1116887)

* Fri Jun 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.2-5.20131220gita11349d
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide
- Added option to build without tests ("--without tests")
- Updated dependencies to use php-composer virtual provides

* Sat Jan 11 2014 Remi Collet <rpms@famillecollet.com> 1.1.2-3.20131220gita11349d
- backport for remi repo

* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-3.20131220gita11349d
- Minor syntax changes

* Fri Jan 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-2.20131220gita11349d
- Conditional %%{?dist}
- Added conflict w/ PEAR-based DoctrineCommon pkg (version < 2.4)

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-1.20131220gita11349d
- Initial package
