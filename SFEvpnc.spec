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
Requires: SFEtun
BuildRequires: SFEtun

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
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} PREFIX=%{_prefix} ETCDIR=%{_sysconfdir}/vpnc MANDIR=%{_mandir}

# no section 8
install -d 0755 %{buildroot}%{_datadir}/man/man1m
for i in %{buildroot}%{_datadir}/man/man8/*.8
do
  base=`basename $i 8`
  name1m=${base}1m
  mv $i %{buildroot}%{_datadir}/man/man1m/${name1m}
done
rmdir %{buildroot}%{_datadir}/man/man8
for i in %{buildroot}%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done


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
%{_mandir}


%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/vpnc

%changelog
* Thu Dec 02 2010 - Milan Jurik
- fix build on the latest Solaris builds
- no man8 on Solaris
* Fri Jul 18 2008 - trisk@acm.jhu.edu
- Initial spec
