#
# spec file for package SFEldtp
#
# includes module(s): ldtp

%include Solaris.inc
%define python_version 2.4

Name:          SFEldtp
Summary:       Linux Desktop Testing Project
Version:       1.5.1
SUNW_BaseDir:  %{_basedir}
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
Source:        http://download.freedesktop.org/ldtp/1.x/1.5.x/ldtp-%{version}.tar.gz
URL:           http://ldtp.freedesktop.org
%include default-depend.inc
Requires: SUNWPython
Requires: SUNWgnome-a11y-libs
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWlxml
Requires: SUNWmlib
Requires: SUNWzlib
BuildRequires: SUNWgnome-a11y-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWlibpopt-devel

%prep
%setup -n ldtp-%{version}


%build
export LDFLAGS="$LDFLAGS -lsocket -lnsl"
libtoolize --force
aclocal
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} --bindir=%{_bindir}
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
cd $RPM_BUILD_ROOT%{_libdir}/python%{python_version}
mv site-packages vendor-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%{_datadir}/*

%changelog
* Mon Dec 8 2008 - tim.miao@sun.com
- Bump to 1.4.0
* Thu Mar 29 2007 - daymobrew@users.sourceforge.net
- Correct source url.
* Wed Mar 21 2007 - daymobrew@users.sourceforge.net
- Bump to 0.8.0.
* Wed Oct 11 2006 - laca@sun.com
- remove -I flags from aclocal call
* Wed Jul  5 2006 - laca@sun.com
- rename to SFEldtp
- move to /usr
- update file attributes
* Fri Mar 24 2006 - damien.carbery@sun.com
- Bump to 0.4.0.
* Wed Mar 22 2006 - damien.carbery@sun.com
- Incorporate patch from maintainer (#335383).
* Tue Mar 21 2006 - damien.carbery@sun.com
- Bump to 0.3.1 and get it building.
* Fri Jul  1 2005 - damien.carbery@sun.com
- Initial version.

