#
# spec file for package SFEfuse-exfat
#
#
# you will need FUSE see: http://www.opensolaris.org/os/project/fuse

%include Solaris.inc

%include base.inc

%define SFEscons         %(/usr/bin/pkg info scons >/dev/null 2>&1 && echo 0 || echo 1)
%define SUNWlibfuse      %(/usr/bin/pkginfo -q SUNWlibfuse && echo 1 || echo 0)

Name:                    SFEfuse-exfat
Summary:                 Free exFAT file system implementation
Version:                 0.9.2
License:                 GPLv3
Source:			 http://exfat.googlecode.com/files/fuse-exfat-%{version}.tar.gz
Url:                     http://code.google.com/p/exfat/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%if %SFEscons
BuildRequires: SFEscons
%endif

%if %SUNWlibfuse
BuildRequires:  SUNWlibfuse
Requires:       SUNWfusefs
Requires:       SUNWlibfuse
%else
BuildRequires:  SFElibfuse
Requires:       SFEfusefs
Requires:       SFElibfuse
%endif

%prep
%setup -q -n fuse-exfat-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export CPPPATH="/usr/include/fuse"

scons -j $CPUS CC="$CC" CFLAGS="$CFLAGS" CPPPATH="$CPPPATH"

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fs/exfat
cp fsck/exfatck $RPM_BUILD_ROOT%{_sbindir}
cp fuse/mount.exfat-fuse $RPM_BUILD_ROOT%{_sbindir}
ln -s %{_sbindir}/mount.exfat-fuse $RPM_BUILD_ROOT%{_libdir}/fs/exfat/mount
ln -s %{_sbindir}/exfatck $RPM_BUILD_ROOT%{_libdir}/fs/exfat/fsck
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/exfat
%{_libdir}/fs/exfat/*

%changelog
* Fri Sep 21 2010 - Albert Lee <trisk@opensolaris.org>
- Bump to 0.9.2, drop upstreamed patches
- Support SFEfusefs
* Fri Jun 18 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
