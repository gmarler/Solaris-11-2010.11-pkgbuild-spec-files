Name:                SFEgd
Summary:             library for the dynamic creation of images by programmers
Version:             %{src_ver}
Source:              http://www.libgd.org/releases/gd-%{version}.tar.bz2
Url:	    	     http://www.libgd.org/
SUNW_BaseDir:        %{_basedir}

%prep
%setup -q -n gd-%version
mkdir Patches
cp %{SOURCE2} Patches
gpatch -p 0 < Patches/%{src2_name}

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{xorg_inc} -I%{gnu_inc}"
export CFLAGS="%{gcc_optflags}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path}"

# There is no 64 bit libpng12-config or libpng-config :(
export LIBPNG12_CONFIG="%{_prefix}/bin/libpng12-config"
export LIBPNG_CONFIG="%{_prefix}/bin/libpng-config"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}	\
            --libdir=%{_libdir}	\
            --libexecdir=%{_libexecdir}	\
            --sbindir=%{_prefix}/bin/%{bld_arch} \
            --includedir=%{_includedir}/gd2 \
            --mandir=%{_mandir} \
            --enable-static=no \
	    --localstatedir=/var \
 	    --disable-static \
 	    --disable-rpath \
 	    --with-libiconv-prefix=%{_prefix} \
 	    --with-png=%{_prefix} \
 	    --with-jpeg=%{_prefix} \
 	    --with-fontconfig=%{_prefix} \
 	    --with-freetype=%{_prefix}/sfw \
 	    --with-xpm=%{_prefix}/X11 \
 	    --with-x \
 	    --with-pic
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libgd.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sat Jun 5 2010 - markwright@internode.on.net
- Initial base spec file
