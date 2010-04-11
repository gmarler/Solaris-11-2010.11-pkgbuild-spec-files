# spec file for package fribidi
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:        fribidi 
Version:     0.19.2
Summary:     Library implementing the Unicode Bidirectional Algorithm
Group:       System/Libraries
License:     LGPL
URL:         http://fribidi.org/
Source:      http://fribidi.org/download/%{name}-%{version}.tar.gz
BuildRoot:   %{_tmppath}/%{name}-%{version}-root

%prep
%setup -q

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

./configure --prefix=%{_prefix}		\
	    --libdir=%{_libdir}		\
	    --bindir=%{_bindir}		\
	    --includedir=%{_includedir}	\
	    --sysconfdir=%{_sysconfdir}	\
	    --datadir=%{_datadir}       \
	    --mandir=%{_mandir}

make -j $CPUS
 
%install
rm -rf ${RPM_BUILD_ROOT}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf ${RPM_BUILD_ROOT}

%changelog
* Sun Apr 11 2010 - Milan Jurik
- cleanup for the latest pkgtool
* Sun Aug 17 2008 - nonsea@users.sourceofrge.net
- Bump to 0.19.1
* Fri Oct 19 2007 - nonsea@users.sourceforge.net
- Initial spec
