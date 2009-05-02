#
# spec file for package SFEperl-encode-detect
#
# includes module(s): Encode-Detect
#

%define module_version 1.1
%define module_version_download 1.01
%define module_name Encode-Detect
%define module_name_major Encode
%define module_package_name encode-detect
#still unused: %define module_name_minor Detect

%define perl_version 5.8.4

%include Solaris.inc
Name:                    SFEperl-%{module_package_name}
Summary:                 %{module_name}-%{module_version} PERL module
Version:                 %{perl_version}.%{module_version_download}
Source:                  http://www.cpan.org/modules/by-module/%{module_name_major}/%{module_name}-%{module_version_download}.tar.gz
Patch1:	                 encode-detect-01-sunpro.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWperl584core
BuildRequires:           SUNWperl584core
BuildRequires:           SUNWsfwhea
BuildRequires:           SFEperl-extutils-cbuilder

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

%prep
%setup -q            -c -n %name-%version
cd %{module_name}-%{module_version_download}
chmod +w Detector.xs
%patch1 -p1

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
cd %{module_name}-%{module_version_download}
perl Build.PL \
    --install_path lib=%{_prefix}/perl5/vendor_perl/%{perl_version} \
    --install_path arch=%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    --install_path bin=%{_bindir} \
    --install_path bindoc=%{_mandir}/man1 \
    --install_path libdoc=%{_mandir}/man3 \
    --destdir $RPM_BUILD_ROOT
# hack: use C++ compiler
perl Build --installdirs vendor --makefile_env_macros 1 build \
    --config "cc=$CXX" --config "ld=$CXX" \
    --extra_compiler_flags "-Iinclude" --extra_linker_flags "" \
    CCCDLFLAGS="%picflags" OPTIMIZE="%cxx_optflags"

%install
rm -rf $RPM_BUILD_ROOT
cd %{module_name}-%{module_version_download}
perl Build install

rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}/*
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%changelog
* Thr Apr 30 2009 - Thomas Wagner
- bump to 1.01
- rework patch1
- make version number IPS capable
* Tue Apr 08 2008 - trisk@acm.jhu.edu
- Initial spec
