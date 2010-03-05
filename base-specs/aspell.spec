#
# License (c) 2005 Sun Microsystems Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=245&atid=100245&aid=
#
Name:     	aspell
Version: 	0.60.4
Release:        356
Vendor:		Sun Microsystems, Inc.
Distribution:	Java Desktop System
License:	LGPL
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:         %{_datadir}/doc
Autoreqprov:	on
URL:		http://www.sun.com/software/javadesktopsystem/
Epoch:		2
Source:		ftp://ftp.gnu.org/gnu/aspell/%{name}-%{version}.tar.gz
# date:2004-05-27 type:bug owner:yippi bugzilla:1415029
Patch1:		aspell-01-forte.diff
Summary:	A spelling checker.
Group:		Applications/Text
Obsoletes:	pspell < 0.50
Obsoletes:	aspell-en-gb < 0.50
Obsoletes:	aspell-en-ca < 0.50
Obsoletes:	aspell-en < 0.50

%description
Aspell is a spelling checker designed to eventually replace Ispell.
It also has support for checking (La)TeX and Html files, and run time
support for other non-English languages.

%files
%defattr(-, root, root)
%doc README TODO
%{_bindir}/*
%{_datadir}/*
%{_libdir}/lib*.so.*
%{_libdir}/aspell

%package -n aspell-devel
Summary:	Static libraries and header files for aspell
Group:		Applications/Text
Requires:	aspell => %{version}-%{release}
Obsoletes:	pspell-devel < 0.50

%description -n aspell-devel
Aspell is a spelling checker. The aspell-devel package includes the
static libraries and header files needed for Aspell development.  Note
that the recommend way to use aspell is through the Pspell library.

%files -n aspell-devel
%defattr(-, root, root)
%{_libdir}/*.so*
%{_includedir}/*

%prep
%setup  -q -n %{name}-%{version}
%patch1 -p1

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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I ./m4
autoconf
automake -a -c -f

%ifos solaris
%define curses_options "--disable-wide-curses"
%else
%define curses_options ""
%endif

# For some reason, wide curses fails on Solaris, so disabling for now.
./configure \
    --prefix=%{_prefix} \
    --sysconfdir=/etc \
    --mandir=%{_mandir} \
    --infodir=%{_datadir}/info \
    --localstatedir=/var %{curses_options} \
    --enable-pkgdatadir=%{_libdir}/aspell  \
    --enable-pkglibdir=%{_libdir}/aspell

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT mkdir_p="mkdir -p"
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_datadir}/info

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Tue Mar 12 2007 - jeff.cai@sun.com
- Move to sourceforge from opensolaris.
* Thu Apr 20 2006 - halton.huo@sun.com
- Change pkgdatadir and pkglibdir to %{_libdir}/aspell, request by 
  LSARC/2006/231.
- Delete *.la and *.a in %install.
* Fri Jan 27 2006 - damien.carbery@sun.com
- Remove libtool hack as forte bug is fixed.
* Wed Jan 25 2006 - brian.cameron@sun.com
- Updated so aspell 0.60.4 now builds.  Added --disable-wide-curses when
  building on Solaris, since this causes build problems.
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 0.60.4.
* Fri Sep 09 2005 - laca@sun.com
- make it not crash when built with libtool 1.5.20
* Wed Sep 07 2005 - laca@sun.com
- run autoconf; remove libtool hack -- no longer needed
* Fri Aug 05 2005 - laca@sun.com
- simplify spec file
* Fri Jan 28 2005 - takao.fujiwara@sun.com
- Fix the wrong description by script failure.
* Fri Jan 14 2005 - damien.carbery@sun.com
- Fix 5108760: Remove Epoch macro, causing dependency problem with YaST.
* Mon Aug 23 2004 - niall.power@sun.com
- Add Epoch macro to requires feild of the devel package.
  Under rpm4 rules it won't install without it.
* Fri Aug 20 2004 - damien.carbery@sun.com
- Delete *.la in %install so they are not reported as unpackaged files.
* Thu May 27 2004 - laca@sun.com
- added patch to compile with Forte
- hack libtool to work around a forte bug
