#
# spec file for package SFElibmusicbrainz3
#
# includes module(s): libmusicbrainz3
#
%include Solaris.inc

%define SFEfftw   %(/usr/bin/pkginfo -q SFEfftw && echo 1 || echo 0)

Name:		SFElibofa
Summary:	library for accesing MusicBrainz servers
Version:	0.9.3
License:	LGPL
Source:		http://musicip-libofa.googlecode.com/files/libofa-%{version}.tar.gz
Patch1:         libofa-01-libadd.diff
Patch2:         libofa-02-libadd2.diff
Patch3:         libofa-03-missinghdrs.diff 
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%if %SFEfftw
Requires: SFEfftw
BuildRequires: SFEfftw-devel
%else
BuildRequires:	SUNWfftw3
Requires:	SUNWfftw3
%endif

%prep
%setup -q -n libofa-%version
%patch1 -p0
%patch2 -p0
%patch3 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure -prefix %{_prefix} \
           --sysconfdir %{_sysconfdir} \
           --enable-shared=yes \
           --enable-static=no

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CMAKE_INSTALL_PREFIX=/usr
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Wed Apr  7 2010 - Miroslav Osladil <mira@osladil.cz>
- updated source url to Google Code
* Sat Jun 13 2009 - Milan Jurik
- support for SUNWfftw3
* Sun Jun 29 2008 - river@wikimedia.org
- fftw is required
- some examples are missing <unistd.h> and do not build
- need to link with -lc -lCrun -lCstd, as -xnolib is specified
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Initial Spec.
