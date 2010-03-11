#
# spec file for package SFEcrrcsim
# Fly with OpenSolaris.
# Gilles Dauphin
#

%include Solaris.inc

Name:           SFEcrrcsim
Summary:        crrcsim flight simulator
Version:        0.9.9
Source:		http://surfnet.dl.sourceforge.net/sourceforge/crrcsim/crrcsim-%{version}.tar.gz
License:	GPLv2
URL:            http://crrcsim.berlios.de/wiki/
#Source1:	plib-01.sh
Patch1:		crrcsim-01.diff
Patch2:		crrcsim-02.diff
Patch3:		crrcsim-03.diff
Patch4:		crrcsim-04.diff
Patch5:		crrcsim-05.diff
Patch6:		crrcsim-06.diff
Patch7:		crrcsim-07.diff
Patch8:		crrcsim-08.diff
SUNW_BaseDir:   %{_basedir}
SUNW_Copyright:	%{name}.copyright
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include	default-depend.inc
#Requires:	%name-root
Requires: 	SFEfreeglut
Requires: 	SUNWxorg-mesa
Requires: 	SUNWxwice
Requires: 	SFEplib
Requires: 	SUNWlibsdl

#%package root
#Summary:         %summary - platform dependent files, / filesystem
#SUNW_BaseDir:            /
#%include default-depend.inc
#
#%package devel
#Summary:		 %summary - developer files
#SUNW_BaseDir:            %{_basedir}
#%include default-depend.inc
#Requires:		 %name

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:        %{name}
%endif

%prep
%setup -q -c -n %{name}
#cd crrcsim-%{version}
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0

%build

CC=cc
CXX=CC
LIBS="-lsocket -lnsl"
CPPFLAGS="-I%_includedir"
CFLAGS="-I%_includedir"
CXXFLAGS="-I%_includedir"
LDFLAGS="-L%_libdir -R%_libdir"
export CXX CC LIBS CFLAGS CXXFLAGS CPPFLAGS LDFLAGS
#PROTO_PKG=$RPM_BUILD_DIR/%{name}/usr/X11/lib/pkgconfig
#export PKG_CONFIG_PATH="$PROTO_PKG"

cd crrcsim-%{version}
./configure --prefix=%{_prefix} 
gmake

%install
CC=cc
CXX=CC
CFLAGS="-I%_includedir"
CXXFLAGS="-I%_includedir"
CPPFLAGS="-I%_includedir"
LIBS="-lsocket -lnsl"
LDFLAGS="-L%_libdir -R%_libdir"
export CXX CC LIBS CFLAGS CXXFLAGS CPPFLAGS LDFLAGS

rm -rf $RPM_BUILD_ROOT
cd crrcsim-%{version}
gmake install DESTDIR=$RPM_BUILD_ROOT

#%if %build_l10n
#%else
#rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_datadir}/games/
%{_datadir}/games/*
%dir %attr (0755, root, bin) %{_datadir}/doc/crrcsim
%{_datadir}/doc/crrcsim/*
#%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/*

#%if %build_l10n
#%files l10n
#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
#%endif

%changelog
* Mar 2010
- try to move it in /usr/SFE
* Nov 2 2008 - Gilles Dauphin ( Gilles DOT Dauphin AT enst DOT fr)
* Initial spec, fly simulator for OpenSolaris
