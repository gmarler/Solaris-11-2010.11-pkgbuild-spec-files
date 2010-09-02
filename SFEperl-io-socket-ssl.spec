#
# spec file for package SFEperl-io-socket-ssl
#
# includes module(s): perl-io-socket-ssl
#
%include Solaris.inc

%define perl_version 5.8.4

Name:		SFEperl-io-socket-ssl
Version:	1.33
Summary:	Perl library for transparent SSL
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/IO-Socket-SSL/
Source:		http://search.cpan.org/CPAN/authors/id/S/SU/SULLR/IO-Socket-SSL-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWperl584core
Requires:	SUNWperl584core

%description
This module is a true drop-in replacement for IO::Socket::INET that
uses SSL to encrypt data before it is transferred to a remote server
or client. IO::Socket::SSL supports all the extra features that one
needs to write a full-featured SSL client or server application:
multiple SSL contexts, cipher selection, certificate verification, and
SSL version selection. As an extra bonus, it works perfectly with
mod_perl.

%prep
%setup -q -n IO-Socket-SSL-%{version}

%build
export PATH=$PATH:/usr/perl5/bin

perl Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}/man $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}
cp -r docs certs example util $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc BUGS Changes README
%{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{name}/docs
%{_docdir}/%{name}/certs
%{_docdir}/%{name}/example
%{_docdir}/%{name}/util
%{_mandir}/man3/*.3

%changeLog
* Thu Sep 02 2010 - Milan Jurik
- Initial spec based on Fedora
