#
# spec file for package SFElensfun
#
# includes module(s): lensfun
#
%include Solaris.inc

%define src_name lensfun

Name:		SFElensfun
Version:	0.2.5
Summary:	A library to rectify the defects introduced by your photographic equipment
License:	LGPLv3
Group:		System Environment/Libraries
URL:		http://lensfun.berlios.de/
Source:		http://download.berlios.de/%{src_name}/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWdoxygen
Requires: SUNWglib2
BuildRequires: SUNWglib2
Requires: SUNWpng
BuildRequires: SUNWpng
BuildRequires: SUNWgnome-common-devel
Requires: SUNWzlib
BuildRequires: SUNWzlib

%description
%{summary}.

%package devel
Summary: Development tools for %{name}
Group:   Development/Libraries
Requires: %{name}
Requires: SUNWgnome-common-devel
%description devel
%{summary}.

%prep
%setup -q -n %{src_name}-%{version} 

%build
# hack to make configure script and linking happy
export LD=$CC

./configure \
  --cflags="%{optflags}" \
  --cxxflags="%{optflags}" \
  --prefix=%{_prefix} \
  --bindir=%{_bindir} \
  --sysconfdir=%{_sysconfdir} \
  --datadir=%{_datadir}/%{src_name} \
  --libdir=%{_libdir} \
  --includedir=%{_includedir} \
  --libexecdir=%{_libexecdir} \
  --target=..generic		\
  --vectorization=""

# set GCC.LDFLAGS to avoid stripping and useless -debuginfo
make AUTODEP=0 lensfun manual \
  V=1 \
  GCC.LDFLAGS.release=""


%install
rm -rf $RPM_BUILD_ROOT
make AUTODEP=0 INSTALL_PREFIX=$RPM_BUILD_ROOT install


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %{_docdir}/%{src_name}-%{version}
%{_docdir}/%{src_name}-%{version}/README
%{_docdir}/%{src_name}-%{version}/*.txt
%{_datadir}/%{src_name}/
%{_libdir}/liblensfun.so.0*

%files devel
%defattr(-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}-%{version}/manual/
%{_includedir}/lensfun.h
%{_libdir}/liblensfun.so
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/lensfun.pc

%changelog
* Thu Jul 15 2010 - Milan Jurik
- Initial spec based on Fedora
