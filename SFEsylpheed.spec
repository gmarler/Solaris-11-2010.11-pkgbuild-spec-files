#
# spec file for package SUNWsylpheed
#

%include Solaris.inc

%include base.inc

%define src_name        sylpheed
#note: download path changes with beta versions
%define src_url         http://sylpheed.sraoss.jp/sylpheed/v2.7


Name:                     SFEsylpheed
Summary:                  a GTK+ based, lightweight, and fast e-mail client
Version:                  2.7.1
Source:                   %{src_url}/%{src_name}-%{version}.tar.gz
License:                  GPL
URL:                      http://sylpheed.sraoss.jp/
SUNW_BaseDir:  %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#what is the build-req. for SUNWlibmsr?? BuildRequires: 
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWopenssl-include
Requires: SUNWlibmsr
Requires: SUNWgnome-base-libs
Requires: SUNWopenssl-libraries


#descriton taken from original sylpheed.spec file:
%description
Sylpheed is an e-mail client (and news reader) based on GTK+, running on
X Window System, and aiming for
 * Quick response
 * Simple, graceful, and well-polished interface
 * Easy configuration
 * Intuitive operation
 * Abundant features
The appearance and interface are similar to some popular e-mail clients for
Windows, such as Outlook Express, Becky!, and Datula. The interface is also
designed to emulate the mailers on Emacsen, and almost all commands are
accessible with the keyboard.

The messages are managed by MH format, and you'll be able to use it together
with another mailer based on MH format (like Mew). You can also utilize
fetchmail or/and procmail, and external programs on receiving (like inc or
imget).


%prep
%setup -q -n %{src_name}-%{version}


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}          \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --disable-gtkspell		\
            --enable-shared             \
            --disable-static


make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
install -m 644 *.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc AUTHORS COPYING COPYING.LIB ChangeLog ChangeLog.ja ChangeLog-1.0 ChangeLog-1.0.ja README README.es README.ja INSTALL INSTALL.ja NEWS NEWS-1.0 NEWS-2.0 LICENSE TODO TODO.ja
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/%{src_name}
%dir %attr (0755, root, bin) /usr/include/sylpheed
%/usr/include/sylpheed/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/locale
%defattr (-, root, other)
%{_datadir}/locale/*/LC_MESSAGES/%{src_name}.mo
#%dir %attr (0755, root, other) %{_datadir}/%{src_name}
%{_datadir}/%{src_name}/faq/*/*
%{_datadir}/%{src_name}/manual/*/*
#%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
#%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%changelog
* Thu Oct 16 2009 - Dick Hoogendijk
- update to 2.7.1 stable
* Thu Jan 1 2009 - Dick Hoogendijk
- update to the stable 2.6 release
* Thu Jul 3 2008 - Dick Hoogendijk
- update to the stable 2.5 release
* Mon May 12 2008 - Thomas Wagner
- inital spec including base-specs/syhlpeed.spec from the tarball
