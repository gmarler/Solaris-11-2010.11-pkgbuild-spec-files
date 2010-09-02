#
# spec file for package SFEperl-date-manip
#
# includes module(s): SFEperl-date-manip
#
%include Solaris.inc

%define perl_version 5.8.4

Name:		SFEperl-date-manip
Summary:	Date manipulation routines
Version:	5.56
License:	Artistic/GPL
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Date-Manip/
Source:		http://search.cpan.org/CPAN/authors/id/S/SB/SBECK/Date-Manip-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWperl584core
Requires:	SUNWperl584core

%description
This is a set of routines designed to make any common date/time manipulation
easy to do. Operations such as comparing two times, calculating a time a given
amount of time from another, or parsing international times are all easily
done. From the very beginning, the main focus of Date::Manip has been to be
able to do ANY desired date/time operation easily, not necessarily quickly.
Also, it is definitely oriented towards the type of operations we (as people)
tend to think of rather than those operations used routinely by computers.

%prep
%setup -n Date-Manip-%{version}

%build
perl Makefile.PL INSTALLDIRS="vendor" PREFIX="$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}"
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install

### Clean up buildroot
find $RPM_BUILD_ROOT -name .packlist -exec rm {} \;

### Clean up docs
find examples/ -type f -exec chmod a-x {} \;

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/man $RPM_BUILD_ROOT%{_mandir}

mv $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/lib/Date $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/
rm -r $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/lib

mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}
cp -r examples $RPM_BUILD_ROOT%{_docdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc HISTORY INSTALL LICENSE MANIFEST META.yml README README.FIRST TODO
%{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{name}/examples
%{_mandir}/man3/*.3


%changeLog
* Thu Sep 02 2010 - Milan Jurik
- Initial spec based on Fedora
