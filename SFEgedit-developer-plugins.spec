#
# spec file for package: Gedit Developer Plugins
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby 
#

%include Solaris.inc

Name:		gedit-developer-plugins
Summary:      	Plugins provides additional editing, checking, and project management features to Gedit
Version:       	0.4.0
License:	GPLv2
Url: 		https://launchpad.net/gdp/
Source:         http://launchpad.net/gdp/trunk/4.0/+download/%{name}-%{version}.tar.gz
Group:		Accessories
Vendor:		SUN

BuildRoot:      %{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:   /
SUNW_Copyright: %{name}.copyright
%include default-depend.inc

Requires:       SUNWgnome-text-editor
Requires:       SUNWgnome-python-desktop
Requires:       SUNWgnome-gtksourceview
Requires:       SUNWpython26 


BuildRequires:  SUNWgnome-text-editor-devel
BuildRequires:  SUNWgnome-doc-utils
BuildRequires:  SUNWgnome-base-libs
BuildRequires:  SUNWgnome-common-devel 
BuildRequires:  SUNWxwinc
BuildRequires:  SUNWxorg-headers
BuildRequires:  SUNWperl-xml-parser
BuildRequires:  SUNWgnome-doc-utils
BuildRequires:  SUNWgnome-base-libs
BuildRequires:  SUNWgnome-common-devel


%description
This project provides plugins for word and python symbol completion, text formatting,
syntax and style checking, find and replace in files, and Bazaar DVCS integration.
%prep
rm -rf %name-%version
%setup -q -n %name-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}			

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1    
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL   

%post
%restart_fmri gconf-cache desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/gedit-2/plugins/*

%changelog
* Mon Apr 27 2010 - yuntong.jin@sun.com 
- Initial spec
