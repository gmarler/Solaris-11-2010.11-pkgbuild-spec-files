#
# spec file for package SFElibgsm
#
# includes module(s): libgsm
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use libgsm_64 = libgsm.spec
%endif

%include base.inc
%use libgsm = libgsm.spec

Name:		SFElibgsm
Summary:	%{libgsm.summary}
Version:	%{libgsm.version}
License:	%{libgsm.license}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
This is a free and public implementation of GSM audio encoding and
decoding. The gsm library is used in many free software projects
including 'rplay', but has never been packaged as a stand-alone shared
library. GSM encoding has specific uses in transmission of packetized
audio over the Internet.

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
%libgsm_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libgsm.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%libgsm_64.build -d %name-%version/%_arch64
%endif

%libgsm.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libgsm_64.install -d %name-%version/%_arch64
%endif

%libgsm.install -d %name-%version/%{base_arch}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man1

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/man3

%changelog
* Tue Sep 08 2009 - Milan Jurik
- update to 1.0.13
- multiarch support
* Tue Dec 02 2008 - Giles Dauphin
- Fix to mandir ownership by Giles Dauphin (again sorry)
* Fri May 23 2008 - michal.bielicki@voiceworks.pl
- Fix to mandir ownership by Giles Dauphin
* Sun Jan 06 2008 - moinak.ghosh@sun.com
- Changed a failing install -d to mkdir -p
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
