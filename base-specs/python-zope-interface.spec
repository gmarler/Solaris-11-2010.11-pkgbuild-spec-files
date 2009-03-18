#
# base spec file for package python-zope-interface
#
# Owner: dkenny
#


Name:                    python-zope-interface
Summary:                 A separate distribution of the zope.interface package used in Zope 3
URL:                     http://zope.org/Wikis/Interfaces/FrontPage
Version:                 3.3.0
Source:                  http://www.zope.org/Products/ZopeInterface/%{version}/zope.interface-%{version}.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:                Python

%{?!pythonver:%define pythonver 2.4}

%prep
%setup -q -n zope.interface-%version

%build
python%{pythonver} ./setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} ./setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Copied from spec-files-other
* Thu Nov 27 2008 - darren.kenny@sun.com
- Split from SUNWpython-zope-interface.spec
* Tue Sep 16 2008 - matt.keenn@sun.com
- Update copyright
* Mon May 26 2008 - damien.carbery@sun.com
- Add Build/Requires SUNWPython/-devel.
* Wed Feb 19 2008 - darren.kenny@sun.com
- Revert to 3.3.0 since 3.4.x series seems to be too unstable (and version
  number keeps changing). Wait until 3.4.x stabilises before returning to it.
* Tue Feb 19 2008 - ghee.teo@sun.com
- Updated version to 3.4.1
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- Initial version
