#
# spec file for package libggz
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner migi
#

%define OSR 8489:0.0.14.1

Name:         libggz
License:      LGPL
Group:        Amusements/Games
Version:      0.0.14.1
Release:      1
Distribution: Java Desktop System
Vendor:	      GGZ Online Gaming
Summary:      GGZ online gaming
Source:       http://mirrors.ibiblio.org/pub/mirrors/ggzgamingzone/ggz/%{version}/libggz-%{version}.tar.gz
# owner:migi date:2008-03-06 type:bug
Patch1:       libggz-01-config.diff
URL:          http://www.ggzgamingzone.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf


%description
The GGZ project makes free online gaming possible. We develop games and work
with other game projects to create a better environment for playing on the
internet   The libggz library wraps many common low-level functions used by
GGZ.

%prep
%setup -q
%patch1 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

#aclocal $ACLOCAL_FLAGS
#automake -a -c -f
#autoconf
./configure --prefix=%{_prefix} 	\
	    --sysconfdir=%{_sysconfdir} \
	    --bindir=%{_bindir} \
	    --libdir=%{_libdir} \
            --includedir=%{_includedir} \
	    --libexecdir=%{_libexecdir} \
            --with-tls \
            --with-gcrypt

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sun May 11 2008 - Michal.Pryc@Sun.Com
- Enabled encryption functionality.
  libgzz is classified under the ECCN (Export Control 
  Classification Number) 5D002. 

* Fri Mar 08 2008 - Michal.Pryc@Sun.Com
- Added libggz-01-config.diff. Disabled encryption functionallity

* Mon Feb 25 2008 - brian.cameron@sun.com
- Bump to 0.0.14.1.  Remove upstream patch.

* Wed Dec 19 2007 - damien.carbery@sun.com
- Add %install section.

* Tue Dec 18 2007 - damien.carbery@sun.com
- Created.
