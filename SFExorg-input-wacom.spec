#
# spec file for package SFExorg-input-wacom
#
# includes module(s): xorg-input-wacom
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use wacom_64 = linuxwacom.spec
%endif

%include base.inc
%use wacom = linuxwacom.spec

Name:                   SFExorg-input-wacom
Summary:                %{wacom.summary}
Version:                %{wacom.version}
License:                GPLv2+
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWxorg-server
Requires: SUNWxwrtl
Requires: SUNWxwplt
BuildRequires: SUNWxorg-headers
Requires: SUNWhal
BuildRequires: SUNWhea
Requires: SUNWTcl

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:		 %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%{_arch64}
%wacom_64.prep -d %name-%version/%{_arch64}
%endif

mkdir %name-%version/%{base_arch}
%wacom.prep -d %name-%version/%{base_arch}

%build
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%wacom_64.build -d %name-%version/%{_arch64}
%endif

%wacom.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%wacom_64.install -d %name-%version/%{_arch64}
#rm -f $RPM_BUILD_ROOT%{_prefix}/X11/bin/*
#rm -f $RPM_BUILD_ROOT%{_prefix}/X11/lib/lib*so*
#rm -rf $RPM_BUILD_ROOT%{_prefix}/X11/lib/TkXInput
%endif
%wacom.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/bin
%{_prefix}/X11/bin/*
%dir %attr (0755, root, bin) %{_prefix}/X11/lib
%{_prefix}/X11/lib/lib*.so*
%{_prefix}/X11/lib/TkXInput
%dir %attr (0755, root, bin) %{_prefix}/X11/lib/modules
%dir %attr (0755, root, bin) %{_prefix}/X11/lib/modules/input
%{_prefix}/X11/lib/modules/input/*.so
%ifarch amd64 sparcv9
%{_prefix}/X11/lib/modules/input/%{_arch64}
%endif
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/hal
%{_libdir}/hal/*
%dir %attr (0755, root, bin) %{_prefix}/X11/share
%dir %attr (0755, root, bin) %{_prefix}/X11/share/man
%dir %attr (0755, root, bin) %{_prefix}/X11/share/man/man4
%{_prefix}/X11/share/man/man4/*
%dir %attr (0755, root, other) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/hal
%dir %attr (0755, root, sys) %{_datadir}/hal/fdi
%dir %attr (0755, root, sys) %{_datadir}/hal/fdi/policy
%dir %attr (0755, root, sys) %{_datadir}/hal/fdi/policy/20thirdparty
%{_datadir}/hal/fdi/policy/20thirdparty/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/include
%{_prefix}/X11/include/*

%changelog
* Sun Sep 20 2009 - Albert Lee <trisk@opensolaris.org>
- Add fdi file
- Add hal-setup-wacom
* Tue Dec 16 2008 - trisk@acm.jhu.edu
- Initial spec
