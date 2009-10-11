#
# spec file for package SFEbzr
#
# includes module(s): bzr
#
%include Solaris.inc

%define python_version 2.6
%define tarball_version 2.0.0

Name:			SFEbzr
Summary:		Bazaar Source Code Management System
License:		GPL
Group:			system/dscm
Version:		2.0.0
Distribution:		spec-files-extra
Source:                 http://launchpad.net/bzr/2.0/%{version}/+download/bzr-%{tarball_version}.tar.gz
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
export PYTHON="/usr/bin/python%{python_version}"
CFLAGS="$RPM_OPT_FLAGS"
/usr/bin/python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
/usr/bin/python%{python_version} setup.py install --prefix=$RPM_BUILD_ROOT%{_prefix}
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
* Sun Oct 11 2009 - brian.cameron@sun.com
- Bump to 2.0.0, and use Python 2.6.
* Fri Jul 31 2009 - halton.huo@sun.com
- Bump to 1.17
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
