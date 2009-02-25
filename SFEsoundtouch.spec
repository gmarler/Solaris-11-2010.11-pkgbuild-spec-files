#
# spec file for package SFEsoundtouch
#
# includes module(s): soundtouch
#

%include Solaris.inc
Name:                    SFEsoundtouch
Summary:                 Audio Processing Library
URL:                     http://www.surina.net/soundtouch
Version:                 1.4.0
Source:                  http://www.surina.net/soundtouch/soundtouch-%{version}.tar.gz
Patch1:                  soundtouch-01-noopt.diff
Patch2:                  soundtouch-02-fixpow.diff
Patch3:                  soundtouch-03-nomsse.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
%setup -q -n soundtouch

%patch1 -p1
%patch2 -p1
%patch3 -p1

touch NEWS README AUTHORS ChangeLog COPYING

%build
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ."
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -lCrun -lCstd"
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags"

libtoolize -f -c
aclocal $ACLOCAL_FLAGS -I .
autoconf -f
autoheader
automake -a -c -f

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --datadir=%{_datadir}       \
            --docdir=%{_datadir}        \
            --libdir=%{_libdir}         \
            --mandir=%{_mandir}         \
            --enable-shared             \
            --disable-static

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_prefix}/doc $RPM_BUILD_ROOT%{_datadir}/doc
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %dir %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, other) %dir %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Tue Feb 24 2009 - brian.cameron@sun.com
- Bump to 1.4.0, remove upstream patch soundtouch-03-fixconst.diff.
* Mon Mar 17 2008 - brian.cameron@sun.com
- Created with version 1.3.1
