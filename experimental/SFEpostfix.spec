#
# spec file for package SFEpostfix
#
# prepared for SunStudio compiler
# note: this spec derived partly from the provided postfix.spec, you might update this by comparing with vimdiff SFEpostfix.spec BUILD/postfix-*/tmp/postfix.spec
# note: it also takes several files from the original source-rpm line postfix.spec, make-postfix.spec, postfix-aliases

%include Solaris.inc

%define src_name	postfix
# see much more special variables below

Name:                    SFEpostfix
Summary:                 postfix - Mailer System
URL:                     http://postfix.org/
Version:                 2.5.6
Source:                  ftp://ftp.porcupine.org/mirrors/postfix-release/official/postfix-%{version}.tar.gz
Source2:                 http://ftp.wl0.org/official/2.5/SRPMS/postfix-%{version}-1.src.rpm
Patch1:			postfix-01-make-postfix.spec.diff

SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

#TODO: BuildReqires:
BuildRequires: SFEcpio
BuildRequires: SUNWrpm
BuildRequires: SUNWggrp
#TODO: Requires:

#variables altered from postfix.spec
%define rmail_patch %(which rmail)
%define docdir %{_docdir}/%{name}
#probably not used directly, SMF is the way we should go
%define initdir /etc/init.d
%define	V_postfinger	1.30

#original from postfix.spec
%define readme_dir   %{docdir}/readme
%define html_dir     %{docdir}/html
%define examples_dir %{docdir}/examples

%define newaliases_path %{_bindir}/newaliases.postfix
%define mailq_path %{_bindir}/mailq.postfix
%define rmail_path %{_bindir}/rmail.postfix
%define sendmail_path %{_sbindir}/sendmail.postfix
# Don't use %{_libdir} as it gives the wrong directory on x86_64 servers
%define usrlib_sendmail /usr/lib/sendmail.postfix



%include default-depend.inc

# from the postfix source rpm
#  grep "^%define.*__" postfix.spec.in
# %define distribution __DISTRIBUTION__
# %define mysql_paths __MYSQL_PATHS__
# %define requires_db __REQUIRES_DB__
# %define requires_zlib __REQUIRES_ZLIB__
# %define smtpd_multiline_greeting __SMTPD_MULTILINE_GREETING__
# %define with_alt_prio     __WITH_ALT_PRIO__
# %define with_cdb          __WITH_CDB__
# %define with_ldap         __WITH_LDAP__
# %define with_mysql        __WITH_MYSQL__
# %define with_mysql_redhat __WITH_MYSQL_REDHAT__
# %define with_pcre         __WITH_PCRE__
# %define with_pgsql        __WITH_PGSQL__
# %define with_sasl         __WITH_SASL__
# %define with_spf          __WITH_SPF__
# %define with_dovecot      __WITH_DOVECOT__
# %define with_tls          __WITH_TLS__
# %define with_tlsfix       __WITH_TLSFIX__
# %define with_vda          __WITH_VDA__
# %define rel 1__SUFFIX__
 
#define this here (in original spec generated)
%define mysql_local 0

%define distribution Solaris
%define mysql_paths 0
%define requires_db 0
%define requires_zlib 0
%define smtpd_multiline_greeting 0
%define with_alt_prio     0
%define with_cdb          0
%define with_ldap         0
%define with_mysql        0
%define with_mysql_redhat 0
%define with_pcre         0
%define with_pgsql        0
%define with_sasl         0
%define with_spf          0
%define with_dovecot      0
%define with_tls          0
%define with_tlsfix       0
%define with_vda          0
%define rel 1



%prep
%setup -q -n postfix-%version

mkdir tmp
(cd tmp;
 #rpm2cpio %{SOURCE2} | /usr/gnu/bin/cpio -iumdv  --no-absolute-filenames  postfix.spec.in make-postfix.spec postfix-aliases
 rpm2cpio %{SOURCE2} | /usr/gnu/bin/cpio -iumdv  --no-absolute-filenames 
)

%patch1 -p1

(cd tmp; bash make-postfix.spec)

#last step: change /bin/sh into /usr/bin/bash
#alternatively we could search fo rexecutalbes, then if it starts with "#!/bin/sh"
perl -w -pi.bak -e "s,^#\!\s*/bin/sh,#\!/usr/bin/bash," `find . -type f -exec grep -q "^#\!.*/bin/sh" {} \; -print`

