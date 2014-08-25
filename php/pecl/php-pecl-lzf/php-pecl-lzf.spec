%{?scl:          %scl_package        php-pecl-lzf}
%{!?php_inidir:  %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:      %global __pecl      %{_bindir}/pecl}
%{!?__php:       %global __php       %{_bindir}/php}

%define pecl_name   LZF
%define  ext_name   lzf
%global with_zts    0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ini_name    %{ext_name}.ini
%else
%global ini_name    40-%{ext_name}.ini
%endif

Name:           %{?scl_prefix}php-pecl-lzf
Version:        1.6.2
Release:        10%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        Extension to handle LZF de/compression
Group:          Development/Languages
License:        PHP
URL:            http://pecl.php.net/package/%{pecl_name}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz


# https://bugs.php.net/65860 - Please Provides LICENSE file
# URL taken from lzf.c header
Source1:        http://www.php.net/license/2_02.txt

# remove bundled lzf libs
Patch0:         php-lzf-rm-bundled-libs.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  liblzf-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires(post): %{__pecl}
Requires(postun): %{__pecl}

Provides:       %{?scl_prefix}php-%{ext_name} = %{version}
Provides:       %{?scl_prefix}php-%{ext_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:      php53-pecl-%{ext_name}
Obsoletes:      php53u-pecl-%{ext_name}
Obsoletes:      php54-pecl-%{ext_name}
Obsoletes:      php54w-pecl-%{ext_name}
%if "%{php_version}" > "5.5"
Obsoletes:      php55u-pecl-%{ext_name}
Obsoletes:      php55w-pecl-%{ext_name}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:      php56u-pecl-%{ext_name}
Obsoletes:      php56w-pecl-%{ext_name}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
This extension provides LZF compression and decompression using the liblzf
library

LZF is a very fast compression algorithm, ideal for saving space with a 
slight speed cost.


%prep
%setup -c -q

mv %{pecl_name}-%{version} NTS
cd NTS
%patch0 -p1 -b liblzf
rm -f lzf_c.c lzf_d.c lzf.h

cp %{SOURCE1} LICENSE

extver=$(sed -n '/#define PHP_LZF_VERSION/{s/.* "//;s/".*$//;p}' php_lzf.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
cd ..

%if %{with_zts}
cp -r NTS ZTS
%endif

cat >%{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=lzf.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}
make install -C NTS INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
cd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
done
for i in LICENSE $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}/%{php_extdir}/%{ext_name}.so \
    --modules | grep -i %{ext_name}

TEST_PHP_EXECUTABLE=%{__php} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__php} run-tests.php \
    -n -q \
    -d extension=%{buildroot}%{php_extdir}/%{ext_name}.so

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}/%{php_ztsextdir}/%{ext_name}.so \
    --modules | grep %{ext_name}

TEST_PHP_EXECUTABLE=%{__ztsphp} \
REPORT_EXIT_STATUS=1 \
NO_INTERACTION=1 \
%{__ztsphp} run-tests.php \
    -n -q \
    -d extension_dir=modules \
    -d extension=%{buildroot}%{php_ztsextdir}/%{ext_name}.so
%endif

%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]  ; then
   %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{pecl_name}
%doc %{pecl_testdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so
%{pecl_xmldir}/%{name}.xml
%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.6.2-10
- improve SCL build

* Wed Apr 16 2014 Remi Collet <remi@fedoraproject.org> - 1.6.2-9
- add numerical prefix to extension configuration file

* Wed Mar 19 2014 Remi Collet <remi@fedoraproject.org> - 1.6.2-8
- allow SCL build

* Mon Mar 10 2014 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-7
- cleanups for Copr

* Fri Feb 28 2014 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-6
- cleanups
- move doc in pecl_docdir
- move tests in pecl_docdir
- add missing LICENSE file

* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-2.1
- also provides php-lzf

* Sun Oct 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-2
- sync with rawhide (use system liblzf)

* Sat Oct 20 2012 Andrew Colin Kissa - 1.6.2-1
- Upgrade to latest upstream
- Fix bugzilla #838309 #680230

* Mon Jul 09 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-1
- update to 1.6.2

* Sat Jul 07 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.6.1-1
- update to 1.6.1

* Fri Nov 18 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.5.2-8
- php 5.4 build

* Sat Oct 15 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.5.2-7
- zts extension
- spec cleanup

* Fri Jul 15 2011 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-7
- Fix bugzilla #715791

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 12 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.5.2-4
- rebuild for new PHP 5.3.0 ABI (20090626)

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-3
- Consistent use of macros

* Mon Jun 22 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-2
- Fixes to the install to retain timestamps and other fixes raised in review

* Sun Jun 14 2009 Andrew Colin Kissa <andrew@topdog.za.net> - 1.5.2-1
- Initial RPM package
