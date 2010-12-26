#
# spec file for package SFElibxmlpp
#
# includes module(s): libxml++
#
%include Solaris.inc

Name:		SFElibxmlpp
Summary:	libxml++ - C++ Wrapper for the libxml2 XML Library
Version:	2.33.1
Group:		System/Libraries
Source:		http://ftp.gnome.org/pub/GNOME/sources/libxml++/2.33/libxml++-%{version}.tar.bz2
URL:		http://libxmlplusplus.sourceforge.net/
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWglibmm
Requires: SUNWlxml
Requires: SUNWgnome-base-libs
Requires: SUNWlibmsr
Requires: SUNWsigcpp
Requires: SUNWzlib
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgawk
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWsigcpp-devel
BuildRequires: SUNWglibmm-devel
BuildRequires: SUNWlxsl
BuildRequires: SUNWdoxygen
BuildRequires: SFEgraphviz

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWglibmm-devel

%prep
%setup -q -n libxml++-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-static

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/libxml++*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%{_datadir}/devhelp

%changelog
* Sun Dec 26 2010 - Milan Jurik
- bump to 2.33.1
* Fri Aug 17 2007 - trisk@acm.jhu.edu
- Bump to 2.19.1
* Fri Jun 30 2006 - laca@sun.com
- bump to 2.14.0
- rename to SFElibxmlpp
- update file attributes
* Thu Nov 17 2005 - laca@sun.com
- create
