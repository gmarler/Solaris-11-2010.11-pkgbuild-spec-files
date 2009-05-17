#
# spec file for package SFEpython-crypto
#
# includes module(s): pycrypto
#
%include Solaris.inc

%define  src_name   pycrypto

Name:                    SFEpython25-crypto
Summary:                 Cryptographic library for the Python Programming Language
URL:                     http://www.amk.ca/python/code/crypto
Version:                 2.0.1
Source:                  http://www.amk.ca/files/python/crypto/pycrypto-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SUNWPython25-devel
Requires:                SUNWPython25

%define python_version  2.5

%prep
%setup -q -n pycrypto-%version

%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

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
%{_libdir}/python%{python_version}

%changelog
* Thu May 14 2009 - Denis Bernard <denis@wildservices.net>
- Python 2.5 port
* Sat Oct 06 2007 - ananth@sun.com
- Initial spec file
