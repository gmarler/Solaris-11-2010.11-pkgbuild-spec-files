#
# spec file for package SFEarj.spec
#
# includes module(s): arj
#
%include Solaris.inc

%define src_name	arj
%define src_url		http://testcase.newmail.ru
%define src_version 3.10.22
# =========================================================================== 
#                    SVR4 required definitions
# =========================================================================== 
SUNW_Pkg: SFE%{src_name}-%{base_arch}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Tag definitions
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

Name:                   SFEarj
Summary:                ARJ - File archiving utlitity
Version:                %{src_version}
Source:                 %{src_url}/files/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
Patch0:                 %{src_name}-01-%{version}.gcc.diff

Requires: SUNWcsl
Requires: SUNWlibms
BuildRequires: SUNWgcc

%prep
%setup -q -n %{src_name}-%{version}
%patch0 -p1
cd gnu
autoconf
./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir}
cd ..

%build
CC=gcc CXX=g++ make 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr(0755,root,bin) %{_bindir}
%{_bindir}/*

%dir %attr(0755,root,bin) %{_libdir}
%{_libdir}/*

%dir %attr(0755,root,bin) %{_mandir}
%{_mandir}/*

%changelog
* Sat Aug 11 2007 - ananth@sun.com
- Initial version
