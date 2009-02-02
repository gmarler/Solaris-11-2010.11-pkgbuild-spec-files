#
# spec file for package SFEpython-hashlib
#
# includes module(s): hashlib
#
%include Solaris.inc

Name:                    SFEpython-hashlib
Summary:                 Python secure hash and message digest module (backport for 2.4)
URL:                     http://code.krypto.org/python/hashlib
Version:                 20081119
Source:                  http://code.krypto.org/python/hashlib/hashlib-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
SUNW_Copyright:		 %{name}.copyright

%include default-depend.inc

%define python_version  2.4

%prep
%setup -q -n hashlib-%version

%build
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/site-packages/*

%changelog
* Mon Feb  2 2009 - Sergio Schvezov <sergiusens@ieee.org>
- Initial Version
