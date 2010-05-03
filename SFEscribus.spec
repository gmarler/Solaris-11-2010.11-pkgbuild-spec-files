#
# spec file for package SFEscribus
# Gilles Dauphin
# look at http://davekoelmeyer.wordpress.com/2010/03/09/build-scribus-1-3-5svn-on-opensolaris-x64/
#

%include Solaris.inc


Name:           SFEscribus-ng
Summary:        Graphical desktop publishing (DTP) application
Group:		Applications/Office
Version:        1.3.6
#Source:		http://sourceforge.net/projects/scribus/files/scribus-devel/1.3.6/scribus-1.3.6.tar.bz2/download
Source:		http://jaist.dl.sourceforge.net/project/scribus/scribus-devel/1.3.6/scribus-1.3.6.tar.bz2
#Patch1:		scribus-01.diff
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
#Requires:	%name-root

BuildRequires: 	SFEqt45
Requires: 	SFEqt45

Requires: 	SUNWgmake
BuildRequires: 	SUNWPython

SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%description
Scribus is a GUI desktop publishing (DTP) application for GNU/Linux.


%prep
%setup -q -c -n %{name}
#%patch1 -p0

%build
cd scribus-%{version}
mkdir builddir
cd builddir
# use gcc because SFEqt45 is build whith
export CC=/usr/gcc/4.3/bin/gcc
export CXX=/usr/gcc/4.3/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -fno-omit-frame-pointer"
export LD="/usr/bin/ld"
export PATH="/usr/gcc/4.3/bin:$PATH"
#export LDFLAGS="%_ldflags"

cmake -DHAVE_GCC_VISIBILITY:INTERNAL=0 -DCMAKE_INSTALL_PREFIX:PATH=%_prefix -DHAVE_VISIBILITY_SWITCH:INTERNAL=0 .. 
make


%install
rm -rf $RPM_BUILD_ROOT
cd scribus-%{version}
cd builddir
mkdir -p $RPM_BUILD_ROOT/%_prefix
export CC=/usr/gcc/4.3/bin/gcc
export CXX=/usr/gcc/4.3/bin/g++
export CFLAGS="-O4 -fPIC -DPIC -fno-omit-frame-pointer"
export LD="/usr/bin/ld"
export PATH="/usr/gcc/4.3/bin:$PATH"
export DESTDIR=$RPM_BUILD_ROOT
make install
#make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_includedir}
# Todo
#%dir %attr(0755, root, other) %{_datadir}/applications
%{_bindir}/scribus
#TODO
#%{_datadir}/gnome/apps/Applications/scribus.desktop
%{_datadir}/mime/packages/scribus.xml
# TODO
#%{_datadir}/pixmaps/scribus.png
#%{_datadir}/pixmaps/scribusicon.png
%{_datadir}/scribus
%{_includedir}/scribus/
%{_libdir}/scribus/
%{_datadir}/doc
#%{_datadir}/doc/scribus-%{version}./
%{_datadir}/mimelnk
%{_datadir}/man


%changelog
* 29 Apr 2010 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- Initial spec
