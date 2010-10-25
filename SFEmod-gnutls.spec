#
# spec file for package SFEmod-gnutls
#
# includes module(s): mod_gnutls
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use mod_gnutls_64 = mod_gnutls.spec
%endif

%include base.inc
%use mod_gnutls = mod_gnutls.spec

Name:		SFEmod-gnutls
Version:	%{mod_gnutls.version}
Summary:	%{mod_gnutls.summary}
Group:		System Environment/Daemons
License:	ASL 2.0
URL:		%{mod_gnutls.url}
Source:		http://www.outoforder.cc/downloads/mod_gnutls/mod_gnutls-%{version}.tar.bz2
Source1:	mod_gnutls.conf
Patch1:		mod_gnutls-01-extra.diff
Patch2:		mod_gnutls-02-wall.diff
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgawk
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SUNWapch22u
BuildRequires:	SUNWgnutls-devel
Requires:	SUNWapch22u
Requires:	SUNWgnutls

%description
mod_gnutls uses the GnuTLS library to provide SSL 3.0, TLS 1.0 and TLS 1.1
encryption for Apache HTTPD.  It is similar to mod_ssl in purpose, but does
not use OpenSSL.  A primary benefit of using this module is the ability to
configure multiple SSL certificates for a single IP-address/port combination
(useful for securing virtual hosts).
    
Features
    * Support for SSL 3.0, TLS 1.0 and TLS 1.1.
    * Support for client certificates.
    * Support for RFC 5081 OpenPGP certificate authentication.
    * Support for Server Name Indication.
    * Distributed SSL Session Cache via Memcached
    * Local SSL Session Cache using DBM
    * Sets enviromental vars for scripts (compatible with mod_ssl vars)
    * Small and focused code base:
         Lines of code in mod_gnutls: 3,593
         Lines of code in mod_ssl: 15,324

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%mod_gnutls_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%mod_gnutls.prep -d %name-%version/%{base_arch}


%build
%ifarch amd64 sparcv9
%mod_gnutls_64.build -d %name-%version/%_arch64
%endif

%mod_gnutls.build -d %name-%version/%{base_arch}


%install
rm -rf %{buildroot}
%ifarch amd64 sparcv9
%mod_gnutls_64.install -d %name-%version/%_arch64
%endif

%mod_gnutls.install -d %name-%version/%{base_arch}


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%config(noreplace) %{_sysconfdir}/apache2/2.2/conf.d/mod_gnutls.conf
%dir %attr (0755, root, sys) %{_prefix}
%{_prefix}/apache2/2.2/libexec/mod_gnutls.so
%ifarch amd64 sparcv9
%{_prefix}/apache2/2.2/libexec/%{_arch64}/mod_gnutls.so
%endif
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/cache/mod_gnutls

%changelog
* Mon Oct 25 2010 - Milan Jurik
- initial spec based on Fedora
