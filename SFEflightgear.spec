#
# spec file for package SFEFligthGear.spec
# Gilles Dauphin
#
#
%include Solaris.inc

%define src_name	FlightGear
%define src_url		ftp://ftp.kingmont.com/flightsims/flightgear/Source
# mirror that works sometime:
# http://flightgear.mxchange.org/pub/fgfs/Source/FlightGear-1.0.0.tar.gz
# http://mirror.fslutd.org/flightgear/Source/FlightGear-1.0.0.tar.gz
#ftp://ftp.kingmont.com/flightsims/flightgear/Source/FlightGear-1.0.0.tar.gz
# TODO: make package with:
# http://www.flightgear.org/Docs/getstart/getstart.html
# http://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Docs/getstart.pdf
# faire un package pour installer modele son et scene.
# ftp://ftp.flightgear.org/pub/fgfs/Shared/fgfs-base-1.0.0.tar.bz2

Name:                   SFEFlightGear
Summary:                Flight Simulator for 'true' airplane
Version:                1.0.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			FlightGear-01.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SFEopenal-devel
Requires:		SFEopenal
BuildRequires:		SFEfreealut-devel
Requires:		SFEfreealut
# Take care: needed freeglut-2.6.0-rc1
BuildRequires:		SFEfreeglut-devel
Requires:		SFEfreeglut
BuildRequires:		SFESimGear-devel
Requires:		SFESimGear
# TODO: somethings i don't understand
#BuildRequires:		SFEplib-devel
Requires:		SFEplib

#%package root
#Summary:                 %{summary} - root files
#SUNW_BaseDir:            %{_prefix}
#%include default-depend.inc

%prep
#%setup -q -n -c %{src_name}-%{version}
%setup -q -c -n  %{name}
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
export CC=cc
export CXX=CC
#CC=cc CXX=CC ./configure --without-logging --prefix==%{_prefix}
/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix}
make # -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

#%files devel
#%defattr (-, root, bin)
#%{_includedir}
#%dir %attr(0755,root,bin) %{_libdir}
#%dir %attr(0755,root,other) %{_libdir}/pkgconfig
#%{_libdir}/pkgconfig/*

%changelog
* Mon Nov 20 2008 - dauphin@enst.fr
- Initial version
