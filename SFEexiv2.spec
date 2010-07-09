#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc
%include stdcxx.inc


Name:		SFEexiv2
License:	GPL
Summary:	A C++ library and CLI utility to manage image metadata.
Version:	0.20
URL:		http://www.exiv2.org/
Source:		http://www.exiv2.org/exiv2-%{version}.tar.gz
Patch1:		exiv2-01-unsigned-char.diff 
Patch2:		exiv2-02-sunstudio.diff
Patch3:		exiv2-03-make.diff
Patch4:		exiv2-04-stdcxx4.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SUNWTiff
BuildRequires: SUNWTiff-devel
Requires: SUNWpng
BuildRequires: SUNWpng-devel
Requires: SUNWjpg
BuildRequires: SUNWjpg-devel
Requires: SUNWgnome-libs
BuildRequires: SUNWgnome-libs-devel
Requires: SUNWlibstdcxx4
BuildRequires: SUNWlibstdcxx4
Requires: SUNWlexpt
BuildRequires: SUNWlexpt
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWlxsl
BuildRequires: SUNWlxsl-devel
BuildRequires: SFEgraphviz

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%setup -q -n exiv2-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"

export CXXFLAGS="%cxx_optflags -library=no%Cstd -I%{stdcxx_include}"

export LDFLAGS="%_ldflags -L%{stdcxx_lib} -R%{stdcxx_lib} -lstdcxx4 -Wl,-zmuldefs"

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --enable-shared=yes \
            --enable-static=no  \
            --disable-visibility \
            --with-pic

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_localedir}
%endif
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%{_datadir}/locale/*
%endif

%changelog
* Fri Jul 09 2010 - Milan Jurik
- fix build deps
* Wed Jun 30 2010 - Milan Jurik
- fix 0.20 build
* Sun Jun 27 2010 - Milan Jurik
- update to 0.20, but it has problem with Sun Studio
* Wed Jan 30 2008 - moinak.ghosh@sun.com
- Initial spec.
