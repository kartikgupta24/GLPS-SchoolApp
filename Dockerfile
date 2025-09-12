# Use the official SQL Server image
FROM mcr.microsoft.com/mssql/server:2019-latest

# Set the SA password and authentication mode
ENV ACCEPT_EULA=Y
ENV MSSQL_AUTHENTICATION_MODE=SqlAuthentication
ENV SA_PASSWORD=Techtalks@24

# Expose the default SQL Server port
EXPOSE 1433

# Start SQL Server
CMD ["/opt/mssql/bin/sqlservr"]