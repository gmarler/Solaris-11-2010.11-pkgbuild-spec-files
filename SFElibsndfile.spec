#
# spec file for package SFElibsndfile
#
# includes module(s): libsndfile
#
%include Solaris.inc
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use libsndfile64 = libsndfile.spec
%endif

%include base.inc
%use libsndfile = libsndfile.spec

%define SFEogg_vorbis    %(/usr/bin/pkginfo -q SFEogg-vorbis && echo 1 || echo 0)

Name:                    SFElibsndfile
Summary:                 %{libsndfile.summary}
Version:                 %{libsndfile.version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SFEogg_vorbis
%ifarch amd64 sparcv9
BuildRequires: SFEogg-vorbis-devel
%endif
%endif
BuildRequires: SUNWogg-vorbis-devel
Requires: SUNWogg-vorbis
Requires: SUNWflac
Requires: SUNWlibms
BuildRequires: SUNWaudh

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
rm -rf %name-%version
mkdir %name-%version
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%libsndfile64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libsndfile.prep -d %name-%version/%{base_arch}

%build
%ifarch amd64 sparcv9
%libsndfile64.build -d %name-%version/%_arch64
%endif

%libsndfile.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
%libsndfile64.install -d %name-%version/%_arch64
%endif

%libsndfile.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sndfile-convert
%{_bindir}/sndfile-info
%{_bindir}/sndfile-play
%{_bindir}/sndfile-regtest
%{_bindir}/sndfile-jackplay
%{_bindir}/sndfile-cmp
%{_bindir}/sndfile-metadata-set
%{_bindir}/sndfile-metadata-get
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
#%{_datadir}/octave
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/sndfile-convert
%{_bindir}/%{_arch64}/sndfile-info
%{_bindir}/%{_arch64}/sndfile-play
%{_bindir}/%{_arch64}/sndfile-regtest
%{_bindir}/%{_arch64}/sndfile-jackplay
%{_bindir}/%{_arch64}/sndfile-cmp
%{_bindir}/%{_arch64}/sndfile-metadata-set
%{_bindir}/%{_arch64}/sndfile-metadata-get
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Sat May 09 2009 - Thomas Wagner
- submitting changes suggested by Srirama Sharma:
- add log note about removal of obsoleted libsndfile-01-flac-1.1.3.diff (removal on behalf Srirama Sharma)
- add libsndfile-01-common.diff (new) to fix feature with SUNSPRO compiler detection (add patch on behalf Srirama Sharma)
* Wed Apr 29 2009 - Srirama Sharma
- Fix files section to make 1.0.19 build without problems.
- Remove duplicate Requires: SUNWflac entry
* Tue Mar 03 2009 - Thomas Wagner
- bump to 1.0.19  in base-specs/libsndfile.spec
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Add BuildRequires: SUNWaudh
* Fri Jun 13 2008 - trisk@acm.jhu.edu
- Allow building with SFEogg-vorbis again
* Mon May 05 2008 - brian.cameron@sun.com
- Now that we are building 64-bit libraries in SUNWogg-vorbis, remove
  dependency of SFEogg-vorbis and add SUNWogg-vorbis.
* Thu Jan 24 2007 - Thomas Wagner
- remove %{_mandir}/man1/* from the -devel package
* Sun Aug 12 2007 - dougs@truemail.co.th
- Converted to build 64bit
* Mon Apr 30 2007 - laca@sun.com
- bump to 1.0.17
- add gentoo patch that makes it build with flac 1.1.3
- add patch that fixes the cpp_test test program when built with sun studio
* Mon Jun 12 2006 - laca@sun.com
- rename to SFElibsndfile
- change to root:bin to follow other JDS pkgs.
- get rid of -share pkg
- move stuff around between base and -devel
- add missing deps
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
