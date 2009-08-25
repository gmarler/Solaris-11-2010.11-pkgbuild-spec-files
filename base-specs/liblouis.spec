# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
Summary:	Support for contracted braille
Name:		liblouis
Version:	1.7.0
License:	GPL V3
Group:		Libraries
Source: 	http://liblouis.googlecode.com/files/%{name}-%{version}.tar.gz

%define python_version 2.4

%description
Library and tools for supporting contracted braille

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --infodir=%{_infodir} --enable-ucs4
make

%install
make install DESTDIR=$RPM_BUILD_ROOT
cd python
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/usr/lib:$LD_LIBRARY_PATH python setup.py build
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/usr/lib:$LD_LIBRARY_PATH python setup.py install --root $RPM_BUILD_ROOT --install-lib %{_libdir}/python%{python_version}/vendor-packages
cd ..

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}/
%{_datadir}/liblouis/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/liblouis*
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/liblouis.info
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/liblouis.pc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}/
%{_includedir}/liblouis/*
%dir %attr (0755, root, bin) %{_libdir}/python?.?
%dir %attr (0755, root, bin) %{_libdir}/python?.?/vendor-packages
%dir %attr (0755, root, bin) %{_libdir}/python?.?/vendor-packages/louis
%{_libdir}/python?.?/vendor-packages/louis/*

%changelog
* Tue Aug 25 2009 - Willie Walker
- Upgrade to liblouis 1.7.0
* Tue Jun 16 2009 - Willie Walker
- Upgrade to liblouis 1.6.2 to get us the 'louis' python module
* Fri Feb 13 2009 - Willie Walker
- Initial spec
