#
# spec file for package SFEpython-buildbot
#
# includes module(s): Buildbot 
#
%include Solaris.inc

%define src_name         buildbot

Name:                    SFEpython-buildbot
Summary:                 A system to automate the compile/test cycle required bymost software projects to validate code changes 
Licence:                 GPL
URL:                     http://buildbot.net/trac 
Version:                 0.7.11
Source:                  %{sf_download}/buildbot/buildbot-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

%include default-depend.inc

%define python_version  2.4

%prep
%setup -q -n buildbot-%version

%build
python setup.py build

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}/vendor-packages/buildbot
%{_libdir}/python%{python_version}/vendor-packages/%{src_name}-%{version}-py%{python_version}.egg-info
%changelog
* Fri Dec 11 2009 - Simon Jin <yuntong.jin@sun.com>
- Initial Version