%build

#./configure --prefix=%{_prefix}  \
#            --mandir=%{_mandir}   \
#            --disable-static

#make tidy
#make makefiles \
	#CC=/opt/SUNWspro/bin/cc \
	#AUXLIBS='-L/usr/mysql/lib/mysql -R/usr/mysql/lib/mysql -lmysqlclient -lldap -lpcre' \
	#CCARGS='-DHAS_LDAP \
		#-DHAS_MYSQL \
		#-DHAS_PCRE \
		#-DDEF_DAEMON_DIR=\\\"%daemon_directory\\\" \
		#-I /usr/include/pcre \
		#-I /usr/mysql/include/mysql \
		#'

#make


CCARGS=
AUXLIBS=

%ifarch s390 s390x ppc
CCARGS="${CCARGS} -fsigned-char"
%endif

%if %{with_cdb}
  CCARGS="${CCARGS} -DHAS_CDB"
  AUXLIBS="${AUXLIBS} -lcdb"
%endif

%if %{with_ldap}
  CCARGS="${CCARGS} -DHAS_LDAP"
  AUXLIBS="${AUXLIBS} -L/usr/%{_lib} -lldap -llber"
%endif

%if %{with_pcre}
  # -I option required for pcre 3.4 (and later?)
  CCARGS="${CCARGS} -DHAS_PCRE -I/usr/include/pcre"
  AUXLIBS="${AUXLIBS} -lpcre"
%else
  # we need to explicitly disable pcre unless asked for, otherwise it will
  # be included if present on the build system. This may cause problems.
  CCARGS="${CCARGS} -DNO_PCRE"
%endif

# Postfix compiles without needing zlib on RedHat's mysql package, but
# requires zlib when using MySQL's package or if using a locally installed
# MySQL binary.
%if %{with_mysql}
  CCARGS="${CCARGS} -DHAS_MYSQL -I/usr/include/mysql"
  AUXLIBS="${AUXLIBS} -L/usr/%{_lib}/mysql -lmysqlclient -lm"
%endif

%if %{mysql_local}
  CCARGS="${CCARGS} -DHAS_MYSQL -I%{mysql_include}"
  AUXLIBS="${AUXLIBS} -L%{mysql_lib} -lmysqlclient -lm"
%endif

%if %{with_pgsql}
  CCARGS="${CCARGS} -DHAS_PGSQL -I/usr/include/pgsql"
  AUXLIBS="${AUXLIBS} -lpq -lcrypt"
%endif

%if %{with_sasl}
  if [ "%{with_sasl}" -le 1 ]; then
    %define sasl_lib_dir %{_libdir}/sasl
    CCARGS="${CCARGS} -DUSE_SASL_AUTH -DUSE_CYRUS_SASL"
    AUXLIBS="${AUXLIBS} -L%{sasl_lib_dir} -lsasl"
  else
    %define sasl_lib_dir %{_libdir}/sasl2
    CCARGS="${CCARGS} -I/usr/include/sasl -DUSE_SASL_AUTH -DUSE_CYRUS_SASL"
    AUXLIBS="${AUXLIBS} -L%{sasl_lib_dir} -lsasl2"
  fi
%endif

# Provide support for Dovecot SASL
%if %{with_dovecot}
  CCARGS="${CCARGS} -DUSE_SASL_AUTH"
  # make dovecot the default IFF we don't include SASL
  if [ "%{with_sasl}" = 0 ]; then
    CCARGS="${CCARGS} -DDEF_SERVER_SASL_TYPE=\\\"dovecot\\\""
  fi
%endif

%if %{with_spf}
    AUXLIBS="${AUXLIBS} -lspf2"
    CCARGS="${CCARGS} -DHAVE_NS_TYPE"
%endif

