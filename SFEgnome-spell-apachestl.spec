#
# spec file for package SUNWgnome-spell
#
# includes module(s): enchant
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby 
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%define _ldflags    %ldadd -Wl,-zignore -Wl,-zcombreloc -Wl,-Bdirect ${EXTRA_LDFLAGS}
%use enchant_64 = enchant.spec
%endif

%include base.inc
%use enchant = enchant.spec

Name:          SFEgnome-spell-apachestl
Summary:       GNOME spell checker component builded with apache std(stdcxx4)
Version:       %{default_pkg_version}
SUNW_BaseDir:  %{_basedir}
#SUNW_Copyright:%{name}.copyright
BuildRoot:     %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWglib2
Requires:      SUNWgnome-component
Requires:      SUNWgnome-config
Requires:      SUNWgnome-libs
Requires:      SUNWiso-codes
Requires:      SUNWlibC
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWiso-codes-devel

#Source1:    %{name}-manpages-0.1.tar.gz

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires:                %{name} = %{version}
%include default-depend.inc
Requires:      SUNWglib2-devel

%prep
rm -rf %name-%version
mkdir -p %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%enchant_64.prep -d %name-%version/%_arch64
%endif

%enchant.prep -d %name-%version

mkdir %name-%version/%base_arch
%enchant.prep -d %name-%version/%base_arch

# Expand manpages tarball
cd %{_builddir}/%name-%version
#gzcat %SOURCE1 | tar xf -

%build
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif

# See http://bugzilla.abisource.com/show_bug.cgi?id=10668 for why LD is set 
# to $CXX.
#export LD=$CXX

%ifarch amd64 sparcv9
export PKG_CONFIG_LIBDIR=%{_pkg_config_path64}
export LD="${CXX} -m64"
%enchant_64.build -d %name-%version/%_arch64
%endif

export PKG_CONFIG_LIBDIR=%{_pkg_config_path}
export LD=$CXX
%enchant.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%enchant_64.install -d %name-%version/%_arch64
rm $RPM_BUILD_ROOT%{_libdir}/%_arch64/*.la
rm $RPM_BUILD_ROOT%{_libdir}/%_arch64/enchant/*.la
%endif

%enchant.install -d %name-%version/%base_arch
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/enchant/*.la
rm $RPM_BUILD_ROOT%{_mandir}/man1/*

#cd %{_builddir}/%name-%version/sun-manpages
#make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files

%doc -d enchant-%{enchant.version} AUTHORS README
%doc(bzip2) -d enchant-%{enchant.version} ChangeLog
%doc(bzip2) -d enchant-%{enchant.version} COPYING.LIB
%doc(bzip2) -d enchant-%{enchant.version} NEWS
%dir %attr (0755, root, other) %{_datadir}/doc

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/enchant*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/enchant*
%endif
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libenchant*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/libenchant*
%endif

%dir %{_libdir}/enchant
%{_libdir}/enchant/*.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/enchant
%{_libdir}/%{_arch64}/enchant/*.so
%endif

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/enchant
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
#%{_mandir}/man1/*
#%dir %attr(0755, root, bin) %{_mandir}/man3
#%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Jan 02 2009 - yuntong.jin@sun.com
- Init spec file, this spec file copied from SUNWgnome-spec.spec to produce
  spell lib linked with apache std,which depeneded by SFEwebkit.spec
