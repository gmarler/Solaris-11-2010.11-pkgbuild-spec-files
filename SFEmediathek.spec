#
# spec file for package SFEre2c
#

%include Solaris.inc

%define src_name  mediathek
%define subdir    mediathek

Name:                    SFEmediathek
Summary:                 mediathek - tool for writing very fast and very flexible scanners
URL:                     http://mediathek.org/
Version:                 2.0.1
Source:                  %{sf_download}/project/zdfmediathk/Mediathek/Mediathek\ %{version}/Mediathek_mit_libs_%{version}.zip
#http://downloads.sourceforge.net/project/zdfmediathk/Mediathek/Mediathek%202.0.1/Mediathek_mit_libs_2.0.1.zip
Source2:                 %{sf_download}/project/zdfmediathk/Mediathek/Mediathek\ %{version}/Anleitung_MediathekView_%{version}.pdf
#http://downloads.sourceforge.net/project/zdfmediathk/Mediathek/Mediathek%202.0.1/Anleitung_MediathekView_2.0.1.pdf


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

%description
Das Programm durchsucht die Mediathek verschiedener Sender (ARD, ZDF, Arte, 3Sat, MDR, NDR, ORF, SF), lädt Beiträge mit einem Programm eigener Wahl und kann Themen als Abos anlegen und neue Beiträge automatisch downloaden. Es gibt auch eine Möglichkeit, Podcast zu verwalten und zu Downloaden.


%prep
%setup -c -q -n %{src_name}-%version
cp -p %{SOURCE2} .

%build
#nothing to do

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p             $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
cp -p  Mediathek.jar $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
cp -pr lib/          $RPM_BUILD_ROOT%{_basedir}/lib/%{subdir}/
mkdir -p $RPM_BUILD_ROOT%{_bindir}/
echo "java -jar "%{_basedir}/lib/%{subdir}/"Mediathek.jar" > $RPM_BUILD_ROOT%{_bindir}/%{src_name}
chmod a+rx $RPM_BUILD_ROOT%{_bindir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc Anleitung_MediathekView_%{version}.pdf 
%dir %attr (0755, root, bin) %{_basedir}/lib/%{subdir}/
%{_basedir}/lib/%{subdir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}


%changelog
* Sun Apr 25 2010 - Thomas Wagner
- Initial spec
