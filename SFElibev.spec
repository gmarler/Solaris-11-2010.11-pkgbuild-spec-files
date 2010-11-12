#
# spec file for package SFElibev
#
# includes module(s): libev
#
%include Solaris.inc

%define	src_name libev
%define	src_version 4.01

Name:		SFElibev
Version:	4.0.0.1
Summary:	High-performance event loop/event model with lots of features
Group:		System Environment/Libraries
License:	BSD or GPLv2+
URL:		http://software.schmorp.de/pkg/libev.html
Source:		http://dist.schmorp.de/libev/Attic/%{src_name}-%{src_version}.tar.gz
Source1:	%{src_name}.pc.in
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgsed

%description
Libev is modelled (very losely) after libevent and the Event perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller.

%package 	devel
Summary:	High-performance event loop/event model with lots of features
Group:		System Environment/Libraries
Requires:	%{name}
Requires:	SUNWgnome-common-devel

%description 	devel
Libev is modelled (very losely) after libevent and the Event perl
module, but is faster, scales better and is more correct, and also more
featureful. And also smaller. Development libraries.

%prep
%setup -q -n %{src_name}-%{src_version}

# Add pkgconfig support
cp -p %{SOURCE1} .
sed -i.pkgconfig -e 's|Makefile|Makefile libev.pc|' configure.ac configure
sed -i.pkgconfig -e 's|lib_LTLIBRARIES|pkgconfigdir = $(libdir)/pkgconfig\n\npkgconfig_DATA = libev.pc\n\nlib_LTLIBRARIES|' Makefile.am Makefile.in
aclocal
automake

%build
./configure --prefix=%{_prefix} \
	--disable-static \
	--with-pic \
	--includedir=%{_includedir}/%{src_name}
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

rm -rf $RPM_BUILD_ROOT%{_libdir}/%{src_name}.la

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc Changes LICENSE README
%{_libdir}/%{src_name}.so.4
%{_libdir}/%{src_name}.so.4.0.0
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_mandir}/man?/*


%files devel
%defattr(-, root, bin)
%{_libdir}/%{src_name}.so
%{_includedir}/%{src_name}/
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/%{src_name}.pc


%changelog
* Fri Nov 12 2010 - Milan Jurik
- bump to 4.01
* Thu Sep 07 2010 - Milan Jurik
- Initial spec based on Fedora
