#
# spec file for package SFEpython-4Suite-XML
#
# includes module(s): python-4Suite-XML
#

%define pythonver 2.6

%include Solaris.inc
Name:		SFEpython-4Suite-XML
Summary:	4Suite is a Python-based toolkit for XML and RDF application development
Version:	1.0.2
URL:		http://4suite.org/
Group:		Development/Languages/Python
License:	4Suite License
Source:		%{sf_download}/foursuite/4Suite-XML-%{version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n 4Suite-XML-%version

%build
export PYTHON=/usr/bin/python%{pythonver}
python%{pythonver} setup.py config --system \
	--bindir=%{_bindir} --datadir=%{_datadir}/4Suite \
	--sysconfdir=%{_sysconfdir}/4Suite \
	--localstatedir=%{_localstatedir}/lib/4Suite \
	--libdir=%{_libdir}/4Suite --docdir=%{_datadir}/doc/4Suite \
	--localedir=%{_datadir}/locale --mandir=%{_mandir} 

python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}/4Suite
%{_libdir}/python%{pythonver}/vendor-packages/4Suite_XML-1.0.2-py2.6.egg-info
%{_libdir}/python%{pythonver}/vendor-packages/Ft
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/4Suite
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/4Suite

%changelog
* Thu Jun 10 - Milan Jurik
- Initial version
