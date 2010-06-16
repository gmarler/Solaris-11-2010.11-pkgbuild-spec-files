#
# spec file for package SFEperl-acme-damn
#
# includes module(s): perl-acme-damn
#
%include Solaris.inc

%define perl_version	5.8.4

Name:		perl-acme-damn
Version:	0.04
Summary:	Unbless Perl objects
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Acme-Damn/
Source:		http://search.cpan.org/CPAN/authors/id/I/IB/IBB/Acme-Damn-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires:	SUNWperl584core
BuildRequires:	SUNWperl584core


%description
Acme::Damn provides a single routine, damn(), which takes a blessed
reference (a Perl object), and unblesses it, to return the original
reference. I can't think of any reason why you might want to do this,
but just because it's of no use doesn't mean that you shouldn't be
able to do it.

%prep
%setup -q -n Acme-Damn-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}/man $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc Changes README
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man3/*.3
%{_prefix}/perl5/vendor_perl/%{perl_version}

%changelog
* Wed Jun 16 2010 - Milan Jurik
- Initial spec
