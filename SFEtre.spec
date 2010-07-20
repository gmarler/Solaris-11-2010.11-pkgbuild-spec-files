#
# spec file for package SFEtre.spec
#
# includes module(s): TRE
#
%include Solaris.inc

%define src_name	tre
%define src_url		http://laurikari.net/tre
%define src_version	0.8.0
%define pkg_release	1

SUNW_Pkg: SFE%{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:                   SFEtre
Summary:                TRE - Lightweight, Robust, and Efficient POSIX compliant regexp matching library 
Version:                %{src_version}
Source:                 %{src_url}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --includedir=%{_includedir} \
            --libdir=%{_libdir}

%build
make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%dir %attr(0755,root,sys) %{_datadir}
%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%dir %attr(0755,root,bin) %{_includedir}
%{_includedir}/*

%changelog
* Tue July 20 2010 - markwright@internode.on.net
- bump to 0.8.0
* Sun Oct 14 2007 - laca@sun.com
- fix some directory attributes
* Sat Aug 11 2007 - ananth@sun.com
- Initial version

