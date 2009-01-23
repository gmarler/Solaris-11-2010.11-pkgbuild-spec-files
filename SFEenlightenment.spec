# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
#
# bugdb: http://trac.enlightenment.org/e/report 
#
%include Solaris.inc
%include base.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	e16-0
%define src_version	16.8.15
%define pkg_release	1
# %{_topdir} is by default set to RPM_BUILD_ROOT
# Default path for RPM_BUILD_ROOT is /var/tmp/pkgbuild-{username}
# Install the software here as part of package building steps

# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
Name:         	Enlightenment
Summary:      	Enlightenment - light weight X window manager
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2
Group:          User Interface/Desktops
Source:         %{sf_download}/enlightenment/%{src_name}.%{version}.tar.gz
# Reported as bug #199
Patch1:         enlightenment-01-bourneshell.diff
Vendor:       	Refer URL
URL:            http://enlightenment.org
Packager:     	SFE
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build
SUNW_BaseDir:   %{_basedir}

Source1:		Xinitrc.E
Source2:		Xsession.E
Source3:		Xsession2.E
Source4:		Xresources.E


#Ideally these should be included for requires: glib2, gtk2, pango
Requires:                SFEimlib2
#BuildRequires: 

%description 
Enlightenment - light weight X window manager

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}.%{version}
%patch1 -p1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

./configure --prefix=%{_prefix}            

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#Below steps integrate Enlightenment with dtlogin
mkdir -p $RPM_BUILD_ROOT/usr/dt/config/C/Xresources.d
cp %{SOURCE1} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE2} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE3} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE4} $RPM_BUILD_ROOT/usr/dt/config/C/Xresources.d

rm $RPM_BUILD_ROOT%{_libdir}/e16/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%defattr(-,root,bin)
%dir %attr (0755, root, bin) /usr/dt
%dir %attr (0755, root, bin) /usr/dt/config
%dir %attr (0755, root, bin) /usr/dt/config/C
%dir %attr (0755, root, bin) /usr/dt/config/C/Xresources.d
/usr/dt/config/C/Xresources.d/*
%attr (0755, root, bin) /usr/dt/config/Xinitrc.E
%attr (0755, root, bin) /usr/dt/config/Xsession.E
%attr (0755, root, bin) /usr/dt/config/Xsession2.E

%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/e16/*
%{_datadir}/xsessions/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/e16/*

%changelog
* Thu Jan 15 2008 - brian.cameron@sun.com
- Remove .la files from libdir.
* Sat Jan 10 2008 - brian.cameron@sun.com
- Add patch enlightenment-01-bourneshell.diff so the startup script uses
  bourne shell syntax, so it works on Nevada.
* Mon Jan 05 2008 - brian.cameron@sun.com
- Bump to 16.8.15.  Fix packaging.
* Tue Oct 22 2008 - Pradhap Devarajan <pradhap (at) gmail.com>
- Bump to 16.8.14.
* 2007.Nov.15 - <shivakumar dot gn at gmail dot com>
- Initial spec.

