#
# spec file for package faad2
#
# includes module(s): faad2
#

Name:                    faad2
Summary:                 A high-quality MPEG audio decoder
Version:                 2.7
Source:                  %{sf_download}/faac/faad2-%{version}.tar.gz
Patch4:                  faad-04-wall.diff
Patch6:                  faad-06-iquote.diff
Patch7:                  faad-07-sunpro.diff
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}-%{version}
%patch4 -p1
%patch6 -p1
%patch7 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
%ifarch sparc
export CXXFLAGS="-norunpath -xO5 -xlibmil -xlibmopt -features=tmplife"
%else
export CXXFLAGS="-norunpath -xO3 -xlibmil -xlibmopt -features=tmplife"
%endif

autoreconf --install
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --with-mpeg4ip                   \
            --with-drm                       \
            --enable-shared		     \
	    --disable-static

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Aug 21 2009 - Milan Jurik
- Initial base spec file
