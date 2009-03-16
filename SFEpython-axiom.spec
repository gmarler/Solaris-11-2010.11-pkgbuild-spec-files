#
# spec file for package SFEpython-axiom.spec
#
# includes module(s): python-axiom
#

%include Solaris.inc
Name:                    SFEpython-axiom
Summary:                 An in-process object-relational database
URL:                     http://www.divmod.org/trac/wiki/DivmodAxiom
Version:                 0.5.31
Source:                  http://divmod.org/trac/attachment/wiki/SoftwareReleases/Axiom-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
BuildRequires:           SUNWpython-twisted
BuildRequires:           SFEpython-epsilon

%include default-depend.inc

%define pythonver 2.4

%prep
%setup -q -n Axiom-%version

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
%{_libdir}/python%{pythonver}/vendor-packages/axiom/*
%{_libdir}/python%{pythonver}/vendor-packages/twisted/*

%changelog
* Mon Mar 17 2009 - alfred.peng@sun.com
- Created
