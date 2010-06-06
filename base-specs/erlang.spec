# base spec for erlang
#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%define pkg_src_name     otp_src
%define src_name         erlang
%define src_ver          R13B04

Name:                    SFEerlang 
Summary:                 erlang - Erlang programming language and OTP libraries (g++-built)
Version:                 %{src_ver}
Release:                 1
License:                 ERLANG PUBLIC LICENSE
Group:                   Development/Languages/Erlang
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://www.erlang.org
Source:                  http://erlang.org/download/%{pkg_src_name}_%{src_ver}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}_%{src_ver}

Patch1:                  erlang-01-lib-wx-c_src-wxe_gl.h.diff

%prep
%setup -q -n %{pkg_src_name}_%{src_ver}
%patch1 -p1
mkdir Patches
cp %{SOURCE2} Patches
cp %{SOURCE3} Patches
cp %{SOURCE4} Patches
cp %{SOURCE5} Patches
cp %{SOURCE6} Patches
cp %{SOURCE7} Patches

gpatch -p 0 < Patches/%{src3_name}
gpatch -p 0 < Patches/%{src4_name}
gpatch -p 0 < Patches/%{src7_name}

chmod 0755 configure

sed -i -e 's,WX_LIBS=`$WX_CONFIG_WITH_ARGS --libs`,WX_LIBS="`$WX_CONFIG_WITH_ARGS --libs` -lGLU",' lib/wx/configure lib/wx/configure.in
sed -i -e '/SSL_DYNAMIC_ONLY=/s:no:yes:' erts/configure erts/configure.in

sed -i -e 's,$rdir/include,$rdir/include/odbc,g' lib/odbc/configure lib/odbc/configure.in
sed -i -e 's,${libdir}/64,${libdir}/%{_arch64},g' lib/odbc/configure lib/odbc/configure.in

export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{gnu_inc} -I%{gnu_inc}/wx-2.8 -I%{_includedir}/gd2 -I%{sfw_inc} -I%{xorg_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} %{sfw_lib_path} %{xorg_lib_path}"
%if %{is64}
export CPPFLAGS="${CPPFLAGS} -DSIZEOF_VOID_P=8 -DSIZEOF_LONG=8"
export CFLAGS="%{gcc_optflags64}"
export CXXFLAGS="%{gcc_cxx_optflags64}"
export LDFLAGS="-m64 ${LDFLAGS}"
%else
export CFLAGS="%{gcc_optflags}"
export CXXFLAGS="%{gcc_cxx_optflags}"
%endif

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}	\
            --libdir=%{_libdir}	\
            --libexecdir=%{_libexecdir}	\
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --enable-static=no \
	    --localstatedir=/var \
 	    --disable-static \
 	    --disable-rpath \
 	    --enable-smp-support \
 	    --enable-threads \
 	    --enable-hipe \
 	    --with-ssl \
%if %{is64}
            --enable-m64-build \
%endif
 	    --enable-dynamic-ssl-lib

%build
export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{gnu_inc} -I%{gnu_inc}/wx-2.8 -I%{_includedir}/gd2 -I%{sfw_inc} -I%{xorg_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} %{sfw_lib_path} %{xorg_lib_path}"
%if %{is64}
export CPPFLAGS="${CPPFLAGS} -DSIZEOF_VOID_P=8 -DSIZEOF_LONG=8"
export CFLAGS="%{gcc_optflags64}"
export CXXFLAGS="%{gcc_cxx_optflags64}"
export LDFLAGS="-m64 ${LDFLAGS}"
%else
export CFLAGS="%{gcc_optflags}"
export CXXFLAGS="%{gcc_cxx_optflags}"
%endif

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
${MAKE}

%install
export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{gnu_inc} -I%{gnu_inc}/wx-2.8 -I%{_includedir}/gd2 -I%{sfw_inc} -I%{xorg_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} %{sfw_lib_path} %{xorg_lib_path}"
%if %{is64}
export CPPFLAGS="${CPPFLAGS} -DSIZEOF_VOID_P=8 -DSIZEOF_LONG=8"
export CFLAGS="%{gcc_optflags64}"
export CXXFLAGS="%{gcc_cxx_optflags64}"
export LDFLAGS="-m64 ${LDFLAGS}"
%else
export CFLAGS="%{gcc_optflags}"
export CXXFLAGS="%{gcc_cxx_optflags}"
%endif

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

$MAKE install DESTDIR=${RPM_BUILD_ROOT}

if [ ! -f ${RPM_BUILD_ROOT}/usr/lib/%{_arch64}/erlang/lib/tools-2.6.5.1/emacs/erlang-skels.el ]
then
    # These files are not installed by make install in the R13B04 Erlang/OTP release
    install -m 0644 lib/tools/emacs/erlang-skels.el ${RPM_BUILD_ROOT}/usr/lib/%{_arch64}/erlang/lib/tools-2.6.5.1/emacs
    install -m 0644 lib/tools/emacs/erlang-skels-old.el ${RPM_BUILD_ROOT}/usr/lib/%{_arch64}/erlang/lib/tools-2.6.5.1/emacs
fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Jun 6 2010 - markwright@internode.on.net
- create
