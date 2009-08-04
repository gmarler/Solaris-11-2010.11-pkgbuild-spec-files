#
# spec file for package SFElibmng
#
# includes module(s): libmng
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
##FIXME##%define arch_ldadd -Wl,-znolazyload -Wl,-L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64}
%use libmng64 = libmng.spec
%endif

%include base.inc
%use libmng = libmng.spec

Name:                    SFElibmng
Summary:                 libmng  - the MNG reference library
Version:                 %{libmng.version}
Source:                  %{sf_download}/libmng/libmng-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlcms
BuildRequires: SUNWjpg-devel
##FIXME## SFElcms/SUNWlcms need to be a 64bit version for full 64-bit support, create test on lib/amd64/liblcms.so*
##FIXME## SUNWlcms from spec-files-extra is now 32/64bit
Requires: SUNWlcms
Requires: SUNWjpg


%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libmng64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libmng.prep -d %name-%version/%{base_arch}

%build

%ifarch amd64 sparcv9
%libmng64.build -d %name-%version/%_arch64
%endif

%libmng.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libmng64.install -d %name-%version/%_arch64
%endif

%libmng.install -d %name-%version/%{base_arch}


%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*


%changelog
* Aug 01 2009 - Gilles Dauphin
- lcms-devel equiv to lcms.
* Sat Mar 22 2008 - Thomas Wagner
- change to (Build-)Requires: SUNWlcms(-devel) from spec-files-extra which is 32/64bit, 
  note1: spec-files-extra/SUNWlcms.spec should replace the already moved file spec-files-other/SUNWlcms.spec (32bit only!)
  note2: pls don't delete spec-files-extra/SUNWlcms.spec base-specs/lcms.spec now
* Wed Mar  5 2008 - Thomas Wagner
- create 64bit spec, move ancestor spec to base-spec/libmng.spec
- add (Build-)Requires: SUNWjpg(-devel)
