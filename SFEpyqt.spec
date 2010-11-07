#
# spec file for package SFEpyqt
#
# includes module(s): 
#
%include Solaris.inc

%define python_version 2.6

Name:			SFEpyqt
Summary:		Python interface to Qt
License:		GPL
Version:		4.8.1
Source:			http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-x11-gpl-%{version}.tar.gz
URL:			http://www.riverbankcomputing.co.uk/software/pyqt
Group:			Development/Languages/Python
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWPython26
%include default-depend.inc
Requires: SFEqt4
BuildRequires: SUNWPython26-devel
BuildRequires: SFEsip

%prep
%setup -q -n PyQt-x11-gpl-%{version}

%build
export PYTHON="/usr/bin/python%{python_version}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export QMAKESPEC=/usr/share/qt/mkspecs/default
python configure.py -w --confirm-license \
    -d %{_libdir}/python%{python_version}/vendor-packages
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Delete optimized py code.
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pylupdate4
%{_bindir}/pyuic4
%{_bindir}/pyrcc4
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/sip

%changelog
* Sun Nov 07 2010 - Milan Jurik
- bump to 4.8.1 (qt4 support)
* Sat Mar 29 2008 - laca@sun.com
- create
