#
# spec file for package SFEpyglet
#
# includes module(s): pyglet
#
%include Solaris.inc

%define python_version  2.4

Name:                    SFEpyglet
Summary:                 Cross-platform windowing and multimedia library for Python. 
URL:                     http://www.pyglet.org/
Version:                 1.1.3
Source:                  http://pyglet.googlecode.com/files/pyglet-%{version}.tar.gz
Patch1:                  pyglet-01-lib.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SUNWPython-devel
Requires:                SUNWPython
Requires:                SFEsdl-image
Requires:                SFEsdl-mixer
Requires:                SFEsdl-ttf

%prep
%setup -q -n pyglet-%{version}
%patch1 -p1

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
* Mon Aug 10 2009 - Brian Cameron  <brian.cameron@sun.com>
- Bump to 1.1.3.
* Wed Jan 21 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with version 1.1.2.

