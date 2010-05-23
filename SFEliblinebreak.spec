#
# spec file for package SFEliblinebreak
#
# includes module(s): liblinebreak
#
%include Solaris.inc

%define src_name liblinebreak

Name:		SFEliblinebreak
Version:	2.0
Summary:	A Unicode line-breaking library
Group:		Development/Libraries
License:	zlib
URL:		http://vimgadgets.sourceforge.net/liblinebreak/
Source:		%{sf_download}/vimgadgets/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
liblinebreak is an implementation of the line breaking algorithm as
described in Unicode 5.0.0 Standard Annex 14, Revision 19, available
at http://www.unicode.org/reports/tr14/tr14-19.html

This package currently only provides a static library, and as such
should not be a runtime dependency.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}

%description  devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{src_name}-%{version}
./configure --prefix=%{_prefix} --disable-static


%build
make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,bin)
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Sun May 23 2010 - Milan Jurik
- initial import to SFE
