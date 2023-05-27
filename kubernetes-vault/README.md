Vault Init
```
❯ kubectl exec -it vault-0 -- vault operator init --key-shares=1 --key-threshold=1
Unseal Key 1: 8le4JVqIrnIl3GodM4TJ766ns73OA10tGkQWGwBf+zE=

Initial Root Token: hvs.9r0UqnGzHBR5spgT7jcQv5ns
```

Vault Unseal
```
❯ kubectl exec -it vault-0 -- vault operator unseal 8le4JVqIrnIl3GodM4TJ766ns73OA10tGkQWGwBf+zE=
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.13.1
Build Date      2023-03-23T12:51:35Z
Storage Type    file
Cluster Name    vault-cluster-84143d11
Cluster ID      decf3d5a-a911-0d87-964d-d3b9173e7e0f
HA Enabled      false
```
Vault status
```
❯ kubectl exec -it vault-0 -- vault status
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.13.1
Build Date      2023-03-23T12:51:35Z
Storage Type    file
Cluster Name    vault-cluster-84143d11
Cluster ID      decf3d5a-a911-0d87-964d-d3b9173e7e0f
HA Enabled      false
```

Vault Login
```
❯ kubectl exec -it vault-0 --  vault login
Token (will be hidden):
Success! You are now authenticated. The token information displayed below
is already stored in the token helper. You do NOT need to run "vault login"
again. Future Vault requests will automatically use this token.

Key                  Value
---                  -----
token                hvs.9r0UqnGzHBR5spgT7jcQv5ns
token_accessor       nFU32wYhrpmA887jNaR041gH
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
```
 
Read secret
```
❯ kubectl exec -it vault-0 -- vault read otus/otus-ro/config
Key                 Value
---                 -----
refresh_interval    768h
password            asajkjkahs
username            otus
❯ kubectl exec -it vault-0 -- vault kv get otus/otus-rw/config
====== Data ======
Key         Value
---         -----
password    asajkjkahs
username    otus
```

Authorizations list
```
❯ kubectl exec -it vault-0 --  vault auth list
Path           Type          Accessor                    Description                Version
----           ----          --------                    -----------                -------
kubernetes/    kubernetes    auth_kubernetes_a4f23cc2    n/a                        n/a
token/         token         auth_token_4ded33ab         token based credentials    n/a
```

Policy update
Для возможности изменения секрета otus/config для policy otus-rw необходимо добавить разрешения update

consul template
index.html
```
root@vault-agent-example:/# cat /usr/share/nginx/html/index.html
<html>
<body>
<p>Some secrets:</p>
<ul>
<li><pre>username: otus</pre></li>
<li><pre>password: asajkjkahs</pre></li>
</ul>

</body>
</html>
```

