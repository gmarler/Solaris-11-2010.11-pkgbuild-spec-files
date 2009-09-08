#
# spec file for package SFElibquicktime
#
# includes module(s): libquicktime
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libquicktime64 = libquicktime.spec
%endif

%include base.inc
%use libquicktime = libquicktime.spec

Name:		SFElibquicktime
Summary:	%{libquicktime.summary}
Version:	%{libquicktime.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEffmpeg-devel
Requires: SFEffmpeg
BuildRequires: SUNWgnome-base-libs-devel
%ifarch amd64 sparcv9
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis-devel
%endif

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libquicktime64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libquicktime.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libquicktime64.build -d %name-%version/%_arch64
%endif

%libquicktime.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libquicktime64.install -d %name-%version/%_arch64
%endif

%libquicktime.install -d %name-%version/%{base_arch}
find $RPM_BUILD_ROOT%{_libdir} -name \*.la -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/libquicktime_config
%{_bindir}/lqt_transcode
%{_bindir}/lqt-config
%{_bindir}/lqtplay
%{_bindir}/qt2text
%{_bindir}/qtdechunk
%{_bindir}/qtdump
%{_bindir}/qtinfo
%{_bindir}/qtrechunk
%{_bindir}/qtstreamize
%{_bindir}/qtyuv4toyuv
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/libquicktime
%{_libdir}/libquicktime/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale/
%dir %attr (0755, root, other) %{_datadir}/locale/de
%dir %attr (0755, root, other) %{_datadir}/locale/de/LC_MESSAGES
%{_datadir}/locale/de/LC_MESSAGES/*
%{_mandir}
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/libquicktime_config
%{_bindir}/%{_arch64}/lqt_transcode
%{_bindir}/%{_arch64}/lqt-config
%{_bindir}/%{_arch64}/lqtplay
%{_bindir}/%{_arch64}/qt2text
%{_bindir}/%{_arch64}/qtdechunk
%{_bindir}/%{_arch64}/qtdump
%{_bindir}/%{_arch64}/qtinfo
%{_bindir}/%{_arch64}/qtrechunk
%{_bindir}/%{_arch64}/qtstreamize
%{_bindir}/%{_arch64}/qtyuv4toyuv
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/libquicktime
%{_libdir}/%{_arch64}/libquicktime/*.so*
%endif

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Tue Sep 08 2009 - Milan Jurik
- update to 1.1.3
* Fri Feb 22 2007 - trisk@acm.jhu.edu
- Use SUNWogg-vorbis dependency (disabled for 64-bit)
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial version
