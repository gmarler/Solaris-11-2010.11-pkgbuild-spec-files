#
# spec file for package SFExz
#
# includes module(s): xz
#

%include Solaris.inc

Name:		SFExz
Version:	5.0.0
Summary:	LZMA utils
URL:		http://tukaani.org/xz
Source:		http://tukaani.org/xz/xz-%{version}.tar.bz2

Group:		Applications/Archivers
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%define cc_is_gcc 0

%description
XZ Utils is free general-purpose data compression software with high
compression ratio. XZ Utils were written for POSIX-like systems (GNU/Linux,
*BSDs, etc.), but also work on some not-so-POSIX systems like Windows. XZ Utils
are the successor to LZMA Utils. 

%if %build_l10n
%package l10n
Summary:        %{summary} - l10n files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc
Requires:       %{name}
%endif

%prep
%setup -q -c -n %{name}-%{version}

%build
cd xz-%{version}
CFLAGS="$CFLAGS -D_FILE_OFFSET_BITS=64"
CXXFLAGS="$CXXFLAGS -D_FILE_OFFSET_BITS=64"
export CFLAGS CXXFLAGS
./configure --prefix=%{_prefix}                 \
            --libexecdir=%{_libexecdir}         \
            --mandir=%{_mandir}                 \
            --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info          \
	    --disable-static			\
	    --disable-assembler
make

%install
cd xz-%{version}
rm -rf ${RPM_BUILD_ROOT}
gmake install DESTDIR=${RPM_BUILD_ROOT}

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0755, root, sys)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %_datadir
%attr (-, root, other) %_datadir/locale
%endif

%changelog
* Fri Nov  5 2010 - Alex Viskovatoff
- Update to 5.0.0, adding l10n
* Wed Jun 02 2010 - brian.cameron@oracle.com
- Initial setup.
