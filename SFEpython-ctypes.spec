#
# spec file for package SFEpython-ctypes
#
# includes module(s): python-ctypes
#
%include Solaris.inc

%define python_version  2.4

Name:                    SFEpython-ctypes
Summary:                 Python C data types
URL:                     http://python.net/crew/theller/ctypes/
Version:                 1.0.2
Source:                  %{sf_download}/ctypes/ctypes-1.0.2.tar.gz
Patch1:                  python-ctypes-01-ffitarget.diff
Patch2:                  python-ctypes-02-util-find-library.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SUNWPython-devel
Requires:                SUNWPython
Requires:                SFEsdl-image
Requires:                SFEsdl-mixer
Requires:                SFEsdl-ttf

%prep
%setup -q -n ctypes-%{version}
%patch1 -p1
%patch2 -p1

%build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

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
%{_libdir}/python%{python_version}/vendor-packages/

%changelog
* Fri Feb 20 2009 - Ke Wang <ke.wang@sun.com>
- Added patch2 for find_library in util.py
* Wed Jan 21 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with version 1.0.2.

