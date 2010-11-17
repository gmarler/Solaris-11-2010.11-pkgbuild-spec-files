#
# spec file for package SFEperl-file-rsyncp
#
# includes module(s): File-RsyncP
#
%include Solaris.inc

%define perl_version 5.8.4

Name:		SFEperl-file-rsyncp
Version:	0.70
Summary:	A perl implementation of an Rsync client
License:	GPLv2
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/File-RsyncP/
Source:		http://search.cpan.org/CPAN/authors/id/C/CB/CBARRATT/File-RsyncP-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires:	SUNWperl584usr

%description
File::RsyncP is a perl implementation of an Rsync client.  It is
compatible with Rsync 2.x (protocol versions up to 28).  It can send
or receive files, either by running rsync on the remote machine, or
connecting to an rsyncd deamon on the remote machine.

%prep
%setup -q -n File-RsyncP-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
make

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}/man $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc Changes LICENSE README
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_prefix}/perl5/vendor_perl/%{perl_version}
%{_mandir}/man3/*

%changelog
* Wed Nov 17 2010 - Milan Jurik
- initial import to SFE based on Fedora
