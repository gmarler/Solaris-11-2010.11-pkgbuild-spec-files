#
# spec file for package SFElibnids.spec
#
%include Solaris.inc

%define src_name libfuse
%define src_url http://hub.opensolaris.org/bin/download/Project+fuse/files
%define tarball_version 20100615

Name:		SFElibfuse
Summary:	Library for FUSE
Version:	0.%{tarball_version}
Group:		System Environment/Libraries
URL:		http://hub.opensolaris.org/bin/view/Project+fuse/
Source:		%{src_url}/%{src_name}-%{tarball_version}.tgz
Source1:	libfuse.exec_attr
Source2:	libfuse.prof_attr
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%name-%version
%include default-depend.inc

Requires:	%{name}-root
Requires:	SFEfusefs
BuildRequires:	SFEfusefs

%description
FUSE stands for 'File system in User Space'. It provides a simple
interface to allow implementation of a fully functional file system
in user-space.  FUSE originates from the Linux community and is
included in the Linux kernel (2.6.14+).

%package devel
Summary:	%{summary} - development files
Requires:	%name

%description devel
This package contains development libraries and C header files needed for
building applications which use libfuse.

%package root
Summary:	%{summary} - root files
SUNW_BaseDir:	/
%include default-depend.inc

%description root
This package contains root files for libfuse.

%prep
%setup -q -n %{src_name}

%build
export MAKE=/usr/ccs/bin/make

/usr/ccs/bin/make

%install
rm -rf $RPM_BUILD_ROOT
/usr/ccs/bin/make install

cp -r proto/ $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/exec_attr.d
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/security/exec_attr.d/libfuse

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/security/prof_attr.d
cp %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/security/prof_attr.d/libfuse

cd $RPM_BUILD_ROOT%{_libdir} && ln -s libfuse.so.* libfuse.so

%ifarch amd64 sparcv9
cd $RPM_BUILD_ROOT%{_libdir}/%{_arch64} && ln -s libfuse.so.* libfuse.so
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri rbac

%postun
%restart_fmri rbac

%files
%defattr(-, root, bin)
%{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_libdir}/fs
%{_libdir}/fs/fuse

%files devel
%defattr(-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/fuse.pc

%files root
%defattr (-, root, sys)
%{_sysconfdir}


%changelog
* Wed Jun 19 2010 - Milan Jurik
- Initial spec
