#
# spec file for package SFEbzr
#
# includes module(s): bzr
#
%include Solaris.inc

%define python_version 2.4
%define tarball_version 1.14.1

Name:			SFEbzr
Summary:		Bazaar Source Code Management System
License:		GPL
Group:			system/dscm
Version:		1.14.1
Distribution:		spec-files-extra
Source:			http://launchpad.net/bzr/1.14/%{tarball_version}/+download/bzr-%{tarball_version}.tar.gz
URL:			http://bazaar-vcs.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SUNWPython
%include default-depend.inc
BuildRequires: SUNWPython-devel


%description
Bazaar source code management system.

%prep
%setup -q -n bzr-%{tarball_version}

%build
export PYTHON="/usr/bin/python"
CFLAGS="$RPM_OPT_FLAGS"
python setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages

# Delete optimized py code
find $RPM_BUILD_ROOT%{_prefix} -type f -name "*.pyo" -exec rm -f {} ';'
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_prefix}/man $RPM_BUILD_ROOT%{_mandir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
%{_libdir}/python%{python_version}/vendor-packages/*
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/bzr.1

%changelog
* Mon May 11 2009 - brian.cameron@sun.com
- Bump to 1.14.1
* Tue Sep 02 2008 - halton.huo@sun.com
- Bump to 1.6.1rc1
* Wed Jan  3 2007 - laca@sun.com
- bump to 0.13
* Mon Jun 12 2006 - laca@sun.com
- rename to SFEbzr
- change to root:bin to follow other JDS pkgs.
* Sat Jan 7 2006  <glynn.foster@sun.com>
- initial version
