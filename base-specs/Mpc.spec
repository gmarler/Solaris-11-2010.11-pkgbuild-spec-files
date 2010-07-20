Name:                SFEMpc
Summary:             mpc - C library for the arithmetic of complex numbers
Version:             %{src_ver}
Source:              http://www.multiprecision.org/mpc/download/%{pkg_src_name}-%{version}.tar.gz
Url:	    	     http://www.multiprecision.org/
SUNW_BaseDir:        %{_basedir}

%prep
%setup -q -n mpc-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{gnu_inc}"
export CFLAGS="%{gcc_optflags}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}	\
            --libdir=%{_libdir}	\
            --libexecdir=%{_libexecdir}	\
            --sbindir=%{_prefix}/bin/%{bld_arch} \
            --includedir=%{_includedir} \
            --mandir=%{_mandir} \
            --infodir=%{_infodir} \
            --enable-static=no \
	    --localstatedir=/var \
 	    --disable-static

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Mon July 19 2010 - markwright@internode.on.net
- Initial base spec file
