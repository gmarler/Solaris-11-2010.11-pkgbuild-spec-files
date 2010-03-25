#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFElibassuan
Summary:             An IPC libbray used by GnuPG 2, GPGME etc. 
Version:             1.0.5
Source:              ftp://ftp.gnupg.org/gcrypt/libassuan/libassuan-%{version}.tar.bz2

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWlibgpg-error
Requires: SUNWlibgpg-error
Requires: SUNWtexi

%prep
%setup -q -n libassuan-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}  \
	    --with-pth=yes    \
            --mandir=%{_mandir} \
	    --with-pth-prefix=%{_prefix}
            --infodir=%{_datadir}/info

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#rm -rf $RPM_BUILD_ROOT/usr/lib/*.a*
rm -rf $RPM_BUILD_ROOT/usr/share/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gawk gawkinet' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'gawk gawkinet' ;
  echo '"';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} --delete %{_infodir}/$info';
  echo 'done';
  echo 'exit 0' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*

%changelog
* Mars 25 2010 - Gilles Dauphin
- build with pth, add --with-pth-prefix
* Sat Jul 11 2009 - Thomas Wagner
- bump to 1.0.5
* Sat Dec 29 2007 - jijun.yu@sun.com
- Initial spec
