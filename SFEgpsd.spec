#
# spec file for package: gpsd
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define src_name gpsd
%define pythonver 2.6

Name:		SFEgpsd
Version:	2.95
Summary:	Service daemon for mediating access to a GPS
Group:		System Environment/Daemons
License:	BSD
URL:		http://developer.berlios.de/projects/gpsd/
Source:		http://download.berlios.de/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:		gpsd-01-sunstudio.diff
Patch2:		gpsd-02-solaris.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:	%{_prefix}

BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWdbus-devel
Requires: SUNWdbus
BuildRequires: SUNWlxsl
BuildRequires: SUNWgawk
BuildRequires: SUNWncurses-devel
Requires: SUNWncurses

%description 
gpsd is a service daemon that mediates access to a GPS sensor
connected to the host computer by serial or USB interface, making its
data on the location/course/velocity of the sensor available to be
queried on TCP port 2947 of the host computer.  With gpsd, multiple
GPS client applications (such as navigational and wardriving software)
can share access to a GPS without contention or loss of data.  Also,
gpsd responds to queries with a format that is substantially easier to
parse than NMEA 0183.  

%package devel
Summary: Client libraries in C and Python for talking to a running gpsd or GPS
Group: Development/Libraries
Requires: %{name}

%description devel
This package provides C header files and python modules for the gpsd shared 
libraries that manage access to a GPS for applications

%package clients
Summary: Clients for gpsd
Group: Applications/System

%description clients
xgps is a simple test client for gpsd with an X interface. It displays
current GPS position/time/velocity information and (for GPSes that
support the feature) the locations of accessible satellites.

xgpsspeed is a speedometer that uses position information from the GPS.
It accepts an -h option and optional argument as for gps, or a -v option
to dump the package version and exit. Additionally, it accepts -rv
(reverse video) and -nc (needle color) options.

cgps resembles xgps, but without the pictorial satellite display.  It
can run on a serial terminal or terminal emulator.


%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="-I/usr/include/ncurses %{optflags}"
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib %{_ldflags}"

./configure --prefix=%{_prefix} \
	--enable-dbus \
	--enable-raw \
	--enable-squelch \
	--disable-libQgpsmm \
	--disable-static

make

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} pythondir=%{python_sitearch} install

# remove .la files
rm -f %{buildroot}%{_libdir}/libgps*.*a

mkdir -p %{buildroot}/%{_datadir}/applications
install -p -m 0644 packaging/X11/xgps.desktop %{buildroot}/%{_datadir}/applications
install -p -m 0644 packaging/X11/xgpsspeed.desktop %{buildroot}/%{_datadir}/applications

mkdir -p %{buildroot}%{_datadir}/gpsd
install -p -m 0644 packaging/X11/gpsd-logo.png %{buildroot}%{_datadir}/gpsd/gpsd-logo.png


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%doc README INSTALL COPYING
%{_sbindir}/gpsd
%{_bindir}/gpsprof
%{_bindir}/gpsmon
%{_bindir}/gpsctl
%{_libdir}/libgps*.so.*
%{_libdir}/python%{pythonver}/site-packages/gps*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man8/gpsd.8*
%{_mandir}/man1/gpsprof.1*
%{_mandir}/man1/gpsmon.1*
%{_mandir}/man1/gpsctl.1*

%files devel
%defattr(-, root, bin)
%doc TODO
%{_bindir}/gpsfake
%{_libdir}/libgps*.so
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%{_libdir}/python%{pythonver}/site-packages/gps/fake*
%{_includedir}/gps.h
%{_includedir}/libgpsmm.h
%{_includedir}/gpsd.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man1/gpsfake.1*
%{_mandir}/man3/libgps.3*
%{_mandir}/man3/libgpsmm.3*
%{_mandir}/man3/libgpsd.3*
%{_mandir}/man5/rtcm-104.5*
%{_mandir}/man5/srec.5*

%files clients
%defattr(-, root, bin)
%{_bindir}/cgps
%{_bindir}/gpscat
%{_bindir}/gpsdecode
%{_bindir}/gpspipe
%{_bindir}/gpxlogger
%{_bindir}/lcdgps
%{_bindir}/xgps
%{_bindir}/xgpsspeed
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/gps.1*
%{_mandir}/man1/gpsdecode.1*
%{_mandir}/man1/gpspipe.1*
%{_mandir}/man1/lcdgps.1*
%{_mandir}/man1/xgps.1*
%{_mandir}/man1/xgpsspeed.1*
%{_mandir}/man1/cgps.1*
%{_mandir}/man1/gpscat.1*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %{_datadir}/gpsd
%{_datadir}/gpsd/gpsd-logo.png


%changelog
* Wed Dec 29 2010 - Milan Jurik
- initial spec based on Fedora but no UBS support :-(
