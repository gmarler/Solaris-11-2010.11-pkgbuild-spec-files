#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

Name:                SFEscreen
Summary:             Multiplexing text-terminal window manager
Version:             4.0.3
Source:              ftp://ftp.uni-erlangen.de/pub/utilities/screen/screen-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n screen-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-telnet \
            --enable-colors256 \
            --infodir=%{_datadir}/info

# Invocation of setenv in misc.c source file is coded to
# be platform dependent, but it doesn't treat sun platform
# properly. Fixed by appending ` || defined(sun)' to the end
# of the if statement at line 616, thusly...
# (TODO: Report this bug upstream.)

perl -i.orig -lpe 's/$/ || defined(sun)/ if $. == 616' misc.c

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_datadir}/info/dir

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr(0755, root, bin) %{_datadir}/info
%{_datadir}/info/*
%dir %attr (0755, root, other) %{_datadir}/screen
%{_datadir}/screen/*

%changelog
* Mon Jul 19 2010 - pradhap (at) gmail.com
- Enable telnet and color
* Mon Jan 17 2007 - daymobrew@users.sourceforge.net
- Add pkgbuild_postprocess step.
* Wed Nov 08 2006 - Eric Boutilier
- Initial spec