%if %{with_tls}
# See http://www.openldap.org/lists/openldap-devel/200105/msg00008.html
# - rh6.2 needs LIBS=-ldl to build correctly.
# - reported by Jauder Ho <jauderho@carumba.com>
  if pkg-config openssl; then
    CCARGS="${CCARGS} -DUSE_TLS $(pkg-config --cflags openssl)"
    AUXLIBS="${AUXLIBS} $(pkg-config --libs openssl)"
  else
    #
    # CHECK THIS - these lines may no longer be needed (required for external TLS patch)
    #
    [ "%{with_tlsfix}" = 1 ] && LIBS=-ldl
    [ "%{with_tlsfix}" = 2 ] && CCARGS="${CCARGS} -I/usr/kerberos/include"
    CCARGS="${CCARGS} -DUSE_TLS -I/usr/include/openssl"
    AUXLIBS="${AUXLIBS} -lssl -lcrypto"
  fi
%else
# explicitly disable TLS otherwise will be built on machine if
# openssl is available
	CCARGS="${CCARGS} -DNO_TLS"
%endif

# Required by some TLS implementations (RHEL 3 and RH9) and also some MySQL
# packages
%if %{requires_zlib}
  AUXLIBS="${AUXLIBS} -lz"
%endif

export CCARGS AUXLIBS
make -f Makefile.init makefiles
unset CCARGS AUXLIBS
# -Wno-comment needed due to large number of warnings on RHEL5
# suggestion by Eric Hoeve <eric@ehoeve.com>
#make DEBUG="%{?_with_debug:-g}" OPT="$RPM_OPT_FLAGS -Wno-comment"
make DEBUG="%{?_with_debug:-g}" OPT="$RPM_OPT_FLAGS"


%install
rm -rf $RPM_BUILD_ROOT
#make install DESTDIR=$RPM_BUILD_ROOT
#mkdir -p %buildroot{%_libdir,%_mandir,%daemon_directory/postqueuedir}

[ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != "/" ] && {
    rm -rf   ${RPM_BUILD_ROOT}
    mkdir -p ${RPM_BUILD_ROOT}
}

#%{?!debug:strip -R .comment --strip-unneeded bin/* libexec/*}
#%{?!debug:strip bin/* libexec/*}

# rename man pages which may conflict with sendmail's
mv man/man1/mailq.1      man/man1/mailq.postfix.1
mv man/man1/newaliases.1 man/man1/newaliases.postfix.1
mv man/man1/sendmail.1   man/man1/sendmail.postfix.1
mv man/man5/aliases.5    man/man5/aliases.postfix.5

#adjust renamed manpages ./conf/postfix-files:$manpage_directory/man1/mailq.1:f:root:-:644
perl -pi -e "s?/man(1|5)/(mailq|newaliases|sendmail|aliases).(1|5)?/man\1/\2.postfix.\3?; " \
            conf/postfix-files

# add missing man pages
mantools/srctoman - auxiliary/qshape/qshape.pl >man/man1/qshape.1
mantools/srctoman src/smtpstone/smtp-source.c  >man/man1/smtp-source.1
mantools/srctoman src/smtpstone/smtp-sink.c    >man/man1/smtp-sink.1

# update conf/postfix-files
cat <<EOF >> conf/postfix-files
\$manpage_directory/man1/qshape.1:f:root:-:644
\$manpage_directory/man1/smtp-sink.1:f:root:-:644
\$manpage_directory/man1/smtp-source.1:f:root:-:644
EOF


# install postfix into build root
sh postfix-install -non-interactive \
       install_root=${RPM_BUILD_ROOT} \
       config_directory=%{_sysconfdir}/postfix \
       daemon_directory=%{_libexecdir}/postfix \
       command_directory=%{_sbindir} \
       queue_directory=%{_var}/spool/postfix \
       sendmail_path=%{sendmail_path} \
       newaliases_path=%{newaliases_path} \
       mailq_path=%{mailq_path} \
       mail_owner=postfix \
       setgid_group=postdrop \
       html_directory=%{html_dir} \
       manpage_directory=%{_mandir} \
       readme_directory=%{readme_dir} || exit 1

# To be compatible with later versions of RH sendmail/postfix packages
# make /usr/lib/sendmail.postfix point to /usr/sbin/sendmail.postfix.
# The alternatives then point /usr/lib/sendmail to /usr/lib/sendmail.postfix.
# This *is* all a bit silly ...

install -d -m755 $RPM_BUILD_ROOT/usr/lib
ln -sf ../sbin/sendmail.postfix $RPM_BUILD_ROOT%{usrlib_sendmail}

# RPM compresses man pages automatically.  Edit postfix-files to avoid
# confusing post-install.
ed ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/postfix-files <<EOF || exit 1
H
,s/\(\/man[158]\/.*\.[158]\):/\1%{mps}:/
w
q
EOF

