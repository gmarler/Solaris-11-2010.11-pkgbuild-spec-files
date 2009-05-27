#
# spec file for packages SFEtelepathy-idle
#
# includes module(s): telepathy-idle
#
# Owner:elaine_sun
#
%include Solaris.inc

%use telepathy_idle = telepathy-idle.spec

Name:                    SFEtelepathy-idle
Summary:                 An IRC connection manager for Telepathy framework. 
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%telepathy_idle.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%telepathy_idle.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%telepathy_idle.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc telepathy-idle-%{telepathy_idle.version}/COPYING
%doc telepathy-idle-%{telepathy_idle.version}/NEWS
%doc telepathy-idle-%{telepathy_idle.version}/ChangeLog
%doc telepathy-idle-%{telepathy_idle.version}/AUTHORS
%doc telepathy-idle-%{telepathy_idle.version}/README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/dbus-1/*
%{_datadir}/man/*
%{_datadir}/telepathy/*

%changelog
* Wed May 27 2009 - elaine.xiong@sun.com
- created
