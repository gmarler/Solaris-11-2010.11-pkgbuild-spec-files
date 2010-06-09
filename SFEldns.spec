#
# spec file for package SFEldns.spec
#
# includes module(s): ldns
#
%include Solaris.inc

%define src_name	ldns

Name:		SFEldns
URL:		http://www.nlnetlabs.nl/projects/ldns/
Summary:	ldns library for DNS programming
Version:	1.6.4
Group:		System/Libraries
License:	BSD
Source:		http://www.nlnetlabs.nl/downloads/%{src_name}/%{src_name}-%{version}.tar.gz 
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries

%description
The goal of ldns is to simplify DNS programming, it supports recent RFCs like the DNSSEC documents, and allows developers to easily create software conforming to current RFCs, and experimental software for current Internet Drafts.

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}

%build
./configure --prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir} \
	--disable-static 

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}/libldns.so*

%files devel
%defattr (-, root, bin)
%{_bindir}/ldns-config
%{_includedir}/%{src_name}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man3/*

%changelog
* Wed Jun 09 2010 - Milan Jurik
- Initial version
