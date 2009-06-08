#
# spec file for package SFEgdata-python
#
# includes module(s): gdata-python
#

%include Solaris.inc
Name:                    SFEgdata-python
Summary:                 Google Data API provide a simple protocol for reading and writing data on the web
URL:                     http://code.google.com/p/gdata-python-client/
Version:                 1.3.3
Source:                  http://gdata-python-client.googlecode.com/files/gdata-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n gdata-%version

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=%{buildroot}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/atom/*
%{_libdir}/python%{pythonver}/vendor-packages/gdata/*

%changelog
* Mon Jun 08 2009 - brian.cameron@sun.com
- Bump to 1.3.3.
* Mon Mar 17 2009 - alfred.peng@sun.com
- Bump to 1.2.4
* Mon Jun 16 2008 - brian.cameron@sun.com
- Bump to 1.1.1
* Fri Jun 06 2008 - brian.cameron@sun.com
- Bump to 1.0.13
* Tue Apr 29 2008 - brian.cameron@sun.com
- Created
