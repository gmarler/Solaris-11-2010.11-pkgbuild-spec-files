#
# spec file for packages SFEfarsight2
#
# includes module(s): farsight2
#
# Owner:jefftsai
#
%include Solaris.inc

%use farsight2= farsight2.spec

Name:                    SFEfarsight2
Summary:                 A library that binds farsight to the Connection Manager
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SFElibnice

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%farsight2.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CFLAGS="%optflags -DBSD_COMP"
export LDFLAGS="%_ldflags -lsocket -lnsl"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%farsight2.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%farsight2.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc farsight2-%{farsight2.version}/COPYING
%doc farsight2-%{farsight2.version}/NEWS
%doc farsight2-%{farsight2.version}/ChangeLog
%doc farsight2-%{farsight2.version}/AUTHORS
%doc farsight2-%{farsight2.version}/README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/lib*.so*
%{_libexecdir}/farsight2-0.0/lib*.so*
%{_libexecdir}/gstreamer-0.10/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/python2.6/*

%changelog
* Fri Oct 08 2010 - jeff.cai@oracle.com
- created
