#
# spec file for package SFEpyopenssl
#
# includes module(s): pyopenssl
#

%include Solaris.inc
Name:                    SFEpyopenssl26
Summary:                 Python Interface to the OpenSSL library
URL:                     http://pyopenssl.sourceforge.net/
Version:                 0.8
Source:                  %{sf_download}/pyopenssl/pyOpenSSL-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define pythonver 2.6

%prep
%setup -q -n pyOpenSSL-%version

%build
export CFLAGS="%optflags -I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"

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
* Thu Feb 12 2009 - brian.cameron@sun.com
- created 2.6 version based on SFEpyopenssl.spec.
* Wed Oct 29 2008 - brian.cameron@sun.com
- Bump to 0.8.
* Mon Apr 28 2008 - brian.cameron@sun.com
- Created with 0.7.
