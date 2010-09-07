#
# spec file for package gnome-js-common
#
# Copyright (c) 2010 Sun Microsystems, Inc.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#
%include Solaris.inc
%include default-depend.inc

Summary:	Common modules for GNOME JavaScript bindings

Name:		gnome-js-common
Version:	0.1.2
Release:	1
License:	GPL v3
Group:		Libraries
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gnome-js-common/0.1/%{name}-%{version}.tar.bz2

SUNW_BaseDir:   /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%description
This package provides common modules for GNOME JavaScript bindings.


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


intltoolize --copy --force --automake
libtoolize --force
aclocal 
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}			\
	    --sysconfdir=%{_sysconfdir}		\
	    --libexecdir=%{_libexecdir}		\
	    --localstatedir=%{_localstatedir}   \
	    --mandir=%{_mandir}			


make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/gnome_js_common

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%{_libdir}/gnome-js
%{_libdir}/pkgconfig/*.pc

%define date	%(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%changelog
* Tue Sep 07 2010 - <yuntong.jin@sun.com>
- Init spec file
