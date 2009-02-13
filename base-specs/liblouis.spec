# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
%define src_name tuntap
%define src_url http://www.whiteboard.ne.jp/~admin2/tuntap/source/%{src_name}
Summary:	Support for contracted braille
Name:		liblouis
Version:	1.5.2
License:	GPL V3
Group:		Libraries
Source: 	http://liblouis.googlecode.com/files/%{name}-%{version}.tar.gz

%description
Library and tools for supporting contracted braille

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --infodir=%{_infodir} --disable-ucs4
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}/
%{_datadir}/liblouis/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/liblouis*
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/liblouis-guide.info
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/liblouis.pc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}/
%{_includedir}/liblouis/*

%changelog
* Fri Feb 13 2009 - Willie Walker
- Initial spec
