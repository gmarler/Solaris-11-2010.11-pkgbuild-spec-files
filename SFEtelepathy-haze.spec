#
# spec file for packages SFEtelepathy-haze
#
# includes module(s): telepathy-haze
#
# Owner:alfred
#
%include Solaris.inc

%use telepathy_haze = telepathy-haze.spec

Name:                    SFEtelepathy-haze
Summary:                 A connection manager based on libpurple for IM protocols.
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%prep
rm -rf %name-%version
mkdir %name-%version
%telepathy_haze.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%telepathy_haze.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT

%telepathy_haze.install -d %name-%version

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libexecdir}
%{_libexecdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%doc(bzip2) telepathy-haze-%{telepathy_haze.version}/COPYING
%doc(bzip2) telepathy-haze-%{telepathy_haze.version}/NEWS
%doc(bzip2) telepathy-haze-%{telepathy_haze.version}/ChangeLog
%doc telepathy-haze-%{telepathy_haze.version}/AUTHORS
%doc telepathy-haze-%{telepathy_haze.version}/README
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/dbus-1/*
%{_datadir}/man/*
%{_datadir}/telepathy/*

%changelog
* Wed Feb 11 2009 - alfred.peng@sun.com
- created
