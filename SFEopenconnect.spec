#
# spec file for package SFEopenconnect.spec
#
# includes module(s): openconnect
#

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	openconnect

Name:		SFEopenconnect
Version:	2.26
Summary:	Open client for Cisco AnyConnect VPN
Group:		Productivity/Networking/Security
License:	LGPLv2+
URL:		http://www.infradead.org/openconnect.html
Source:		ftp://ftp.infradead.org/pub/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

Requires:	SFEvpnc

%description
This package provides a client for Cisco's "AnyConnect" VPN, which uses
HTTPS and DTLS protocols.

%prep
%setup -q -n %{src_name}-%{version}

%build
export CC=gcc
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
make

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_libdir}
mv %{buildroot}/%{_prefix}/libexec/nm-openconnect-auth-dialog %{buildroot}/%{_libdir}
rmdir %{buildroot}/%{_prefix}/libexec
mkdir -p %{buildroot}/%{_mandir}/man1m
install -m 0644 openconnect.8 %{buildroot}/%{_mandir}/man1m/openconnect.1m
for i in %{buildroot}%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done



%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%doc TODO COPYING.LGPL
%{_bindir}/openconnect
%{_libdir}/nm-openconnect-auth-dialog
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_mandir}/man1m/*

%changelog
* Thu Dec 02 2010 - Milan Jurik
- Initial spec based on opensuse
