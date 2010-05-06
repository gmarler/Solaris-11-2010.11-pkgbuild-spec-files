#
# spec file for package SFEwaf.spec
#
# includes module(s): waf
#
#
%include Solaris.inc

%define pythonver 2.6

Summary:	The Waf build system
Name:		waf
Version:	1.5.16
SUNW_BaseDir:   %{_basedir}
Release:	1
License:	BSD
Group:		Development/Building
Source0:	http://waf.googlecode.com/files/%{name}-%{version}.tar.bz2
Patch0:		%{name}-01-path.diff
URL:		http://code.google.com/p/waf/

Requires:       SUNWgnome-python26-libs
BuildRequires: SUNWPython26-devel
Requires: SUNWPython26

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

#define		_libdir	%{_prefix}/lib

%description
Waf is a general-purpose build system which was modelled from Scons.
Though it comes last in the arena of the build systems, we believe
that Waf is a vastly superior alternative to its competitors
(Autotools, Scons, Cmake, Ant, etc) for building software,

%prep

rm -rf %name-%version
mkdir -p %name-%version

%setup -q -n %name-%version
%patch0 -p1

%build
./waf-light configure \
	--prefix=%{_prefix}
./waf-light --make-waf

%install
rm -rf $RPM_BUILD_ROOT
	

echo y | ./waf install \
	--prefix %{_prefix} \
	--destdir $RPM_BUILD_ROOT

find $RPM_BUILD_ROOT \( -name \*.pyc -o -name \*.pyo \) -exec rm {} \;


%clean
rm -rf $RPM_BUILD_ROOT

%files

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%attr(755,root,root) %{_bindir}/waf
%dir %{_libdir}/waf
%dir %{_libdir}/waf/wafadmin
%{_libdir}/waf/wafadmin/*.py
%dir %{_libdir}/waf/wafadmin/Tools
%{_libdir}/waf/wafadmin/Tools/*.py
%doc README TODO ChangeLog

%changelog
* Fri May 05 2010 yuntong.jin@sun.com
- Init spec file