Создание сертификата
```
❯ kubectl exec -it vault-0 -- vault write pki_int/issue/example-dot-ru common_name="gitlab.example.ru" ttl="24h"
Key                 Value
---                 -----
ca_chain            [-----BEGIN CERTIFICATE-----
MIIDnDCCAoSgAwIBAgIUK0VcuCqaQeU99Zftag7FkD8aoa4wDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhtYXBsZS5ydTAeFw0yMzA1MjcxNzU2MDJaFw0yODA1
MjUxNzU2MzJaMCwxKjAoBgNVBAMTIWV4YW1wbGUucnUgSW50ZXJtZWRpYXRlIEF1
dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAL+63m3Y+HA5
Q/YmenLzRKrvdWZitb8+AFNZ526zR3x3+eRwF+UipHa+qmGw0hwq2k+6r3JeuRO/
RwLS44VWpMnZZbdUm3pQ+9a/RTAyWMChuLMihkmEvpE515nUQCCNOFUBCw05bJxJ
heQslR1JzEY6iefv/ahk6sXEO49gEwCFkwyRoQSdNc1j2zg0aKgxvuElCrpKQXte
sJ+jn1ActFn3TfKRdNZ7YO/B/EUOlGq2bfBkJ0DyTFp54ojIaGwH2vc5mG9RwteU
ew/lAHLRHZDgF4ElqClFl5fBEgmC2R/O+hO5yZohQWN9TB58nuF7bfgPUD/yJQly
a7WyTdTd5jkCAwEAAaOBzDCByTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUw
AwEB/zAdBgNVHQ4EFgQUxn7D9eiYo3qu/yVjBcFkEy8fAAEwHwYDVR0jBBgwFoAU
TLhqWrSXYHMalm4Xw1Q9wgY7fhcwNwYIKwYBBQUHAQEEKzApMCcGCCsGAQUFBzAC
hhtodHRwOi8vdmF1bHQ6ODIwMC92MS9wa2kvY2EwLQYDVR0fBCYwJDAioCCgHoYc
aHR0cDovL3ZhdWx0OjgyMDAvdjEvcGtpL2NybDANBgkqhkiG9w0BAQsFAAOCAQEA
JQyqeaYNdt+dfVySlMPqquAMVQP/QP30BNupPi7yfwdsLsGkGDt18cQCnLInbJmK
kRLkrX3MORZuXZlm+EpX3ipqmxOTsNMzntQ7GbdUPcoUpkGi3AwyKvVfd8PvyPwH
p0K6ATIO4LKP6nFsyUsjtIOJTlJfW0y6nd46p1CtYLNOCDRvpUFMdKuIu+8n8ojk
ApYNEVE0Sh5UZiCzj2xF+J7UTWaHB9pA3vpky8Do+mQK+njMredHVHhC6J1dxgjn
TV09G8ou7w1IjfyASmJ1lPSNBYoRREJsc+nTspFK8912iht7yLCpAMdB9tHOAUrJ
yS7mO1OnxBxBfmxpesdVwg==
-----END CERTIFICATE----- -----BEGIN CERTIFICATE-----
MIIDMjCCAhqgAwIBAgIUBZQ8eWX14gFbY9zcCaZiWo/p8cQwDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhtYXBsZS5ydTAeFw0yMzA1MjcxNzQ0NTlaFw0zMzA1
MjQxNzQ1MjhaMBUxEzARBgNVBAMTCmV4bWFwbGUucnUwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQDA4UsO8ifEN3L16wj4WqK7ETlYXjq328+eeCpo4DCh
7OLi9Y+gBjf3qvRy4mclwPebBPRVFARjwJuzSWRrzVAo/+lA+/O5PETtz6HiDSYr
yOldTiAjXyQASnoXs+p+QacYsabgskWL7sZF7HhsndpPPvX3/AsXK2YhE0/h9DiW
tGRcqTWL1e/C5B02iLIT17CwXTNEe/eZ99q2zDl5dCHxaCAlryvcpxPVDnhO+qpf
OjN6rLwPlBzYi4EgweXB6/2lY3xZBLlois2nbVlS9f4S+vX5/TEavyjBhxChu46K
jmbFu1nvI8tdKEvcr0058bUD9ngDbgcsEfcpTtEddyl9AgMBAAGjejB4MA4GA1Ud
DwEB/wQEAwIBBjAPBgNVHRMBAf8EBTADAQH/MB0GA1UdDgQWBBRMuGpatJdgcxqW
bhfDVD3CBjt+FzAfBgNVHSMEGDAWgBRMuGpatJdgcxqWbhfDVD3CBjt+FzAVBgNV
HREEDjAMggpleG1hcGxlLnJ1MA0GCSqGSIb3DQEBCwUAA4IBAQC84sKE+rf2wAXz
eWXGWyA5C7fVKKyJkPvK/LaZ5gDqW3uCAI+8mR3ebz60qX+MDQWGvk+45w0nEnuH
jVz7+W2geWGbpSCMOy5E0Y7Wh7ukSDcn7ryDaIrjFjw9Y/WGAaHivcU3SaAp5gNd
18BHRJsjHQ14LB1JIZUWAOy+WdV/Iauv1S5ZA3OA5oFMOjOdQXDwCyITUJL1jFCJ
BGy8CFVK6vO9XcjN7iVA+9BeiwjBAygyT7D2NTLbxspqOv8DRi7Mrpl6qur33mtT
lVaQ3T6mWmpFX9jQMYoih0OSoNgTf1N1aItOGUOPhirB3lrR/BPtJe9VTHWWIdl3
JMrahXvg
-----END CERTIFICATE-----]
certificate         -----BEGIN CERTIFICATE-----
MIIDZzCCAk+gAwIBAgIUZDddGDNVdlLBWQeV6yDddrlrlgowDQYJKoZIhvcNAQEL
BQAwLDEqMCgGA1UEAxMhZXhhbXBsZS5ydSBJbnRlcm1lZGlhdGUgQXV0aG9yaXR5
MB4XDTIzMDUyNzE4MDYyMVoXDTIzMDUyODE4MDY1MVowHDEaMBgGA1UEAxMRZ2l0
bGFiLmV4YW1wbGUucnUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCu
UFCXvu0W9mxxYNPQ58x/y/RPxU+dsJhWM/aPItAvmn9r5J+gGP4rD0oTfJhHHDNk
/pPpQEa/w1hq8z78JDCs6ZuITqTUaFQVaTAESnWMFjjWzuDdJqdJkFkaKHZZzZPh
XH0zXiJE3PG9Ib9xjGT7+GpTRETUga8CzcsdcWNIrTCMxbvdIr6pq+oHaWg1jgov
V4zI8QAD57Q4+08cIs+V1k8IKnqxfZnBFDZOV0jPtiG8s41D+p12LrlI+8cKkSog
zpc4oGp+N5gxOdbDBolcH/yrkjvHcSriEOl6dPmaZuXzUMupXfvo/4aY/SK+cTaq
oq1akvfN89Wv4F6bcErBAgMBAAGjgZAwgY0wDgYDVR0PAQH/BAQDAgOoMB0GA1Ud
JQQWMBQGCCsGAQUFBwMBBggrBgEFBQcDAjAdBgNVHQ4EFgQUPAMuwARVcrNyvtRy
YqSFbqG9qMkwHwYDVR0jBBgwFoAUxn7D9eiYo3qu/yVjBcFkEy8fAAEwHAYDVR0R
BBUwE4IRZ2l0bGFiLmV4YW1wbGUucnUwDQYJKoZIhvcNAQELBQADggEBAH2fyKbb
rsUOapo1TRegsfAynKQ5nq0tfm5lk+ifWmqQWI2bc4dWJ6s+GQCfZ0GpX0o5tMJZ
FX+J/B2w4DbdNMESEjOGqZ9HMp1tYnCeI1QriQJnUh4seFtX+FjFqKFxWtiWYVxs
GetLSZVRTk+Ri2I515ZyJL1uD4nCJoNb2sykPT3mc35R88UhG4ZERWk1jAo+koQE
4tySH65wliupedDr0tkXbGLdWLB7xNRUUYOvTlIDHMv9cnGpeHcV387ArY8jfIFl
R/b0PN0MtwALvHrSW9RRFFM8xcJa/+dxYg3oRtqsEio/IbWuwYSAEDGyo7sgyYJ8
8W+Dz2xcZAoVtWg=
-----END CERTIFICATE-----
expiration          1685297211
issuing_ca          -----BEGIN CERTIFICATE-----
MIIDnDCCAoSgAwIBAgIUK0VcuCqaQeU99Zftag7FkD8aoa4wDQYJKoZIhvcNAQEL
BQAwFTETMBEGA1UEAxMKZXhtYXBsZS5ydTAeFw0yMzA1MjcxNzU2MDJaFw0yODA1
MjUxNzU2MzJaMCwxKjAoBgNVBAMTIWV4YW1wbGUucnUgSW50ZXJtZWRpYXRlIEF1
dGhvcml0eTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAL+63m3Y+HA5
Q/YmenLzRKrvdWZitb8+AFNZ526zR3x3+eRwF+UipHa+qmGw0hwq2k+6r3JeuRO/
RwLS44VWpMnZZbdUm3pQ+9a/RTAyWMChuLMihkmEvpE515nUQCCNOFUBCw05bJxJ
heQslR1JzEY6iefv/ahk6sXEO49gEwCFkwyRoQSdNc1j2zg0aKgxvuElCrpKQXte
sJ+jn1ActFn3TfKRdNZ7YO/B/EUOlGq2bfBkJ0DyTFp54ojIaGwH2vc5mG9RwteU
ew/lAHLRHZDgF4ElqClFl5fBEgmC2R/O+hO5yZohQWN9TB58nuF7bfgPUD/yJQly
a7WyTdTd5jkCAwEAAaOBzDCByTAOBgNVHQ8BAf8EBAMCAQYwDwYDVR0TAQH/BAUw
AwEB/zAdBgNVHQ4EFgQUxn7D9eiYo3qu/yVjBcFkEy8fAAEwHwYDVR0jBBgwFoAU
TLhqWrSXYHMalm4Xw1Q9wgY7fhcwNwYIKwYBBQUHAQEEKzApMCcGCCsGAQUFBzAC
hhtodHRwOi8vdmF1bHQ6ODIwMC92MS9wa2kvY2EwLQYDVR0fBCYwJDAioCCgHoYc
aHR0cDovL3ZhdWx0OjgyMDAvdjEvcGtpL2NybDANBgkqhkiG9w0BAQsFAAOCAQEA
JQyqeaYNdt+dfVySlMPqquAMVQP/QP30BNupPi7yfwdsLsGkGDt18cQCnLInbJmK
kRLkrX3MORZuXZlm+EpX3ipqmxOTsNMzntQ7GbdUPcoUpkGi3AwyKvVfd8PvyPwH
p0K6ATIO4LKP6nFsyUsjtIOJTlJfW0y6nd46p1CtYLNOCDRvpUFMdKuIu+8n8ojk
ApYNEVE0Sh5UZiCzj2xF+J7UTWaHB9pA3vpky8Do+mQK+njMredHVHhC6J1dxgjn
TV09G8ou7w1IjfyASmJ1lPSNBYoRREJsc+nTspFK8912iht7yLCpAMdB9tHOAUrJ
yS7mO1OnxBxBfmxpesdVwg==
-----END CERTIFICATE-----
private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEArlBQl77tFvZscWDT0OfMf8v0T8VPnbCYVjP2jyLQL5p/a+Sf
oBj+Kw9KE3yYRxwzZP6T6UBGv8NYavM+/CQwrOmbiE6k1GhUFWkwBEp1jBY41s7g
3SanSZBZGih2Wc2T4Vx9M14iRNzxvSG/cYxk+/hqU0RE1IGvAs3LHXFjSK0wjMW7
3SK+qavqB2loNY4KL1eMyPEAA+e0OPtPHCLPldZPCCp6sX2ZwRQ2TldIz7YhvLON
Q/qddi65SPvHCpEqIM6XOKBqfjeYMTnWwwaJXB/8q5I7x3Eq4hDpenT5mmbl81DL
qV376P+GmP0ivnE2qqKtWpL3zfPVr+Bem3BKwQIDAQABAoIBADZt/bxkccPpzpLY
mUtyFfkRxofiJKooqmjAcQzg4gD7TS5zhSSIqVTowUi0bxhFRgcTNzxuRak7ZjB/
I/u3kTts9pPpeq6YpSjKX6P3XB0SE01/69ciarodyLTSTaJc/wAv0ShpDGpUU2er
UgwyupWzTAAUISn6FJvbhsD61vWqGrQIEVp/ewRChqiG3pDhxQOqVWk5vJi+unYe
eKo+y4cB5hXatHtCbbgawU1YRAc4p3PdlPiiVJimChZiA+4AQHlP29DxbGNhOzqZ
wrPDi51Th8yJbd7iDu+auNcIpSddmeoNU7/yErHTdScwbrR8cXQjkrFEGYGGH/m/
PPdQKsECgYEAzTuRxDf3v+OK/66E1ExvtT9C0hb7pW5ZE+EhU4yRhN0TC/gc/r7y
iohVFV2vtpZbDaAlSrcs8M9OQJ54FDYnZJndG+AdhqFLs0zV0I4M9vPl5vT/gE6Z
36qXvxP5ML8WmR7qdD7HqjU7oWmcxVV9aae0dJ24M981VFA8xqyYlLsCgYEA2W7K
niSoOV96pifisAkjqYk1cP46iP1L7yTmaFY6wIqPDrmTQm2NjJaDkIam9BtfsuEL
2P1mbapYuympmWjge7/702eOu5JK/FzSi1eGFuZWCudlXeUgYNASYTihD7ZAEknN
DJeMrbmxZMBrf/m54Z7KG6eNkgX3h/r4YDUiJLMCgYAWJkSwGZ46bnNU7t/VDb7M
n9w1UlesXgFtHNH882HNJhLlKszuTWtduiL8oFTTbty61rrPmn9WKfl3DeNFwyZz
PAvZ81Ecc5H48uTskjgh+uaoC277yP/gXMftzlkJgsYMloKVMyVXYFFkNUK/JV/Y
pEncgB0eNAvMYrB8fKom+wKBgHxO1xAqrPKAH8K2sucpknXut9rtvdFr3unOEtw7
0EMb9EXa2tHziCWEN5t9IB4XOFMwTnG0DcdMyIXYf9nxF8YoMHTgk72xGaXF+6km
VMbq0O5S9KUFxckTrC5hDdPJwj+yacR1MDxyGXUcfVkhEKBpA+tjk5CUULwxQ6bd
ObP5AoGADTaVqOBxuaurMUmAuAA9r8moqudFmeFKV66mXkCEVNcgSkrciFQioCof
JvxmB6KF7sT4+CrJON7JkZ/k5Fm38RX2w9ky0iZMxNOxiY1xIfaU5G3WWmdR49xC
z1/XbX+9MxlJBcUJ/DXqfoiygGOjQWg+8AeQxlxJVnY6Pq2Dh+M=
-----END RSA PRIVATE KEY-----
private_key_type    rsa
serial_number       64:37:5d:18:33:55:76:52:c1:59:07:95:eb:20:dd:76:b9:6b:96:0a
```