# Change alias_maps and alias_database default directory to use
# %{_sysconfdir}/postfix
bin/postconf -c ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix -e \
	"alias_maps = hash:%{_sysconfdir}/postfix/aliases" \
	"alias_database = hash:%{_sysconfdir}/postfix/aliases" \
|| exit 1

# Change default smtpd_sasl... parameters for dovecot
# - override postfix default behaviour IFF not using cyrus sasl.
# - main.cf can still be adjusted manually after installation if required.
%if %{with_dovecot}
  if [ "%{with_sasl}" = 0 ]; then
    bin/postconf -c ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix -e \
	"smtpd_sasl_type = dovecot" \
	"smtpd_sasl_path = private/auth" \
    || exit 1
  fi
%endif
# Fix a typo in some of the documentation.
perl -pi -e "s/DEF_SASL_SERVER_TYPE/DEF_SERVER_SASL_TYPE/g" */SASL_README*

# Install Sys V init script
mkdir -p ${RPM_BUILD_ROOT}%{initdir}
#install -c %{_sourcedir}/postfix-etc-init.d-postfix \
install -c tmp/postfix-etc-init.d-postfix \
                ${RPM_BUILD_ROOT}%{initdir}/postfix

install -c auxiliary/rmail/rmail ${RPM_BUILD_ROOT}%{rmail_path}
install -c auxiliary/qshape/qshape.pl ${RPM_BUILD_ROOT}/%{_sbindir}/qshape

# copy new aliases files and generate a ghost aliases.db file
#cp -f %{_sourcedir}/postfix-aliases ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/aliases
cp -f tmp/postfix-aliases ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/aliases
chmod 644 ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/aliases

touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/postfix/aliases.db

for i in active bounce corrupt defer deferred flush incoming private saved \
         hold maildrop public pid; do
    mkdir -p ${RPM_BUILD_ROOT}%{_var}/spool/postfix/$i
done

# install qmqp-source, smtp-sink & smtp-source by hand
for i in qmqp-source smtp-sink smtp-source; do
  install -c -m 755 bin/$i ${RPM_BUILD_ROOT}%{_sbindir}/$i
done

# install postfinger and postfix-chroot.sh scripts
# - postfix-chroot.sh is placed in /etc/postfix to make it more visible
#install -c -m 755 %{_sourcedir}/postfinger-%{V_postfinger} ${RPM_BUILD_ROOT}%{_bindir}/postfinger
install -c -m 755 tmp/postfinger-%{V_postfinger} ${RPM_BUILD_ROOT}%{_bindir}/postfinger
#install -c -m 755 %{_sourcedir}/postfix-chroot.sh ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/
install -c -m 755 tmp/postfix-chroot.sh ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/

