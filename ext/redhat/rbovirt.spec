# Generated from rbovirt-0.0.15.gem by gem2rpm -*- rpm-spec -*-
%{!?ruby_sitelib: %global ruby_sitelib %(ruby -rrbconfig -e "puts Config::CONFIG['sitelibdir']")}
%define release %{rpm_release}%{?dist}

%global gem_name rbovirt
%global rubyabi 1.9.1

Summary: A Ruby client for oVirt REST API
Name: rubygem-%{gem_name}
Version: 0.0.15
Release: 1%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://github.com/rbovirt/rbovirt
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.tgz
Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems) 
Requires: ruby 
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems-devel 
BuildRequires: ruby 
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
A Ruby client for oVirt REST API


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -n %{name}

%build

%install
rm -rf %{buildroot}
%{__install} -d -m0755  %{buildroot}/%{ruby_sitelib}/%{name}
cp -R ./lib/* %{buildroot}/%{ruby_sitelib}/%{name}/
cp -R ./spec/* %{buildroot}/%{ruby_sitelib}/%{name}/

%files
%dir %{ruby_sitelib}/%{name}
%{ruby_sitelib}/%{name}/client/cluster_api.rb
%{ruby_sitelib}/%{name}/client/datacenter_api.rb
%{ruby_sitelib}/%{name}/client/host_api.rb
%{ruby_sitelib}/%{name}/client/storage_domain_api.rb
%{ruby_sitelib}/%{name}/client/template_api.rb
%{ruby_sitelib}/%{name}/client/vm_api.rb
%{ruby_sitelib}/%{name}/endpoint.yml.example
%{ruby_sitelib}/%{name}/integration/api_spec.rb
%{ruby_sitelib}/%{name}/integration/vm_crud_spec.rb
%{ruby_sitelib}/%{name}/lib/endpoint.rb
%{ruby_sitelib}/%{name}/ovirt/base_object.rb
%{ruby_sitelib}/%{name}/ovirt/cluster.rb
%{ruby_sitelib}/%{name}/ovirt/datacenter.rb
%{ruby_sitelib}/%{name}/ovirt/host.rb
%{ruby_sitelib}/%{name}/ovirt/interface.rb
%{ruby_sitelib}/%{name}/ovirt/network.rb
%{ruby_sitelib}/%{name}/ovirt/storage_domain.rb
%{ruby_sitelib}/%{name}/ovirt/template.rb
%{ruby_sitelib}/%{name}/ovirt/vm.rb
%{ruby_sitelib}/%{name}/ovirt/volume.rb
%{ruby_sitelib}/%{name}/rbovirt.rb
%{ruby_sitelib}/%{name}/spec_helper.rb
%{ruby_sitelib}/%{name}/unit/vm_spec.rb


%files doc

%changelog
* Wed Nov 14 2012 Marco - 0.0.15-1
- Initial package
