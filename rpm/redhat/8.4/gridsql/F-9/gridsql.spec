Summary:	Parallel Server for PostgreSQL
Name:		gridsql
Version:	1.1
Release:	0beta%{?dist}
License:	Commercial
URL:		http://sourceforge.net/projects/gridsql/
Group:		Applications/Databases
#Source0:	http://downloads.sourceforge.net/%{name}/%{name}-src-%{version}beta.tar.gz
#Source0:	http://dfn.dl.sourceforge.net/sourceforge/gridsql-src-1.1beta.tar.gz
Source0:	http://garr.dl.sourceforge.net/sourceforge/gridsql/gridsql-1.1beta.tar.gz
Source1:	http://garr.dl.sourceforge.net/sourceforge/gridsql/gridsql-client-1.1beta.tar.gz
Source2:	http://garr.dl.sourceforge.net/sourceforge/gridsql/gridsql-agent-1.1beta.tar.gz

Requires: 	postgresql-server
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

%description
GridSQL is a shared-nothing clustered database system
that provides the heart of a Business Intelligence infrastructure.
It includes intelligence to maximize parallelization over multiple
servers, for querying large sets of data.

%package agent
Summary:        The agent programs needed for GridSQL
Group:   	Applications/Databases
Requires:	gridsql %{version}-%{release}

%description agent
Agent programs needed for GridSQL

%package client
Summary:        The client programs needed for GridSQL
Group:   	Applications/Databases
Requires:	gridsql %{version}-%{release}

%description client
Client programs needed for GridSQL

%prep
%setup -q -n %{name}-%{version} -c -a 2 -a 1

%build

%install
install -d %{buildroot}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sysconfdir}
install -d %{buildroot}%{_sysconfdir}/%{name}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_docdir}/%{name}-%{version}
install -d %{buildroot}%{_datadir}
install -d %{buildroot}%{_datadir}/java
pushd gridsql-1.1

install -m 755 bin/* %{buildroot}%{_bindir}
install -m 755 config/* %{buildroot}%{_sysconfdir}/%{name}
install -m 755 docs/*.PDF %{buildroot}%{_docdir}/%{name}-%{version}
install -m 755 lib/*.jar %{buildroot}%{_datadir}/java

#FIXME: We need to patch this script before installing
install -m 755 gridsql_env.sh %{buildroot}%{_bindir}

cd ../gridsql-agent-1.1

install -m 755 bin/* %{buildroot}%{_bindir}
install -m 755 config/* %{buildroot}%{_sysconfdir}/%{name}
install -m 755 lib/*.jar %{buildroot}%{_datadir}/java

cd ../gridsql-client-1.1

install -m 755 bin/* %{buildroot}%{_bindir}
install -m 755 lib/*.jar %{buildroot}%{_datadir}/java

%clean
rm -rf %{buildroot}

%files
%attr(0644,postgres,postgres) %{_bindir}/xdbcmdline.jar
%attr(0640,postgres,postgres) %{_bindir}/xdbengine.jar
%attr(0640,postgres,postgres) %{_bindir}/xdbprotocol.jar
%attr(0640,postgres,postgres) %{_bindir}/xdbserver.jar
%attr(0640,postgres,postgres) %{_bindir}/xdbutil.jar
%attr(0640,postgres,postgres) %{_bindir}/gs-agent.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-cmdline.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-createdb.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-createmddb.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-dbstart.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-dbstop.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-dropdb.sh
%attr(0640,postgres,postgres) %{_bindir}/gridsql_env.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-execdb.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-impex.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-loader.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-server.sh
%attr(0640,postgres,postgres) %{_bindir}/gs-shutdown.sh
%attr(0640,postgres,postgres) %{_datadir}/java/edb-jdbc14.jar
%attr(0640,postgres,postgres) %{_datadir}/java/jline-0_9_5.jar
%attr(0640,postgres,postgres) %{_datadir}/java/log4j.jar

%attr(0640,postgres,postgres) %{_sysconfdir}/gridsql/gridsql.config

%doc %attr(0644,postgres,postgres) %{_docdir}/%{name}-%{version}/*.PDF

%files agent
%attr(0755,postgres,postgres) %{_bindir}/gs-agent.sh
%attr(0640,postgres,postgres) %{_sysconfdir}/gridsql/gridsql_agent.config

%files client
%attr(0755,postgres,postgres) %{_bindir}/gs-cmdline.sh

%changelog
* Tue May 12 2009 Devrim Gunduz <devrim@CommandPrompt.com> 1.1-0beta
- Initial build
