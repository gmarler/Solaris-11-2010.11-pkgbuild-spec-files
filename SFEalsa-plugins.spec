#
# spec file for package SFEalsa-plugins
#
# includes module(s): alsa-plugins
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use alsa64 = alsa-plugins.spec
%endif

%include base.inc
%use alsa = alsa-plugins.spec

%define oss      %(/usr/bin/pkginfo -q oss && echo 1 || echo 0)

Name:                    SFEalsa-plugins
Summary:                 %{alsa.summary}
Version:                 %{alsa.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
Group: 			 Audio
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %oss
BuildRequires: oss
%else
BuildRequires: SUNWaudh
%endif
BuildRequires: SUNWdbus-devel
Requires: SUNWdbus
BuildRequires: SFEalsa-lib-devel
Requires: SFEalsa-lib
BuildRequires: SUNWspeex-devel
Requires: SUNWspeex

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%alsa64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%alsa.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%alsa64.build -d %name-%version/%_arch64
%endif

%alsa.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%alsa64.install -d %name-%version/%_arch64
%endif

%alsa.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%config %{_sysconfdir}/asound.conf

%changelog
* Wed Oct 20 2010 - Milan Jurik
- bump to 1.0.23
* Fri Aug 15 2008 - glynn.foster@sun.com
- Add license and grouping
* Sun Aug 12 2007 - dougs@truemail.co.th
- Changed to build 64bit
* Sun Aug 12 2007 - dougs@truemail.co.th
- Initial version
