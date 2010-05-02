#
# spec file for package SFEfreeglut.spec
#
# includes module(s): freeglut
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use freeglut_64 = freeglut.spec
%endif

%include base.inc
%use freeglut = freeglut.spec

Name:                   SFEfreeglut
Summary:                %{freeglut.summary}
Version:                %{freeglut.version}
Patch1:                 freeglut-01-sun.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

Requires:		SUNWxorg-mesa
BuildRequires:		SUNWxorg-mesa

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%freeglut_64.prep -d %name-%version/%_arch64
cd %name-%version/%_arch64/freeglut-%{version}
%patch1 -p0
cd ../../..
%endif

mkdir %name-%version/%{base_arch}
%freeglut.prep -d %name-%version/%{base_arch}
cd %name-%version/%{base_arch}/freeglut-%{version}
%patch1 -p0
cd ../../..

%build
%ifarch amd64 sparcv9
%freeglut_64.build -d %name-%version/%_arch64
%endif

%freeglut.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%freeglut_64.install -d %name-%version/%_arch64
%endif

%freeglut.install -d %name-%version/%{base_arch}

mkdir -p $RPM_BUILD_ROOT/%{_prefix}/include
mv $RPM_BUILD_ROOT/%{_prefix}/X11/include/GL $RPM_BUILD_ROOT/%{_prefix}/include
rmdir $RPM_BUILD_ROOT/%{_prefix}/X11/include
rmdir $RPM_BUILD_ROOT/%{_prefix}/X11

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_prefix}/include/GL

%changelog
* Sun May 02 2010 - Milan Jurik
- fix for new builds, new place for header files
* Sun Apr 11 2010 - Milan Jurik
- adding missing build dep
* Fri Aug 21 2009 - Milan Jurik
- multiarch support, the official tarball URL
* Thu Nov 20 2008 - dauphin@enst.fr
- freeglut-2.6.0-rc1, but i comment old line in case of...
- TODO, there is no 2.6.0 tar file, I make it from the cvs repo. and 
- make my own tar file on my own site. When 2.6.0 is out change the url.
* Sat Aug 30 2008 - harry.lu@sun.com
- use %sf_download instead of a specific server.
* Sat Oct 13 2007 - laca@sun.com
- add /usr/X11 to CFLAGS and LDFLAGS to be able to build with FOX
* Tue Jun  5 2007 - dougs@truemail.co.th
- Added SFEjam as a build requirement
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
