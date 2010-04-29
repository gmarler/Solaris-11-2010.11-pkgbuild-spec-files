#
# spec file for package SFEperl-gettext
#
# includes module(s): Gettext perl module
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define gettext_version 1.05
%define perl_version 5.8.4

Name:                    SFEperl-gettext
Summary:                 Gettext-%{gettext_version} PERL module
Version:                 105
Source:                  http://www.cpan.org/modules/by-module/Locale/gettext-%{gettext_version}.tar.gz
SUNW_Pkg:                SFEperl-gettext
IPS_package_name:        library/perl-5/gettext
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWperl584core
BuildRequires:           SUNWperl584usr

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd gettext-%{gettext_version}
perl Makefile.PL \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd gettext-%{gettext_version}
make install

#mkdir -p $RPM_BUILD_ROOT%{_prefix}/perl5
#mv $RPM_BUILD_ROOT%{_prefix}/lib/site_perl $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl
#mv $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/Image $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}
#mv $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/auto/Image/Size/* $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/Image/Size/
#rm -rf $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/auto
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

#mkdir -p $RPM_BUILD_ROOT%{_datadir}
#mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_mandir}

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
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%changelog
* Sun Apr 11 2010 - Milan Jurik
- added missing build dependency
* Tue Mar 24 2009 - andras.barna@gmail.com
- IPSize version
* Wed Sep 12 2007 - nonsea@users.sourceforge.net
- Initial spec
