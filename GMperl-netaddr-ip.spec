#
# spec file for package SFEperl-netaddr-ip
#
# includes module(s): NetAddr:IP
#

#note: download file version differs from package version (for IPS not accepting "015" / leading zero)
%define module_version 4.40
%define module_version_download 4.040

%define module_name NetAddr-IP
%define module_name_major NetAddr
%define module_package_name netaddr-ip
#still unused: %define module_name_minor NetAddr

%define perl_version 5.10.1
%define perl         /usr/perl5/5.10.1/bin/perl

# The prefix matches the one that Sun/Oracle has used for deployment over
# the years, and prevents any kind of collision with existing versions
%ifarch sparc
%define perl_arch_dir sun4-solaris-64int
%else
%define perl_arch_dir i86pc-solaris-64int 
%endif

%define           vendor          GM  
%define           perl5_dir       %{_prefix}/perl5
%define           perl_prefix     %{perl5_dir}/%{perl_version}
%define           perl_lib        %{perl_prefix}/lib
%define           perl_archlib    %{perl_lib}/%{perl_arch_dir}
%define           perl_mandir     %{perl_prefix}/man
%define           perl_sitedir    %{perl5_dir}/site_perl
%define           perl_sitelib    %{perl_sitedir}/%{perl_version}
%define           perl_sitearch   %{perl_sitelib}/%{perl_arch_dir}
%define           perl_vendordir  %{perl5_dir}/vendor_perl
#%define           perl_vendorlib  %{perl_vendordir}/%{version}/%{vendor}
#%define           perl_vendorarch %{perl_vendordir}/%{version}/%{vendor}/%{perl_arch_dir}
%define           perl_vendorlib  %{perl_vendordir}/%{perl_version}
%define           perl_vendorarch %{perl_vendorlib}/%{perl_arch_dir}

%include Solaris.inc

Name:                    GMperl-%{module_package_name}
Summary:                 %{module_name}-%{module_version} PERL module
Version:                 %{perl_version}.%{module_version}
Source:                  http://www.cpan.org/modules/by-module/%{module_name_major}/MIKER/%{module_name}-%{module_version_download}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

Requires:                GMperl510

BuildRequires:           GMperl510
BuildRequires:           SUNWgmake
#BuildRequires:           SUNWsfwhea

%description
Provides vendor_perl modules:
NetAddr::IP

%include default-depend.inc

%prep
%setup -q            -c -n %name-%module_version

%build

cd %{module_name}-%{module_version_download}
%{perl} Makefile.PL \
        UNINST=0 \
        PREFIX=$RPM_BUILD_ROOT%{_prefix} \
        INSTALLSITELIB=$RPM_BUILD_ROOT%{perl_sitelib} \
        INSTALLSITEARCH=$RPM_BUILD_ROOT%{perl_sitearch} \
        INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{perl_mandir}/man1 \
        INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{perl_mandir}/man3 \
        INSTALLMAN1DIR=$RPM_BUILD_ROOT%{perl_mandir}/man1 \
        INSTALLMAN3DIR=$RPM_BUILD_ROOT%{perl_mandir}/man3 


gmake CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version_download}
gmake test
gmake install

#remove:       /usr/lib/i86pc-solaris-64int/perllocal.pod
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{perl_sitedir}
%dir %attr(0755, root, bin) %{perl_sitelib}
%{perl_sitelib}/*
%dir %attr(0755, root, bin) %{perl_mandir}
%dir %attr(0755, root, bin) %{perl_mandir}/man3
%{perl_mandir}/man3/*


%changelog
