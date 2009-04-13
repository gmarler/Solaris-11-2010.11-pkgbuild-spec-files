%include Solaris.inc

%define src_name stardict
%define src_url http://downloads.sourceforge.net/stardict

Summary:	stardict
SUNW_BaseDir:   %{_basedir}
Name:		SUNWstardict
Version: 	3.0.1
Release:	1
License: 	GPLv3
Source: 	%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:         stardict-01-ss12.diff
BuildRoot:      %{_tmppath}/%{src_name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWlibpopt
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-panel
Requires: SUNWpostrun
Requires: SUNWstardict-root
Requires: SUNWespeak
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWespeak-devel

%package root
Summary:        %{summary} (ROOT)
SUNW_BaseDir:   /
%include default-depend.inc
Requires: SUNWgnome-base-libs-root
Requires: SUNWgnome-panel-root
Requires: SUNWpostrun-root

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
export CFLAGS="%optflags"
./autogen.sh --prefix=%{_prefix}        \
             --disable-festival         \
             --disable-advertisement    \
             --disable-gucharmap
make

%install
rm -rf ${RPM_BUILD_ROOT}
%makeinstall
find ${RPM_BUILD_ROOT} -name "*.a" -exec rm  {} \; -print
find ${RPM_BUILD_ROOT} -name "*.la" -exec rm {} \; -print

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files 
%defattr(-, root, bin)
%{_bindir}/*
%{_libdir}/bonobo/*
%{_libdir}/stardict/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%dir %attr (0755, root, other) %{_datadir}/applications
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%attr (0755, root, other) %{_datadir}/locale
%dir %attr (0755, root, bin) %{_datadir}/omf
%dir %attr (0755, root, bin) %{_datadir}/idl
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/omf/*
%{_datadir}/idl/*
%{_datadir}/stardict/*
%{_datadir}/gnome/*
%{_datadir}/man/*

%files root
%attr (0755, root, sys) %{_sysconfdir}

%changelog
* Tue Aug 26 2008 - yongsun@users.sourceforge.net
- Initial spec
