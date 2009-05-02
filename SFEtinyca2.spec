#
# spec file for package SFEtinyca2
#
# works: snv104 / pkgbuild 1.3.91
# works: snv104 / pkgbuild 1.2.0
# works: snv96  / pkgbuild 1.3.1

%define src_name tinyca2

%define	tinyca2libdir		%{_datadir}/tinyca2/lib
%define	tinyca2templatesdir	%{_datadir}/tinyca2/templates
%define	tinyca2localedir	%{_datadir}/tinyca2/locale/

%include Solaris.inc
Name:                    SFE%{src_name}
Summary:                 %{src_name} - Frontend to manage SSL Certificates / Keys for muliple root-CAs
URL:                     http://tinyca.sm-zone.net/
Version:                 0.7.5
Source:                  http://tinyca.sm-zone.net/%{src_name}-%{version}.tar.bz2
License:             GPL


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SFEperl-glib
Requires: SFEperl-glib
BuildRequires: SFEperl-gtk2
Requires: SFEperl-gtk2
BuildRequires: SFEperl-gettext
Requires: SFEperl-gettext
Requires: SUNWopensslr
Requires: SUNWopenssl-libraries
Requires: SUNWgtar
Requires: SUNWzip

#just for note: dependencies by SFEperl-gtk2 are
# SFEperl-extutils-dep
# SFEperl-extutils-pkg
# SFEperl-glib
# SFEperl-cairo




%include default-depend.inc

%description 
TinyCA is a graphical tool written in Perl/Gtk to manage a small
Certification Authority (CA) using openssl.

TinyCA supports - creation and revocation of x509 - S/MIME
   certificates.

- PKCS#10 requests.

- exporting certificates as PEM, DER, TXT, and PKCS#12.

- server certificates for use in web servers, email servers, IPsec,
   and more.

- client certificates for use in web browsers, email clients, IPsec,
  and more.

- creation and management of SubCAs




%prep
%setup -q -n %{src_name}-%version
perl -pi -e 's:./lib:%{tinyca2libdir}:g' tinyca2
perl -pi -e 's:./templates:%{tinyca2templatesdir}:g' tinyca2
perl -pi -e 's:./locale:%{tinyca2localedir}:g' tinyca2

#we live in Solaris
perl -pi -e 's:/usr/bin/openssl:/usr/sfw/bin/openssl:g' tinyca2
perl -pi -e 's:/bin/tar:/usr/bin/gtar:g' tinyca2

%build
make -C po

%install
rm -rf $RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT%{_bindir}
install -d -m 0755 $RPM_BUILD_ROOT%{tinyca2libdir}
install -d -m 0755 $RPM_BUILD_ROOT%{tinyca2libdir}/GUI
install -d -m 0755 $RPM_BUILD_ROOT%{tinyca2templatesdir}
install -d -m 0755 $RPM_BUILD_ROOT/%{_datadir}/applications
install -m 644 %{src_name}.desktop $RPM_BUILD_ROOT/%{_datadir}/applications

install -m 644 lib/GUI/*.pm $RPM_BUILD_ROOT%{tinyca2libdir}/GUI/
install -m 644 templates/openssl.cnf $RPM_BUILD_ROOT%{tinyca2templatesdir}
install -m 755 tinyca2 $RPM_BUILD_ROOT%{_bindir}

LANGUAGES="de es cs fr sv"

for LANG in $LANGUAGES; do
   install -d -m 0755 $RPM_BUILD_ROOT%{tinyca2localedir}/$LANG
   install -d -m 0755 $RPM_BUILD_ROOT%{tinyca2localedir}/$LANG/LC_MESSAGES/
   install -m 644 locale/$LANG/LC_MESSAGES/tinyca2.mo %{buildroot}%{tinyca2localedir}/$LANG/LC_MESSAGES/
done

install -m 644 lib/*.pm $RPM_BUILD_ROOT%{tinyca2libdir}

# for older pkgbuild/pkgtool
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT


%files

%files
%defattr(-, root, bin)
%doc CHANGES INSTALL templates/openssl.cnf
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/tinyca2/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*


%changelog
* Mar 26 2009 - Thomas Wagner
- fix %doc
- add (Build)Requires: SFEperl-glib, (Build)Requires: SFEperl-gtk2, BuildRequires: SFEperl-gtk2
* Nov 13 2008 - Thomas Wagner
- Fix Requires to be SUNWopensslr and SUNWopenssl-libraries
* Tue Oct 21 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Fix Requires
* Thu Oct 07 2008  - Thomas Wagner
- Initial spec - derived from tinyca2.spec inside the tarball - thanks to Stephan Martin <sm@sm-zone.net>
