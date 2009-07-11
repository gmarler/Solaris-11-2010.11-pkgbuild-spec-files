#
# spec file for package SFEspamassassin
#
#

#TODO# re-work perl specific prerequisites...

%define src_name spamassassin
%define module_version 3.2.5
%define module_name Mail-Spamassassin
%define module_name_major Mail
%define module_package_name mail-spamassassin
#still unused: %define module_name_minor spamassassin

%define perl_version 5.8.4

%include Solaris.inc

%define perlmodulepkgnameprefix SFEperl
%define contact_address_spamreport postmaster@localhost

Name:                    SFEspamassassin
Summary:                 spamassassin - a spam filter for email which can be invoked from mail delivery agents
URL:                     http://spamassassin.apache.org/
Version:                 %{module_version}
Source:                  http://ftp.uni-erlangen.de/pub/mirrors/apache/spamassassin/source/Mail-SpamAssassin-%{version}.tar.bz2
Source1:		 spamassassin.xml
License: Apache License 2.0

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWperl584core
BuildRequires:           SUNWperl584core
BuildRequires:           SUNWsfwhea

#Absolutely necessary perl modules
BuildRequires: SFEperl-digest-sha1
Requires: SFEperl-digest-sha1
BuildRequires: SFEperl-html-parser
Requires: SFEperl-html-parser
BuildRequires: SFEperl-net-dns
Requires: SFEperl-net-dns
#INSTALL file says this is required, build/check_dependencies does not complain..
BuildRequires: SFEperl-libwww-perl
Requires: SFEperl-libwww-perl

BuildRequires: SFEperl-encode-detect
Requires: SFEperl-encode-detect
BuildRequires: SFEperl-mail-spf
Requires: SFEperl-mail-spf

Requires: SFEperl-razor-agents
#http://www.opensourcehowto.org/how-to/postfix/fighting-spam-with-spamassassin-pyzor-dcc-razor--rules-du-jour.html#Rules Du Jour
#8. Next make a razor user
#useradd -d /bin/null -s /bin/bash razor
#9. now change into the razor user and
#su razor
#razor-admin -create
#exit
#10. Register your Razor install with the Razor servers. Replace the address with your admin’s e-mail address:
#razor-admin -register -user= admin@mydomain.comThis e-mail address is being protected from spam bots, you need JavaScript enabled to view it This email address is being protected from spam bots, you need Javascript enabled to view it
#11.  comming soon ... 


#TODO# make the spec file for that: Requires: SFEperl-pyzor

#optional perl modules for improvements/special features

BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries

#obsolete pkgbuild: Requires: SFEperl-mail-spf-query
#pkgbuild: Requires: SFEperl-ip-country


#we *want* this one   (Note: this is the output of a pkgbuild run of *this* spec file, just in case you want to refresh the list below by copy&paste)
#pkgbuild: Requires: SFEperl-net-ident
#pkgbuild: Requires: SFEperl-io-socket-sl
#pkgbuild: Requires: SFEperl-mail-domainkeys
#pkgbuild: Requires: SFEperl-mail-dkim
#pkgbuild: Requires: SFEperl-lwp-useragent
#pkgbuild: Requires: SFEperl-htp-date
#pkgbuild: Requires: SFEperl-archive-tar
#pkgbuild: Requires: SFEperl-io-zlib

#we have in SFE a special naming mess for the perl modules. :)
Requires: SFEperl-compress-zlib
Requires: SFEperl-archive-tar
Requires: SFEperl-io-zlib
#for sa-update we need more
Requires: SFEperl-package-constants
Requires: SFEgnupg2

#INSTALL file says this is highly recommended:
#DB_File
#MIME::Base64
#Net::SMTP
#IP::Country::Fast
#Mail::DKIM
#Mail::DomainKeys
#Net::SMTP
#Time::HiRes
#Razor2 (If you do not plan to use this plugin, be sure to comment out its loadplugin line in /etc/spamassassin/v310.pre)

#from http://advosys.ca/papers/email/53-postfix-filtering.html
#install MIME::Base64
#install MIME::QuotedPrint
#install Net::DNS
#install DB_File


#from: http://www.opensourcehowto.org/how-to/postfix/fighting-spam-with-spamassassin-pyzor-dcc-razor--rules-du-jour.html#Rules Du Jour
# 5. Once it has installed change the local.cf configuration file
# nano /etc/mail/spamassassin/local.cf
# local.cf:
# dcc_path /usr/local/bin/dccproc
# dcc_body_max 999999
# dcc_timeout 10
# dcc_fuz1_max 999999
# dcc_fuz2_max 999999 

%ifarch sparc
%define perl_dir sun4-solaris-64int
%else
%define perl_dir i86pc-solaris-64int 
%endif
%include default-depend.inc

#from the original spamassassin.spec in the source tarball
%description
SpamAssassin provides you with a way to reduce, if not completely eliminate,
Unsolicited Bulk Email (or "spam") from your incoming email.  It can be
invoked by a MDA such as sendmail or postfix, or can be called from a procmail
script, .forward file, etc.  It uses a perceptron-optimized scoring system
to identify messages which look spammy, then adds headers to the message so
they can be filtered by the user's mail reading software.  This distribution
includes the spamc/spamc components which considerably speeds processing of
mail.

%prep
%setup -q -n Mail-SpamAssassin-%{version}


# below: not rock solid detection of missing perl modules because manually installed perl modules would not"
# result in complete (Build)Requires entries (package dependencies) in this spec file
# it uses the spamassassin provided check script in build/check_dependencies

REQUIREDPERLMODULES=`build/check_dependencies 2>/dev/null| grep -i "REQUIRED module missing: " | sed -e 's/^.*missing: //' -e 's/::/-/g' | tr -s '[:upper:]' '[:lower:]'`

