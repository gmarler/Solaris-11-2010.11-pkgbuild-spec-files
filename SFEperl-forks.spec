#
# spec file for package SFEperl-forks.spec
#
# includes module(s): perl-forks
#
%include Solaris.inc

%define perl_version	5.8.4

Name:		SFEperl-forks
Version:	0.34
Summary:	A drop-in replacement for Perl threads using fork()
Group:		Development/Libraries
License:	(GPL+ or Artistic) and (GPLv2+ or Artistic)
URL:		http://search.cpan.org/~rybskej/perl-forks-%{version}/
Source:		http://search.cpan.org/CPAN/authors/id/R/RY/RYBSKEJ/forks-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWgnu-findutils
Requires:	SUNWperl584core
BuildRequires:	SUNWperl584core
Requires:	SFEperl-list-moreutils
Requires:	SFEperl-sys-sigaction
Requires:	SFEperl-acme-damn

%description
The forks.pm module is a drop-in replacement for threads.pm.  It has the
same syntax as the threads.pm module (it even takes over its namespace) but
has some significant differences:

- you do _not_ need a special (threaded) version of Perl
- it is _much_ more economic with memory usage on OS's that support COW
- it is more efficient in the startup of threads
- it is slightly less efficient in the stopping of threads
- it is less efficient in inter-thread communication

If for nothing else, it allows you to use the Perl threading model in
non-threaded Perl builds and in older versions of Perl (5.6.0 and
higher are supported).


%prep
%setup -q -n forks-%{version}

%build
find . -type f -print | xargs chmod a-x
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}/man $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc CHANGELOG CREDITS README TODO
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man3/*.3
%{_prefix}/perl5/vendor_perl/%{perl_version}


%changelog
* Wed Jun 16 2010 - Milan Jurik
- Initial spec
