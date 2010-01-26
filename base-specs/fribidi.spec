# spec file for package fribidi
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

Name:        fribidi 
Version:     0.19.2
Release:     1
Summary:     Library implementing the Unicode Bidirectional Algorithm
Copyright:   LGPL
URL:         http://fribidi.org/
Source:      http://fribidi.org/download/%{name}-%{version}.tar.gz
BuildRoot:   %{_tmppath}/%{name}-%{version}-root

%description
A library to handle bidirectional scripts (eg. hebrew, arabic), so that
the display is done in the proper way; while the text data itself is
always written in logical order.

%package -n %{name}
Summary: Library implementing the Unicode Bidirectional Algorithm
Group: System/Libraries
Provides: lib%{name}
Provides: lib%{name}-devel
%description -n %{name}
A library to handle bidirectional scripts (eg. hebrew, arabic), so that
the display is done in the proper way; while the text data itself is
always written in logical order.

Install %{name} if you want to run or develop programs that use %{name}.


%package -n lib%{name}
Summary: Library implementing the Unicode Bidirectional Algorithm
Group: System/Libraries
Conflicts: %{name}
%description -n lib%{name}
The lib%{name} package includes the shared libraries for the %{name} package.

nstall lib%{name} if you want to run programs which use %{name}.


%package -n lib%{name}-devel
Summary: Library implementing the Unicode Bidirectional Algorithm
Group: Development/C
Requires: lib%{name} = %{ver}
Conflicts: %{name}
%description -n lib%{name}-devel
The lib%{name}-devel package includes the static libraries and header files
for the %{name} package.

Install lib%{name}-devel if you want to develop programs which will use
%{name}.

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

%files
%defattr(-,root,root)
%doc README AUTHORS COPYING ChangeLog TODO THANKS NEWS
%{_bindir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/*.so.*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*

%files -n lib%{name}
%defattr(-, root, root)
%doc README AUTHORS COPYING ChangeLog TODO THANKS NEWS
%{_bindir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/*.so.*

%files -n lib%{name}-devel
%defattr(-, root, root)
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Sun Aug 17 2008 - nonsea@users.sourceofrge.net
- Bump to 0.19.1
* Fri Oct 19 2007 - nonsea@users.sourceforge.net
- Initial spec
