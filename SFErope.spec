#
# spec file for package: xfconf
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): xfconf-base.spec
#

%include Solaris.inc

Name:                       rope
Summary:                    Rope is a Python refactoring library that can be used with several editors and IDEs. It provides many refactoring operations as well as forms of code assistance like auto-completion and access to documentation.
URL:                        http://rope.sourceforge.net/
Version:                    0.9.2
SUNW_BaseDir:               %{_basedir}
BuildRoot:                  %{_tmppath}/%{name}-%{version}-build
License:                    GPLv2
Source:                     %{sf_download}/rope/rope-%{version}.tar.gz
SUNW_Copyright:             %{name}.copyright
Meta(info.upstream):        Ali Gholami Rudi
Meta(info.repository_url):  http://bitbucket.org/agr/rope/    
Meta(pkg.detailed_url):     http://rope.sourceforge.net/       
Meta(info.classification):  org.opensolaris.category.2009:Development/Python
Meta(info.maintainer):      Petr Sobotka sobotkap@gmail.com

Requires:                   SUNWPython26

%prep
%setup -q -n rope-%{version}

%build


%install
rm -rf $RPM_BUILD_ROOT
python2.6 setup.py install --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, bin) %{_libdir}/python2.6/site-packages
%{_libdir}/python2.6/site-packages/*

%changelog
* Sat Jan 09 2010 - sobotkap@gmail.com
- Inital version.
