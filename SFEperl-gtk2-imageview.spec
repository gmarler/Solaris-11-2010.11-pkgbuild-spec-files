#
# spec file for package SFEperl-gtk2-imageview
#
# includes module(s): perl-gtk2-imageview
#
%include Solaris.inc

%define tarball_version 0.05
%define perl_version 5.8.4

Name:		SFEperl-gtk2-imageview
Version:	%{tarball_version}
Summary:	Perl bindings to the GtkImageView image viewer widget
Group:		Development/Libraries
License:	LGPLv3
URL:		http://search.cpan.org/dist/Gtk2-ImageView/
Source0:	http://search.cpan.org/CPAN/authors/id/R/RA/RATCLIFFE/Gtk2-ImageView-%{tarball_version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWperl584core
Requires:	SUNWperl584core

BuildRequires:	SFEperl-extutils-pkg
BuildRequires:	SFEperl-extutils-dep
Requires:	SFEperl-glib
Requires:	SFEperl-gtk2
BuildRequires:	SFEgtkimageview
Requires:	SFEgtkimageview

%description
Perl bindings to the GtkImageView image viewer widget.
Find out more about GtkImageView at http://trac.bjourne.webfactional.com/.

The Perl bindings follow the C API very closely, and the C reference
should be considered the canonical documentation.

%prep
%setup -q -n Gtk2-ImageView-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make 

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}/man $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_prefix}/perl5/%{perl_version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc AUTHORS COPYING.LESSER INSTALL MANIFEST README
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man3/*.3
%{_prefix}/perl5/vendor_perl/%{perl_version}

%changelog
* Thu Jun 17 2010 - Milan Jurik
- initial import to SFE
* Wed Jul  2 2008 J. Randall Owens <jrowens@ghiapet.net> - 0.04-3
- add version to gtkimageview-devel BuildRequires

* Wed Jul  2 2008 J. Randall Owens <jrowens@ghiapet.net> - 0.04-2
- Use CPAN for URL & Source
- rm unnecessary comments

* Wed Jul  2 2008 J. Randall Owens <jrowens@ghiapet.net> - 0.04-1
- Initial RPM build from source, in case it's needed for gscan2pdf

