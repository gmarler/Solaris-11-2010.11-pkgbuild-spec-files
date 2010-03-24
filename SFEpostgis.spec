#
# NoCopyright 2009 - Gilles Dauphin (from Fedora 10)
#

%include Solaris.inc

%ifarch x86_64
%define java_arch amd64
%else
%define java_arch %{_arch}
%endif

%define src_name	postgis

Name:			SFEpostgis
Version:		1.3.6
Summary:		Spatial database capabilities for PostgreSQL
URL:			http://postgis.refractions.net/
License:		GPLv2+
SUNW_Copyright: 	%{name}.copyright
Group:			Applications/Databases
Source:			http://postgis.refractions.net/download/%{src_name}-%{version}.tar.gz
Patch1:			postgis-Makefile.diff
Patch2:			postgis-isinf.diff
Patch3:			postgis-Makefile2.diff
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
#Requires:		SPROcc
#Requires:		SPROcmpl
#Requires:		SPROcpl
Requires:		sunstudioexpress
Requires:		SUNWpmdbdpg
Requires:		SUNWgmake
Requires:		SUNWbtool
Requires:		SUNWcsu
Requires:		SUNWpng
Requires:		SUNWjpg
Requires:		SUNWgnu-readline
Requires:		SUNWpcre
Requires:		SUNWzlib
Requires:		postgres-83/developer
Requires:		postgres-83/library
Requires:		SUNWzlib
Requires:		SUNWzlib

Meta(info.upstream):		postgis.refractions.net
Meta(info.maintainer):		Gilles Dauphin
Meta(info.repository_url):	http://postgis.refractions.net/download

%description
PostGIS adds support for geographic objects to the PostgreSQL
object-relational database. In effect, PostGIS "spatially enables" the
PostgreSQL server, allowing it to be used as a backend spatial
database for geographic information systems (GIS), much like ESRI's
SDE or Oracle's Spatial extension. PostGIS follows the OpenGIS "Simple
Features Specification for SQL" and has been certified as compliant
with the "Types and Functions" profile.  PostGIS/PostgreSQL includes
the following functionality:
* Simple Features as defined by the OpenGIS Consortium (OGC)
* Support for Well-Known Text and Well-Known Binary
  representations of GIS objects
* Fast spatial indexing using GiST
* Geospatial analysis functions
* PostgreSQL JDBC extension objects corresponding to the
  geometries
* Support for OGC access functions as defined by the Simple
  Features Specification

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
# because of foreign -Wno-long-long !!! Argh :(
#export ac_cv_prog_CC="cc -m32"
#export CC="cc -m32"
#export CXX="CC -m32"
#export CXXFLAGS="-library=stlport4"
#export SHLIB_CXXFLAGS="-library=stlport4"
#export SHLIB_CXXLD="CC -m32 "
#export SHLIB_CXXFLAGS="-library=stlport4"
#export SHLIB_CXXLDFLAGS="-G -library=stlport4"

./configure 	--prefix=%{_prefix}                 \
    		--libexecdir=%{_libexecdir}         \
    		--mandir=%{_mandir}                 \
    		--datadir=%{_datadir}               \
    		--infodir=%{_datadir}/info	    \
		--with-pgsql=/usr/postgres/8.3/bin/pg_config

#    		--with-system-zlib --with-system-bzlib --with-system-pcre 

#make %{?_smp_mflags} LPATH=`pg_config --pkglibdir` shlib="%{name}.so"
gmake 

%install
rm -rf ${RPM_BUILD_ROOT}
gmake install DESTDIR=${RPM_BUILD_ROOT}
install -d  ${RPM_BUILD_ROOT}%{_datadir}/pgsql/contrib/
install -m 644 *.sql ${RPM_BUILD_ROOT}%{_datadir}/pgsql/contrib/
rm -f  ${RPM_BUILD_ROOT}%{_datadir}/*.sql

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0755, root, sys)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/pgsql
%dir %attr (0755, root, bin) %{_datadir}/pgsql/contrib
%{_datadir}/pgsql/contrib/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*


%changelog
* Aug 2009 - Gilles Dauphin
- add --with-pgsql=/usr/postgres/8.3/bin/pg_config (for b117)
* Fri Jun 26 2009 - Gilles Dauphin
- readline is in B117
* Fri Jun 26 2009 - Gilles Dauphin
- inital config 
