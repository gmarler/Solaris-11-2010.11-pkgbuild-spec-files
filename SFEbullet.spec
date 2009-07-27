#
# spec file for package SFEbullet.spec
#
# includes module(s): bullet
#
%include Solaris.inc

%define src_name	bullet
%define src_url		http://nchc.dl.sourceforge.net/sourceforge/bullet

Name:                   SFEbullet
Summary:                Bullet Physics Library
Version:                2.50
Source:                 %{src_url}/%{src_name}-%{version}b.tgz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}b-build
%include default-depend.inc
BuildRequires: SFEjam
BuildRequires: SFEfreeglut-devel
Requires: SFEfreeglut

%prep
%setup -q -n %{src_name}-%{version}b
find . -type f -exec dos2unix {} {} \;
/bin/ex - configure.ac << EOM
/_AC_SRCPATHS/d
w
q!
EOM

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

bash ./autogen.sh
chmod 755 ./configure
export CPPFLAGS="-I/usr/X11/include"
export CC=/usr/sfw/bin/gcc
export CXX=/usr/sfw/bin/g++
export CFLAGS="-O3 -fno-omit-frame-pointer"
export CXXFLAGS="-O3 -fno-omit-frame-pointer"
export LDFLAGS="%_ldflags -lX11"
export LD_OPTIONS="-i"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
jam

%install
rm -rf $RPM_BUILD_ROOT

/bin/ex - Jamconfig << EOM
/^prefix
s:%{_prefix}:$RPM_BUILD_ROOT%{_prefix}:
/^bindir
s:%{_bindir}:$RPM_BUILD_ROOT%{_bindir}:
/^datadir
s:%{_datadir}:$RPM_BUILD_ROOT%{_datadir}:
/^libdir
s:%{_libdir}:$RPM_BUILD_ROOT%{_libdir}:
wq!
EOM

jam install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}
%{_libdir}/lib*.a
%dir %attr(0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Jul 2009 - Gilles Dauphin
- version is b
* April 2008 - Gilles Dauphin
- adjust name for IPS
* Sun May  6 2007 - dougs@truemail.co.th
- Initial version
