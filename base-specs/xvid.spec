#
# spec file for package xvid
#
# includes module(s): xvid
#

%define	src_ver 1.2.2
%define	src_name xvidcore
%define	src_url	http://downloads.xvid.org/downloads


Name:		SFExvid
Summary:	ISO MPEG-4 compliant video codec
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		xvid-01-solaris.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{xorg_inc} -I%{gnu_inc}"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export ac_cv_prog_ac_yasm=no

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
	ASSEMBLY="--disable-assembly"
	export CFLAGS="-m64 $CFLAGS"
	export LDFLAGS="-m64 $LDFLAGS"
else
	ASSEMBLY="--enable-assembly"
fi

cd build/generic
bash ./bootstrap.sh

./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir}		\
            $ASSEMBLY

make -j$CPUS

%install
cd build/generic
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
(
   cd $RPM_BUILD_ROOT%{_libdir}
   ln -s libxvidcore.so.4.2 libxvidcore.so.4
   ln -s libxvidcore.so.4.2 libxvidcore.so
)

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Aug 22 2009 - Milan Jurik
- Initial base spec file
