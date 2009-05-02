#
# spec file for package SFEperl-dbfile
#
# includes module(s): DB_File
#

##TODO## needs some cleaning (moving around directory in install probably can be cleaned up)

%define module_version 1.820
%define module_name DB_File
%define module_name_major DB_File
%define module_package_name dbfile
#still unused: %define module_name_minor DBFIle

%define perl_version 5.8.4

%include Solaris.inc
Name:                    SFEperl-%{module_package_name}
Summary:                 %{module_name}-%{module_version} PERL module
Version:                 %{perl_version}.%{module_version}
Source:                  http://www.cpan.org/modules/by-module/%{module_name_major}/%{module_name}-%{module_version}.tar.gz
Patch1:			perl-dbfile-01-config.in-include_gnu.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWperl584core
BuildRequires:           SUNWperl584core
BuildRequires:           SUNWsfwhea
Requires:                SFEbdb

%description
Provides vendor_perl modules:
Date::Format
Date::Parse
Time::Zone


%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%module_version
cd %{module_name}-%{module_version}
%patch1 -p1

%build




cd %{module_name}-%{module_version}
perl Makefile.PL \
    UNINST=0 \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \

#make CC=$CC CCCDLFLAGS="                %picflags" OPTIMIZE="             %optflags" LD=$CC
make  CC=$CC CCCDLFLAGS="%{gnu_lib_path} %picflags" OPTIMIZE="-I%{gnu_inc} %optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version}
make install

#no idea why this is in the wrong place, so move it
mkdir -p $RPM_BUILD_ROOT/%{_prefix}/perl5/vendor_perl/%{perl_version}/
mv  $RPM_BUILD_ROOT/%{_prefix}/lib/%{perl_dir}    $RPM_BUILD_ROOT/%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}
rm -r $RPM_BUILD_ROOT/%{_prefix}/lib

#remove: 
rm $RPM_BUILD_ROOT/%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/perllocal.pod

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
#%{_prefix}/perl5/vendor_perl/%{perl_version}/*
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{module_name_major}
#%{_prefix}/perl5/vendor_perl/%{perl_version}/%{module_name_major}/*
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}
#%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}/*
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}.*
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Mon, 28 Apr 2009  - Thomas Wagner
- initial spec
