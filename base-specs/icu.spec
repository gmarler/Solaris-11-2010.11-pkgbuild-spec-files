# Base SPEC file for SFEicu.spec
#
# Copyright 2009 Stefan Teleman
# Copyright 2010 Adriaan de Groot
#
# This file is released under the terms of an MIT / 1-clause BSD
# license. See the file LICENSE.MIT for details.

%define tarball_name    icu4c
%define tarball_version 4_4_2

Name:                   icu
Summary:                International Components for Unicode
Version:                4.4.2
Source:			http://download.icu-project.org/files/%tarball_name/%version/%tarball_name-%tarball_version-src.tgz

Patch1: icu-01-qt-bug-7702.diff
Patch2: icu-02-qt-bug-7702.diff
#from upstream http://bugs.icu-project.org/trac/ticket/7695
Patch3:	icu-03-Rpath.diff
# This is executed in the context either of 32- or 64-bit builds.

%prep
%setup -q -n %name
%patch1 -p 1
%patch3
# Patch2 applied below

export LD=CC
export CFLAGS="%optflags"
export CPPFLAGS=""
export CXXFLAGS="-library=stdcxx4 %cxx_optflags"
export LDFLAGS="-library=stdcxx4"
export LIBS=""
PATH=%{_bindir}:$PATH

# Kind of peculiar, but we need to avoid accidentally linking to the
# already installed icu4c libraries in the system, so we push some
# local directories to the front.
PWD=`pwd`
LOCAL_LIB="-L$PWD/source/lib -L$PWD/source/stubdata"
CXXFLAGS="$LOCAL_LIB $CXXFLAGS"
CFLAGS="$LOCAL_LIB $CFLAGS"
LDFLAGS="$LOCAL_LIB $LDFLAGS"
CPPFLAGS="$LOCAL_LIB $CPPFLAGS"

# arch64.inc defines _bindir etc. but not _sbindir
%if %opt_arch64
%define _sbindir %_prefix/sbin/%bld_arch
%endif

cd source
chmod 0755 ./runConfigureICU
./runConfigureICU Solaris \
	--prefix=%{_prefix} \
	--bindir=%{_bindir}\
	--sbindir=%{_sbindir} \
	--libexecdir=%{_libexecdir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--disable-warnings \
	--disable-debug \
	--disable-dependency-tracking \
	--disable-strict \
%if %opt_arch64
	--with-library-bits=64 \
%else
	--with-library-bits=32 \
%endif
	--enable-release \
	--enable-draft \
	--disable-renaming \
	--enable-rpath \
	--enable-threads \
	--enable-extras \
	--enable-icuio \
	--enable-layout \
	--enable-tests \
	--enable-samples \
	--enable-shared \
	--disable-static \
        || { r=$?; cat config.log; exit $r; }
# That runConfigure wrapper will mess up configure's exit code,
# so also check that Makefile was created.
test -f Makefile || { cat config.log ; exit 1 ; }

# Patch2, but by now we're in the source/ dir; the second patch is already
# relative to that directory.
%patch2 -p1

%build
test -f ./runConfigureICU || cd source
# Parallelism seems to break after a while, so finish single-threaded
${MAKE} ${MAKE_CPUS} || ${MAKE}

%install
test -f ./runConfigureICU || cd source
${MAKE} install DESTDIR=${RPM_BUILD_ROOT}


%changelog
* Fri Nov 19 2010 - Alex Viskovatoff
- Adapt kde-solaris base-icu4c.spec, bumping to 4.4.2 from 4.4.1
