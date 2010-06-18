#
# spec file for package libmp4v2
#
# includes module(s): libmp4v2
#

%define src_ver		1.9.1
%define src_name	mp4v2
%define src_url		http://mp4v2.googlecode.com/files

Name:                    libmp4v2
Summary:                 The MP4v2 library provides an API to create and modify mp4 files as defined by ISO-IEC:14496-1:2001 MPEG-4 Systems.
Version:                 %{src_ver}
Source:                  %{src_url}/%{src_name}-%{version}.tar.bz2
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags" 

if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
    export LDFLAGS="$LDFLAGS -m64"
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jun 18 2010 - Milan Jurik
- fix 64-bit build
* Fri Aug 21 2009 - Milan Jurik
- Initial base spec file
