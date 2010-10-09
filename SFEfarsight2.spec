#
# spec file for packages SFEfarsight2
#
# includes module(s): farsight2
#
# Owner:jefftsai
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use farsight264 = farsight2.spec
%endif

%include base.inc
%use farsight2= farsight2.spec

Name:                    SFEfarsight2
Summary:                 A library that binds farsight to the Connection Manager
Version:                 %{farsight2.version}
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
%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%farsight264.prep -d %name-%version/%_arch64
%endif
    
mkdir -p %name-%version/%base_arch
%farsight2.prep -d %name-%version/%base_arch

%build
export CFLAGS="%optflags -DBSD_COMP"
export LDFLAGS="%_ldflags -lsocket -lnsl"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%ifarch amd64 sparcv9
%farsight264.build -d %name-%version/%_arch64
%endif
    
%farsight2.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%farsight264.install -d %name-%version/%_arch64
%endif
 
%farsight2.install -d %name-%version/%base_arch

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/farsight2-%{farsight2.version} COPYING NEWS 
%doc -d %{base_arch}/farsight2-%{farsight2.version} ChangeLog AUTHORS README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/farsight2-0.0/lib*.so*
%{_libdir}/%{_arch64}/gstreamer-0.10/lib*.so*
%endif
%{_libdir}/lib*.so*
%{_libdir}/farsight2-0.0/lib*.so*
%{_libdir}/gstreamer-0.10/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*

%files devel
%defattr (-, root, bin)
%ifarch sparcv9 amd64
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/python2.6/*

%changelog
* Fri Oct 08 2010 - jeff.cai@oracle.com
- created
