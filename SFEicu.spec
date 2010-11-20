#
# spec file for package SFEicu
#
# includes module(s): icu
#

# The reason that SFEicu is required is that library/icu is built against
# libcStd, whereas some libraries such as Boost require ICU but do not
# build against libcStd.

# This package does not conflict with library/icu because its base directory
# is /usr/stdcxx.

%define _basedir /usr/stdcxx
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use icu_64 = icu.spec
%endif

%include base.inc
# arch64.inc defines opt_arch64 as 1, but base.inc doesn't define it as 0
%define opt_arch64 0
%use icu = icu.spec

Name:			SFEicu
Summary:		%icu.summary
Version:		%icu.version
License:		BSD.icu
SUNW_BaseDir:		%_basedir
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:		SUNWlibstdcxx4
Requires:		SUNWlibstdcxx4

%package devel
Summary:		%{summary} - development files
SUNW_BaseDir:		%{_basedir}
%include default-depend.inc
Requires: %name

%description 
ICU is a mature, widely used set of C/C++ and Java libraries providing 
Unicode and Globalization support for software applications. ICU is widely 
portable and gives applications the same results on all platforms and 
between C/C++ and Java software.

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%icu_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%icu.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%icu_64.build -d %name-%version/%_arch64
%endif

%icu.build -d %name-%version/%{base_arch}


%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%icu_64.install -d %name-%version/%_arch64
%endif

%icu.install -d %name-%version/%base_arch


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/derb
%{_bindir}/genbrk
%{_bindir}/gencfu
%{_bindir}/gencnval
%{_bindir}/genctd
%{_bindir}/genrb
%{_bindir}/icu-config
%{_bindir}/icuinfo
%{_bindir}/makeconv
%{_bindir}/pkgdata
%{_bindir}/uconv
%ifarch amd64 sparcv9
%_bindir/%_arch64
%endif

%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/genccode
%{_sbindir}/gencmn
%{_sbindir}/gennorm2
%{_sbindir}/gensprep
%{_sbindir}/genuca
%{_sbindir}/icupkg

%ifarch amd64 sparcv9
%_sbindir/%_arch64
%endif

%dir %attr (0755, root, sys) %{_datadir}
%_datadir/icu/%version
%_mandir/man1
%_mandir/man8

%{_libdir}/lib*.so*
%{_libdir}/icu
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/icu
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Sat Nov 20 2010 - Alex Viskovatoff
- Create new spec using base spec from kde-solaris modified for SFE, with
  some code taken from FOSSicu4c.spec
