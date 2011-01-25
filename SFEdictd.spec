#
# spec file for package SFEdictd
#
# includes module(s): dictd
#
%include Solaris.inc
%define srcname		 dictd

Name:                    SFEdictd
Summary:                 Dictd Server and Client
Version:                 1.12.0
URL:                     http://dict.org
License:		 GPLv2
Source:                  %sf_download/project/dict/%srcname/%srcname-%version/%srcname-%version.tar.gz
Patch1:			 dictd-01-Makefile.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

Requires: SUNWcsu
BuildRequires: SFElibmaa-devel
Requires: SFElibmaa

Requires: %name-root
%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
Requires: %name


%prep
%setup -q -n dictd-%version
%patch1 -p1

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

# Use libxnet instead of libsocket
sed 's/-lnsl -lsocket/-lxnet -lnsl/' Makefile > Makefile.xnet
mv Makefile.xnet Makefile

gmake


%install
gmake install DESTDIR=$RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT%_sysconfdir
echo "server dict.org" > $RPM_BUILD_ROOT%_sysconfdir/dict.conf

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) /usr/sbin
/usr/sbin/*

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man8/*

%dir %attr (0755, root, bin) %{_libdir}

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%attr (-, root, root) %{_sysconfdir}/dict.conf


%changelog
* Tue Jan 25 2011 - Alex Viskovatoff
- Update to 1.12.0
* Jun 19 2010 - pradhap (at) gmail.com
- Fixed URL
* Mar 29 2008 - pradhap (at) gmail.com
- Initial dictd spec file.
