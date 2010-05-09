#
# spec file for package SFEsupertux.spec
#
# includes module(s): supertux
#
%include Solaris.inc

%define src_name	supertux
%define src_url		http://download.berlios.de/supertux

Name:                   SFEsupertux
Summary:                Super Tux Game
Version:                0.3.1
Source:                 %{src_url}/%{src_name}-%{version}d.tar.bz2
Patch1:                 supertux-01-sprite.diff

SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEphysfs-devel
Requires: SFEphysfs
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-image
BuildRequires: SFEopenal-devel
Requires: SFEopenal
BuildRequires: SFEjam
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -c -n %{name}-%{version}
%patch1 -p0

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd %{src_name}-%{version}

export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
unset CFLAGS
unset CXXFLAGS
unset LDFLAGS
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
            --enable-opengl=no
jam

%install
rm -rf $RPM_BUILD_ROOT

cd %{src_name}-%{version}
ex - Jamconfig << EOM
/^bindir
s:/usr/bin:$RPM_BUILD_ROOT%{_bindir}:
/^datadir
s:/usr/share:$RPM_BUILD_ROOT%{_datadir}:
w
q!
EOM

jam install
( cd $RPM_BUILD_ROOT%{_datadir}
  tar fcp - supertux2 | bzip2 -c > supertux2.tar.bz2
  rm -rf supertux2
  mkdir supertux2
  mv supertux2.tar.bz2 supertux2
)

%post
( cd ${BASEDIR}/share
  bzcat supertux2/supertux2.tar.bz2 | tar xf -
  cd ..
  removef $PKGINST share/supertux2/supertux2.tar.bz2
  rm -f share/supertux2/supertux2.tar.bz2
  removef -f $PKGINST || exit 2
)
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%{_datadir}/supertux2
%dir %attr (0755,root,other) %{_datadir}/doc
%dir %attr (0755,root,other) %{_datadir}/applications
%dir %attr (0755,root,other) %{_datadir}/pixmaps
%{_datadir}/doc/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*

%changelog
* Thu Feb 14 2008 - moinak.ghosh@sun.com
- Fix some kinks with latest SuperTux version.
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
