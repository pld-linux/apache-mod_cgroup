%define		snapdate	20110824
%define		snap		59adb1a668f0a8504b1124cf0bb93d7e61b21b01
#
%define		apxs		/usr/sbin/apxs
%define		mod_name	cgroup
Summary:	Resource management per vhost
Name:		apache-mod_%{mod_name}
Version:	0.%{snapdate}.1
Release:	1
License:	GPL
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/MatthewIfe/mod_cgroup/archive/59adb1a668f0a8504b1124cf0bb93d7e61b21b01.zip
# Source0-md5:	c960aec82d2edc2fb1ecd27b8dd97c69
URL:		https://github.com/MatthewIfe/mod_cgroup
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	apr-util-devel >= 1:1.0
BuildRequires:	libcgroup-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_cgroup provides a system administrator with the capability to provide predictable service levels for each virtual host declared in httpd.

mod_cgroup can be used for:
* Offering grades of service per virtual host or a group of virtual hosts.
* Protecting other virtual hosts from problematic resource abuse in another vhost.
* Penalizing a virtual host which fails to respect resouce limitations.
* Ensuring a predictable capacity level is provided to all web services.

mod_cgroup is an Apache 2 filter which scans the content delivered by
the proxy module (mod_proxy) for viruses using the Clamav virus
scanning engine.

%prep
%setup -q -n mod_%{mod_name}-%{snap}

%build
%{apxs} -c mod_%{mod_name}/mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install mod_%{mod_name}/mod_%{mod_name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/33_mod_cgroup.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README.md 
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_cgroup.so
