# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
%include Solaris.inc
%include base.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	e16-0
%define src_version	16.8.10
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
%{_datadir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/e16/*

%changelog
* 2007.Nov.15 - <shivakumar dot gn at gmail dot com>
- Initial spec.

