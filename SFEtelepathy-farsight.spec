#
# spec file for packages SFEtelepathy-farsight
#
# includes module(s): telepathy-farsight
#
# Owner:jefftsai
#
%include Solaris.inc

%use telepathy_farsight = telepathy-farsight.spec

Name:                    SFEtelepathy-farsight
Summary:                 A library that binds farsight to the Connection Manager
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%telepathy_farsight.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%telepathy_farsight.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%telepathy_farsight.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc telepathy-farsight-%{telepathy_farsight.version}/COPYING
%doc telepathy-farsight-%{telepathy_farsight.version}/NEWS
%doc telepathy-farsight-%{telepathy_farsight.version}/ChangeLog
%doc telepathy-farsight-%{telepathy_farsight.version}/AUTHORS
%doc telepathy-farsight-%{telepathy_farsight.version}/README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_libdir}/pkgconfig/*.pc
%{_libdir}/python2.6/*
%attr(755, root, bin) %{_includedir}/telepathy-1.0/*

%changelog
* Fri Oct 08 2010 - jeff.cai@oracle.com
- created