if echo $REQUIREDPERLMODULES | grep -v "^$" 
  then
  echo "Required missing: $REQUIREDPERLMODULES"
  echo "ERROR: missing required Spamassassin Perl Module(s). Requirements of SFEspamassassin.spec seem to have changes and must be extended in SFEspamassassin.spec."
  echo "ERROR: required perl modules missing, you need to add them to BuildRequires: and Requires: in the spec file."
  echo "ERROR: eventually you need to write a new spec file to get the required perl module."
  for PERLMODULE in $REQUIREDPERLMODULES
   do
   echo "BuildRequires: %perlmodulepkgnameprefix-$PERLMODULE"
   echo "Requires: %{perlmodulepkgnameprefix}-$PERLMODULE"
   done #REQUIREDPERLMODULES
  exit 1
fi #$REQUIREDPERLMODULES

#below: only tell about the optional modules. e.g. Archive::Tar for having sa-update working
WANTEDPERLMODULES=`build/check_dependencies 2>/dev/null| grep -i " module missing: " | sed -e 's/^.*missing: //' -e 's/::/-/g' | tr -s '[:upper:]' '[:lower:]'`

if echo $WANTEDPERLMODULES | grep -v "^$" 
  then
  echo "suggested perl modules missing, consider adding them to BuildRequires: and Requires: in the spec file"
  echo "suggestion for this spec build recipe: add or write and add required perl modules with this syntax:"
  for PERLMODULE in $WANTEDPERLMODULES
   do
   echo "BuildRequires: %{perlmodulepkgnameprefix}-$PERLMODULE"
   echo "Requires: %{perlmodulepkgnameprefix}-$PERLMODULE"
   done #WANTEDPERLMODULES
fi #$WANTEDPERLMODULES


#smapassassin manifest
cp -p %{SOURCE1} spamassassin.xml

%build

#NOTE# special to this module: --no-online-tests

perl Makefile.PL \
	PREFIX=%{_prefix} SYSCONFDIR=%{_sysconfdir} DESTDIR=$RPM_BUILD_ROOT \
	CONFDIR=%{_sysconfdir}/%{src_name} \
	INSTALLSITELIB=%{_prefix}/perl5/vendor_perl/%{perl_version} \
	INSTALLSITEARCH=%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
	ENABLE_SSL=yes \
	CONTACT_ADDRESS=%{contact_address_spamreport} \
	--no-online-tests

make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC \

#TODO# check if the make libspamc.so is needed
[ -f spamd/libspamc.so ] && cp -p spamd/libspamc.so spamd/libspamc.so.$$
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC \
      spamc/libspamc.so


%install
rm -rf $RPM_BUILD_ROOT
make install \
	INSTALLSITELIB=%{_prefix}/perl5/vendor_perl/%{perl_version} \
	INSTALLSITEARCH=%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
	INSTALLMAN1DIR=%{_mandir}/man1 \
	INSTALLMAN3DIR=%{_mandir}/man3 \
	INSTALLSITEMAN1DIR=%{_mandir}/man1 \
	INSTALLSITEMAN3DIR=%{_mandir}/man3 \
	INSTALLVENDORMAN1DIR=%{_mandir}/man1 \
	INSTALLVENDORMAN3DIR=%{_mandir}/man3

mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/site/
cp spamassassin.xml ${RPM_BUILD_ROOT}/var/svc/manifest/site/

#remove /usr/lib/i86pc-solaris-64int/perllocal.pod 
rm -rf $RPM_BUILD_ROOT%{_prefix}/lib

[ -f $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/5.8.4/%{perl_dir}/auto/Mail/SpamAssassin/.packlist ] && rm $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/5.8.4/%{perl_dir}/auto/Mail/SpamAssassin/.packlist
[ -d $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/5.8.4/%{perl_dir} ] && rm -r $RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/5.8.4/%{perl_dir}

#%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr (-, root, bin)
#%doc README Changes sample-nonspam.txt sample-spam.txt INSTALL LICENSE TRADEMARK USAGE UPGRADE
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, sys) %{_datadir}/%{src_name}
%{_datadir}/%{src_name}/*
#%dir %attr(0755, root, other) %{_docdir}
#%{_docdir}/%{src_name}/*
%attr (0755, root, sys) %dir %{_sysconfdir}
%attr (0755, root, bin) %dir %{_sysconfdir}/%{src_name}
#%{_sysconfdir}/%{src_name}/*
%class(renamenew) %{_sysconfdir}/%{src_name}/*
%dir %attr (0755,root,bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_prefix}/perl5
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
%{_prefix}/perl5/vendor_perl/%{perl_version}/*
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}
#%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/%{module_name_major}/*
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto
#%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, sys) %{_localstatedir}
%defattr (-, root, sys)
%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/spamassassin.xml



%changelog
* Sat Jul 11 2009 - Thomas Wagner
- add Requires: SFEperl-archive-tar, SFEperl-io-zlib, SFEgnupg2.spec to have sa-update working
- add patch to sa-update (use /usr/bin/gpg2 instead /usr/bin/gpg)
- add Requires: SFEperl-compres-zlib
- adjust paths in sa-update/sa-compile/sa-learn by complete refresh of the "make" parameters. The
  spamassassin.spec form the source tarball was of great help
- add Requires: SFEperl-razor-agents
* Sat Mai 02 2009 - Thomas Wagner
- add (Build)Requires: SFEperl-encode-detect and (Build)Requires: SFEperl-mail-spf
* Sun Apr 26 2009  - Thomas Wagner
- add %iclass(renamenew) for /etc/spamassassin/*
* Sun Apr 19 2009  - Thomas Wagner
- add manifest for SMF
* Sat Apr 18 2009  - Thomas Wagner
- Initial spec
