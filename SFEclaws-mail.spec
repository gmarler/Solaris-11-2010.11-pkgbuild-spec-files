#
# spec file for package SUNWclaws-mail
#

%include Solaris.inc

%include base.inc

%define src_name         claws-mail


Name:                    SFEclaws-mail
Summary:                 Claws-Mail is an e-mail client (and news reader) based on GTK+
Version:                 3.5.0
Source:                  %{sf_download}/sylpheed-claws/%{src_name}-%{version}.tar.bz2
License:                 GPL
URL:                     http://claws-mail.org/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWopenssl-include
BuildRequires: SFEaspell-devel
BuildRequires: SFElibetpan-devel
Requires: SUNWlibmsr
Requires: SUNWgnome-base-libs
Requires: SUNWopenssl-libraries
Requires: SFEpth
Requires: SFElibassuan
Requires: SFEgnupg2
Requires: SFEaspell
Requires: SFEdillo
Requires: SFEbogofilter
Requires: SFElibetpan


%description
Claws-Mail is an e-mail client (and news reader) based on GTK+

%prep
%setup -q -n %{src_name}-%{version}
sed -i -e "s,CFLAGS -Wall,CFLAGS,g" configure configure.ac

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags -xc99"
export LDFLAGS="%_ldflags -lsocket -lnsl"

./configure --prefix=%{_prefix}          \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared             \
            --disable-static            \
            --disable-ldap

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
install -m 644 *.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
rm ${RPM_BUILD_ROOT}%{_bindir}/sylpheed-claws

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/%{src_name}

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/claws-mail
%dir %attr (0755, root, other) %{_libdir}/claws-mail/plugins
%{_libdir}/claws-mail/plugins/*
%dir %attr (0755, root, sys) %{_datadir}
%defattr (-, root, other)
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/%{src_name}/
%dir %attr (0755, root, other) %{_datadir}/doc/%{src_name}/manual
%dir %attr (0755, root, other) %{_datadir}/doc/%{src_name}/manual/en
%dir %attr (0755, root, other) %{_datadir}/doc/%{src_name}/manual/es
%dir %attr (0755, root, other) %{_datadir}/doc/%{src_name}/manual/fr
%dir %attr (0755, root, other) %{_datadir}/doc/%{src_name}/manual/pl
%{_datadir}/doc/%{src_name}/RELEASE_NOTES
%{_datadir}/doc/%{src_name}/manual/en/*
%{_datadir}/doc/%{src_name}/manual/es/*
%{_datadir}/doc/%{src_name}/manual/fr/*
%{_datadir}/doc/%{src_name}/manual/pl/*
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/claws-mail.png
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, bin) %{_datadir}/man
%dir %attr (0755, root, bin) %{_datadir}/man/man1
%{_datadir}/man/man1/claws-mail.1

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/claws-mail.pc
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/claws-mail
%dir %attr (0755, root, bin) %{_includedir}/claws-mail/common
%dir %attr (0755, root, bin) %{_includedir}/claws-mail/gtk
%dir %attr (0755, root, bin) %{_includedir}/claws-mail/etpan
%{_includedir}/claws-mail/*.h
%{_includedir}/claws-mail/common/*.h
%{_includedir}/claws-mail/gtk/*.h
%{_includedir}/claws-mail/etpan/*.h

%changelog
* Thu Oct 2 2008 - markwright@internode.on.net
- create
