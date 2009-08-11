#
# spec file for package SFEpython26-sqlalchemy
#
# includes module(s): sqlalchemy
#
%include Solaris.inc

%define src_url     http://nchc.dl.sourceforge.net/sourceforge/sqlalchemy
%define src_name    SQLAlchemy

Name:                    SFEpython26-sqlalchemy
Summary:                 SQL-Alchemy is a Python SQL toolkit and Object Relational Mapper
URL:                     http://www.sqlalchemy.org
Version:                 0.5.5
Source:                  %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython26

%include default-depend.inc

%define python_version  2.6

%prep
%setup -q -n %{src_name}-%{version}

%build
python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT/% --prefix=%{_prefix} --no-compile

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
* Mon Aug 10 2009 - matt@greenviolet.net
- Initial spec based on SFEpython-sqlalchemy.spec
* Sun Nov 04 2007 - Ananth Shrinivas <ananth@sun.com>
- Initial Version
