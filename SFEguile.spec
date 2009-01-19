#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEguile
URL:                 http://www.gnu.org/software/guile/
Summary:             Embeddable Scheme implementation written in C
Version:             1.8.5
Source:              http://ftp.gnu.org/pub/gnu/guile/guile-%{version}.tar.gz
Patch1:              guile-01-autoconf.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnu-mp
Requires: SUNWlibtool
Requires: SUNWltdl
Requires: SUNWlibm

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:      %{name}

%prep
%setup -q -n guile-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags -I/usr/include/gmp"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I . -I m4"

#libtoolize --copy --force
#aclocal $ACLOCAL_FLAGS
#autoheader
#automake -a -c -f
#autoconf
./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --infodir=%{_datadir}/info \
            --enable-static=no

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir

#create site folder
mkdir -p $RPM_BUILD_ROOT%{_datadir}/guile/site

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%{_datadir}/guile/*
%{_datadir}/info/*
%dir %attr (0755, root, bin) %{_datadir}/emacs
%dir %attr (0755, root, bin) %{_datadir}/emacs/site-lisp
%{_datadir}/emacs/site-lisp/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Jan 18 2009 - halton.huo@sun.com
- Change SFEgmp to SUNWgnu-mp
- Add patch autoconf.diff to fix AM_INTL_SUBDIR not found issue
* Tue Sep 02 2008 - halton.huo@sun.com
- Add /usr/share/aclocal to ACLOCAL_FLAGS to fix build issue
* Tue Jun 24 2008 - nonsea@users.sourceforge.net
- Add site dir
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Bump to 1.8.5
- Remove upstreamed patches: suncc-inline.diff,
  var-imaginary.diff and define-function.diff.
- Update %files 
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Update Requires
* Thu Oct 25 2007 - nonsea@users.sourceforge.net
- Bump to 1.8.3 
- Add patch define-function.diff
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 1.8.2
- Use default automake and aclocal
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Fix Source from ftp to http.
* Sat Apr 21 2007 - dougs@truemail.co.th
- Use automake-1.9 and aclocal-1.9
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 1.8.1.
- Add patch suncc-inline.diff and var-imaginary.diff
- Seperate package -devel
- Add Requires/BuildRequries after check-deps.pl run.
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency. Add %post/%preun to update the info dir file.
* Wed Dec 20 2006 - Eric Boutilier
- Initial spec
