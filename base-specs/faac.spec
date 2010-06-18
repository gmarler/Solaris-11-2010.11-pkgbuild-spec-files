#
# spec file for package faac
#
# includes module(s): faac
#

Summary:	Reference encoder and encoding library for MPEG2/4 AAC
Name:		SFEfaac
Version:	1.28
License:	LGPL
Group:		Applications/Multimedia
URL:		http://www.audiocoding.com/
Source:		%{sf_download}/faac/faac-src/faac-%{version}.tar.gz
Patch1:		faac-01-mp4v2.diff
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n faac-%{version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="%{optflags} -I/usr/include/mp4v2"
export CXXFLAGS="%{cxx_optflags} -I/usr/include/mp4v2"
export LDFLAGS="-lmp4v2 -lm"

sh bootstrap

./configure --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --disable-static \
    --with-mp4v2

make -j$CPUS


%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jun 18 2010 - Milan Jurik
- Initial version
