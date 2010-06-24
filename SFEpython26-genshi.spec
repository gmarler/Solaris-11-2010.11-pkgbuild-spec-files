#
# spec file for package SFEpython-genshi
#
# includes module(s): genshi
#
%include Solaris.inc

%define src_url         http://ftp.edgewall.com/pub/genshi
%define src_name        Genshi
%define python_version  2.6

Name:                   SFEpython26-genshi
Summary:                Python library that provides components for parsing, generating, and processing HTML, XML or Text
URL:                    http://www.genshitemplates.org
Version:                0.4.4
Source:                 %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-python26-libs
Requires: SUNWPython26
BuildRequires: SUNWgnome-python26-libs-devel
BuildRequires: SUNWPython26-devel


%prep
%setup -q -n %{src_name}-%{version}

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
* Thu Jun 24 2010 - Thomas Wagner
- initial spec was `svn copied' from SFEpython-genshi.spec
- make use the python2.6 version, adjust (Build)Requires and python26 binary
* Sun Oct 14 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