[ -d "${RPM_BUILD_ROOT}%{html_dir}" ]     || mkdir -p ${RPM_BUILD_ROOT}%{html_dir}
[ -d "${RPM_BUILD_ROOT}%{readme_dir}" ]   || mkdir -p ${RPM_BUILD_ROOT}%{readme_dir}
#install -c -m 644 %{_sourcedir}/README-Postfix-SASL-RedHat.txt ${RPM_BUILD_ROOT}%{readme_dir}/
install -c -m 644 tmp/README-Postfix-SASL-RedHat.txt ${RPM_BUILD_ROOT}%{readme_dir}/
[ -d "${RPM_BUILD_ROOT}%{examples_dir}" ] || mkdir -p ${RPM_BUILD_ROOT}%{examples_dir}
cp -pr examples/* ${RPM_BUILD_ROOT}%{examples_dir}/
# disable execution permissions to avoid rpm generating dependencies
find ${RPM_BUILD_ROOT}%{examples_dir}/ -type f -exec chmod -x {} \;

# Install odd documentation files
for file in AAAREADME COMPATIBILITY COPYRIGHT HISTORY PORTING \
	RELEASE_NOTES RELEASE_NOTES-1.0 RELEASE_NOTES-1.1 RELEASE_NOTES-2.0 \
	RELEASE_NOTES-2.1 RELEASE_NOTES-2.2 RELEASE_NOTES-2.3 \
	RELEASE_NOTES-2.4 TLS_ACKNOWLEDGEMENTS TLS_CHANGES TLS_LICENSE \
	US_PATENT_6321267
do
	install -c -m 644 $file ${RPM_BUILD_ROOT}%{docdir}/
done
cat <<EOF >${RPM_BUILD_ROOT}%{docdir}/SEE_ALSO
%{_docdir}/%{name}-%{version} may contain other documentation files.
EOF

# added for convenience
ln -sf %{html_dir}     ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/html
ln -sf %{readme_dir}   ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/readme
ln -sf %{examples_dir} ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/examples

# Install the smtpd.conf file for SASL support.
%if %{with_sasl}
mkdir -p ${RPM_BUILD_ROOT}%{sasl_lib_dir}
install -m 644 %SOURCE100 ${RPM_BUILD_ROOT}%{sasl_lib_dir}/smtpd.conf
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
install -m 644 %SOURCE101 ${RPM_BUILD_ROOT}%{_sysconfdir}/pam.d/smtp.postfix
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %SOURCE102 ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/saslauthd.postfix
%endif

# Include README.rpm explaining where the documentation can be found and
# also pointing out how to get updated copies of my package
cat <<EOF > ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/README.rpm
README.rpm
==========

Documentation
-------------

Postfix documentation should be available in the directory %{docdir}/.
I have also added a symbolic link to the readme_files and html
directories from %{_sysconfdir}/postfix.

The main Postfix web site is http://www.postfix.org.

Packages
--------

Newer versions of source and standard binary packages may be available from
http://ftp.WL0.org or the mirrors listed at http://postfix.WL0.org.  Look
in the appropriate directory according to your distribution.

Mailing List
------------

I host a mailing list to announce new packages as they are released. If you
are interested in subscribing take a look at
http://postfix.WL0.org/en/lists/.  Previous announcements are archived.

Chrooting
---------

The chroot behaviour of my packages has changed over time. Current
packages will NOT turn on the chroot environment in Postfix.  Older
versions did the opposite.  If you upgrade from an older version
of my package the chroot behaviour will NOT be changed. (Check
%{_sysconfdir}/postfix/master.cf for details.)

I have provided a simple script postfix-chroot.sh which attempts to
cover most situations and should enable you to disable or enable the
chroot on your system with little effort.

Package Build Options
---------------------

This package can be built on several Linux distributions and with several
optional features.  %{_sysconfdir}/postfix/postfix.spec.cf contains the 
information used to build this version of the rpm. It can also
be used to build a new rpm with the same options.

Enjoy!

Simon J Mudd, <sjmudd@pobox.com>
EOF

# generate postfix.spec.cf
# - used to build a newer version of the rpm with the same parameters
#   as the current package.
# - provides build instructions
#cat - %{_sourcedir}/postfix.spec.cf <<EOF | sed -e '/^# NOTE:/d' > ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/postfix.spec.cf
cat - tmp/postfix.spec.cf <<EOF | sed -e '/^# NOTE:/d' > ${RPM_BUILD_ROOT}%{_sysconfdir}/postfix/postfix.spec.cf
#
# This file contains the following information:
#
# - configuration options used to build the installed postfix rpm
#   - generated when the binary rpm was built
#
# - Postfix RPM build instructions
#   - for upgrading the installed rpm with the same options
#   - for building the rpm with other options
#
# 1. CONFIGURATION OPTIONS OF INSTALLED BINARY RPM
#
# Package built on: %{build_dist_full} (%{build_dist})

POSTFIX_ALT_PRIO=%{with_alt_prio}
POSTFIX_CDB=%{with_cdb}
POSTFIX_DB=%{requires_db}
POSTFIX_DOVECOT=%{with_dovecot}
POSTFIX_LDAP=%{with_ldap}
POSTFIX_MYSQL=%{with_mysql}
POSTFIX_MYSQL_PATHS=%{mysql_paths}
POSTFIX_MYSQL_REDHAT=%{with_mysql_redhat}
POSTFIX_PCRE=%{with_pcre}
POSTFIX_PGSQL=%{with_pgsql}
POSTFIX_SASL=%{with_sasl}
POSTFIX_SMTPD_MULTILINE_GREETING=%{smtpd_multiline_greeting}
POSTFIX_SPF=%{with_spf}
POSTFIX_TLS=%{with_tls}
POSTFIX_VDA=%{with_vda}

# export values to child processes
export POSTFIX_MYSQL POSTFIX_MYSQL_PATHS POSTFIX_MYSQL_REDHAT \\
 POSTFIX_LDAP POSTFIX_PCRE POSTFIX_PGSQL \\
 POSTFIX_SASL POSTFIX_TLS POSTFIX_VDA \\
 POSTFIX_SMTPD_MULTILINE_GREETING POSTFIX_DB \\
 POSTFIX_INCLUDE_DB POSTFIX_SPF \\
 POSTFIX_CDB POSTFIX_ALT_PRIO POSTFIX_DOVECOT

# other options used in the build (but not explicitly changeable by the user) are:
# - debug=%{?_with_debug:1}%{?!_with_debug:0}
# - pcre_requires=%{pcre_requires},
# - requires_zlib=%{requires_zlib},
# - sasl_library=%{sasl_library}
# - tlsfix=%{with_tlsfix}
#
# %{_sysconfdir}/postfix/makedefs.out is also produced by the build and may be of
# interest if you are building Postfix by hand.
EOF



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc AAAREADME COMPATIBILITY COPYRIGHT HISTORY INSTALL IPv6-ChangeLog LICENSE PORTING RELEASE_NOTES RELEASE_NOTES-1.0 RELEASE_NOTES-1.1 RELEASE_NOTES-2.0 RELEASE_NOTES-2.1 RELEASE_NOTES-2.2 RELEASE_NOTES-2.3 RELEASE_NOTES-2.4 TLS_ACKNOWLEDGEMENTS TLS_CHANGES TLS_LICENSE US_PATENT_6321267 README_FILES/AAAREADME README_FILES/ADDRESS_CLASS_README README_FILES/ADDRESS_REWRITING_README README_FILES/ADDRESS_VERIFICATION_README README_FILES/BACKSCATTER_README README_FILES/BASIC_CONFIGURATION_README README_FILES/BUILTIN_FILTER_README README_FILES/CDB_README README_FILES/CONNECTION_CACHE_README README_FILES/CONTENT_INSPECTION_README README_FILES/CYRUS_README README_FILES/DATABASE_README README_FILES/DB_README README_FILES/DEBUG_README README_FILES/DSN_README README_FILES/ETRN_README README_FILES/FILTER_README README_FILES/INSTALL README_FILES/IPV6_README README_FILES/LDAP_README README_FILES/LINUX_README README_FILES/LOCAL_RECIPIENT_README README_FILES/MAILDROP_README README_FILES/MILTER_README README_FILES/MYSQL_README README_FILES/NFS_README README_FILES/OVERVIEW README_FILES/PACKAGE_README README_FILES/PCRE_README README_FILES/PGSQL_README README_FILES/QMQP_README README_FILES/QSHAPE_README README_FILES/RELEASE_NOTES README_FILES/RESTRICTION_CLASS_README README_FILES/SASL_README README_FILES/SCHEDULER_README README_FILES/SMTPD_ACCESS_README README_FILES/SMTPD_POLICY_README README_FILES/SMTPD_PROXY_README README_FILES/SOHO_README README_FILES/STANDARD_CONFIGURATION_README README_FILES/STRESS_README README_FILES/TLS_LEGACY_README README_FILES/TLS_README README_FILES/TUNING_README README_FILES/ULTRIX_README README_FILES/UUCP_README README_FILES/VERP_README README_FILES/VIRTUAL_README README_FILES/XCLIENT_README README_FILES/XFORWARD_README
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_docdir}/[a-z]*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*
#%class(manifest) %attr(0444, root, sys)/var/svc/manifest/site/postfix.xml

%attr (0755, root, bin) %dir %{_sysconfdir}
%attr (0755, root, bin) %dir %{_sysconfdir}/%{src_name}
%{_sysconfdir}/%{src_name}/*
# only for oldtimers the original init.d/postfix script - *not* tested on Solaris
# this is %{_sysconfdir}/init.d
%attr (0755, root, bin) %dir %{initdir}
%{initdir}/*



%changelog
* Thu Jan 22 2009 - Thomas Wagner
- %doc made monstrous 
* Sun Jan 2009 - Thomas Wagner
- Initial spec, parts derived from postfix.spec from the original SRPM

