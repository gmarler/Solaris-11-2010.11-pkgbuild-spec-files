#
# spec file for package freeglut
#
# includes module(s): freeglut
#

%define src_name	freeglut
%define src_url		%{sf_download}/freeglut

Name:                   SFEfreeglut
Summary:                Free OpenGL Library
Version:                2.6.0
Source:                 %{src_url}/freeglut/%{src_name}-%{version}.tar.gz
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -c -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd freeglut-2.6.0
chmod 755 ./configure

export CFLAGS="%optflags -DTARGET_HOST_POSIX_X11=1"
export LDFLAGS="%_ldflags" 

./configure --prefix=%{_prefix}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
            --enable-shared             \
            --disable-static            \
            --includedir=%{_prefix}/X11/include

make -j$CPUS

%install
cd freeglut-2.6.0
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Feb 03 2010 - Brian Cameron <brian.cameron@sun.com>
- Bump to 2.6.0.
* Tue Oct 13 2009 - Milan Jurik
- autogen is not needed, all configure stuff is on place already.
* Fri Aug 21 2009 - Milan Jurik
- Initial base spec file.
