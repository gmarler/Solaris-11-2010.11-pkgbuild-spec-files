#
# spec file for package SFEobby
#
# includes module(s): obby
#
%include Solaris.inc

%define SFEavahi         %(/usr/bin/pkginfo -q SFEavahi && echo 1 || echo 0)

Name:                    SFEobby
Summary:                 obby - Network Text Editing Library
Version:                 0.4.4
Source:                  http://releases.0x539.de/obby/obby-%{version}.tar.gz
Patch1:                  obby-01-cast.diff
URL:                     http://gobby.0x539.de/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgmp
Requires: SFEsigcpp
Requires: SFEnet6 >= 1.3.3
%if %SFEavahi
Requires: SFEavahi
%else
Requires: SUNWavahi-bridge-dsd
%endif
BuildRequires: SFEnet6-devel >= 1.3.3
BuildRequires: SFEsigcpp-devel
%if %SFEavahi
BuildRequires: SFEavahi-devel
%else
BuildRequires: SUNWavahi-bridge-dsd-devel
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n obby-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-ipv6                    \
            --with-zeroconf
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Sep 17 2007 - trisk@acm.jhu.edu
- Enable IPv6 support and Zeroconf (avahi)
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 0.4.4
- Add URL
* Tue Jul 11 2006 - laca@sun.com
- rename to SFEobby
- update file attributes
- bump to 0.4.0.rc2
* Fri May 05 2006 - damien.carbery@sun.com
- Bump to 0.4.0rc1. Add SUNWsigcpp and SUNWnet6 dependencies.
* Thu Nov 17 2005 - laca@sun.com
- create
