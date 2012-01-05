# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

Name:           PyPass
Version:        0.0.1
Release:        2%{?dist}
Summary:        Manage your accounts information easily and safely

Group:          Development/Languages
License:        GPLv3+
URL:            http://pypass.org
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       python-gnupg
Requires:       python-argparse

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

# TODO: fix languages
#find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

#files -f %{name}.lang
%files
%defattr(-,root,root,-)
%doc README LICENSE
%{python_sitelib}/*
%{_bindir}/pypass

%changelog
* Thu Jan 5 2012 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.1-2
- Adjust spec to the split pypass/pypass-gnome
- Add missing Requires

* Fri Mar 11 2011 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.0.1-1
- First package
