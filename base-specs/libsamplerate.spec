#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%define src_name libsamplerate
%define src_url http://www.mega-nerd.com/SRC

Name:		SFElibsamplerate
Summary:	libsamplerate - Sample Rate Converter for audio
Version:	0.1.6
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n libsamplerate-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --enable-static=no

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jan 20 2009 - Thomas Wagner
- Bump to 0.1.6
* Thu Sep 18 2008 - Jijun.yu@sun.com
- Bump to 0.1.4.
* Mon May 05 2008 - brian.cameron@sun.com
- Bump to 0.1.3.
* Sun Aug 12 2007 - dougs@truemail.co.th
- Changed to build 64bit
* 20070522 Thomas Wagner
- Initial spec

