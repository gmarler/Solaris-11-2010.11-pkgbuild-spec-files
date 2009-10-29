#
# spec file for package SFElibmtp
#
# includes module(s): libmtp
#
%include Solaris.inc
# There is no 64bit libusb :(

%define cc_is_gcc 1
%include base.inc

%use libmtp = libmtp.spec

%define SFEdoxygen      %(/usr/bin/pkginfo -q SFEdoxygen && echo 1 || echo 0)

Name:		SFElibmtp
Summary:	%{libmtp.summary}
Version:	%{libmtp.version}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SFElibiconv

%package devel
Summary:         %{summary} - development files
SUNW_BaseDir:    %{_basedir}
%include default-depend.inc
Requires: %name

%package root
Summary:         %{summary} - system files
SUNW_BaseDir:    /
%include default-depend.inc

#%if %SFEdoxygen
#%package doc
#Summary:                 %{summary} - Documentation
#SUNW_BaseDir:            %{_prefix}
#%include default-depend.inc
#Requires: %name
#%endif

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%libmtp.prep -d %name-%version/%{base_arch}

%build
%libmtp.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%libmtp.install -d %name-%version/%{base_arch}
# Remove libtool archive remnant
rm -f $RPM_BUILD_ROOT%{_libdir}/libmtp.la

mkdir -p $RPM_BUILD_ROOT/etc/hal/fdi/information/10freedesktop
install -p -m 644 %{_builddir}/%name-%version/i386/libmtp-%version/libmtp.fdi $RPM_BUILD_ROOT%{_sysconfdir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi


# Remove Doxygen HTML documentation. This changes every time it is
# generated and thus creates multiarch conflicts.
# Will wait for upstream to fix this to generate consistent files.
rm -rf $RPM_BUILD_ROOT%{_docdir}/libmtp-%{version}/html
rm -rf $RPM_BUILD_ROOT%{_datadir}

#%if %SFEdoxygen
#%else
#rm -rf $RPM_BUILD_ROOT%{_datadir}
#%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/mtp-*
%dir %attr (0755, root, bin) %{_cxx_libdir}
%{_cxx_libdir}/lib*.so*

%files root
%defattr (-, root, bin)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/hal/fdi/information/10freedesktop/10-usb-music-players-libmtp.fdi

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_cxx_libdir}
%dir %attr (0755, root, other) %{_cxx_libdir}/pkgconfig
%{_cxx_libdir}/pkgconfig/*

#%if %SFEdoxygen
#%files doc
#%defattr (-, root, bin)
#%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, other) %{_datadir}/doc
#%{_datadir}/doc/*
#%endif

%changelog
* Fri Oct 23 2009 - jchoi42@pha.jhu.edu
- modified libdir locations, build prefix
- add root pkg for hal fdi, commented out doc pkg due to doxygen instability
* Tue Sep 18 2007 - dougs@truemail.co.th
- Initial version
