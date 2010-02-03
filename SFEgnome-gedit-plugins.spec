#
# spec file for package: gedit-plugins
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby 
#

%include Solaris.inc

Name:		gedit-plugins
Summary:      	Plugins for gedit
Version:       	2.28.0
License:	GPLv2
Url: 		http://live.gnome.org/Gedit/Plugins
Source:         http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.28/%{name}-%{version}.tar.bz2
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
BuildRequires:  SUNWgmake
BuildRequires:  SUNWgnu-automake-110
BuildRequires:  SUNWgnome-doc-utils
BuildRequires:  SUNWgnome-base-libs
BuildRequires:  SUNWgnome-common-devel
BuildRequires:  SUNWgnu-gettext


%description
Plugins for gedit including: bracketcompletion charmap codecomment colorpicker
drawspaces joinlines sessionsaver showtabbar smartspaces terminal 

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
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}                 \
            --infodir=%{_infodir}		\
            --sysconfdir=%{_sysconfdir}		\
            --disable-scrollkeeper

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1    
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL   

rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.pyo
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*/*.pyo

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gedit-show-tabbar-plugin.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/gedit-2/plugins/*
%{_datadir}/gedit-2/*
%{_datadir}/locale/*

%defattr (-, root, sys)
%dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/*

%changelog
* Wen Feb 03 2010 - yuntong.jin@sun.com
- Add dependency SUNWgnome-gtksourceview SUNWpython26
* Tue Jan 13 2010 - yuntong.jin@sun.com
- Bump to 2.28.0 and put it into SFE 
* Mon Apr 27 2009 - andras.barna@gmail.com
- Initial spec


