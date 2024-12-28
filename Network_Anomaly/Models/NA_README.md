# Attack Classes and Types

## Attack Class: DoS (Denial of Service)

These attacks aim to disrupt the normal functioning of a target system by overwhelming it with traffic or requests. The attack types under this class are:

- **Back**
- **Land**
- **Neptune**
- **Pod**
- **Smurf**
- **Teardrop**
- **Apache2**
- **Udpstorm**
- **Processtable**
- **Worm**

## Attack Class: Probe

Probe attacks are those where the attacker scans the network or system to gather information about the target, often as a precursor to a more harmful attack. The attack types under this class are:

- **Satan**
- **Ipsweep**
- **Nmap**
- **Portsweep**
- **Mscan**
- **Saint**

## Attack Class: R2L (Remote to Local)

R2L attacks involve an attacker trying to gain unauthorized access to a system from a remote location, often by exploiting vulnerabilities. The attack types under this class are:

- **Guess_Password**
- **Ftp_write**
- **Imap**
- **Phf**
- **Multihop**
- **Warezmaster**
- **Warezclient**
- **Spy**
- **Xlock**
- **Xsnoop**
- **Snmpguess**
- **Snmpgetattack**
- **Httptunnel**
- **Sendmail**
- **Named**

## Attack Class: U2R (User to Root)

U2R attacks involve an attacker trying to escalate their privileges from a normal user to a root user on a target system. The attack types under this class are:

- **Buffer_overflow**
- **Loadmodule**
- **Rootkit**
- **Perl**
- **Sqlattack**
- **Xterm**
- **Ps**


# Network Connection Data Set Features

## List of Columns

- `duration`: Length of time duration of the connection
- `protocol_type`: Protocol used in the connection
- `service`: Destination network service used
- `flag`: Status of the connection – Normal or Error
- `src_bytes`: Number of data bytes transferred from source to destination in a single connection
- `dst_bytes`: Number of data bytes transferred from destination to source in a single connection
- `land`: If source and destination IP addresses and port numbers are equal, this variable takes value 1, else 0
- `wrong_fragment`: Total number of wrong fragments in this connection
- `urgent`: Number of urgent packets in this connection. Urgent packets are packets with the urgent bit activated
- `hot`: Number of "hot" indicators in the content such as entering a system directory, creating programs, and executing programs
- `num_failed_logins`: Count of failed login attempts
- `logged_in`: Login status: 1 if successfully logged in; 0 otherwise
- `num_compromised`: Number of "compromised" conditions
- `root_shell`: 1 if root shell is obtained; 0 otherwise
- `su_attempted`: 1 if "su root" command attempted or used; 0 otherwise
- `num_root`: Number of "root" accesses or number of operations performed as root in the connection
- `num_file_creations`: Number of file creation operations in the connection
- `num_shells`: Number of shell prompts
- `num_access_files`: Number of operations on access control files
- `num_outbound_cmds`: Number of outbound commands in an FTP session
- `is_host_login`: 1 if the login belongs to the "hot" list (i.e., root or admin); else 0
- `is_guest_login`: 1 if the login is a "guest" login; 0 otherwise
- `count`: Number of connections to the same destination host as the current connection in the past two seconds
- `srv_count`: Number of connections to the same service (port number) as the current connection in the past two seconds
- `serror_rate`: The percentage of connections that have activated the flag (4) s0, s1, s2, or s3, among the connections aggregated in `count`
- `srv_serror_rate`: The percentage of connections that have activated the flag (4) s0, s1, s2, or s3, among the connections aggregated in `srv_count`
- `rerror_rate`: The percentage of connections that have activated the flag (4) REJ, among the connections aggregated in `count`
- `srv_rerror_rate`: The percentage of connections that have activated the flag (4) REJ, among the connections aggregated in `srv_count`
- `same_srv_rate`: The percentage of connections that were to the same service, among the connections aggregated in `count`
- `diff_srv_rate`: The percentage of connections that were to different services, among the connections aggregated in `count`
- `srv_diff_host_rate`: The percentage of connections that were to different destination machines, among the connections aggregated in `srv_count`
- `dst_host_count`: Number of connections having the same destination host IP address
- `dst_host_srv_count`: Number of connections having the same port number
- `dst_host_same_srv_rate`: The percentage of connections that were to the same service, among the connections aggregated in `dst_host_count`
- `dst_host_diff_srv_rate`: The percentage of connections that were to different services, among the connections aggregated in `dst_host_count`
- `dst_host_same_src_port_rate`: The percentage of connections that were to the same source port, among the connections aggregated in `dst_host_srv_count`
- `dst_host_srv_diff_host_rate`: The percentage of connections that were to different destination machines, among the connections aggregated in `dst_host_srv_count`
- `dst_host_serror_rate`: The percentage of connections that have activated the flag (4) s0, s1, s2, or s3, among the connections aggregated in `dst_host_count`
- `dst_host_srv_serror_rate`: The percentage of connections that have activated the flag (4) s0, s1, s2, or s3, among the connections aggregated in `dst_host_srv_count`
- `dst_host_rerror_rate`: The percentage of connections that have activated the flag (4) REJ, among the connections aggregated in `dst_host_count`
- `dst_host_srv_rerror_rate`: The percentage of connections that have activated the flag (4) REJ, among the connections aggregated in `dst_host_srv_count`
- `attack`: Type of attack or "normal" traffic
- `last_flag`: Last flag of the connection

