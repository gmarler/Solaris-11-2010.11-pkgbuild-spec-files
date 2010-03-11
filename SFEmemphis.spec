#
# spec file for package SFEmemphis
#
# includes module(s): memphis
#

%include Solaris.inc
Name:                    SFEmemphis
Summary:                 Map Rendering Application
URL:                     https://trac.openstreetmap.ch/trac/memphis/
Version:                 0.1.0
License:                 LGPL
Source:                  http://wenner.ch/files/public/mirror/memphis/memphis-%{version}.tar.gz
Patch1:                  memphis-01-configure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWglib2
Requires:                SUNWcairo
BuildRequires:           SUNWglib2-devel
BuildRequires:           SUNWcairo-devel

%include default-depend.inc

%package devel
Summary:		 %{summary} - development files
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires: SFEhippo-canvas

%prep
%setup -q -n memphis-%version
%patch1 -p1

%build
test ! -d ./m4 && mkdir ./m4
glib-gettextize -f
intltoolize --force --copy --automake
libtoolize --force
aclocal $ACLOCAL_FLAGS -I ./m4
autoheader
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Clean up unpackaged files
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Wed Mar 10 2010 - brian.cameron@sun.com
- Created with version 0.1.0.
