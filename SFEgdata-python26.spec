#
# spec file for package SFEgdata-python26
#
# includes module(s): gdata-python
#

%include Solaris.inc
Name:                    SFEgdata-python26
Summary:                 Google Data API provide a simple protocol for reading and writing data on the web
URL:                     http://code.google.com/p/gdata-python-client/
Version:                 2.0.1
Source:                  http://gdata-python-client.googlecode.com/files/gdata-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython26

%include default-depend.inc

%define pythonver 2.6

%prep
%setup -q -n gdata-%version

%build
python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install --root=%{buildroot}

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
%{_libdir}/python%{pythonver}/vendor-packages/*

%changelog
* Mon Aug 10 2009 - matt@greenviolet.net
- Initial spec, based on SFEgdata-python.spec
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
