#
# spec file for package SFEbullet.spec
#
# includes module(s): bullet
#
%include Solaris.inc

%define src_name	bullet
%define src_url		http://bullet.googlecode.com/files

Name:                   SFEbullet
Summary:                Bullet Physics Library
Version:                2.76
URL:			http://code.google.com/p/bullet/
Source:                 %{src_url}/%{src_name}-%{version}.tgz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}b-build
%include default-depend.inc
BuildRequires: SFEjam
BuildRequires: SFEfreeglut-devel
Requires: SFEfreeglut
BuildRequires: SUNWcmake

%prep
%setup -q -n %{src_name}-%{version}
#find . -type f -exec dos2unix {} {} \;

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I/usr/X11/include"
#export CC=/usr/sfw/bin/gcc
#export CXX=/usr/sfw/bin/g++
export CC=/usr/gcc/4.3/bin/gcc
export CXX=/usr/gcc/4.3/bin/g++
export CFLAGS="-O2 -fno-omit-frame-pointer -I%{_prefix}/X11/include "
export CXXFLAGS="-O2 -fno-omit-frame-pointer -I%{_prefix}/X11/include "
export LDFLAGS="-R%{_libdir} -L%{_libdir} -lX11 "

mkdir -p BUILD
cd BUILD

cmake -DCMAKE_LIBRARY_PATH="/opt/SFE/lib:/usr/lib" -DCMAKE_INCLUDE_PATH="/opt/SFE/include:/usr/include" -DHAVE_GCC_VISIBILITY:INTERNAL=0 -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DHAVE_VISIBILITY_SWITCH:INTERNAL=0 -DGLUT_INCLUDE_DIR="%{_prefix}/X11/include" -DGLUT_LIBRARIES="-L%{_libdir} -R%{_libdir} -lglut" -DGLUT_glut_LIBRARY="/opt/SFE/lib/libglut.so" -DBUILD_EXTRAS="off" -DBUILD_DEMOS=off -DBUILD_BULLET_MAYA_DYNAMICA_PLUGIN=off -DINSTALL_LIBS="on" .. -G "Unix Makefiles"

make VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT
cd BUILD
mkdir -p $RPM_BUILD_ROOT/%{_prefix}
make install
mv ./sfw_stage/* $RPM_BUILD_ROOT/%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}
%{_libdir}/lib*.a

%changelog
* May 2010 - Gilles DAuphin
- bump release
* Mar 2010 - Gilles Dauphin
- shared is the default
- jam is in _bindir
* Jul 2009 - Gilles Dauphin
- version is b
* April 2008 - Gilles Dauphin
- adjust name for IPS
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
