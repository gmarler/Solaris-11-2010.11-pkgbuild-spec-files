#
# spec file for package stdcxx
#
# includes module(s): stdcxx
#
%define src_ver 4.2.1
%define src_name stdcxx
%define src_url http://www.apache.org/dist/stdcxx

Name:		stdcxx
Summary:	Apache Standard C++ Library
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		stdcxx-01-config.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export TOPDIR=`pwd`
unset LD
export SPRODIR=%{sunpro_prefix}
export GNUDIR=%{gnu_prefix}
export SPROCONFIG=sunpro.config
export GNUCONFIG=gcc.config
export SPROOPTS="%cxx_optflags"
export GNUOPTS="-O4"
export LDOPTIONS="-i -zignore -zcombreloc -Bdirect"

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
	LIBDIR=lib/%{_arch64}
	export BUILDMODE=optimized,shared,pthreads,wide
	export GNUOPTS="$GNUOPTS -m64"
	bldnls=false
else
	LIBDIR=lib
	export BUILDMODE=optimized,shared,pthreads
	bldnls=true
fi

# Sun Studio C++
export BUILDDIR=$SPRODIR
export CXXOPTS="$SPROOPTS"
export CONFIG="$SPROCONFIG"
export INSTALLDIR=%{_prefix}/$SPRODIR
make builddir
(
  cd ${BUILDDIR}
  export LD_OPTIONS="-R${INSTALLDIR}/${LIBDIR}"
  export LD_LIBRARY_PATH=${PWD}/lib
  gmake config
  gmake lib
if $bldnls ; then
  gmake util
  gmake locales
fi
)

# GNU C++
export BUILDDIR=$GNUDIR
export CXXOPTS="$GNUOPTS"
export CONFIG="$GNUCONFIG"
export INSTALLDIR=%{_prefix}/$GNUDIR
make builddir
(
  cd ${BUILDDIR}
  export LD_OPTIONS="-R${INSTALLDIR}/${LIBDIR}"
  export LD_LIBRARY_PATH=${PWD}/lib
  gmake config
  gmake lib
  gmake util
  gmake locales
)

%install
export SPRODIR=%{sunpro_prefix}
export GNUDIR=%{gnu_prefix}

# Sun Studio C++
export BUILDDIR=$SPRODIR
export INSTALLDIR=%{_prefix}/$SPRODIR
export DESTDIR=${RPM_BUILD_ROOT}${INSTALLDIR}

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  LIBDIR=lib/%{_arch64}
  mkdir -p ${DESTDIR}/${LIBDIR}
else
  LIBDIR=lib
  mkdir -p ${DESTDIR}/${LIBDIR}
  cp -pr ${BUILDDIR}/nls ${DESTDIR}/${LIBDIR}
  cp -pr include ${DESTDIR}
  cp -p ${BUILDDIR}/include/config.h ${DESTDIR}/include/
fi

cp ${BUILDDIR}/lib/libstd.so.*.*.* ${DEiles.STDIR}/${LIBDIR}
( cd ${DESTDIR}/${LIBDIR} && ln -s libstd.so.*.*.*  libstd.so )

# GNU C++
export BUILDDIR=$GNUDIR
export INSTALLDIR=%{_prefix}/$GNUDIR
export DESTDIR=${RPM_BUILD_ROOT}${INSTALLDIR}

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  LIBDIR=lib/%{_arch64}
  mkdir -p ${DESTDIR}/${LIBDIR}
else
  LIBDIR=lib
  mkdir -p ${DESTDIR}/${LIBDIR}
  cp -pr ${BUILDDIR}/nls/* ${DESTDIR}/${LIBDIR}
  cp -pr include ${DESTDIR}
  cp -p ${BUILDDIR}/include/config.h ${DESTDIR}/include/
fi

cp ${BUILDDIR}/lib/libstd.so.*.*.* ${DESTDIR}/${LIBDIR}
( cd ${DESTDIR}/${LIBDIR} && ln -s libstd.so.*.*.*  libstd.so )

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Oct 04 2009 - sobotkap@gmail.com
- Added generated config file to be delivered.
* Tue Sep  4 2007 - dougs@truemail.co.th
- Added quicktime and system ffmpeg
* Tue Sep  4 2007 - dougs@truemail.co.th
- Initial base spec file
