#
# spec file for package ggz-client-libs
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner migi
#

%define OSR 8489:0.0.14.1

Name:         ggz-client-libs
License:      LGPL
Group:        Amusements/Games
Version:      0.0.14.1
Release:      1
Distribution: Java Desktop System
Vendor:	      ggzgamingzone.org
Summary:      GGZ online gaming
Source:       http://mirrors.ibiblio.org/pub/mirrors/ggzgamingzone/ggz/%{version}/ggz-client-libs-%{version}.tar.gz
# owner:yippi date:2008-02-25 type:bug bugzilla:518756 state:upstream
Patch1:       ggz-client-libs-01-fixvoid.diff
# owner:migi date:2008-02-18 type:bug bugzilla:517215
Patch2:       ggz-client-libs-02-manpages.diff
# svn://svn.ggzgamingzone.org/svn/trunk/ggz-client-libs/po
# owner:fujiwara date:2008-02-27 type:bug state:upstream
Patch3:       ggz-client-libs-03-po.diff
# owner:migi date:2008-06-01
Patch4:       ggz-client-libs-04-manpages.diff
# owner:yippi date:2010-05-26 type:bug bugzilla:620303
Patch5:       ggz-client-libs-05-m4.diff
URL:          http://www.ggzgamingzone.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf

%description
The GGZ project makes free online gaming possible. We develop games and work
with other game projects to create a better environment for playing on the
internet.   ggz-client-libs are the client base libraries.  This includes
ggzcore for GGZ core clients and ggzmod for game clients.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

# create dummy config.rpath required by AC_REQUIRE_AUX_FILE
# otherwise automake complains and fails.
touch config.rpath

aclocal $ACLOCAL_FLAGS -I ./m4 -I ./m4/ggz
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} 	\
	    --sysconfdir=%{_sysconfdir} \
	    --bindir=%{_bindir} \
	    --libdir=%{_libdir} \
            --includedir=%{_includedir} \
	    --libexecdir=%{_libexecdir} \
	    --with-libggz-includes=%{libggz_build_dir}/src \
	    --with-libggz-libraries=%{libggz_build_dir}/src/.libs \
	    --disable-ggzwrap

make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed May 26 2010 - brian.cameorn@oracle.com
- Add patch ggz-client-libs-05-m4.diff so the code will compile.
* Fri Jun 06 2008 - Michal.Pryc@Sun.Com
- Added patch ggz-client-libs-04-manpages.diff.
* Wed Feb 27 2008 - takao.fujiwara@sun.com
- Add ggz-client-libs-03-po.diff to add it.po.
* Mon Feb 25 2008 - Brian.Cameron@sun.com
- Bump to 0.0.14.1.  Remove upstream patches.
* Mon Feb 18 2008 - Michal.Pryc@Sun.Com
- Added patch ggz-client-libs-03-manpages.diff which disables ggzwrap manpages
  if the module is build with --disable-ggzwrap. Bugzilla: 517215.
* Wed Jan 02 2008 - damien.carbery@sun.com
- Created.
