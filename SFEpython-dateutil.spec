#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%define src_name python-dateutil
%define python_version 2.4

%include Solaris.inc

Name:                SFEpython-dateutil
URL:                 http://labix.org/python-dateutil
Summary:             dateutil - A python module provides powerful extensions to the standard datetime
Version:             1.5
Source:              http://labix.org/download/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
Requires: SUNWpython-setuptools
Requires: SUNWPython

%prep
%setup -q -n %{src_name}-%version

%build
exit 0

%install
rm -rf $RPM_BUILD_ROOT
/usr/bin/python%{python_version} ./setup.py install --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%changelog
* Tue Apr 27 2010 - brian.cameron@sun.com
- Bump to 1.5.
* Tue Aug 26 2008 - halton.huo@sun.com
- Bump to 1.4.1
* Mon Mar 17 2007 - jijun.yu@sun.com
- Bump to 1.4
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial spec
