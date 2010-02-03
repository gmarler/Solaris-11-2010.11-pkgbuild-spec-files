#
# spec file for package SFEstorm
#
# includes module(s): storm
#

%define pythonver 2.6

%include Solaris.inc
Name:                    SFEstorm
Summary:                 Object-relational mapper (ORM) for Python
URL:                     http://storm.canonical.com/
Version:                 0.14
Source:                  http://launchpad.net/storm/trunk/0.14/+download/storm-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n storm-%version

%build
python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install --root=%{buildroot}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/storm
%{_libdir}/python%{pythonver}/vendor-packages/storm*egg-info

%changelog
* Tue Jul 07 2009 - Brian Cameron  <brian.cameron@sun.com>
- Created with 0.14.
