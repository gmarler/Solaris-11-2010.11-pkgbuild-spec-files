# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%use liblouis = liblouis.spec

Summary:	   %liblouis.summary
Name:              SFEliblouis
Version:           %{default_pkg_version}
SUNW_BaseDir:      %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:         %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%package devel
Summary:           %{summary} - development files
SUNW_BaseDir:      %{_basedir}
%include default-depend.inc
Requires:          %{name}

%prep
rm -rf %name-%version
mkdir %name-%version
%liblouis.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE | tar xf -

%build
%liblouis.build -d %name-%version

%install
%liblouis.install -d %name-%version
rm $RPM_BUILD_ROOT/%{_infodir}/dir

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'liblouis-guide.info' ;
  echo '"';
  echo 'retval=0';
  echo 'for info in $infos; do';
  echo '  install-info --info-dir=%{_infodir} %{_infodir}/$info || retval=1';
  echo 'done';
  echo 'exit $retval' ) | $PKG_INSTALL_ROOT/usr/lib/postrun -b -c SFE

%preun
( echo 'PATH=/usr/bin:/usr/sfw/bin; export PATH' ;
  echo 'infos="';
  echo 'liblouis-guide.info' ;
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
%{_libdir}/liblouis*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/liblouis.pc
%dir %attr (0755, root, bin) %{_infodir}
%defattr (0444, root, bin)
%{_infodir}/liblouis-guide.info
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/liblouis
%dir %attr (0755, root, sys) %{_datadir}/liblouis/doc
%{_datadir}/liblouis/doc/*
%dir %attr (0755, root, sys) %{_datadir}/liblouis/tables
%{_datadir}/liblouis/tables/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}/
%{_includedir}/liblouis/*

%changelog
* Fri Feb 13 2009 - Willie Walker
- Initial spec
