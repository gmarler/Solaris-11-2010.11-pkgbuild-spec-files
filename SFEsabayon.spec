#
# spec file for package sabayon
#
# Copyright (c) 2010 Sun Microsystems, Inc.
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby 
#
%include Solaris.inc
%include default-depend.inc

%define python_version 2.6

Name:		sabayon
Summary:	Tool to maintain user profiles in a GNOME desktop
Version:	2.30.0
Release:	2
Distribution:	Java Desktop System
Vendor:		Gnome Community
License:	GPLv2+
Group:		Applications/System
Source0:	http://ftp.gnome.org/pub/GNOME/sources/sabayon/2.30/%{name}-%{version}.tar.bz2
URL:		http://www.gnome.org/projects/sabayon
SUNW_BaseDir:   /


BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%description
Sabayon is a tool to help sysadmins and user change and maintain the
default behaviour of the GNOME desktop.

%package admin
%include default-depend.inc
SUNW_BaseDir:   %{_basedir} 
Summary:	Graphical tools for Sabayon profile management
Group:		Applications/System


##OSOL Requres
Requires:       SFEpessulus
Requires:       SUNWgnome-python-libs
Requires:       SUNWgnome-python26-libs
#Requires:       xorg-x11-server-Xephyr 

%description admin
The sabayon-admin package contains the graphical tools which a
sysadmin should use to manage Sabayon profiles.


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
	    --mandir=%{_mandir}			\
	    --with-distro=debian

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2

make install  DESTDIR=$RPM_BUILD_ROOT

echo 'include "$(HOME)/.gconf.path.defaults"'  > $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/local-defaults.path
echo 'include "$(HOME)/.gconf.path.mandatory"' > $RPM_BUILD_ROOT%{_sysconfdir}/gconf/2/local-mandatory.path

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
   rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

   find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
   find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'
   find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'
   find $RPM_BUILD_ROOT -type f -name "*.pyc" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%pre admin
groupadd -g 225 sabayon
useradd -u 225 -d %{_datadir}/empty -c "Sabayon user" -g sabayon sabayon

%post admin
%restart_fmri desktop-mime-cache gconf-cache

%postun admin
%restart_fmri desktop-mime-cache gconf-cache

if [ "$1" -eq 0 ]; then
	userdel sabayon
	groupdel sabayon
fi

%files 
#%files apply -f sabayon.lang 
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO ISSUES sabayon.schema

%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/gconf/2/local-defaults.path
%config(noreplace) %{_sysconfdir}/gconf/2/local-mandatory.path

%attr(755,root,root) %{_sbindir}/sabayon-apply
%attr(755,root,root) %{_sysconfdir}/sabayon

%files admin
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/sabayon
%attr(755,root,root) %{_libexecdir}/sabayon-session


%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages/sabayon/
%{_libdir}/python%{python_version}/vendor-packages/sabayon/*

%dir %{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/locale/*
%{_datadir}/man/*
%{_datadir}/%{name}/ui/*
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg 
%defattr(-, root, root, -)
%doc %{_datadir}/gnome/help/sabayon/*
%doc %{_datadir}/omf/sabayon/* 

%changelog
* Mon Jul 12 2010 - <yuntong.jin@sun.com>
- Init spec file

