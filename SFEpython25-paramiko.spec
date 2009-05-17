#
# spec file for package SFEpython-paramiko
#
# includes module(s): paramiko
#
%include Solaris.inc

%define src_url         http://www.lag.net/paramiko/download
%define src_name        paramiko

Name:                   SFEpython25-paramiko
Summary:                Python module that implements the SSH2 protocol
URL:                    http://www.lag.net/paramiko
Version:                1.7.4
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:			python-paramiko-01-arc4_and_ctr.patch
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires:               SUNWPython25
BuildRequires:          SUNWPython25-devel
Requires:               SFEpython25-crypto

%define python_version  2.5

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

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

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages

%changelog
* Thu May 14 2009 - Denis Bernard <denis@wildservices.net>
- Python 2.5, bump to paramiko 1.7.4
- arcfour and aes-ctr patches
* Fri Oct 12 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
