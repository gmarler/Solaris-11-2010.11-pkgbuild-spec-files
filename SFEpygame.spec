#
# spec file for package SFEpygame
#
# includes module(s): pygame
#
%include Solaris.inc

%define python_version  2.4

Name:                    SFEpygame
Summary:                 Python gaming
URL:                     http://www.pygame.org/
Version:                 1.8.1
Source:                  http://www.pygame.org/ftp/pygame-%{version}release.tar.gz
Patch1:                  pygame-01-scrap.diff
Patch2:                  pygame-02-noconfirm.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           SUNWPython-devel
Requires:                SUNWPython
Requires:                SFEsdl-image
Requires:                SFEsdl-mixer
Requires:                SFEsdl-ttf

%package devel
Summary:                 %{summary} - developer files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%prep
%setup -q -n pygame-%{version}release
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

%files devel
%defattr (0755, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/python2.4/pygame

%changelog
* Wed Jan 21 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with version 1.8.1.

