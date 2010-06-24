#
# spec file for package SFEgooglecl 
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%define owner jouby 
# 
%include Solaris.inc
#

Summary:       Command line tools for the Google Data APIs
Name:          googlecl
Version:       0.9.7
Release:       0.1
License:       Apache v2.0
Group:         Applications/Text
Source0:       http://googlecl.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5: 936bdb036c340eb1f9d5b9b6b592e1b2
URL:           http://code.google.com/p/googlecl/
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

Requires:    SFEgdata-python26

%{?!pythonver:%define pythonver 2.6}

%include default-depend.inc

%description
The Google Data APIs allow programmatic access to various Google
services. This package wraps a subset of those APIs into a
command-line tool that makes it easy to do things like posting to a
Blogger blog, uploading files to Picasa, or editing a Google Docs
file.

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}
%setup -q

%build
python%{pythonver} setup.py build 

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install \
       --optimize=2 \
       --root=$RPM_BUILD_ROOT


# move to vendor-packages
#
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

echo deleting pyo files
find $RPM_BUILD_ROOT -name '*.pyo' -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_bindir}/google
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/*

%changelog
* Thu Jun 24 2010 - yuntong.jin@sun.com
- Initial add

