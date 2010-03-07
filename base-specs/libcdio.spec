#
# spec file for package libcdio
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#

%define CBEgettext      %(/usr/bin/pkginfo -q CBEgettext && echo 1 || echo 0)

Name:         libcdio
License:      LGPL
Group:        System Environment/Libraries
Version:      0.82
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Utilities for CD interaction
URL:          http://www.gnu.org/software/libcdio/
Source:       http://ftp.gnu.org/gnu/libcdio/%{name}-%{version}.tar.gz
Patch1:       libcdio-01-usehal.diff
Patch2:       libcdio-02-stdint.diff
URL:          http://ftp.gnu.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%description
Utilities for CD interaction

%package devel
Summary: Headers for developing programs that will use libcdio
Group:      Development/Libraries
Requires:   %{name}

%description   devel
This package contains the headers that programmers will need to develop
applications which will use libcdio.

%prep
%setup -q
%if %with_hal
%patch1 -p1
%endif
%patch2 -p1

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

%if %CBEgettext
export ACLOCAL_FLAGS="-I `pkgparam CBEgettext BASEDIR`/share/aclocal"
%else
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
%endif

export LDFLAGS="$LDFLAGS -liconv"

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir} \
	--disable-cpp-progs --disable-cxx
make -j $CPUS

%install
make -i install DESTDIR=$RPM_BUILD_ROOT

# Clean up unpackaged files.
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*la

# Create symlink for compatibility with kdemultimedia
(cd $RPM_BUILD_ROOT%{_libdir}/; ln -s libcdio_paranoia.so libcdda_paranoia.so)

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/*.so*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so

%changelog
* Sun Mar 07 2010 - Milan Jurik
- update for 0.82
* Mon Dec 22 2008 - Thomas Wagner
- changed ACLOCAL_FLAGS to conditionally use m4 files from CBEgettext location (/opt/dtbld or /opt/jdsbld, ..) bcs. missing AM_GNU_GETTEXT_VERSION|AM_ICONV when using jds cbe 1.7.0(-rc1)
* Sun Aug 17 2008 - nonsea@users.sourceforge.net
- Move patch from SFElibcdio.spec
- Add -liconv to LDFLAGS to fix link issue.
* Fri Jul 11 2008 - andras.barna@gmail.com
- Add ACLOCAL_FLAGS, SFElibiconv dep, libcddb dep
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Add a compatibility symlink 
* Sat Nov 3 2007 - markwright@internode.on.net
- Bump to 0.79.  Add libcdio-02-stdint.diff.
* Thu Oct 18 2007 - laca@sun.com
- force using automake-1.9
* Wed Nov 01 2006 - damien.carbery@sun.com
- Bump to 0.78.2. Remove upstream patch, 01-noc++lib.
* Tue Mar 22 2006 - Brian.Cameron@sun.com
- Initial spec file checkin
