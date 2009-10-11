# =========================================================================== 
#                    Spec File for Geany
# =========================================================================== 
%include Solaris.inc
%include base.inc

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Software specific variable definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%define src_name	fluxbox
%define src_version	1.1.1
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
Name:         	%{src_name}
Summary:      	fluxbox - light weight X window manager
Version:      	%{src_version}
Release:      	%{pkg_release}
License:      	GPLv2
Group:          User Interface/Desktops
Source:         %{sf_download}/fluxbox/%{src_name}-%{version}.tar.bz2
Patch1:         fluxbox-01-generatemenu.diff
Vendor:       	Refer URL
URL:            http://fluxbox.sourceforge.net
Packager:     	SFE
BuildRoot:		%{_tmppath}/%{src_name}-%{version}-build
SUNW_BaseDir:   %{_basedir}

Source1:		Xinitrc.fluxbox
Source2:		Xsession.fluxbox
Source3:		Xsession2.fluxbox
Source4:		Xresources.fluxbox
Source5:		fluxbox.desktop


#Ideally these should be included for requires: glib2, gtk2, pango
#Requires:      
#BuildRequires: 

%description 
Fluxbox is an X window manager based on Blackbox. Aiming to be lightweight and customizable, Fluxbox has minimal support for graphical icons. The Fluxbox interface has only a taskbar and a menu that is accessible by right-clicking on the desktop. All basic configurations of Fluxbox are controlled by text files.

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Packages to build
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 


#Requires:                %{name}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Prep-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%prep 
%setup -q -n %{src_name}-%{version}
%patch1 -p1

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Build-Section 
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++

# export CFLAGS="%optflags"
# export CFLAGS="-O4 -fPIC -DPIC -i -fno-omit-frame-pointer"
#%if %option_with_fox
#export CFLAGS="$CFLAGS -I/usr/X11/include"
#%endif
#export CXXFLAGS="%cxx_optflags"
#export LDFLAGS="%_ldflags"

aclocal $ACLOCAL_FLAGS
automake -a -c -f
./configure --prefix=%{_prefix}            

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#Below steps integrate fluxbox with dtlogin
mkdir -p $RPM_BUILD_ROOT/usr/dt/config/C/Xresources.d
cp %{SOURCE1} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE2} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE3} $RPM_BUILD_ROOT/usr/dt/config
cp %{SOURCE4} $RPM_BUILD_ROOT/usr/dt/config/C/Xresources.d
mkdir -p $RPM_BUILD_ROOT/usr/share/xsessions
cp %{SOURCE5} $RPM_BUILD_ROOT/usr/share/xsessions


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%defattr(-,root,bin)
%dir %attr (0755, root, bin) /usr/dt
%dir %attr (0755, root, bin) /usr/dt/config
%dir %attr (0755, root, bin) /usr/dt/config/C
%dir %attr (0755, root, bin) /usr/dt/config/C/Xresources.d
/usr/dt/config/C/Xresources.d/*
%attr (0755, root, bin) /usr/dt/config/Xinitrc.fluxbox
%attr (0755, root, bin) /usr/dt/config/Xsession.fluxbox
%attr (0755, root, bin) /usr/dt/config/Xsession2.fluxbox


%changelog
* Sun Oct 11 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 1.1.1.
* 2007.Nov.15 - <shivakumar dot gn at gmail dot com>
- Initial spec.

