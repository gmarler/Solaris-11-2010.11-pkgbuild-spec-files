#
# spec file for package SFEpython-epsilon
#
# includes module(s): python-epsilon
#

%include Solaris.inc
Name:                    SFEpython-epsilon
Summary:                 a small, display independent, and quick thumbnailing library
URL:                     http://www.divmod.org/trac/wiki/DivmodEpsilon
Version:                 0.5.12
License:                 LGPL
Source:                  http://ftp.de.debian.org/debian/pool/main/e/epsilon/epsilon_%{version}.orig.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
BuildRequires:           SUNWpython-twisted

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n Epsilon-%version

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/build/*
%{_libdir}/python%{pythonver}/vendor-packages/epsilon/*

%changelog
* Thu Jun 04 2009 - alfred.peng@sun.com
- Update source URL.
* Mon Mar 17 2009 - alfred.peng@sun.com
- Created
