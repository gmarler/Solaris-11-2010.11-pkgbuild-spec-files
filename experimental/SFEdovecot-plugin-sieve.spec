#
# spec file for package SFEdovecot-plugin-sieve
#


%define src_name dovecot
%define plugin_name sieve
# maybe set to nullstring outside release-candidates (example: 1.1/rc  or just 1.1)
#%define downloadversion	 1.1/rc
%define downloadversion	 1.2

%include Solaris.inc
Name:                    SFEdovecot-plugin-sieve
Summary:                 dovecot-plugin-sieve - A Maildir based pop3/imap email daemon - Plugin for secure serverside scripting
URL:                     http://wiki.dovecot.org/LDA/Sieve/Dovecot
#note: see downloadversion above
Version:                 0.1.14
Source:                  http://www.rename-it.nl/dovecot/%{downloadversion}/%{src_name}-%{downloadversion}-%{plugin_name}-%{version}.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SFEdovecot
Requires: SFEdovecot

%include default-depend.inc


%prep
%setup -q -n %{src_name}-%{downloadversion}-%{plugin_name}-%{version}


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir}         \
            --with-moduledir=%{_libexecdir}/%{src_name}/modules \
            --datadir=%{_datadir}	\
            --sysconfdir=%{_sysconfdir}/%{src_name} \
            --enable-shared		\
            --with-rundir=%{_localstatedir}/run/%{src_name} \
	    --disable-static		\
            --with-dovecot=/usr/lib/dovecot
##TODO## SFEdovecot needs adjustments to the layout to get rid of the double dovecot/dovecot path

            #--libexecdir=%{_libdir}/%{src_name} \

gmake -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libexecdir}/%{src_name}/modules/lda/*.la

mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{name}/
cp -pr doc examples $RPM_BUILD_ROOT/%{_docdir}/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc AUTHORS COPYING COPYING.LGPL ChangeLog INSTALL NEWS README TODO
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/%{src_name}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%{_docdir}/%{name}/doc/*
%{_docdir}/%{name}/examples/*




%changelog
* Thu Feb 04 2010 - Albert Lee <trisk@opensolaris.org>
- Set CFLAGS
* Thu Jan 07 2010 - Thomas Wagner
- initial 0.1.14
