#
# spec file for package SFEplib	
# for games on OpenSolaris. Keep cool !!!
# Gilles Dauphin
#

%include Solaris.inc

Name:           SFEplib
Summary:        plib
Version:        1.8.5
Source:		http://plib.sourceforge.net/dist/plib-%{version}.tar.gz
URL:		http://plib.sourceforge.net/
License:        GPLv2
SUNW_Copyright: %{name}.copyright
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
#Requires: 	SFEfreeglut
Requires: 	SUNWxorg-mesa
Requires: 	SUNWxwice
BuildRequires:	SUNWaudh

%package devel
Summary:		 %summary - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -c -n %{name}

%build

CC=cc
export CC
CXX=CC
export CXX

#PROTO_LIB=$RPM_BUILD_DIR/%{name}/usr/X11/lib
#PROTO_INC=$RPM_BUILD_DIR/%{name}/usr/X11/include
#PROTO_PKG=$RPM_BUILD_DIR/%{name}/usr/X11/lib/pkgconfig
#export PKG_CONFIG_PATH="$PROTO_PKG"

cd plib-%{version}
./configure --prefix=%_basedir
gmake

%install
CC=cc
export CC
CXX=CC
export CXX

rm -rf $RPM_BUILD_ROOT
cd plib-%{version}
#gmake install DESTDIR=$RPM_BUILD_ROOT/%_basedir
gmake install DESTDIR=$RPM_BUILD_ROOT

#%if %build_l10n
#%else
#rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}/plib

#%if %build_l10n
#%files l10n
#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
#%endif

%changelog
* Mon May 03 2010 - Milan Jurik
- fix packaging
* Fri Apr 30 2010 - Milan Jurik
- added missing build dependency
* Mars 02 2010 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
- no need of freeglut
* Nov 1 2008 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
* Initial spec, more funny tools for OpenSolaris ;)
