#
# spec file for package SFEperl-mail-imapclient
#
# includes module(s): perl-mail-imapclient
#
%include Solaris.inc

%define perl_version 5.8.4

Name:		SFEperl-mail-imapclient
Version:	3.25
Summary:	An IMAP Client API
Group:		Development/Libraries
License:	GPL+ or Artistic
URL:		http://search.cpan.org/dist/Mail-IMAPClient/
Source:		http://search.cpan.org/CPAN/authors/id/P/PL/PLOBBES/Mail-IMAPClient-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWperl584core
Requires:	SUNWperl584core


%description
This module provides perl routines that simplify a sockets connection 
to and an IMAP conversation with an IMAP server. 

%prep
%setup -q -n Mail-IMAPClient-%{version}
sed -i 's#/usr/local/bin/perl#/usr/bin/perl#' examples/*.pl

%build
# the extended tests cannot be run without an IMAP server
yes n | perl Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
chmod -R u+w $RPM_BUILD_ROOT/*

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}/man $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc Changes COPYRIGHT README
%{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man3/*.3

%changelog
* Thu Sep 02 2010 - Milan Jurik
- Initial spec based on Fedora
