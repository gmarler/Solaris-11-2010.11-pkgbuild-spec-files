#
# spec file for package nautilus-sendto
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:halton
#

Name:		nautilus-sendto
License:	GPL v2
Group:		Development/Libraries
Version:	2.28.0
Release:	1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:		http://www.gnome.org/
Summary:	Nautilus context menu for sending files
Source:		http://download.gnome.org/sources/%{name}/2.28/%{name}-%{version}.tar.bz2
# date:2008-06-03 owner:halton type:bug bugzilla:601632
Patch1:         %{name}-01-gthread.diff
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires:  gtk2-devel
BuildRequires:  libglade2-devel
BuildRequires:  evolution-data-server-devel >= 1.9.1
BuildRequires:  libgnomeui-devel
BuildRequires:  nautilus-devel >= 2.5.4
BuildRequires:  pidgin-devel >= 2.0.0
BuildRequires:  gettext
BuildRequires:  perl-XML-Parser intltool
BuildRequires:  dbus-glib-devel >= 0.70

%description
The nautilus-sendto package provides a Nautilus context menu for
sending files via other desktop applications.  These functions are
implemented as plugins, so nautilus-sendto can be extended with
additional features.  This package provides a default plugin for
Evolution integration.

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

libtoolize --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
	    --bindir=%{_bindir} \
	    --mandir=%{_mandir} \
	    --libdir=%{_libdir} \
	    --datadir=%{_datadir} \
	    --includedir=%{_includedir} \
	    --sysconfdir=%{_sysconfdir} \
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
%doc AUTHORS ChangeLog COPYING NEWS
%{_libdir}/nautilus/extensions-2.0/libnautilus-sendto.so
%{_libdir}/nautilus-sendto
%{_datadir}/nautilus-sendto
%{_bindir}/nautilus-sendto
%{_sysconfdir}/gconf/schemas/nst.schemas
%{_mandir}/man1/nautilus-sendto.1.gz

%changelog
* Thu Nov 12 2009 - halton.huo@sun.com
- Initial spec.
