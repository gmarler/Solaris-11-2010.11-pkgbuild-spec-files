#
# spec file for package SFEgsl
#
# includes module(s): gsl
#

%include Solaris.inc

%define src_url		http://ftp.gnu.org/gnu/gsl
%define src_name	gsl

Name:		SFEgsl
Summary:	The GNU Scientific Library is a numerical library for C and C++ programmers
Version:	1.14
Group:		Development/Libraries
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
URL:		http://www.gnu.org/software/gsl
License:	GPLv3
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CPPFLAGS="-D__sun__"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}         \
            --includedir=%{_includedir} \
            --datadir=%{_datadir}       \
            --mandir=%{_mandir}			\
            --infodir=%{_infodir}		\
            --enable-shared             \
            --disable-static

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gsl-ref.info  gsl-ref.info-1  gsl-ref.info-2  gsl-ref.info-3  gsl-ref.info-4  gsl-ref.info-5  gsl-ref.info-6' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gsl-ref.info  gsl-ref.info-1  gsl-ref.info-2  gsl-ref.info-3  gsl-ref.info-4  gsl-ref.info-5  gsl-ref.info-6' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/*.la
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_infodir}
%{_infodir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Jun 12 2010 - Milan Jurik
- bump to 1.14, removing "finite" patch
* Sun Nov 04 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial version
