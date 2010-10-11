#
# spec file for packages SFEtelepathy-farsight
#
# includes module(s): telepathy-farsight
#
# Owner:jefftsai
#
%include Solaris.inc

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use telepathy_farsight64 = telepathy-farsight.spec
%endif

%include base.inc
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

%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%telepathy_farsight64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%telepathy_farsight.prep -d %name-%version/%base_arch

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%ifarch amd64 sparcv9
%telepathy_farsight64.build -d %name-%version/%_arch64
%endif
    
%telepathy_farsight.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%telepathy_farsight64.install  -d %name-%version/%_arch64
%endif
    
%telepathy_farsight.install -d %name-%version/%base_arch

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/telepathy-farsight-%{telepathy_farsight.version} COPYING NEWS ChangeLog AUTHORS README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}

%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%ifarch sparcv9 amd64
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%{_libdir}/pkgconfig/*.pc
%{_libdir}/python2.6/*
%attr(755, root, bin) %{_includedir}/telepathy-1.0/*

%changelog
* Fri Oct 08 2010 - jeff.cai@oracle.com
- created
