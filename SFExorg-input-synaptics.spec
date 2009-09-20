#
# spec file for package SFExorg-input-synaptics
#
# includes module(s): xorg-input-synaptics
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use synaptics_64 = xf86-input-synaptics.spec
%endif

%include base.inc
%use synaptics = xf86-input-synaptics.spec

Name:                   SFExorg-input-synaptics
Summary:                %{synaptics.summary}
Version:                %{synaptics.version}
License:                MIT
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWxorg-server
Requires: SUNWxwrtl
Requires: SUNWxwplt
BuildRequires: SUNWxorg-headers

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
%synaptics_64.prep -d %name-%version/%{_arch64}
%endif

mkdir %name-%version/%{base_arch}
%synaptics.prep -d %name-%version/%{base_arch}

%build
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%synaptics_64.build -d %name-%version/%{_arch64}
%endif

%synaptics.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%synaptics_64.install -d %name-%version/%{_arch64}
%endif
%synaptics.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_prefix}/X11
%dir %attr (0755, root, bin) %{_prefix}/X11/bin
%{_prefix}/X11/bin/*
%dir %attr (0755, root, bin) %{_prefix}/X11/lib
%dir %attr (0755, root, bin) %{_prefix}/X11/lib/modules
%dir %attr (0755, root, bin) %{_prefix}/X11/lib/modules/input
%{_prefix}/X11/lib/modules/input/*.so
%ifarch amd64 sparcv9
%{_prefix}/X11/lib/modules/input/%{_arch64}
%endif
%dir %attr (0755, root, bin) %{_prefix}/X11/share
%dir %attr (0755, root, bin) %{_prefix}/X11/share/man
%dir %attr (0755, root, bin) %{_prefix}/X11/share/man/man1
%{_prefix}/X11/share/man/man1/*
%dir %attr (0755, root, bin) %{_prefix}/X11/share/man/man7
%{_prefix}/X11/share/man/man7/*
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
%dir %attr (0755, root, bin) %{_prefix}/X11/include/xorg
%{_prefix}/X11/include/xorg/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Sep 20 2009 - Albert Lee <trisk@opensolaris.org>
- Add fdi file
* Mon Mar 02 2009 - Albert Lee
- Initial spec
