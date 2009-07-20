#
# spec file for package SFEperl-pango
#
# includes module(s): perl-pango
#

%include Solaris.inc

%define tarball_version 1.220
%define perl_version 5.8.4

Name:                    SFEperl-pango
Summary:                 Pango-%{tarball_version} PERL Module
Version:                 %{perl_version}.%{tarball_version}
Source:                  http://search.cpan.org/CPAN/authors/id/T/TS/TSCH/Pango-%{tarball_version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:  SUNWperl584core
Requires:       SUNWperl584core
# Requires:		SUNWgnome-base-libs
BuildRequires:	SFEperl-extutils-dep
BuildRequires:	SFEperl-extutils-pkg
Requires:	SFEperl-cairo

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif

%prep
%setup -q	-c -n %name-%version

%build
cd Pango-%{tarball_version}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd Pango-%{tarball_version}
make install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} 
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Sun Jul 19 2009 - matt@greenviolet.net
- Initial spec file
