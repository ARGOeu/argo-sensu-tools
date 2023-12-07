%define underscore() %(echo %1 | sed 's/-/_/g')
%define stripc() %(echo %1 | sed 's/el7.centos/el7/')
%define mydist %{stripc %{dist}}

Summary:       Tools for ARGO Sensu
Name:          argo-sensu-tools
Version:       0.1.0
Release:       1%{?dist}
Source0:       %{name}-%{version}.tar.gz
License:       ASL 2.0
Group:         Development/System
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Prefix:        %{_prefix}
BuildArch:     noarch

BuildRequires: python3-devel
Requires:      python36-requests


%description
Package includes service used for listening to a socket to which passive metrics are writing results, and sending them to Sensu backend.


%prep
%setup -q


%build
%{py3_build}


%install
%{py3_install "--record=INSTALLED_FILES" }
install --directory %{buildroot}/%{_localstatedir}/log/argo-sensu-tools/


%clean
rm -rf $RPM_BUILD_ROOT


%files -f INSTALLED_FILES
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/argo-sensu-tools.conf
%dir %{python3_sitelib}/%{underscore %{name}}/
%{python3_sitelib}/%{underscore %{name}}/*.py
%{_unitdir}/passive2sensu.service
%attr(-,sensu,sensu) %dir %{_localstatedir}/log/argo-sensu-tools/


%post -n argo-sensu-tools
%systemd_postun_with_restart passive2sensu.service


%preun -n argo-sensu-tools
%systemd_preun passive2sensu.service


%changelog
* Thu Dec 7 2023 Katarina Zailac <kzailac@srce.hr> - 0.1.0-1%{?dist}
- ARGO-4430 passive2sensu service fails when line not complete
- ARGO-4429 Read fifo file line-by-line
- ARGO-4422 Improve handling of passive2sensu service
- ARGO-4414 Create a service that is going to handle passive metrics on Sensu agent
