#
# spec file for package libgda
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#


Name:		libgda
License:        LGPLv2
Group:		Development/Libraries
Version:	3.99.9
Release:	1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://www.gnome-db.org/
Summary:	Library for writing gnome database programs
Source:		http://download.gnome.org/sources/%{name}/3.99/%{name}-%{version}.tar.bz2
Source1:        libgda-jdbc-MANIFEST.MF
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires:    pkgconfig >= 0.8
Requires:         glib2 >= 2.0.0
Requires:         libxml2
Requires:         libxslt >= 1.0.9
Requires:         ncurses
BuildRequires:    glib2-devel >= 2.0.0
BuildRequires:    libxml2-devel
BuildRequires:    libxslt-devel >= 1.0.9
BuildRequires:    ncurses-devel
BuildRequires:    scrollkeeper
BuildRequires:    groff
BuildRequires:    readline-devel

%description
libgda is a library that eases the task of writing
gnome database programs.

%package devel
Summary:          Development libraries and header files for libgda.
Group:            Development/Libraries
Requires:         glib2-devel >= 2.0.0
Requires:         libxml2-devel
Requires:         libxslt-devel >= 1.0.9
Requires:         %{name} = %{epoch}:%{version}-%{release}

%description devel
This package contains the header files and libraries needed to write
or compile programs that use libgda.

%prep
%setup -q
# FIXME: remove SOURCE1 after bugzilla #568388 is fixed
cp %SOURCE1 providers/jdbc/MANIFEST.MF

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --datadir=%{_datadir} \
            --includedir=%{_includedir} \
            --sysconfdir=%{_sysconfdir} \
            --without-mysql \
            %gtk_doc_option

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README NEWS
%dir %{_sysconfdir}/libgda-%{short_version}
%config(noreplace) %{_sysconfdir}/libgda-%{short_version}/config
%{_bindir}/*
%{_datadir}/libgda-%{short_version}
%{_libdir}/*.so.*
%dir %{_libdir}/libgda-%{short_version}
%dir %{_libdir}/libgda-%{short_version}/providers
%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/libgda-%{short_version}
%dir %{_includedir}/libgda-%{short_version}/
%{_includedir}/libgda-%{short_version}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Tue Jan 20 2009 - halton.huo@sun.com
- Bump to 3.99.9
- Remove upstreamed patch suncc-empty-struct.diff
- Remove upstreamed patch sys_errlist.diff
- Add SOURCE1 to fix bugzilla #568388
* Sun Jan 18 2009 - halton.huo@sun.com
- Initial spec
