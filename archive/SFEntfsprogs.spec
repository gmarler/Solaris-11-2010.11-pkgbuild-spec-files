#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#

%include Solaris.inc

Name:                SFEntfsprogs
License:             GPL
Summary:             NTFS Filesystems Utilities with full read-write support
Version:             2.0.0
URL:                 http://www.linux-ntfs.org/doku.php
Source:              %{sf_download}/linux-ntfs/ntfsprogs-%{version}.tar.bz2
Patch1:              ntfsprogs-01-ntfsclone.diff
Patch2:              ntfsprogs-02-libntfs.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
The Linux-NTFS project (http://www.linux-ntfs.org/) aims to bring full support
for the NTFS filesystem to the Linux operating system.  The ntfsprogs package
currently consists of a library and utilities such as mkntfs, ntfscat, ntfsls,
ntfsresize, and ntfsundelete (for a full list of included utilities see man 8
ntfsprogs after installation).

Even though ntfsprogs is developed primarily for the Linux platforms the ntfsprogs
packages is portable to other platorms as well which includes OpenSolaris.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -n ntfsprogs-%version
%patch1 -p1
%patch2 -p1

if [ "x`basename $CC`" != xgcc ]
then
        %error This spec file requires Gcc, set the CC and CXX env variables
fi


%build

export CFLAGS="%optflags -I%{gnu_inc} -DINSTALLPREFIX=\\\"%{_prefix}\\\""
export LDFLAGS="%_ldflags %{gnu_lib_path} -liconv -lintl"
export PATH=/usr/bin:${PATH}

./configure --prefix=%{_prefix}	\
            --mandir=%{_mandir}	\
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes \
            --enable-static=no  \
            --with-pic

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Remove stuff that conflict with Solaris native utilities
rm -rf $RPM_BUILD_ROOT/sbin
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/mkfs.ntfs.8

# Create dirs and symlinks to somewhat match with the OpenSolaris
# scheme of things
#
mkdir -p $RPM_BUILD_ROOT%{_libdir}/fs/ntfs

(cd $RPM_BUILD_ROOT%{_libdir}/fs/ntfs
    ln -s ../../../../%{_sbindir}/mkntfs mkfs
    ln -s ../../../../%{_sbindir}/ntfsresize resize
    ln -s ../../../../%{_sbindir}/ntfslabel labelit
    ln -s ../../../../%{_sbindir}/dumpe2fs dump
    ln -s ../../../../%{_sbindir}/ntfsfix fsck
    ln -s ../../../../%{_sbindir}/ntfsclone ntfsdump)

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%{_libdir}/*.la*
%dir %attr (0755, root, sys) %{_libdir}/fs
%dir %attr (0755, root, sys) %{_libdir}/fs/ntfs
%{_libdir}/fs/ntfs/*
%dir %attr (0755, root, bin) %{_libdir}/gnome-vfs-2.0
%dir %attr (0755, root, bin) %{_libdir}/gnome-vfs-2.0/modules
%{_libdir}/gnome-vfs-2.0/modules/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/gnome-vfs-2.0
%dir %attr (0755, root, sys) %{_sysconfdir}/gnome-vfs-2.0/modules
%{_sysconfdir}/gnome-vfs-2.0/modules/*

%changelog
* Sat Feb 02 2008 - moinak.ghosh@sun.com
- Initial spec.
