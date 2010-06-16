#
# spec file for package SFEperl-sys-sigaction.spec
#
# includes module(s): perl-sys-sigaction
#
%include Solaris.inc

%define perl_version	5.8.4

Name:		perl-sys-sigaction
Version:	0.11
Summary:	Perl extension for Consistent Signal Handling
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Sys-SigAction/
Source:		http://www.cpan.org/modules/by-module/Sys/Sys-SigAction-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:	SUNWperl584core
BuildRequires:	SUNWperl584core

%description
Sys::SigAction provides EASY access to POSIX::sigaction() for signal 
handling on systems that support sigaction().
It is hoped that with the use of this module, your signal handling 
behavior can be coded in a way that does not change from one perl 
version to the next, and that sigaction() will be easier for you to use.

%prep
%setup -q -n Sys-SigAction-%{version}
export PATH=/usr/perl5/bin:$PATH

pod2man < dbd-oracle-timeout.POD > dbd-oracle-timeout.man

%build
perl Makefile.PL INSTALLDIRS=vendor
make 

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}/man $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc Changes README dbd-oracle-timeout.man
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man3/*.3
%{_prefix}/perl5/vendor_perl/%{perl_version}

%changelog
* Wed Jun 16 2010 - Milan Jurik
- Initial spec
