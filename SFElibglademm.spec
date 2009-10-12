#
# spec file for package SFElibglademm
#
# includes module(s): libglademm
#
%include Solaris.inc

Name:                    SFElibglademm
Summary:                 libglademm - C++ Wrapper for the Gtk+ Library
Version:                 2.6.7
URL:                     http://www.gtkmm.org/
Source:                  http://ftp.acc.umu.se/pub/GNOME/sources/libglademm/2.6/libglademm-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWglibmm
Requires: SUNWcairomm
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SUNWsigcpp
Requires: SUNWlibC
Requires: SUNWgtkmm
BuildRequires: SUNWsigcpp-devel
BuildRequires: SUNWglibmm-devel
BuildRequires: SUNWcairomm-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgtkmm-devel

%package devel
Summary:                 libglademm - C++ Wrapper for the Gtk+ Library - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel
Requires: SUNWglibmm-devel
Requires: SUNWsigcpp-devel


%prep
%setup -q -n libglademm-%version

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
#mv $RPM_BUILD_ROOT%{_bindir}/demo $RPM_BUILD_ROOT%{_bindir}/libglademm-demo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*

%files devel
%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Oct 08 2009 - jchoi42@pha.jhu.edu
- Bump to 2.6.7, prevent useless extra_defs_gen from being built
- Add patch to prevent building useless extra_defs_gen
* Wed Sep 19 2007 - trisk@acm.jhu.edu
- Bump to 2.6.4
* Jun 05 2007 Thomas Wagner
- needed by pulseaudio frontends
- initial version from the museeum of spec-files (copy of SFEgtkmm.spec)
