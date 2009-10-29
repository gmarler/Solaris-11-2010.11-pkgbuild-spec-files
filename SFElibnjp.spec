#
# spec file for package SFElibnjp
#
# includes module(s): libnjp
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%use libnjp = libnjp.spec

# FIXME: IMPORTANT NOTE FOR BUMPING
# due to cd acting strangely, the version number is hardcoded twice here
# and once in the base spec :(  -jchoi42

Name:                    SFElibnjp
Summary:                 libnjp - Creative Labs Nomad Jukebox library
Version:		 %{libnjp.version}

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibusb
Requires: SFEsigcpp-gpp
Requires: SUNWlibC
Requires: SUNWgccruntime
BuildRequires: SFEgcc
BuildRequires: SFEsigcpp-gpp-devel

%package devel
Summary:                 %{_summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWsigcpp-devel


%prep
rm -rf %name-%version
mkdir %name-%version
%libnjp.prep -d %name-%version

%build
#%libnjp.build -d %name-%version

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export LDFLAGS="-L%{_cxx_libdir} -R%{_cxx_libdir}"
export CXXFLAGS="%gcc_cxx_optflags -D_XPG4_2 -D__EXTENSIONS__"
export PKG_CONFIG_PATH="%{_cxx_libdir}/pkgconfig"
export LD_LIBRARY_PATH=/usr/gnu/lib
export FV=%{version}
#cd %{_builddir}/SFElibnjp-%{version}/libnjp-%{version}
cd %{_builddir}/%name-%version
# This is where the directory problems begin!
#cd %{libnjp.name}-%version
#cd libnjp-$FV
#export cd_hack_libnjb="cd libnjb-"%version  # HORRIBLE HACK. Somebody fix me.
#export cd_hack_libnjb="cd libnjb-2.2.6"  # HORRIBLE HACK. Somebody fix me.
#`$cd_hack_libnjb`  # No, seriously, /usr/bin/cd. WTF.

cd libnjb-2.2.6  # Even worse hack. ADSFADSF

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_cxx_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
#cd %{_builddir}/%name-%version

#cd libnjb-2.2.6  # again with the /bin/cd hax

%libnjp.install -d %name-%version


# remove doxygen documentation
rm -r $RPM_BUILD_ROOT%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*


%changelog
* Thu Oct 23 2009 - jchoi42@pha.jhu.edu
- initial spec 
