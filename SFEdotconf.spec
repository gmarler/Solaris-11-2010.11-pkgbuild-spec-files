# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%use dotconf = dotconf.spec

Summary:	   %dotconf.summary
Name:              SFEdotconf
Version:           %{dotconf.version}
SUNW_BaseDir:      %{_basedir}
SUNW_Copyright:    %{name}.copyright
BuildRoot:         %{_tmppath}/%{name}-%{dotconf.version}-build
Patch1:            dotconf-01-wall.diff

%include default-depend.inc

%package devel
Summary:           %{summary} - development files
SUNW_BaseDir:      %{_basedir}
%include default-depend.inc
Requires:          %{name}

%prep
rm -rf %name-%dotconf.version
mkdir %name-%dotconf.version
%dotconf.prep -d %name-%dotconf.version
cd %{_builddir}/%name-%dotconf.version
gzcat ../../SOURCES/%{dotconf.name}-%{dotconf.version}.tar.gz | tar xf -
cd %{dotconf.name}-%{dotconf.version}
%patch1 -p0

%build
%dotconf.build -d %name-%dotconf.version

%install
%dotconf.install -d %name-%dotconf.version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{dotconf.version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig/
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}/
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}/
%dir %attr (0755, root, other) %{_datadir}/aclocal/
%{_datadir}/aclocal/dotconf.m4

%changelog
* Mon Sep 14 2009 - Willie Walker
- Initial spec
