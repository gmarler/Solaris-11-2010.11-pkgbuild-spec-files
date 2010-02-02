#

%include Solaris.inc

%define     src_name typolight
#set to blank if not text part like ".RC2" is in the version string. IPS can't handle non-numeric version strings
#mind to include a "dot" if non empty
#%define     src_name_minor_extra 
%define     src_name_minor_extra 
%define apache2_majorversion 2
%define apache2_version 2.2

Name:                SFEtypolight
Summary:             TYPOlight Open Source CMS
Version:             2.7.6
Source:              %{sf_download}/typolight/typolight-%{version}%{src_name_minor_extra}.tar.gz
SUNW_BaseDir:        /
URL:	             http://www.typolight.org/index.html
Source2:             %{src_name}-htaccess-protect-backend
Source3:             %{src_name}.conf.example
BuildRoot:           %{_tmppath}/%{name}-%{version}%{src_name_minor_extra}-build
%include default-depend.inc

#Requires: Apache2 and php
#Requires: optional mcrypt in php

%prep
%setup -q -n %{src_name}-%{version}%{src_name_minor_extra}
cp -p %{SOURCE2} .
cp -p %{SOURCE3} .

[ -f .htaccess.default ] && mv .htaccess.default .htaccess
[ -f ._htaccess ] && mv ._htaccess .htaccess

#%build

#dummy - noting to make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/
mv %{src_name}.conf.example $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf

mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
cp -pr * $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
cp -pr .ht* $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
#mv %{src_name}-htaccess-protect-backend $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/.htaccess
ln -s %{src_name}-%{version}%{src_name_minor_extra} $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT

#the script is found automaticly in ext-sources w/o a Source<n> keyword
%iclass renamenew -f i.renamenew

%files
%defattr (0640, webservd, bin)
%dir %attr (0755, root, sys) %{_localstatedir}
     %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}
#don't let typolight modify it's files - for security owned by root and not writable by the webservd userid
#places explicitly needed writable are system/logs, system/html, system/tmp
%defattr (0644, root, bin)
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/LICENSE.txt
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/CHANGELOG.txt
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/INSTALL.txt
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/typolight-htaccess-protect-backend
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/basic.css
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/cron.php
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/flash.php
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/index.php
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/music_academy.css
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/print.css
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/robots.txt
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/templates
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/templates/*
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/templates/.htaccess
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/tl_files
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/tl_files/*
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/typolight
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/typolight/*


#optionally make these directories 775 or 770 or 777 see http://www.typolight-community.de/showpost.php?p=8448&postcount=5
%defattr (-, webservd, bin)
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/logs
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/logs/.htaccess
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/html
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/html/index.html
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/tmp
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/tmp/.htaccess
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/config
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/config/*
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/config/.htaccess
%dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/plugins
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/plugins/*

#not writable by the webservd user
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/drivers
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/drivers/*
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/drivers/.htaccess
%dir %attr (0755, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/libraries
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/libraries/*
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/libraries/.htaccess
%dir %attr (0755, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/themes
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/themes/*
%dir %attr (0755, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/modules
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/modules/*
%attr (0644, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/initialize.php
%attr (0644, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/mbstring.php
%attr (0644, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/typolight.css
%attr (0644, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/constants.php
%attr (0644, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/functions.php
%attr (0644, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/iefixes.css
%attr (0644, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/system/interface.php

%class(renamenew) %attr (0644, root, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/.htaccess

%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%class(renamenew) %{_sysconfdir}/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf






%changelog
* Sun Jan 31 2010 - Thomas Wagner
- bump to version 2.8
- make typolight.conf class(renamenew)
- add %{src_name_minor_extra}  to have textsctrings expluded from package version number (IPS)
- set installpath to %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/ with symlink to %{_localstatedir}/typolight
* Sat Dec 19 2009 - Thomas Wagner
- initial version
