#
# spec file for package SFEpython-id3lib
#
# includes module(s): python-id3lib
#

%include Solaris.inc
Name:                    SFEpython-id3lib
Summary:                 a small, display independent, and quick thumbnailing library
URL:                     http://sourceforge.net/projects/pyid3lib/
Version:                 0.5.1
Source:                  http://downloads.sourceforge.net/pyid3lib/pyid3lib-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython

Patch1:                  python-id3lib-01-const-char.diff

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n pyid3lib-%version
%patch1 -p1

%build
export PYCC_CC=CC
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
%{_libdir}/python%{pythonver}/vendor-packages/pyid3lib.so

%changelog
* Mon Mar 17 2009 - alfred.peng@sun.com
- Created
