#
# spec file for package SFEquesoglc
#
# includes module(s): quesoglc
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name quesoglc

Name:		SFEquesoglc
Version:	0.7.2
Summary:	The OpenGL Character Renderer
Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://quesoglc.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires:	SUNWfontconfig
BuildRequires:	SFEfreeglut-devel
BuildRequires:  SFElibfribidi-devel
BuildRequires:	SFElibglew-devel
BuildRequires:	SUNWdoxygen
BuildRequires:	SUNWgnome-common-devel
BuildRequires:	SUNWgcc

%package devel
Summary:	Development files for %{src_name}
Group:		Development/Libraries
Requires:	%{name}
Requires:	SUNWxorg-mesa

%description
The OpenGL Character Renderer (GLC) is a state machine that provides OpenGL
programs with character rendering services via an application programming
interface (API).

%description devel
This package provides the libraries, include files, and other resources needed
for developing GLC applications.

%prep
%setup -q -n %{src_name}-%{version}
rm -f include/GL/{glxew,wglew,glew}.h
ln -s %{_includedir}/GL/{glxew,wglew,glew}.h include/GL/

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
./configure --prefix=%{_prefix} --disable-static 
make -j$CPUS
cd docs
doxygen
cd ../

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libGLC.la

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%{_libdir}/libGLC.so.*

%files devel
%defattr(-, root, bin)
%{_includedir}/GL/glc.h
%{_libdir}/libGLC.so
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%changelog
* Sun May 16 2010 - Milan Jurik
- initial import to SFE, update to 0.7.2
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr 22 2008 Karol Trzcionka <karlikt at gmail.com> - 0.7.1-1
- Update to v0.7.1
- Using original tarball
* Sat Feb 23 2008 Karol Trzcionka <karlikt at gmail.com> - 0.7.0-1
- Update to v0.7.0
* Sat Feb 09 2008 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-5
- Rebuild for gcc43
- Fix typo in patch
* Thu Dec 27 2007 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-4
- Delete %%check
* Sun Dec 23 2007 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-3
- Add %%check section
- Remove redundant BuildRequires
* Sat Dec 22 2007 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-2
- Remove freeB and GLXPL files
- Add html docs
- Add Requires for subpackage -devel
- Fix BuildRequires
* Sat Dec 01 2007 Karol Trzcionka <karlikt at gmail.com> - 0.6.5-1
- Initial release
