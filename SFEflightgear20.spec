#
# spec file for package SFEFligthGear.spec
# Gilles Dauphin
#
#
%include Solaris.inc

%define src_name	FlightGear
%define src_url		ftp://ftp.kingmont.com/flightsims/flightgear/Source

# TODO: make package with:
# http://www.flightgear.org/Docs/getstart/getstart.html
# http://mirrors.ibiblio.org/pub/mirrors/flightgear/ftp/Docs/getstart.pdf

Name:                   SFEFlightGear20
Summary:                Flight Simulator for 'true' airplane
Version:                2.0.0
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Source1:		ftp://ftp.de.flightgear.org/pub/fgfs/Shared/FlightGear-data-%{version}.tar.bz2
Group:			Applications/Games
Patch1:			FlightGear20-04.diff
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
Requires:		SFESimGear20
Requires:		SFEplib-gpp
Requires:		SFEboost
Requires:		SFEosg


%prep
%setup -q -c -n  %{name}
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}
export CC=/usr/gcc/4.3/bin/gcc
export CXX=/usr/gcc/4.3/bin/g++
export CFLAGS="-I%{_prefix}/X11/include"
export CXXFLAGS="-I%{_prefix}/X11/include"
export LDFLAGS="-L%{_libdir} -R%{_libdir} -L/usr/X11/lib -R/usr/X11/lib"
#CC=cc CXX=CC ./configure --without-logging --prefix==%{_prefix}
/bin/bash ./configure CONFIG_SHELL=/bin/bash --prefix=%{_prefix} \
	--with-osg=%{_prefix} \
	--with-boost=%{_prefix} \
	--with-boost-libdir=%{_libdir} \
	--with-plib=%{_prefix} \
	--with-simgear=%{_prefix}

make # -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd %{src_name}-%{version}
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/FlightGear
(cd $RPM_BUILD_ROOT/%{_datadir}/FlightGear ; gtar xfj %{SOURCE1} )


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/FlightGear
%{_datadir}/FlightGear/*
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*


%changelog
* May 2010 - G.D.
- update to 2.0
* Mar 2010 - Gilles Dauphin
- search includedir in /usr/SFE (exemple)
- that's where I install freeglut
* Mon Nov 20 2008 - dauphin@enst.fr
- Initial version
