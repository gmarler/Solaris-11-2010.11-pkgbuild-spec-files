#
# spec file for package SFEsshfs
#
#
# you will need FUSE see: http://www.opensolaris.org/os/project/fuse

%include Solaris.inc

%define src_name sshfs-fuse
%include base.inc

Name:                    SFEsshfs
Summary:                 sshfs - filesystem access over SSH
Version:                 2.2
License:                 GPLv2
Source:			 %{sf_download}/fuse/%{src_name}-%{version}.tar.gz
Patch1:                  sshfs-fuse-01-sunpro.diff
Url:                     http://www.tuxera.com/community/sshfs-download/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
%define _execprefix %{_prefix}

BuildRequires: SUNWlibfuse
Requires: SUNWfusefs
Requires: SUNWlibfuse

%prep
%setup -q -n %src_name-%version
%patch1 -p1

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"

aclocal
autoheader
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
	    --mandir=%{_mandir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fs/sshfs
ln -s %{_bindir}/sshfs $RPM_BUILD_ROOT%{_libdir}/fs/sshfs/mount
%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/sshfs
%{_libdir}/fs/sshfs/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Sat May 29 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec.
