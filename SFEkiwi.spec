#
# spec file for package SFEkiwi
#
# includes module(s): kiwi
#
%include Solaris.inc

%define python_version 2.4

Name:			SFEkiwi
Summary:		A framework for Python applications with graphical user interfaces
Version:		1.9.24
Source:			http://ftp.gnome.org/pub/GNOME/sources/kiwi/1.9/kiwi-%{version}.tar.gz
URL:			http://www.async.com.br/projects/kiwi/index.html
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_prefix}

%include default-depend.inc

Requires: SUNWPython
Requires: SUNWgnome-python-libs
BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnome-python-libs-devel

%prep
%setup -q -n kiwi-%{version}

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
%{_datadir}/doc/*
%{_datadir}/kiwi/*
%{_datadir}/gazpacho/*
%{_datadir}/locale/*

%changelog
* Thu Jan 29 2009 - Erwann Chenede <erwann@sun.com>
- Bumped to 1.9.24
* Sun Sep 16 2007 - Ananth Shrinivas <ananth@sun.com>
- Created new spec.

