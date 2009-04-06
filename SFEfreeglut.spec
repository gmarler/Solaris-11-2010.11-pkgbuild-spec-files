#
# spec file for package SFEfreeglut.spec
#
# includes module(s): freeglut
#
%include Solaris.inc

%define src_name	freeglut
# TODO: change me when 2.6.0 is out.
#%define src_url		%{sf_download}/freeglut
%define src_url		http://public.enst.fr/SFE/SOURCES

Name:                   SFEfreeglut
Summary:                Free OpenGL Library
#Version:                2.6.0-rc1
Version:                2.6.0.1
Source:                 %{src_url}/%{src_name}-2.6.0-rc1.tar.gz
Patch1:			freeglut260-01.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEjam

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %{src_name}-%{version}
cd freeglut
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd freeglut/freeglut
bash ./autogen.sh
chmod 755 ./configure
#export CC=/usr/sfw/bin/gcc
#export CXX=/usr/sfw/bin/g++
#export CFLAGS="-O3 -fno-omit-frame-pointer -I/usr/X11/include"
#export CXXFLAGS="-O3 -fno-omit-frame-pointer"
#export CFLAGS="%optflags -I/usr/X11/include"
#export LDFLAGS="%_ldflags -lX11 -L/usr/X11/lib -R/usr/X11/lib"
#export LD_OPTIONS="-i"
#./configure --prefix=%{_prefix}			\
#	    --bindir=%{_bindir}			\
#	    --mandir=%{_mandir}			\
#            --libdir=%{_libdir}			\
#            --includedir=%{_prefix}/X11/include	\
#            --datadir=%{_datadir}		\
#            --libexecdir=%{_libexecdir} 	\
#            --sysconfdir=%{_sysconfdir} 	\
#	    --disable-warnings			\
#            --enable-shared			\
#	    --disable-static

export CC=cc
export CXX=CC
export CFLAGS="-DTARGET_HOST_POSIX_X11=1"

CC=cc CXX=CC CFLAGS="-DTARGET_HOST_POSIX_X11=1" ./configure --prefix=/usr --enable-shared --disable-static --includedir=%{_prefix}/X11/include

jam

%install
rm -rf $RPM_BUILD_ROOT
cd freeglut/freeglut
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_prefix}/X11/include

%changelog
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
