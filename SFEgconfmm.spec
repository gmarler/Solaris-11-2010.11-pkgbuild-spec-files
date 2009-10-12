#
# spec file for package SFEgconfmm
#
# includes module(s): gconfmm
#
%include Solaris.inc

Name:                    SFEgconfmm
Summary:                 gconfmm - configuration dialogues for gtkmm
Version:                 2.28.0
URL:                     http://www.gtkmm.org/
Source:                  http://ftp.acc.umu.se/pub/GNOME/sources/gconfmm/2.28/gconfmm-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEglibmm-gpp
Requires: SFEgtkmm-gpp
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWlibms
Requires: SFEsigcpp-gpp
Requires: SUNWlibC
BuildRequires: SFEsigcpp-gpp-devel
BuildRequires: SFEglibmm-gpp-devel
BuildRequires: SFEgtkmm-gpp-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-config-devel

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SFEglibmm-gpp-devel
Requires: SFEsigcpp-gpp-devel


%prep
%setup -q -n gconfmm-%version

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
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-python

# prevent useless extra_defs_gen from being built
sed -i 's/tools//' Makefile

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -rf $RPM_BUILD_ROOT%{_datadir}/devhelp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/gconfmm*
#%{_libdir}/gdkmm*
#%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Oct 08 2009 - jchoi42@pha.jhu.edu
- Bump to 2.28.0, prevent useless extra_defs_gen from being built
* Sep 19 2007 - trisk@acm.jhu.edu
- Fix dependencies
* Jun 06 2007 Thomas Wagner
- needed by pulseaudio frontends
- initial version from the museeum of spec-files (copy of SFEgtkmm.spec)
