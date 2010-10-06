# Copyright 2009-2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%use liblouisxml = liblouisxml.spec

Summary:	   %liblouisxml.summary
Name:              SFEliblouisxml
Version:           %{liblouisxml.version}
SUNW_BaseDir:      %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:         %{_tmppath}/%{name}-%{liblouisxml.version}-build

Requires:          SFEliblouis
BuildRequires:     SFEliblouis-devel

%include default-depend.inc

%package devel
Summary:           %{summary} - development files
SUNW_BaseDir:      %{_basedir}
%include default-depend.inc
Requires:          %{name}

%prep
rm -rf %name-%liblouisxml.version
mkdir %name-%liblouisxml.version
%liblouisxml.prep -d %name-%liblouisxml.version
cd %{_builddir}/%name-%liblouisxml.version
ls ../../SOURCES
gzcat ../../SOURCES/%{liblouisxml.name}-%{liblouisxml.version}.tar.gz | tar xf -

%build
%liblouisxml.build -d %name-%liblouisxml.version

%install
%liblouisxml.install -d %name-%liblouisxml.version
rm $RPM_BUILD_ROOT/%{_infodir}/dir

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{liblouisxml.version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'liblouisxml.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'liblouisxml.info' ;
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
%{_libdir}/liblouisxml*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/liblouisxml.pc
%dir %attr (0755, root, bin) %{_infodir}
%defattr (0444, root, bin)
%{_infodir}/liblouisxml.info
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/doc/liblouisxml
%{_datadir}/doc/liblouisxml/*
%dir %attr (0755, root, sys) %{_datadir}/liblouisxml
%{_datadir}/liblouisxml/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}/
%{_includedir}/liblouisxml/*

%changelog
* Wed Oct 06 2010 - Brian Cameron
- Initial spec
