#
# spec file for package SFEpybox2d
#
# includes module(s): pybox2d
#

%include Solaris.inc
Name:                    SFEpybox2d
Summary:                 2D physics library for Python
URL:                     http://code.google.com/p/pybox2d/
Version:                 2.0.2
Source:                  http://pybox2d.googlecode.com/files/Box2D-%{version}b1.zip
Patch1:                  pybox2d-01-sun.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
BuildRequires:           SFEbox2d-devel
Requires:                SFEbox2d
Requires:                SUNWPython26

%include default-depend.inc

%define pythonver 2.6

%prep
/bin/rm -fR Box2D-%{version}b1
%setup -q -n Box2D-%{version}b1
%patch1 -p1

%build
export CC="CC"
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
* Sat Oct 23 2010 - brian.cameron@oracle.com
- Created with version 2.0.2
