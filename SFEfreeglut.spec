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
Patch1:			freeglut260-01.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
#BuildRequires: SFEjam

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%freeglut_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%freeglut.prep -d %name-%version/%{base_arch}


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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_prefix}/X11/include

%changelog
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
