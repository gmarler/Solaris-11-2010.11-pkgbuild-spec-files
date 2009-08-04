#
# spec file for package SFExvid
#
# includes module(s): xvid
#
%include Solaris.inc

%define	src_ver 1.2.2
%define	src_name xvidcore
%define	src_url	http://downloads.xvid.org/downloads

Name:		SFExvid
Summary:	ISO MPEG-4 compliant video codec
Version:	%{src_ver}
License:	GPL
Source:		%{src_url}/%{src_name}-%{version}.tar.bz2
Patch1:		xvid-01-solaris.diff
#Patch2:		xvid-02-nasm.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
#BuildConflicts: SFEyasm
%ifarch i386 amd64
BuildRequires: SFEnasm
%endif

%description
ISO MPEG-4 compliant video codec. You can play OpenDivX and DivX4 videos
with it, too.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}
%patch1 -p1
#%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=/usr/sfw/bin/gcc
export CPPFLAGS="-D_LARGEFILE64_SOURCE -I%{xorg_inc} -I%{gnu_inc}"
export CFLAGS="%gcc_optflags -O4"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export ac_cv_prog_ac_yasm=no

cd build/generic
bash ./bootstrap.sh
# autotools changes -Wl,--version-script to -Wl,-M since
# it thinks we are using the Sun linker.  I do not know
# how to persuade autotools that we are actually using the
# gnu linker /usr/gnu/ld.  Hence the following sed hack.
#mv configure configure.genned
#sed -e 's/-Wl,-M,libxvidcore.ld/-Wl,--version-script,libxvidcore.ld/' configure.genned >configure
#chmod ug+x configure
./configure --prefix=%{_prefix}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir}
make

%install
rm -rf $RPM_BUILD_ROOT
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

%files
%defattr (-, root, bin)
%{_libdir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Aug 04 2009 - Gilles Dauphin
- One patch for configure.in, add -mimpure-text and -shared because of nasm
- don't use yasm. option in configure. enable build with yasm installed
* Sat Jun 13 2009 - Milan Jurik
- upgradde to 1.2.2
* Sat Mar 14 2009 - Milan Jurik
- upgrade to 1.2.1, nasm build support
* Mon Jun 30 2008 - andras.barna@gmail.com
- Force SFWgcc, Remove non-standard CFLAGS (pentiumpro,sse2)
* Sat May 31 2008 - trisk@acm.jhu.edu
- Use default gcc and linker, fix arch options
* Fri May 23 2008 - michal.bielicki <at> voiceworks.pl
- use SFW gcc
- use SFW gld
- changes thanks to Giles Dauphin
* Tue Jan 08 2008 - moinak.ghosh@sun.com
- Removed redundant CFLAGS setting that was overwriting the earlier value.
* Mon Dec 31 2007 - markwright@internode.on.net
- Use SFEgcc 4.2.2.  Add sed hack to change -Wl,-M back to
- -Wl,--version-script for /usr/gnu/bin/ld.
* Fri Aug  3 2007 - dougs@truemail.co.th
- Initial spec
