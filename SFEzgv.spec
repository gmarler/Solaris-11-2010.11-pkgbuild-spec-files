#
# spec file for package SFEzgv
#
# includes module(s): zgv
#
%include Solaris.inc

%define	src_name zgv
%define	src_url	ftp://metalab.unc.edu/pub/Linux/apps/graphics/viewers/svga

Name:                SFEzgv
Summary:             Console viewer for many graphics formats
Version:             5.9
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		     zgv-01-solaris.diff
Patch2:		     zgv-02-config.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFElibpcd-devel
Requires: SFElibpcd
BuildRequires: SUNWjpg-devel
Requires: SUNWjpg
BuildRequires: SUNWTiff-devel
Requires: SUNWTiff
BuildRequires: SUNWgawk

%prep
%setup -q -n %{src_name}-%version
%patch1 -p1
%patch2 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export OPTFLAGS="$CFLAGS"
export BACKEND=SDL
export RGB_DB="/usr/X11/lib/X11/rgb.txt"
export RCFILE="%{_sysconfdir}/zgv.conf"
export PREFIX="%{_prefix}"
export AWK=/usr/xpg4/bin/awk
export SHARE_INFIX=/share
export PCDDEF=-DPCD_SUPPORT

make all
make info

%install
rm -rf $RPM_BUILD_ROOT

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
export OPTFLAGS="$CFLAGS"
export BACKEND=SDL
export RGB_DB="/usr/X11/lib/X11/rgb.txt"
export RCFILE="%{_sysconfdir}/zgv.conf"
export PREFIX="%{_prefix}"
export AWK=/usr/xpg4/bin/awk
export SHARE_INFIX=/share
export PCDDEF=-DPCD_SUPPORT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || {
    /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
}

%postun
[ ! -x /usr/sbin/fix-info-dir ] || {
    /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1
}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_infodir}
%{_mandir}

%changelog
* Tue Sep 14 2010 - Milan Jurik
- fix SFEgawk dependency
* Mon Jul 30 2007 - dougs@truemail.co.th
- Initial spec
