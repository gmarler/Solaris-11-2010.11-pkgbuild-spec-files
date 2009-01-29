#
# spec file for package SFEgazpacho
#
# includes module(s): gazpacho
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEgazpacho
Summary:		A GTK+ User Interface Builder
Version:		0.7.2
Source:			http://ftp.gnome.org/pub/gnome/sources/gazpacho/0.7/gazpacho-%{version}.tar.bz2
URL:			http://gazpacho.sicem.biz/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_prefix}

%include default-depend.inc

Requires: SUNWPython
Requires: SUNWgnome-python-libs
Requires: SFEkiwi
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SFEkiwi

%prep
%setup -q -n gazpacho-%{version}

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/site-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gazpacho/*
%{_datadir}/applications/*
%{_datadir}/doc/*
%{_datadir}/locale/*

%changelog
* Sun Sep 16 2007 - Ananth Shrinivas <ananth@sun.com>
- Created new spec.

