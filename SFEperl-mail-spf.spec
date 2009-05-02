#
# spec file for package SFEperl-Mail-SPF
#
# includes module(s): Mail-SPF
#

#TODO# re-work perl specific prerequisites...

#note: download file version differs from package version (for IPS not accepting "015" / leading zero)
%define module_version 2.6
%define module_version_download v2.006

%define module_name Mail-SPF
%define module_name_major Mail
%define module_package_name mail-spf
#still unused: %define module_name_minor SPF

%define perl_version 5.8.4

%include Solaris.inc
Name:                    SFEperl-%{module_package_name}
Summary:                 %{module_name}-%{module_version} PERL module
Version:                 %{perl_version}.%{module_version}
Source:                  http://www.cpan.org/modules/by-module/%{module_name_major}/%{module_name}-%{module_version_download}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWperl584core
BuildRequires:           SUNWperl584core
BuildRequires:           SUNWsfwhea
BuildRequires:           SFEperl-version
BuildRequires:           SFEperl-module-build
BuildRequires:           SFEperl-uri
BuildRequires:           SFEperl-netaddr-ip


%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version

%build
cd %{module_name}-%{module_version_download}
#
#          'perl' => '/usr/perl5/5.8.4/bin/perl',
#build_params:                                            'libdoc' => '/var/tmp/pkgbuild-tom/SFEperl-mail-spf-5.8.4.2.6-build/usr/share/man/man3',
#build_params:                                            'script' => '/usr/perl5/5.8.4/bin',
#build_params:                                            'bindoc' => '/var/tmp/pkgbuild-tom/SFEperl-mail-spf-5.8.4.2.6-build/usr/share/man/man1',
#build_params:                                            'bin' => '/usr/perl5/5.8.4/bin',
#build_params:                                            'arch' => '/usr/perl5/5.8.4/lib/i86pc-solaris-64int',
#build_params:                                            'lib' => '/usr/perl5/5.8.4/lib'
#build_params:                                            'libdoc' => '/var/tmp/pkgbuild-tom/SFEperl-mail-spf-5.8.4.2.6-build/usr/share/man/man3',
#build_params:                                            'script' => '/usr/perl5/5.8.4/bin',
#build_params:                                            'bindoc' => '/var/tmp/pkgbuild-tom/SFEperl-mail-spf-5.8.4.2.6-build/usr/share/man/man1',
#build_params:                                            'bin' => '/usr/perl5/5.8.4/bin',
#build_params:                                            'arch' => '/var/tmp/pkgbuild-tom/SFEperl-mail-spf-5.8.4.2.6-build/usr/perl5/vendor_perl/5.8.4/i86pc-solaris-64int',
#build_params:                                            'lib' => '/var/tmp/pkgbuild-tom/SFEperl-mail-spf-5.8.4.2.6-build/usr/perl5/vendor_perl/5.8.4'
#build_params:                                              'libdoc' => '/usr/perl5/5.8.4/man/man3',
#build_params:                                              'script' => '/usr/perl5/5.8.4/bin',
#build_params:                                              'bindoc' => '/usr/perl5/5.8.4/man/man1',
#build_params:                                              'bin' => '/usr/perl5/5.8.4/bin',
#build_params:                                              'arch' => '/usr/perl5/vendor_perl/5.8.4/i86pc-solaris-64int',
#build_params:                                              'lib' => '/usr/perl5/vendor_perl/5.8.4'
#build_params:                                'sbin' => '/usr/sbin'
#build_params:                                   'core' => '/usr/perl5/5.8.4',
#build_params:                                   'site' => '/usr/perl5/5.8.4',
#build_params:                                   'vendor' => '/usr/perl5/5.8.4'
#build_params:            'prefix' => '/var/tmp/pkgbuild-tom/SFEperl-mail-spf-5.8.4.2.6-build/usr/perl5'
#
perl Makefile.PL \
    UNINST=0 \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    ARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLVENDORARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 

make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version_download}
make install

mkdir -p  $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p  $RPM_BUILD_ROOT%{_mandir}/man3
mv  $RPM_BUILD_ROOT%{_prefix}/man/man1  $RPM_BUILD_ROOT%{_mandir}/man1/
mv  $RPM_BUILD_ROOT%{_prefix}/man/man3  $RPM_BUILD_ROOT%{_mandir}/man3/
rmdir $RPM_BUILD_ROOT%{_prefix}/man/


[ -d $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/ ] || mkdir -p $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/
mv  $RPM_BUILD_ROOT%{_prefix}/lib/site_perl/%{module_name_major} $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{module_name_major}

#remove usr/lib/site_perl/5.8.4/i86pc-solaris-64int/auto/Mail/SPF/.packlist 
rm -rf  $RPM_BUILD_ROOT%{_prefix}/lib


%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
#%{_prefix}/perl5/vendor_perl/%{perl_version}/version.pm
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{module_name_major}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

#special case because package delivers regular binary to non perl localtion  and has non-perl manpages
%dir %attr(0755, root, bin) %{_bindir}
%{_bindir}/*


%changelog
* Thr Apr 30 2009 - Thomas Wagner
- Initial spec file
