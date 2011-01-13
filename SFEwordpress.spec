#

%include Solaris.inc

%define     src_name wordpress
%define     targetdirname wordpress
#set to blank if not text part like ".RC2" is in the version string. IPS can't handle non-numeric version strings
#mind to include a "dot" if non empty
#%define     src_name_minor_extra 
%define     src_name_minor_extra 
%define     apache2_majorversion 2
%define     apache2_version 2.2
#IPS_component_version: <numeric-only>

Name:                SFEwordpress
Summary:             Wordpress
Version:             3.0.4
Source:              http://wordpress.org/wordpress-%{version}%{src_name_minor_extra}.zip
SUNW_BaseDir:        /
URL:	             http://www.wordpress.org/index.html
#Source2:             %{src_name}-htaccess-protect-backend
Source3:             %{src_name}.conf.example
BuildRoot:           %{_tmppath}/%{name}-%{version}%{src_name_minor_extra}-build
%include default-depend.inc

#Requires: Apache2 and php
#Requires: optional mcrypt in php

%prep
%setup -q -c -T -a0 -n %{src_name}-%{version}%{src_name_minor_extra}
#cp -p %{SOURCE2} .

#copy example apache config
cp -p %{SOURCE3} .

[ -f .htaccess.default ] && mv .htaccess.default .htaccess
[ -f ._htaccess ] && mv ._htaccess .htaccess

#%build

#dummy - noting to make

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/
mv %{src_name}.conf.example $RPM_BUILD_ROOT/etc/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf

cd wordpress
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
cp -pr * $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
#just in case we places an .htaccess or .htpasswd file here:
#cp -pr .ht* $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/
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
%{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/*
#don't let wordpress modify it's files - for security owned by root and not writable by the webservd userid
#places explicitly needed writable are system/logs, system/html, system/tmp
%defattr (0644, root, bin)
#example %dir %attr (0750, webservd, bin) %{_localstatedir}/%{src_name}-%{version}%{src_name_minor_extra}/writable_file_this_is

%defattr (-, root, bin)
%dir %attr(0755, root, sys) %{_sysconfdir}
%class(renamenew) %{_sysconfdir}/apache%{apache2_majorversion}/%{apache2_version}/samples-conf.d/%{src_name}.conf


%changelog
* Thu Jan 13 2011 - Thomas Wagner
- bump to 3.0.4 - security fix - upgrade stongly recommended
* Wed Aug 25 2010 - Thomas Wagner
- initial version
