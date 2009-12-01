#
# spec file for package SUNWnet6
#
# includes module(s): net6
#
%include Solaris.inc

Name:                    SFEnet6
Summary:                 net6 - IPv4/IPv6 Network Access Library
Version:                 1.3.5
%define tarball_version  1.3.5
Source:                  http://releases.0x539.de/net6/net6-%{tarball_version}.tar.gz
Patch1:                  net6-01-close-prototype.diff
URL:                     http://gobby.0x539.de/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEsigcpp
Requires: SUNWgnutls
Requires: SUNWlibgpg-error
BuildRequires: SFEsigcpp-devel
BuildRequires: SUNWgnutls-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n net6-%tarball_version
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
            --sysconfdir=%{_sysconfdir} --disable-python

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
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 1.3.5
- Add URL
* Fri Jul  7 2006 - laca@sun.com
- rename to SFEnet6
- bump to 1.3.0rc2
- fix version number
- update file attributes
- remove upstream patch enum_opts.diff
* Mon May 08 2006 - damien.carbery@sun.com
- Add patch, 02-enum_opts, to fix build.
* Fri May 05 2006 - damien.carbery@sun.com
- Bump to 1.3.0rc1
* Wed Nov 16 2005 - laca@sun.com
- create
