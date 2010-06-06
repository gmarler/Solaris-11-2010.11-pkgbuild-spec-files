Name:                    SFEwxwidgets-gnu
Summary:                 wxWidgets - Cross-Platform GUI Library (g++)
URL:                     http://wxwidgets.org/
Version:                 %{src_ver}
Source:			 %{sf_download}/wxwindows/%{pkg_src_name}-%{src_ver}.tar.bz2
Patch1:                  wxwidgets-01-msgfmt.diff
Patch2:                  wxwidgets-02-Tmacro.diff
# http://trac.wxwidgets.org/changeset/61009
Patch3:                  wxwidgets-03-changeset_r61009.diff
# http://trac.wxwidgets.org/ticket/4697
Patch4:                  wxwidgets-04-wxFileName-ticket-4697.diff
Patch5:                  wxwidgets-05-setup.h.in.diff
SUNW_BaseDir:            %{_basedir}

%prep
rm -rf %{name}-%{src_ver}
%setup -q -n %{pkg_src_name}-%{src_ver}
%patch1 -p1
#%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1

sed -i -e 's,\\$(CC),\\$(CC) \\$(CFLAGS),g' configure
sed -i -e 's,\\$(CXX),\\$(CXX) \\$(CXXFLAGS),g' configure
sed -i -e 's,SHARED_LD_CC="${CC} -G -o",SHARED_LD_CC="${CC} \\$(CFLAGS) -G -o",g' configure
sed -i -e 's,SHARED_LD_CXX="${CXX} -G -o",SHARED_LD_CXX="${CXX} \\$(CXXFLAGS) -G -o",g' configure
sed -i -e 's,$(CXX) -o $@ $(WXRC_OBJECTS),$(CXX) -o $@ $(WXRC_CXXFLAGS) $(WXRC_OBJECTS),' utils/wxrc/Makefile.in
# Rename zh dir to zh_CN as zh is a symlink to zh_CN and causing installation
# problems as a dir.
sed -i -e 's,zh zh_CN,zh_CN,' Makefile.in

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I%{xorg_inc}"
export CC=gcc
export CXX=g++
%if %{is64}
export CFLAGS="%{gcc_optflags64}"
export CXXFLAGS="%{gcc_cxx_optflags64}"
%else
export CFLAGS="%{gcc_optflags}"
export CXXFLAGS="%{gcc_cxx_optflags}"
%endif
%if %using_gld
  export LDFLAGS="-L%{_libdir} -L%{xorg_lib} -R%{_libdir} -R%{xorg_lib} -lm"
  CFLAGS="$( echo $CFLAGS | sed 's/ -Xlinker -i//' )"
  CXXFLAGS="$( echo $CXXFLAGS | sed 's/ -Xlinker -i//' )"
%else
  export LDFLAGS="%{_ldflags} -lm"
  export LD_OPTIONS="-i -L%{_libdir} -L%{xorg_lib} -R%{_libdir}:%{xorg_lib}"
%endif

%if %{is_s10}
export CPPFLAGS="${CPPFLAGS} -I/opt/kde4/include"
%if %{is64}
export PATH=/opt/kde4/bin/%{_arch64}:%{_bindir}:${PATH}
export PKG_CONFIG_PATH="/opt/kde4/lib/%{_arch64}/pkgconfig:/usr/lib/%{_arch64}/pkgconfig"
export PKG_CONFIG="/opt/kde4/bin/%{_arch64}/pkg-config"
%if %using_gld
export LDFLAGS="${LDFLAGS} -L/opt/kde4/lib/%{_arch64} -R/opt/kde4/lib/%{_arch64}"
%else
export LD_OPTIONS="${LD_OPTIONS} -L/opt/kde4/lib/%{_arch64} -R/opt/kde4/lib/%{_arch64}"
%endif
%else
export PATH=/opt/kde4/bin:%{_bindir}:${PATH}
export PKG_CONFIG_PATH="/opt/kde4/lib/pkgconfig:/usr/lib/pkgconfig"
export PKG_CONFIG="/opt/kde4/bin/pkg-config"
%if %using_gld
export LDFLAGS="${LDFLAGS} -L/opt/kde4/lib -R/opt/kde4/lib"
%else
export LD_OPTIONS="${LD_OPTIONS} -L/opt/kde4/lib -R/opt/kde4/lib"
%endif
%endif
%endif

# keep PATH from being mangled by SDL check (breaks grep -E and tr A-Z a-z)
perl -pi -e 's,PATH=".*\$PATH",:,' configure
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --includedir=%{_includedir}		\
            --libdir=%{_libdir}			\
            --enable-gtk2			\
%if %{is_s10}
            --without-gnomeprint		\
            --without-gnomevfs			\
            --with-expat                        \
%else
            --with-gnomeprint			\
            --with-gnomevfs			\
            --without-expat                     \
%endif
            --enable-unicode			\
            --enable-mimetype			\
            --enable-gui			\
            --enable-xrc			\
            --with-gtk				\
            --with-subdirs			\
            --with-sdl                          \
            --with-opengl			\
            --without-libmspack

sed -i -e 's,${compiler} -o ${outfile} -MMD -MF,${compiler} -c -o ${outfile} -MMD -MF,' bk-make-pch

make -j$CPUS
cd contrib
make -j$CPUS
cd ..
cd locale
make allmo
cd ..

%install
make install DESTDIR=$RPM_BUILD_ROOT
cd contrib
make install DESTDIR=$RPM_BUILD_ROOT
cd ..

%if %{is64}
rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/%{_arch64}/wx-config
pushd ${RPM_BUILD_ROOT}%{_prefix}/bin/%{_arch64}
ln -s ../../lib/%{_arch64}/wx/config/gtk2-unicode-release-2.8 wx-config
%else
rm -f ${RPM_BUILD_ROOT}%{_prefix}/bin/wx-config
pushd ${RPM_BUILD_ROOT}%{_prefix}/bin
ln -s ../lib/wx/config/gtk2-unicode-release-2.8 wx-config
%endif
perl -pi -e 's,-pthreads,,' wx-config
popd

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT
