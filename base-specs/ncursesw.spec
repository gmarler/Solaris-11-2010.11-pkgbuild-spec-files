#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

# Relegating to /usr/gnu to avoid name collisions with regular curses files

Name:                ncurses
Summary:             Emulation of SVR4 curses with wide character support
Version:             5.7
Source:              http://ftp.gnu.org/pub/gnu/%{name}/%{name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n %{name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%{_ldflags} -L%{_libdir} -R%{_libdir} $LDFLAGS"

./configure --prefix=%{_prefix}	\
	    --bindir=%{_bindir}	\
	    --libdir=%{_libdir}	\
	    --with-shared	\
	    --enable-rpath	\
            --mandir=%{_mandir} \
            --enable-widec

# The following hack sets LD_LIBRARY_PATH in run_tic.sh. It's necessary
# because that script -- which is only run during make install -- fails
# to find the ncurses .so libraries when the install is being done with 
# DESTDIR set. If, for your purposes, /usr/gnu is not the ultimate destination 
# for installation of this package, you need to adjust this accordingly.

perl -i.orig -lne 'print ; if (/^test -z "\${DESTDIR}" \&\& DESTDIR/) {print q^LD_LIBRARY_PATH="$DESTDIR%{_libdir}"; export LD_LIBRARY_PATH^}' misc/run_tic.sh

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_bindir}/clear
rm -f ${RPM_BUILD_ROOT}%{_bindir}/infocmp
rm -f ${RPM_BUILD_ROOT}%{_bindir}/tack
rm -f ${RPM_BUILD_ROOT}%{_bindir}/toe
rm -f ${RPM_BUILD_ROOT}%{_bindir}/tic
rm -f ${RPM_BUILD_ROOT}%{_bindir}/tput
rm -f ${RPM_BUILD_ROOT}%{_bindir}/tset
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
rm -fr ${RPM_BUILD_ROOT}%{_mandir}
rm -fr ${RPM_BUILD_ROOT}%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 15 2010 - Alex Viskovatoff
- Bump to 5.7.
* Sun Aug 10 2008 - andras.barna@gmail.com
- copied from ncurses.spec
* Sat Nov 3 2007 - markwright@internode.on.net
- Bump to 5.6.  Set LDFLAGS=-m64 for 64 bit build.
* Tue Mar 20 2007 - dougs@truemail.co.th
- Changed to be a base spec
* Wed Nov 08 2006 - Eric Boutilier
- Initial spec
