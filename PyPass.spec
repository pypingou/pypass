# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           PyPass
Version:        0.0.1
Release:        1%{?dist}
Summary:        Manage your accounts information easily and safely

Group:          Development/Languages
License:        GPLv3+
URL:            http://pypass.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel pygtk2
BuildRequires:  desktop-file-utils
Requires:       pygtk2


%description
PyPass allows you to manage easily and safely your accounts. The sensible
information are stored in a GPG encrypted file.
You can also encrypt a file to send it to a friend. It comes with both
command line and GTK interfaces.

%prep
%setup -q -n %{name}

%build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install  --root $RPM_BUILD_ROOT

desktop-file-install \
        --dir=%{buildroot}%{_datadir}/applications \
        %{name}.desktop

# TODO: fix languages
#find_lang %{name}

%post
# After install, we update the icons
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :

%postun
# After uninstall, we update the icons
touch --no-create %{_datadir}/icons/hicolor
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
  %{_bindir}/gtk-update-icon-cache -q %{_datadir}/icons/hicolor;
fi
update-mime-database %{_datadir}/mime &> /dev/null || :
update-desktop-database &> /dev/null || :


%clean
rm -rf $RPM_BUILD_ROOT

#files -f %{name}.lang
%files
%defattr(-,root,root,-)
%doc README LICENSE
%{python_sitelib}/*
%{_bindir}/pypass.py
%{_bindir}/pypass-gtk.py
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/PyPass.png

%changelog
* Fri Mar 11 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.1-1
- First package
