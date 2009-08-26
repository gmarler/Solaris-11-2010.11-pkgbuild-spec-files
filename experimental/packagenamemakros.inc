#%if %OS2nnn %( expr %{osbuild} '>=' 118)
## OS2009.11
#%define buildrequiresopenssl	SUNWopenssl
#%define requiresopenssl		SUNWopenssl
#%else
#SXCE
#%define buildrequiresopenssl	SUNWopenssl-includes
#%define requiresopenssl		SUNWopenssl-libraries
#%endif

