#manually created entries

#>=134
%define pnm_buildrequires_SUNWgtk_doc	data/docbook
%define pnm_requires_SUNWgtk_doc	data/docbook

#>=134
%define pnm_buildrequires_SUNWgnome_xml	developer/documentation-tool/gtk-doc
%define pnm_requires_SUNWgnome_xml	developer/documentation-tool/gtk-doc


# SUNWaudh
# exception, we only have a header pacakge ?
%define pnm_buildrequires_SUNWaudh	system/header/header-audio


%changelog
* Sat Jun 12 2010 - Thomas Wagner
- initial include file
