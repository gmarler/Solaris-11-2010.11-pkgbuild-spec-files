#
# spec file for package SUNWPython25-extra
#
# includes module(s): Pyrex, elementtree, numpy
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc
%define pythonver 2.5
%use pyrex = Pyrex.spec
%use elementtree = elementtree.spec
%use numpy = numpy.spec

Name:                    SFEPython25-extra
Summary:                 Supplemental Python libraries and utilities
Version:                 2.5.2
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWPython25
Requires: SUNWlexpt
BuildRequires: SUNWsfwhea
BuildRequires: SUNWPython25-devel
BuildRequires: SUNWpython25-setuptools

%prep
rm -rf %name-%version
mkdir %name-%version
%pyrex.prep -d %name-%version
%elementtree.prep -d %name-%version
%numpy.prep -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
export PYTHON=/usr/bin/python2.5
%pyrex.install -d %name-%version
%elementtree.install -d %name-%version
%numpy.install -d %name-%version

mv $RPM_BUILD_ROOT%{_bindir}/pyrexc $RPM_BUILD_ROOT%{_bindir}/pyrexc2.5

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*


%changelog
* Wed Mar 18 2009 - jeff.cai@sun.com
- Moved from spec-files
* Mon Nov 24 2008 - laca@sun.com
- created, based on SUNWPython-extra.spec
* Thu Oct 25 2007 - brian.cameron@sun.com
- Add numpy to add numerical processing extensions to Python.
* Thu Jul 27 2006 - laca@sun.com
- add elementtree
* Thu Oct 27 2005 - laca@sun.com
- add PyXML
- move pyspi to SUNWgnome-python-libs
- change permissions to root:bin
* Thu Oct 20 2005 - damien.carbery@sun.com
- Use %{default_pkg_version} instead of python version.
* Wed Oct 19 2005 - damien.carbery@sun.com
- Initial version.
