#
# spec file for package netpbm
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): netpbm
#

%include Solaris.inc
# use the --with-svn-code option to use svn co instead of the stable tarball
%define svn_url https://netpbm.svn.sourceforge.net/svnroot/netpbm/advanced

Name:                    netpbm
Summary:                 netpbm - network portable bitmap tools
License:                 BSD, GPLv2, IJG, Public Domain
URL:                     http://netpbm.sourceforge.net/
Distribution:            OpenSolaris
Vendor:                  OpenSolaris Community
%if %{?_with_svn_code:0}%{?!_with_svn_code:1}
# stable tarball build
Version:                 10.26.63
Source:                  http://downloads.sourceforge.net/netpbm/%{name}-%{version}.tgz
%else
# svn code
Version:                 10.35
%endif

Source1:		 netpbm-Makefile.conf

Patch1:			 netpbm-01-strings.diff
Patch2:			 netpbm-02-no-XDefs.diff
Patch3:                  netpbm-03-Makefile.manpage.diff

SUNW_Basedir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:          %{name}.copyright

%include default-depend.inc

BuildRequires:  SUNWbtool
BuildRequires:  SUNWgnu-coreutils
BuildRequires:  SUNWgmake
BuildRequires:  SUNWflexlex
BuildRequires:  web/wget

Requires: SUNWlibC
Requires: print/filter/ghostscript

# OpenSolaris IPS Manifest Fields
Meta(info.upstream):            Bryan Henderson<bryanh@giraffe-data.com>
Meta(info.repository_url):      http://downloads.sourceforge.net/netpbm/netpbm-10.26.63.tgz
Meta(info.maintainer):          Federico Beffa<beffa at ieee dot org>
Meta(info.detailed_url):        http://netpbm.sourceforge.net/
Meta(info.classification):      org.opensolaris.category.2008:Applications/Graphics and Imaging

%description 
Netpbm is a toolkit for manipulation of graphic images,
including conversion of images between a variety of different
formats. There are over 300 separate tools in the package including
converters for about 100 graphics formats.

%prep
%if %{?_with_svn_code:0}%{?!_with_svn_code:1}
# stable tarball build
%setup -q -n netpbm-%version
%patch3 -p1
%else
# svn checkout
rm -rf netpbm-%version
mkdir netpbm-%version
cd netpbm-%version
rm -rf netpbm
[ ! -f ../../SOURCES/netpbm-%version.tar.bz2 ] && {
    svn checkout %{svn_url} netpbm
    tar fcp - netpbm | bzip2 -c > ../../SOURCES/netpbm-%version.tar.bz2
}
[ ! -d netpbm ] && bunzip2 -c ../../SOURCES/netpbm-%version.tar.bz2 | tar fxp -
cd netpbm
%patch1 -p1
%patch2 -p1
%endif

cat Makefile.config.in %{SOURCE1} > Makefile.config
touch Makefile.depend

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="-lz"

%if %{?_with_svn_code:1}%{?!_with_svn_code:0}
# svn code
cd netpbm-%version
cd netpbm
%endif
make # -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
%if %{?_with_svn_code:1}%{?!_with_svn_code:0}
cd netpbm-%version
cd netpbm
%endif
mkdir $RPM_BUILD_ROOT
make package PKGDIR=$RPM_BUILD_ROOT/package

mkdir -p $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 README $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/COPYRIGHT.PATENT $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/copyright_summary $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/GPL_LICENSE.txt $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/HISTORY $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/INSTALL $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/netpbm.html $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/Netpbm.programming $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/README.DJGPP $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
install -c -m 0444 doc/USERDOC $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}

pushd $RPM_BUILD_ROOT/package/lib
ln -s libnetpbm.so.10 libnetpbm.so
cd ..
mv bin $RPM_BUILD_ROOT/%{_basedir}
mv include $RPM_BUILD_ROOT/%{_basedir}
mv lib $RPM_BUILD_ROOT/%{_basedir}
#mv man $RPM_BUILD_ROOT/%{_basedir}/share
rm -rf man
mv misc $RPM_BUILD_ROOT/%{_basedir}/share/netpbm
cd $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/package
rm -rf $RPM_BUILD_ROOT/%{_basedir}/share/man/web
#rm -rf $RPM_BUILD_ROOT/%{_basedir}/bin/doc.url
mv $RPM_BUILD_ROOT/%{_basedir}/bin/doc.url $RPM_BUILD_ROOT%{_pkg_docdir}-%{version}
echo "webdir=%{_pkg_docdir}-%{version}" > manweb.conf
echo "browser=firefox" >> manweb.conf
mkdir $RPM_BUILD_ROOT/etc
mv manweb.conf $RPM_BUILD_ROOT/etc
popd

# Create man pages
export PATH=`pwd`/buildtools:$PATH
mkdir netpbmdoc
pushd netpbmdoc
wget --recursive --relative http://netpbm.sourceforge.net/doc/
cd netpbm.sourceforge.net/doc
make -f ../../../buildtools/Makefile.manpage manpages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man5
make -f ../../../buildtools/Makefile.manpage MANDIR=$RPM_BUILD_ROOT%{_mandir} installman
popd
rm -rf netpbmdoc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc /%{_pkg_docdir}-%{version}/README
%doc /%{_pkg_docdir}-%{version}/COPYRIGHT.PATENT 
%doc /%{_pkg_docdir}-%{version}/copyright_summary 
%doc /%{_pkg_docdir}-%{version}/GPL_LICENSE.txt 
%doc /%{_pkg_docdir}-%{version}/HISTORY 
%doc /%{_pkg_docdir}-%{version}/INSTALL 
%doc /%{_pkg_docdir}-%{version}/netpbm.html 
%doc /%{_pkg_docdir}-%{version}/Netpbm.programming 
%doc /%{_pkg_docdir}-%{version}/README.DJGPP 
%doc /%{_pkg_docdir}-%{version}/USERDOC
%doc /%{_pkg_docdir}-%{version}/doc.url
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, bin) %{_mandir}
%attr (0444, root, bin) %{_mandir}/man?/*
%dir %attr (0755, root, bin) %{_datadir}/%{name}
%{_datadir}/%{name}/*
%attr (0644, root, root) /etc/manweb.conf

#%files devel
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* May 2010 - Gilles dauphin
- import from jucr
- install in /opt/SFE instead of /usr (optional)
* Wed Apr 14 2010 - beffa@ieee.org
- changed from man pages pointing to HTML doc to 
  autogenerated troff man pages.
* Thu Dec 3 2009 - beffa@ieee.org
- added standard header
* Wed Aug 5 2009 - beffa@ieee.org
- adapted from SFEnetpbm.spec
- changed to stable version 10.26.63
- included doc
* Wed Oct 17 2007 - laca@sun.com
- use stable tarball by default, use svn checkout with --with-svn-code
* Tue Sep 18 2007 - markwright@internode.on.net
- Add netpbm. to svn_url
- Comment netpbm-02-stdlib.diff, as stdlib.h now included in generator/ppmrough.c
- Add patch4 netpbm-03-no-XDefs.diff
* Sat Apr 21 2007 - dougs@truemail.co.th
- Disabled parallel make. Can be a problem on a multicpu system
* Wed Feb 28 2007 - markgraf@med.ovgu.de
- need to include stdlib.h in generator/ppmrough.c
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
