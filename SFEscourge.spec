#
# spec file for package SFEscourge.spec
#
# includes module(s): scourge
#
%include Solaris.inc

%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    SFEscourge
Summary:                 S.C.O.U.R.G.E Game
Version:                 0.17
Source:                  %{sf_download}/scourge/scourge-%{version}.src.tar.gz
Source2:		 %{sf_download}/scourge/scourge-%{version}.data.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-net-devel
Requires: SFEsdl-net

%package devel
Summary:                 scourge - developer files, /usr
SUNW_BaseDir:            %{_basedir}
Requires: %name
%include default-depend.inc

%prep
%setup -q -n scourge

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
export CXX=/usr/sfw/bin/g++
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer -fpic -Dpic"
aclocal
autoheader
autoconf
automake -a
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --with-data-dir=%{_datadir}/scourge_data

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}
(
  cd $RPM_BUILD_ROOT%{_datadir} && gtar fxvz %SOURCE2
  dk=scourge_data/models/character/darkness
  nc=scourge_data/models/nightcrawler
  frog=scourge_data/models/frog
  wb=scourge_data/themes/wb-dragoon
  mv "$dk/Read me.txt" $dk/Read_me.txt
  mv "$dk/Lisez moi.txt" $dk/Lisez_moi.txt
  mv "$nc/Read me.txt" $nc/Read_me.txt
  mv "$nc/Lisez moi.txt" $nc/Lisez_moi.txt
  mv "$frog/Sound Readme.txt" $nc/Sound_Readme.txt
  mv "$wb/whiteblazer readme.txt" $wb/whiteblazer_readme.txt
)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/scourge_data

%changelog
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Mon Apr 23 2006 - dougs@truemail.co.th
- Fixed Summary
* Sun Apr 22 2006 - dougs@truemail.co.th
- Initial version
