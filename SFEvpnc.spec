#
# spec file for package SFEvpnc
#
# Owner: trisk
%include Solaris.inc
Name:                    SFEvpnc
Summary:                 vpnc - client for Cisco VPN concentrator
URL:                     http://www.unix-ag.uni-kl.de/~massar/vpnc/
Version:                 0.5.3
Source:                  http://www.unix-ag.uni-kl.de/~massar/vpnc/vpnc-%{version}.tar.gz
Patch1:                  vpnc-01-nogcc.diff
Patch2:                  vpnc-02-solaris.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %name-root
Requires: SUNWlibgcrypt
BuildRequires: SUNWlibgcrypt-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n vpnc-%version
%patch1 -p1
%patch2 -p1

%build
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

make CC=$CC
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} ETCDIR=%{_sysconfdir}/vpnc MANDIR=%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/vpnc
%{_docdir}/vpnc/*
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/vpnc

%changelog
* Fri Jul 18 2008 - trisk@acm.jhu.edu
- Initial spec
