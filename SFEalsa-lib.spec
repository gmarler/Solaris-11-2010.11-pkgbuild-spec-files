#
# spec file for package SFEalsa-lib
#
# includes module(s): alsa-lib
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use alsalib64 = alsa-lib.spec
%endif

%include base.inc
%use alsalib = alsa-lib.spec

Name:                    SFEalsa-lib
Summary:                 %{alsalib.summary}
Version:                 %{alsalib.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
Group:			 Audio
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%alsalib64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%alsalib.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%alsalib64.build -d %name-%version/%_arch64
%endif

%alsalib.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%alsalib64.install -d %name-%version/%_arch64
%endif

%alsalib.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/aserver
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/alsa-lib
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/alsa
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/aserver
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/alsa-lib
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
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Wed Oct 20 2010 - Milan Jurik
- bump to 1.0.23
* Fri Aug 15 2008 - glynn.foster@sun.com
- Add license and group
* Sat Sep 22 2007 - dougs@truemail.co.th
- Added SFEgcc requirement
* Sun Aug 12 2007 - dougs@truemail.co.th
- Fixed headers for easier building of apps
* Sat Aug 11 2007 - dougs@truemail.co.th
- Initial version
