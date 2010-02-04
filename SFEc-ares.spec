#
# spec file for package SFEc-ares
#
# includes module(s): c-ares
#

%include Solaris.inc
Name:                    SFEc-ares
Group:                   System/Libraries
Version:                 1.7.0
Vendor:                  Sun Microsystems, Inc.
Summary:                 Library to perform DNS requests and name resolves asynchronously
Source:                  http://c-ares.haxx.se/c-ares-%{version}.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:            %{_basedir}

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
%setup -q -n c-ares-%version

%build
export PYTHON="/usr/bin/python%{pythonver}"
aclocal $ACLOCAL_FLAGS -I ./m4
autoconf
automake -a -c -f
./configure \
	--prefix=%{_prefix}         \
	--libdir=%{_libdir}	    \
	--mandir=%{_mandir}	    \
	--disable-mono              \
	--disable-glibtest
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/man

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Fri Jan 29 2010 - Brian Cameron  <brian.cameron@sun.com>
- Created with version 1.7.0.
