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


#optional perl modules for improvements/special features

BuildRequires: SUNWopenssl-include
Requires: SUNWopenssl-libraries

#pkgbuild: Requires: SFEperl-mail-spf-query
#pkgbuild: Requires: SFEperl-ip-country
#we *want* this one
#pkgbuild: Requires: SFEperl-razor2
#pkgbuild: Requires: SFEperl-net-ident
#pkgbuild: Requires: SFEperl-io-socket-sl
#pkgbuild: Requires: SFEperl-compres-zlib
#pkgbuild: Requires: SFEperl-mail-domainkeys
#pkgbuild: Requires: SFEperl-mail-dkim
#pkgbuild: Requires: SFEperl-lwp-useragent
#pkgbuild: Requires: SFEperl-htp-date
#pkgbuild: Requires: SFEperl-archive-tar
#pkgbuild: Requires: SFEperl-io-zlib
#pkgbuild: Requires: SFEperl-encode-detect

#INSTALL file says this is highly recommended:
#DB_File
#MIME::Base64
#Net::SMTP
#IP::Country::Fast
#Mail::DKIM
#Mail::DomainKeys
#Net::SMTP
#Time::HiRes
#Encode::Detect
#Razor2 (If you do not plan to use this plugin, be sure to comment out its loadplugin line in /etc/spamassassin/v310.pre)
# BuildRequires: SFEperl-mail-spf
# Requires: SFEperl-mail-spf



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
    UNINST=0 \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    SYSCONFDIR=$RPM_BUILD_ROOT%{_sysconfdir} \
    CONFDIR=$RPM_BUILD_ROOT%{_sysconfdir}/%{src_name} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    ENABLE_SSL=yes \
    CONTACT_ADDRESS=%{contact_address_spamreport} \
    --no-online-tests
make CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC

%install
rm -rf $RPM_BUILD_ROOT
make install

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
* Sun Apr 26 2009  - Thomas Wagner
- add %iclass(renamenew) for /etc/spamassassin/*
* Sun Apr 19 2009  - Thomas Wagner
- add manifest for SMF
* Sat Apr 18 2009  - Thomas Wagner
- Initial spec