## Basic Features of Each Network Connection Vector

### Content Related Features
1. **Duration**: Length of time duration of the connection
2. **Protocol_type**: Protocol used in the connection
3. **Service**: Destination network service used
4. **Flag**: Status of the connection – Normal or Error
5. **Src_bytes**: Number of data bytes transferred from source to destination in a single connection
6. **Dst_bytes**: Number of data bytes transferred from destination to source in a single connection
7. **Land**: If source and destination IP addresses and port numbers are equal, this variable takes value 1, else 0
8. **Wrong_fragment**: Total number of wrong fragments in this connection
9. **Urgent**: Number of urgent packets in this connection. Urgent packets are packets with the urgent bit activated

### Content Related Features
10. **Hot**: Number of "hot" indicators in the content such as: entering a system directory, creating programs, and executing programs
11. **Num_failed_logins**: Count of failed login attempts
12. **Logged_in**: Login Status: 1 if successfully logged in; 0 otherwise
13. **Num_compromised**: Number of "compromised" conditions
14. **Root_shell**: 1 if root shell is obtained; 0 otherwise
15. **Su_attempted**: 1 if "su root" command attempted or used; 0 otherwise
16. **Num_root**: Number of "root" accesses or number of operations performed as root in the connection
17. **Num_file_creations**: Number of file creation operations in the connection
18. **Num_shells**: Number of shell prompts
19. **Num_access_files**: Number of operations on access control files
20. **Num_outbound_cmds**: Number of outbound commands in an FTP session
21. **Is_hot_login**: 1 if the login belongs to the "hot" list (i.e., root or admin); else 0
22. **Is_guest_login**: 1 if the login is a "guest" login; 0 otherwise

### Time Related Traffic Features
23. **Count**: Number of connections to the same destination host as the current connection in the past two seconds
24. **Srv_count**: Number of connections to the same service (port number) as the current connection in the past two seconds
25. **Serror_rate**: The percentage of connections that have activated the flag (4) s0, s1, s2, or s3, among the connections aggregated in `count`
26. **Srv_serror_rate**: The percentage of connections that have activated the flag (4) s0, s1, s2, or s3, among the connections aggregated in `srv_count`
27. **Rerror_rate**: The percentage of connections that have activated the flag (4) REJ, among the connections aggregated in `count`
28. **Srv_rerror_rate**: The percentage of connections that have activated the flag (4) REJ, among the connections aggregated in `srv_count`
29. **Same_srv_rate**: The percentage of connections that were to the same service, among the connections aggregated in `count`
30. **Diff_srv_rate**: The percentage of connections that were to different services, among the connections aggregated in `count`
31. **Srv_diff_host_rate**: The percentage of connections that were to different destination machines, among the connections aggregated in `srv_count`

### Host Based Traffic Features
32. **Dst_host_count**: Number of connections having the same destination host IP address
33. **Dst_host_srv_count**: Number of connections having the same port number
34. **Dst_host_same_srv_rate**: The percentage of connections that were to the same service, among the connections aggregated in `dst_host_count`
35. **Dst_host_diff_srv_rate**: The percentage of connections that were to different services, among the connections aggregated in `dst_host_count`
36. **Dst_host_same_src_port_rate**: The percentage of connections that were to the same source port, among the connections aggregated in `dst_host_srv_count`
37. **Dst_host_srv_diff_host_rate**: The percentage of connections that were to different destination machines, among the connections aggregated in `dst_host_srv_count`
38. **Dst_host_serror_rate**: The percentage of connections that have activated the flag (4) s0, s1, s2, or s3, among the connections aggregated in `dst_host_count`
39. **Dst_host_srv_serror_rate**: The percentage of connections that have activated the flag (4) s0, s1, s2, or s3, among the connections aggregated in `dst_host_srv_count`
40. **Dst_host_rerror_rate**: The percentage of connections that have activated the flag (4) REJ, among the connections aggregated in `dst_host_count`
41. **Dst_host_srv_rerror_rate**: The percentage of connections that have activated the flag (4) REJ, among the connections aggregated in `dst_host_srv_count`


## Feature Types

- **Nominal**: `protocol_type(2)`, `service(3)`, `flag(4)`
- **Binary**: `land(7)`, `logged_in(12)`, `root_shell(14)`, `su_attempted(15)`, `is_host_login(21)`, `is_guest_login(22)`
- **Numeric**: `duration(1)`, `src_bytes(5)`, `dst_bytes(6)`, `wrong_fragment(8)`, `urgent(9)`, `hot(10)`, `num_failed_logins(11)`, `num_compromised(13)`, `num_root(16)`, `num_file_creations(17)`, `num_shells(18)`, `num_access_files(19)`, `num_outbound_cmds(20)`, `count(23)`, `srv_count(24)`, `serror_rate(25)`, `srv_serror_rate(26)`, `rerror_rate(27)`, `srv_rerror_rate(28)`, `same_srv_rate(29)`, `diff_srv_rate(30)`, `srv_diff_host_rate(31)`, `dst_host_count(32)`, `dst_host_srv_count(33)`, `dst_host_same_srv_rate(34)`, `dst_host_diff_srv_rate(35)`, `dst_host_same_src_port_rate(36)`, `dst_host_srv_diff_host_rate(37)`, `dst_host_serror_rate(38)`, `dst_host_srv_serror_rate(39)`, `dst_host_rerror_rate(40)`, `dst_host_srv_rerror_rate(41)`
