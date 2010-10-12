#
# spec file for packages SFEtelepathy-gabble
#
# includes module(s): telepathy-gabble
#
# Owner:jefftsai
#
%include Solaris.inc

%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use telepathy_gabble64 = telepathy-gabble.spec
%endif

%include base.inc
%use telepathy_gabble = telepathy-gabble.spec

Name:                    SFEtelepathy-gabble
Summary:                 A Jabber/XMPP connection manager
Version:                 %{telepathy_gabble.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version

%ifarch amd64 sparcv9
mkdir -p %name-%version/%_arch64
%telepathy_gabble64.prep -d %name-%version/%_arch64
%endif

mkdir -p %name-%version/%base_arch
%telepathy_gabble.prep -d %name-%version/%base_arch

%build
export CFLAGS="%optflags -DBSD_COMP"
export LDFLAGS="%_ldflags -lsocket -lnsl"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

%ifarch amd64 sparcv9
%telepathy_gabble64.build -d %name-%version/%_arch64
%endif
    
%telepathy_gabble.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%telepathy_gabble64.install  -d %name-%version/%_arch64
%endif
    
%telepathy_gabble.install -d %name-%version/%base_arch

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d %{base_arch}/telepathy-gabble-%{telepathy_gabble.version} COPYING NEWS ChangeLog AUTHORS README
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}

%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/*
%endif
%{_libdir}/telepathy-gabble
%{_libdir}/telepathy/gabble-0/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/man/*
%{_datadir}/doc/telepathy-gabble/*
%{_datadir}/dbus-1/*
%{_datadir}/telepathy/*

%changelog
* Oct 12 2010 - jeff.cai@oracle.com
- created
