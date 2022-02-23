Name:     hcache
Version:  1.0.0
Release:  1%{?dist}
Summary:  hcache - a tool fork from pcstat, with a feature that showing top X biggest cache files globally.
License:  Apache 2.0
URL:      https://github.com/silenceshell/hcache
Source0:  %{name}-%{version}.tar.gz
BuildRequires:  golang > 1.2

%define debug_package %{nil}

%description
hcache - a tool fork from pcstat, with a feature that showing top X biggest cache files globally.

%prep
%setup -q

%build
export GO111MODULE=on
export GOPROXY=https://goproxy.cn,direct
go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"

%install
install -Dpm 0755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%{_bindir}/%{name}

%changelog
* Tue Feb 22 2022 xiaobo <xiaobo@uniontech.com> - 1.0.0
- Release 1.0.0
